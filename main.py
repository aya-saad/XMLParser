import py2neo
import xml.etree.ElementTree as ET
import numpy as np
import os
from tqdm import tqdm

from Database.Node import Node
from Database.Site import Site
from Database.Cage import Cage
from Database.Batch import Batch
from Database.Quality import Quality
from Database.Product import Product
from Database.Event import Event
from Database.Observation import Observation
from Database.Sensor import Sensor
from Database.Supplier import Supplier

from utils.config import Config
from utils.utils import parse_args, walkdir, get_id, get_fl_id, find_key_value

## GLOBAL DICTIONARIES

#company_dict, batch_dict, cage_dict, site_dict, supplier_dict, event_dict, \
#    sensor_dict, observation_dict, quality_dict, product_dict, \
#    rel_dict
# nodes
company_dict = {}
batch_dict = {}
cage_dict = {}
site_dict = {}
supplier_dict = {}
event_dict = {}
sensor_dict = {}
observation_dict = {}
quality_dict = {}
product_dict = {}
# relations
rel_dict = []

def create_relation(n1, n2, rel_type):
    """
    // create relation between two nodes
    :param n1: first node
    :param n2: second node
    :param rel_type: relationship type ex: HAS_CAGE
    :return: relation
    """
    has_relation = py2neo.Relationship.type(rel_type)
    return has_relation(n1, n2)


# create_observation(unit_id, observable_property='AverageTemperature',
# sensor_type='Temperature Sensor', sensor_producer='Temperature Sensor Producer',sensor_dict,
# first_day, last_day, observation_type='Temperature', value=average_temperature, biomass=0,
# observation_dict, rel_dict)
def create_observation(aCage, unit_id, observable_property,
                       sensor_type, sensor_producer, sensor_dict,
                       first_day, last_day, observation_type, value, biomass,
                       observation_dict, rel_dict):
    # TODO: a cage can have multiple oxygen sensors each on a specific depth
    #       as a future improvement we need to add the installation depth when we create the id
    sensor_id = unit_id + get_id(observable_property)
    aSensor = Sensor(sensor_id, sensor_type, sensor_producer)
    if sensor_id not in sensor_dict.keys():
        sensor_dict[aSensor.node_id] = aSensor
    # self.first_year = int(first_date_of_input[0:4])
    #         self.first_month = int(first_date_of_input[5:7])
    #         self.first_day = int(first_date_of_input[8:10])
    # observation_id = sensor_id + int(get_id(first_day)) # + get_id(last_day))
    int_first_day = 0
    if first_day is not None:
        int_first_day = int(first_day[0:4] + first_day[5:7] + first_day[8:10])
    int_last_day = 0
    if last_day is not None:
        int_last_day = int(last_day[0:4] + last_day[5:7] + last_day[8:10])
    observation_id = sensor_id + int_first_day + int_last_day
    aObservation = Observation(observation_id, observation_type, value,
                               first_day, last_day, biomass)
    if observation_id not in observation_dict.keys():
        observation_dict[aObservation.node_id] = aObservation
    rel_dict.append([aSensor, aCage, 'HOSTED_BY'])
    rel_dict.append([aObservation, aSensor, 'MADE_BY'])


def parse_xml_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    print("root: ", root)

    Companies = root.findall('./Companies/Company')
    '''
    # nodes
    company_dict = {}
    batch_dict = {}
    cage_dict = {}
    site_dict = {}
    supplier_dict = {}
    event_dict = {}
    sensor_dict = {}
    observation_dict = {}
    quality_dict = {}
    product_dict = {}
    # relations
    rel_dict = []
    '''

    sitemap = []
    for company in tqdm(Companies, desc="Companies"):
        company_id = int(company.find('OrganizationNumber').text)
        aCompany = Node(company_id,
                        company.find('CompanyName').text,
                        'Company')
        if company_id not in company_dict.keys():
            company_dict[aCompany.node_id] = aCompany

        Sites = company.findall('Sites/Site')
        for site in tqdm(Sites, desc="Sites"):
            site_id = int(site.find('SiteID').text)
            aSite = Site(site_id, site.find('SiteName').text,
                         site.find('SiteNumber').text, site.find('MaxAllowedBiomass').text,
                         site.find('LastDateOfRegistration').text,
                         site.find('Latitude').text, site.find('Longitude').text)


            if site_id not in site_dict.keys():
                site_dict[aSite.node_id] = aSite

            rel_dict.append([aCompany, aSite, 'HAS_SITE'])
            rel_dict.append([aSite, aCompany, 'OWNED_BY'])

            Groups = site.findall('Groups/Group')

            for group in tqdm(Groups, desc="Groups"):
                # print('group: ', group)
                unit_name = group.find('UnitName').text
                unit_id = get_id(unit_name)
                print('unit_id: ', unit_id)
                unit_volume = group.find('UnitVolume').text

                batch_id = int(group.find('GroupID').text)
                batch_name = group.find('GroupName').text
                first_date_of_input = group.find('FirstDateOfInput').text
                last_date_of_input = group.find('LastDateOfInput').text
                species_id = group.find('Species/SpeciesID').text
                species_name = group.find('Species/SpeciesName').text
                fish_type_code = group.find('FishTypes/FishType/Code').text
                fish_type_textual = group.find('FishTypes/FishType/Textual').text
                strain = group.find('Strains/Strain').text
                ### idc = 0  ## ?? check this number  site_id --> SiteID batch_id --> GROUPID   cage_id - unit_id --> get_id(unit_name)

                aCage = Cage(unit_id, unit_name, unit_volume,
                             first_date_of_input)
                if unit_name not in cage_dict.keys():
                    cage_dict[aCage.node_id] = aCage  # aCage.node()
                aBatch = Batch(batch_id, batch_name,
                               first_date_of_input,
                               last_date_of_input,
                               species_id, species_name, fish_type_code, fish_type_textual,
                               strain)
                if batch_id not in batch_dict.keys():
                    batch_dict[aBatch.node_id] = aBatch  # aBatch.node()
                # rel_dict.append([aSite, aCage, 'HAS_CAGE'])
                rel_dict.append([aSite, aBatch, 'HAS_BATCH'])
                rel_dict.append([aCage, aSite, 'HAS_SITE'])
                rel_dict.append([aBatch, aCage, 'HAS_CAGE'])

                Periods = group.findall('Periods/Period')
                for period in tqdm(Periods, desc="Periods"):

                    first_day = find_key_value(period.find('FirstDay'))
                    last_day = find_key_value(period.find('LastDay'))
                    average_temperature = find_key_value(period.find('AverageTemperature'))
                    if average_temperature is not None:
                        create_observation(aCage, unit_id, 'Temp',
                                           'Temperature Sensor', 'Temperature Sensor Producer',
                                           sensor_dict,
                                           first_day, last_day,
                                           'Temperature', average_temperature, 0,
                                           observation_dict, rel_dict)
                        # create_observation(aCage, unit_id, observable_property='AverageTemperature',
                        # sensor_type='Temperature Sensor', sensor_producer='Temperature Sensor Producer',sensor_dict,
                        # first_day, last_day, observation_type='Temperature', value=average_temperature, biomass=0,
                        # observation_dict, rel_dict)
                    weight_sample_performed = find_key_value(period.find('WeightSamplePerformed'))
                    if weight_sample_performed is not None:
                        create_observation(aCage, unit_id, 'Weight',
                                           'Weight Sample Sensor', 'Weight Sensor Producer',
                                           sensor_dict,
                                           first_day, last_day,
                                           'Weight Sample', weight_sample_performed, 0,
                                           observation_dict, rel_dict)

                    name_of_feed = find_key_value(period.find('Feed/FeedingDetail/NameOfFeed'))
                    feed_amount = find_key_value(period.find('Feed/FeedingDetail/FeedAmount'))
                    if feed_amount is not None:
                        create_observation(aCage, unit_id, 'Feed',
                                           'Feed Sensor', 'Feed Producer',
                                           sensor_dict,
                                           first_day, last_day,
                                           name_of_feed, feed_amount, 0,
                                           observation_dict, rel_dict)

                    stocked_individ_count = find_key_value(period.find('Stocked/IndividCount'))
                    stocked_biomass = find_key_value(period.find('Stocked/Biomass'))
                    if stocked_biomass is not None:
                        create_observation(aCage, unit_id, 'StkBio',
                                           'Stocked Biomass Sensor', 'Stocked Biomass Sensor Producer',
                                           sensor_dict,
                                           first_day, last_day,
                                           'Stocked Biomass', stocked_individ_count, stocked_biomass,
                                           observation_dict, rel_dict)

                    movedin_individ_count = find_key_value(period.find('MovedIn/IndividCount'))
                    movedin_biomass = find_key_value(period.find('MovedIn/Biomass'))
                    if movedin_biomass is not None:
                        create_observation(aCage, unit_id, 'MovIn',
                                           'MovedIn Biomass Sensor', 'MovedIn Biomass Sensor Producer',
                                           sensor_dict,
                                           first_day, last_day,
                                           'MovedIn Biomass', movedin_individ_count, movedin_biomass,
                                           observation_dict, rel_dict)
                    # create a MOVEDOUT event

                    movedout_siteid = 0
                    mvdout_siteid = find_key_value(period.find('MovedOut/TransferDetail/ToSiteID'))
                    if mvdout_siteid is not None:
                        movedout_siteid = int(mvdout_siteid)
                    movedout_batchid = 0
                    mvdout_batchid = find_key_value(period.find('MovedOut/TransferDetail/ToGroupID'))
                    if mvdout_batchid is not None:
                        movedout_batchid = int(mvdout_batchid)
                    movedout_cageid = get_id(find_key_value(period.find('MovedOut/TransferDetail/ToUnitName')))


                    movedout_individcount = find_key_value(period.find('MovedOut/TransferDetail/StockTransferred/IndividCount'))
                    movedout_biomass = find_key_value(period.find('MovedOut/TransferDetail/StockTransferred/BIOMASS'))


                    #site_id --> SiteID
                    #batch_id --> GROUPID
                    #cage_id - unit_id --> get_id(unit_name)
                    if movedout_batchid > 0:
                        event_id = site_id + unit_id + batch_id + \
                                   movedout_siteid + movedout_cageid + movedout_batchid

                        aEvent = Event(event_id, "Transfer",
                                       site_id, unit_id, batch_id,
                                       movedout_siteid, movedout_cageid, movedout_batchid,
                                       first_day, last_day,
                                       movedout_individcount, movedout_biomass)
                        if event_id not in event_dict.keys():
                            event_dict[aEvent.node_id] = aEvent
                        rel_dict.append([aEvent, aCage, 'HAS_FROMCAGE'])
                        rel_dict.append([aEvent, aSite, 'HAS_FROMSITE'])
                        rel_dict.append([aEvent, aBatch, 'HAS_FROMBATCH'])
                        if movedout_siteid in site_dict.keys():
                            rel_dict.append([aEvent, site_dict[movedout_siteid], 'HAS_TOSITE'])
                        if movedout_cageid in cage_dict.keys():
                            rel_dict.append([aEvent, cage_dict[movedout_cageid], 'HAS_TOCAGE'])
                        if movedout_batchid in batch_dict.keys():
                            rel_dict.append([aEvent, batch_dict[movedout_batchid], 'HAS_TOBATCH'])



                    loss_individ_count = find_key_value(period.find('Loss/IndividCount'))
                    loss_biomass = find_key_value(period.find('Loss/Biomass'))
                    if loss_biomass is not None:
                        create_observation(aCage, unit_id, 'Loss',
                                           'Loss Biomass Sensor', 'Loss Biomass Sensor Producer',
                                           sensor_dict,
                                           first_day, last_day,
                                           'Loss Biomass', loss_individ_count, loss_biomass,
                                           observation_dict, rel_dict)

                    sold_individ_count = find_key_value(period.find('Sold/IndividCount'))
                    sold_biomass = find_key_value(period.find('Sold/Biomass'))
                    if sold_biomass is not None:
                        create_observation(aCage, unit_id, 'Sold',
                                           'Sold Biomass Sensor', 'Sold Biomass Sensor Producer',
                                           sensor_dict,
                                           first_day, last_day,
                                           'Sold Biomass', sold_individ_count, sold_biomass,
                                           observation_dict, rel_dict)

                    QualitySamples = period.findall('QualitySamples/QualitySample')
                    for qualitysample in tqdm(QualitySamples, desc="Quality Samples"):
                        sample_date = find_key_value(qualitysample.find('SampleDate'))
                        sample_individs = find_key_value(qualitysample.find('Individs'))
                        sample_astaxanthin = find_key_value(qualitysample.find('Astaxanthin'))
                        sample_salmofanB = find_key_value(qualitysample.find('SalmofanB'))
                        sample_fat = find_key_value(qualitysample.find('Fat'))
                        sample_weight_living = find_key_value(qualitysample.find('WeightLiving'))
                        sample_condition_factor = find_key_value(qualitysample.find('ConditionFactor'))
                        sample_total_length = find_key_value(qualitysample.find('TotalLength'))
                        sample_weight_gutted = find_key_value(qualitysample.find('WeightGutted'))

                        # quality_id, quality_name,
                        # sample_date, sample_individs,
                        # sample_astaxanthin, sample_salmofanB, sample_fat,
                        # sample_weight_living, sample_condition_factor,
                        # sample_total_length, sample_weight_gutted,
                        if sample_date is not None:
                            quality_id = batch_id + get_id('Quality') + \
                                         int(sample_date[0:4] + sample_date[5:7] + sample_date[8:10])
                            if quality_id not in quality_dict.keys():
                                aQuality = Quality(quality_id, 'Quality',
                                                   sample_date, sample_individs,
                                                   sample_astaxanthin, sample_salmofanB, sample_fat,
                                                   sample_weight_living, sample_condition_factor,
                                                   sample_total_length, sample_weight_gutted)
                                quality_dict[aQuality.node_id] = aQuality
                                rel_dict.append([aBatch, aQuality, 'HAS_Quality'])

                    OxygenReadings = period.findall('OxygenReadings/OxygenReading')
                    for oxygenreading in tqdm(OxygenReadings, desc="Oxygen Reading"):
                        oxy_date_time = find_key_value(oxygenreading.find('DateTime'))
                        oxy_value = find_key_value(oxygenreading.find('Value'))
                        if oxy_value is not None:
                            create_observation(aCage, unit_id, 'Oxy',
                                               'Oxygen Sensor', 'Oxygen Sensor Producer',
                                               sensor_dict,
                                               oxy_date_time, None,
                                               'Oxygen', oxy_value, 0,
                                               observation_dict, rel_dict)

                    # end Product details and their quality information
                    Harvested = period.findall('Harvested/HarvestDetail')
                    for harvestdetail in tqdm(Harvested, desc="Product"):

                        harvest_quality = find_key_value(harvestdetail.find('Quality'))
                        harvest_individcount = find_key_value(harvestdetail.find('IndividCount'))
                        harvest_grossbiomass = find_key_value(harvestdetail.find('GrossBiomass'))
                        harvest_netbiomass = find_key_value(harvestdetail.find('NetBiomass'))

                        # product_id, quality, individual_count,
                        # gross_biomass, net_biomass,
                        if harvest_quality is not None:
                            print("harvest_quality: ", harvest_quality)
                            product_id = int(batch_id + get_fl_id(harvest_quality))
                            print("product_id: ", product_id)
                            if product_id not in product_dict.keys():
                                aProduct = Product(product_id, harvest_quality,
                                                   harvest_individcount, harvest_grossbiomass,
                                                   harvest_netbiomass)
                                product_dict[aProduct.node_id] = aProduct
                                rel_dict.append([aBatch, aProduct, 'HAS_PRODUCT'])

    #return company_dict, batch_dict, cage_dict, site_dict, supplier_dict, event_dict, \
    #       sensor_dict, observation_dict, quality_dict, product_dict, \
    #       rel_dict


def main(settings):
    # XML file
    path = settings.get_value('input', 'path')
    print('path: ', path)
    # TODO: read all nodes from a directory
    #       1. making all dict as global variables
    #       2. loop on path all files

    files = [s for s in os.listdir(path) if s.endswith('.xml')]
    try:
        for filename in tqdm(walkdir(files), total=len(files)):
            with open(os.path.join(path, filename), 'r') as fh:
                print('path+filename: ', os.path.join(path, filename))
                parse_xml_file(os.path.join(path, filename))

    except StopIteration:
        return
    except KeyboardInterrupt:
        return

    '''

    filename = settings.get_value('input', 'filename')
    company_dict, batch_dict, cage_dict, site_dict, supplier_dict, event_dict, \
    sensor_dict, observation_dict, quality_dict, product_dict, \
    rel_dict = \
        parse_xml_file(os.path.join(path, filename))
    '''

    # Database connection
    uri = settings.get_value('database', 'uri')
    username = settings.get_value('database', 'username')
    password = settings.get_value('database', 'password')
    graph = py2neo.Graph(uri, user=username, password=password)
    tx = graph.begin()
    print('#############################################')
    for company in tqdm(company_dict, desc="Create nodes for companies"):
        tx.create(company_dict[company].node())
    for site in tqdm(site_dict, desc="Create nodes for sites"):
        tx.create(site_dict[site].node())
    for cage in tqdm(cage_dict, desc="Create nodes for cages"):
        tx.create(cage_dict[cage].node())
    for batch in tqdm(batch_dict, desc="Create nodes for batches"):
        tx.create(batch_dict[batch].node())
    for sensor in tqdm(sensor_dict, desc="Create nodes for sensors"):
        tx.create(sensor_dict[sensor].node())
    for observation in tqdm(observation_dict, desc="Create nodes for observations"):
        tx.create(observation_dict[observation].node())
    for quality in tqdm(quality_dict, desc="Create nodes for quality"):
        tx.create(quality_dict[quality].node())
    for product in tqdm(product_dict, desc="Create nodes for product"):
        tx.create(product_dict[product].node())
    for event in tqdm(event_dict, desc="Create nodes for event"):
        tx.create(event_dict[event].node())

    graph.commit(tx)
    for rel in tqdm(rel_dict, desc="Create relationships"):
        if len(graph.nodes.match(id=rel[0].node_id)) > 0 \
                and \
                len(graph.nodes.match(id=rel[1].node_id)) > 0:
            #print(rel[0].node_id, len(graph.nodes.match(id=rel[0].node_id)))
            #print(rel[1].node_id, len(graph.nodes.match(id=rel[1].node_id)))
            # print(rel[2])
            graph.create(
                create_relation(
                    graph.nodes.match(id=rel[0].node_id).first(),
                    graph.nodes.match(id=rel[1].node_id).first(),
                    rel[2]
                )
            )

    # for company_site_rel in company_site_rel_dict:
    #    graph.create(company_site_rel)
    # site_dict[aSite.node_id]



if __name__ == "__main__":
    args = parse_args()
    settings = Config(args.config)
    print('configuration file ', args)
    print("settings['input']['path']", settings.get_value('input', 'path'))
    print("settings['input']['filename']", settings.get_value('input', 'filename'))
    print("settings['database']['uri']", settings.get_value('database', 'uri'))
    print("settings['database']['username']", settings.get_value('database', 'username'))
    print("settings['database']['password']", settings.get_value('database', 'password'))

    main(settings)

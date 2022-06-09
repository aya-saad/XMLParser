from Database.Node import Node
import py2neo
import neotime


class Site(Node):
    # site_id, site_name, site_number, max_allowed_biomass,
    #                         last_data_of_registration, latitude, longitude)
    def __init__(self, site_id, site_name, site_number, max_allowed_biomass, last_data_of_registration, latitude,
                 longitude, label='Site'):
        super().__init__(site_id, site_name, label)
        self.site_name = site_name
        self.site_number = site_number
        self.max_allowed_biomass = max_allowed_biomass
        # self.last_data_of_registration = last_data_of_registration
        self.year = int(last_data_of_registration[0:4])
        self.month = int(last_data_of_registration[5:7])
        self.day = int(last_data_of_registration[8:10])
        self.latitude = latitude
        self.longitude = longitude
        # print(self.max_allowed_biomass)

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.site_name,
                           site_number=self.site_number,
                           max_allowed_biomass=self.max_allowed_biomass,
                           last_data_of_registration=neotime.datetime(self.year, self.month, self.day),
                           latitude=self.latitude,
                           longitude=self.longitude)

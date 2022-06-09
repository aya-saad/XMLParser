from Database.Node import Node
import py2neo
import neotime


# sample_date
# sample_individs
# sample_astaxanthin
# sample_salmofanB
# sample_fat
# sample_weight_living
# sample_condition_factor
# sample_total_length
# sample_weight_gutted
class Quality(Node):

    def __init__(self, quality_id, quality_name,
                 sample_date, sample_individs,
                 sample_astaxanthin, sample_salmofanB, sample_fat,
                 sample_weight_living, sample_condition_factor,
                 sample_total_length, sample_weight_gutted,
                 label='Quality'):
        super().__init__(quality_id, quality_name, label)
        self.sample_year = int(sample_date[0:4])
        self.sample_month = int(sample_date[5:7])
        self.sample_day = int(sample_date[8:10])
        self.sample_individs = sample_individs
        self.sample_astaxanthin = sample_astaxanthin
        self.sample_salmofanB = sample_salmofanB
        self.sample_fat = sample_fat
        self.sample_weight_living = sample_weight_living
        self.sample_condition_factor = sample_condition_factor
        self.sample_total_length = sample_total_length
        self.sample_weight_gutted = sample_weight_gutted

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption,
                           sample_date=neotime.datetime(self.sample_year, self.sample_month, self.sample_day),
                           sample_individs=self.sample_individs,
                           sample_astaxanthin=self.sample_astaxanthin,
                           sample_salmofanB=self.sample_salmofanB,
                           sample_fat=self.sample_fat,
                           sample_weight_living=self.sample_weight_living,
                           sample_condition_factor=self.sample_condition_factor,
                           sample_total_length=self.sample_total_length,
                           sample_weight_gutted=self.sample_weight_gutted
                           )

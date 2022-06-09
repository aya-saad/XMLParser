from Database.Node import Node
import py2neo
import neotime


class Observation(Node):
    def __init__(self, observation_id, observation_type, value,
                 first_date_of_input, last_date_of_input,
                 biomass=0, label='Observation'):
        super().__init__(observation_id, observation_type, label)
        self.value = value
        self.first_year = int(first_date_of_input[0:4])
        self.first_month = int(first_date_of_input[5:7])
        self.first_day = int(first_date_of_input[8:10])
        self.last_year = 1900
        self.last_month = 1
        self.last_day = 1
        if last_date_of_input is not None:
            self.last_year = int(last_date_of_input[0:4])
            self.last_month = int(last_date_of_input[5:7])
            self.last_day = int(last_date_of_input[8:10])
        self.biomass = biomass

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption,
                           first_date_of_input=neotime.datetime(self.first_year, self.first_month, self.first_day),
                           last_date_of_input=neotime.datetime(self.last_year, self.last_month, self.last_day),
                           value=self.value,
                           biomass=self.biomass
                           )

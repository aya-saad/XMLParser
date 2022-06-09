from Database.Node import Node
import py2neo
import neotime


# Cage(unit_name, unit_name, unit_volume, idc,
#                              first_date_of_input)
class Cage(Node):
    def __init__(self, cage_id, unit_name, unit_volume, first_date_of_input, label='Cage'):
        # year, month, day
        super().__init__(cage_id, unit_name, label)
        self.unit_volume = unit_volume
        self.year = int(first_date_of_input[0:4])
        self.month = int(first_date_of_input[5:7])
        self.day = int(first_date_of_input[8:10])
        # print(self.unit_volume, self.year, self.month, self.day)

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption,
                           unit_volume=self.unit_volume,
                           first_date_of_input=neotime.datetime(self.year, self.month, self.day)
                           )

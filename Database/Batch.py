from Database.Node import Node
import py2neo
import neotime


# (batch_id, batch_name,
#  first_date_of_input,
#  last_date_of_input,
#  species_id, species_name, fish_type_code, fish_type_textual,
#  strain)
class Batch(Node):

    def __init__(self, batch_id, batch_name,
                 first_date_of_input, last_date_of_input,
                 species_id, species_name, fish_type_code, fish_type_textual, strain,
                 label='Batch'):
        super().__init__(batch_id, batch_name, label)
        self.first_year = int(first_date_of_input[0:4])
        self.first_month = int(first_date_of_input[5:7])
        self.first_day = int(first_date_of_input[8:10])
        self.last_year = int(last_date_of_input[0:4])
        self.last_month = int(last_date_of_input[5:7])
        self.last_day = int(last_date_of_input[8:10])
        self.species_id = species_id
        self.species_name = species_name
        self.fish_type_code = fish_type_code
        self.fish_type_textual = fish_type_textual
        self.strain = strain
        # print(self.first_year, self.first_month, self.first_day,
        #      self.last_year, self.last_month, self.last_day,
        #      self.species_id, self.species_name, self.fish_type_code,
        #      self.fish_type_textual, self.strain)

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption,
                           first_date_of_input=neotime.datetime(self.first_year, self.first_month, self.first_day),
                           last_date_of_input=neotime.datetime(self.last_year, self.last_month, self.last_day),
                           species_id=self.species_id,
                           species_name=self.species_name,
                           fish_type_code=self.fish_type_code,
                           fish_type_textual=self.fish_type_textual,
                           strain=self.strain
                           )

from Database.Node import Node
import py2neo
import neotime


class Product(Node):
    def __init__(self, product_id, quality, individual_count,
                 gross_biomass, net_biomass, label='Product'):
        super().__init__(product_id, quality, label)
        self.individual_count = individual_count
        self.quality = quality
        self.gross_biomass = gross_biomass
        self.net_biomass = net_biomass

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption,
                           individual_count=self.individual_count,
                           quality=self.quality,
                           gross_biomass=self.gross_biomass,
                           net_biomass=self.net_biomass
                           )

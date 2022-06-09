from Database.Node import Node
import py2neo
import neotime
'''
event_id, "Transfer",
site_id, unit_id, batch_id,
movedout_siteid, movedout_unitname, movedout_batchid,
first_day, last_day,
movedout_individcount, movedout_biomass)    
'''

class Event(Node):
    def __init__(self, event_id, event_name, fromsite_id, fromcage_id, frombatch_id,
                 tosite_id, tocage_id, tobatch_id,
                 first_day, last_day,
                 individ_count, biomass, label='Event'):
        super().__init__(event_id, event_name, label)
        self.fromsite_id = fromsite_id
        self.fromcage_id = fromcage_id
        self.frombatch_id = frombatch_id

        self.tosite_id = tosite_id
        self.tocage_id = tocage_id
        self.tobatch_id = tobatch_id

        self.individ_count = individ_count
        self.biomass = biomass

        self.first_year = int(first_day[0:4])
        self.first_month = int(first_day[5:7])
        self.first_day = int(first_day[8:10])

        self.last_year = int(last_day[0:4])
        self.last_month = int(last_day[5:7])
        self.last_day = int(last_day[8:10])

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption,
                           fromsite_id=self.fromsite_id,
                           fromcage_id=self.fromcage_id,
                           frombatch_id=self.frombatch_id,
                           tosite_id=self.tosite_id,
                           tocage_id=self.tocage_id,
                           tobatch_id=self.tobatch_id,
                           first_date_of_input=neotime.datetime(self.first_year, self.first_month, self.first_day),
                           last_date_of_input=neotime.datetime(self.last_year, self.last_month, self.last_day)
                           )
    

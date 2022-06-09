from Database.Node import Node
import py2neo


class Sensor(Node):
    def __init__(self, sensor_id, sensor_type, producer, label='Sensor'):
        super().__init__(sensor_id, sensor_type, label)
        self.sensor_type = sensor_type
        self.producer = producer

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption,
                           sensor_type=self.sensor_type,
                           producer=self.producer)


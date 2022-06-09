from Database.Node import Node
import py2neo


class Supplier(Node):
    def __init__(self, label, suppliername, id):
        super().__init__(label, caption, id)
        self.suppliername = suppliername

    def node(self):
        s = py2neo.Node(self.label,
                        name=self.suppliername,
                        id=self.id)
        return s

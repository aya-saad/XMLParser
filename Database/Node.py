import py2neo


class Node:
    def __init__(self, node_id, caption, label):
        self.label = label
        self.caption = caption
        self.node_id = node_id
        # print(self.label, self.node_id, self.caption)

    def node(self):
        return py2neo.Node(self.label,
                           id=self.node_id,
                           caption=self.caption)

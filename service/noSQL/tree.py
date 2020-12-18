class Tree(object):
  "Generic tree node."
  def __init__(self, name=None, children=None,data=None):
    if name is not None:
        self.name = name
    self.children = []
    if children is not None:
        for child in children:
            self.add_child(child)
    if data is not None:
        self.data = data
  def __repr__(self):
    return self.name
  def add_child(self, node):
    assert isinstance(node, Tree)
    for child in self.children:
      if (child.data is None and node.data is None) or child.data == node.data:
        return child

    self.children.append(node)
    return node
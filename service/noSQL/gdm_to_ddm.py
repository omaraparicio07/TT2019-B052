from .langs import gdmLang as gdm
from .langs import ddmLang as ddm
from pyecore.resources import ResourceSet, URI
from pyecore.resources.xmi import XMIResource
from .tree import Tree


class ParserDDM(object):
  """
  Clase para tranformar el modelo gdm al modelo orientado a documentos
  """
  def loadModel(self, input_file):
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[gdm.nsURI] = gdm
    rset.resource_factory['gdm'] = lambda uri: XMIResource(uri)
    resource = rset.get_resource(URI(input_file))
    model = resource.contents[0]

    return model

  def saveModelDDM(self, model):
    # create a resourceSet that hold the contents of the gdm.ecore model and the instances we use/create
    rset = ResourceSet()
    # register the metamodel (available in the generated files)
    rset.metamodel_registry[ddm.nsURI] = ddm
    rset.resource_factory['ddm'] = lambda uri: XMIResource(uri)

    resource = rset.create_resource(URI('prueba_ddm.xmi'))
    resource.append(model)
    resource.save()
    return

  def addAttributes(self, document,entity):
      # features = list(filter(lambda f: isinstance(f,gdm.Attribute),entity.features))
    for attr in list(filter(lambda f: isinstance(f,gdm.Attribute),entity.features)):
        field = ddm.PrimitiveField()
        field.name = attr.name
        field.type = self.convertType(attr.type)
        document.fields.append(field)
    return

  def convertType(self, type_):
    if type_.name == "ID":
      ddmType = ddm.PrimitiveType.from_string("ID")
    elif type_.name == "NUMBER":
      ddmType = ddm.PrimitiveType.from_string("FLOAT")
    elif type_.name == "DATE":
      ddmType = ddm.PrimitiveType.from_string("DATE")
    elif type_.name == "TIMESTAMP":
      ddmType = ddm.PrimitiveType.from_string("TIMESTAMP")
    elif type_.name == "BOOLEAN":
      ddmType = ddm.PrimitiveType.from_string("BOOLEAN")
    else:
      ddmType = ddm.PrimitiveType.from_string("TEXT")

    return ddmType

  def toFirstLower(self, test_str):
    return test_str[0].lower() + test_str[1:]

  def populateDocument(self, document, entity, tree, mainEntities):
    self.addAttributes(document,entity)

    for child in tree.children:
      reference = child.data
      newField = None
      # si la referencia apunta a una entidad principal, en lugar de generar el documento creamos una referencia
      if any(map(lambda me: me == reference.entity, mainEntities)):
        newField = ddm.PrimitiveField()
        newField.name = self.toFirstLower(reference.entity.name) + "Ref"
        newField.type = ddm.PrimitiveType.from_string("ID")
      else:
        newField = ddm.Document()
        newField.name = self.toFirstLower(reference.entity.name)
        self.populateDocument(newField, reference.entity, child, mainEntities)

      if (reference.cardinality != "1"):
        # encapsulate field in an array
        arrayField = ddm.ArrayField()
        arrayField.name = newField.name + "Array"
        arrayField.type = newField
        document.fields.add(arrayField)
      else:
        document.fields.add(newField)

    return


  def createAccessTree(self, queries):
    tree = Tree()

    for query in queries:
      for inclusion in query.inclusions:
        auxTree = tree
        for ref in inclusion.refs:
          child = auxTree.add_child(Tree(data=ref))
          auxTree = child

    return tree

  def getTree(self, entity2accessTree, entity):

    for pair in entity2accessTree:
      if pair[0] == entity:
        tree = pair[1]

    return tree

  def getAllTrees(self, entity2accessTree):
    lista = []

    for pair in entity2accessTree:
      #if pair[1] != tree:
      lista.append(pair[1])
    return lista

  def addAllTreeNodes(self, treeNodes,lista):
    for item in lista:
      treeNodes.append(item)
    return

  def searchEntity(self, entity,tree):
    treeNodes = []
    for child in tree.children:
      if child.data.entity == entity:
        treeNodes.append(child)
      self.addAllTreeNodes(treeNodes, self.searchEntity(entity,child))
    return treeNodes

  def addTreeNode(self, tree, treeNode):
    for child in treeNode.children:
      addedChild = tree.add_child(Tree(data=child.data))
      self.addTreeNode(addedChild,child)
    return

  def completeAccessTree(self, entity, tree, othersTrees):

    for oTree in othersTrees:
      treeNodes = self.searchEntity(entity,oTree)
      for treeNode in treeNodes:
        self.addTreeNode(tree,treeNode)
    return

  def main(self, gdmModelFileName = ''):

    gdmModel = self.loadModel(f"{gdmModelFileName}.xmi")

    ddmModel = ddm.DocumentDataModel()

    # Obtenemos las entidades de los elementos From
    # mainEntities = gdm.queries.map[q | q.from.entity].toSet
    mainEntities = set(map(lambda q: q.from_.entity, gdmModel.queries))

    # entityToQueries =  mainEntities.map[me | me -> gdm.queries.filter[q | q.from.entity.equals(me)]]
    entityToQueries = list(map(lambda me: (me, list(filter(lambda q: q.from_.entity.name == me.name, gdmModel.queries))), mainEntities))

    # val entity2accessTree = newImmutableMap(entityToQueries.map[e2q | e2q.key -> createAccessTree(e2q.value)])
    entity2accessTree = list(map(lambda e2q: ( e2q[0], self.createAccessTree(e2q[1])), entityToQueries))

    # Completamos cada árbol de acceso
    for entity in mainEntities:
      tree = self.getTree(entity2accessTree,entity)
      othersTrees = self.getAllTrees(entity2accessTree)
    #   for t in othersTrees:
    #       if t == tree:
    #           othersTrees.remove(t)
    #           hola = "hola"
      self.completeAccessTree(entity, tree, othersTrees)

    # Generamos las colecciones
    for entity in mainEntities:
      tree = self.getTree(entity2accessTree,entity)
      collection = ddm.Collection()
      collection.name = entity.name
      docType = ddm.Document()
      docType.name = "root"
      collection.root = docType
      self.populateDocument(docType,entity,tree,mainEntities)
      ddmModel.collections.append(collection)
      self.saveModelDDM(ddmModel)

    self.saveModelDDM(ddmModel)


if __name__ == '__main__':
  main()
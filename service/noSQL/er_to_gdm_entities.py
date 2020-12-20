import logging as Log

Log.basicConfig(level=Log.DEBUG)

class GDMEntities(object):
  """
  Clase para obtener las entidades del gdm de texto simple a partir de un diagrama er creado con gojs
  """
  def isConnectedTo(self, key, nodeKey,linkData):

    for link in linkData:
      if ( link["from"] == key and link["to"] == nodeKey ) \
      or ( link["from"] == nodeKey and link["to"] == key ):
        # están enlazados los nodos
        return True

    return False

  def getConnectedNodes(self, key, nodeData, linkData):    
    lista = list(filter(lambda item: self.isConnectedTo(key,item['key'],linkData), nodeData))
    return lista

  def isAttribute(self, type_):
    if type_ == "attribute" or type_ == "keyAttribute" or type_ == "multivalueAttribute" or type_ == "compositeAttribute":
      return True
    return  False

  def getNode(self, key, nodeData):
    node = list(filter(lambda item: item['key'] == key, nodeData))
    return node[0]

  def getRelationInfo(self, key,linkData,nodeData):
    relation = {}
    links = []
    for link in linkData:
      if link["from"] == key or link["to"] == key:
        links.append(link)
    
    # elements = list()
    # for link in links:
    #     elements.append(getNode(link["to"], nodeData))
    #     elements.append(getNode(link["from"], nodeData))

    # elements = list(dict((v['key'],v) for v in elements).values())

    # Si la key de la relación está en ambos elementos "from"
    if all(list(map(lambda link: link["from"] == key, links))):
      relation["from"] =  self.getNode(links[0]["to"],nodeData)
      relation["fromC"] = links[0]["cardinality"]
      relation["to"] =  self.getNode(links[1]["to"],nodeData)
      relation["toC"] = links[1]["cardinality"]
    # Si la key de la relación está en ambos elementos "to"
    elif all(list(map(lambda link: link["to"] == key, links))):
      relation["from"] =  self.getNode(links[0]["from"],nodeData)
      relation["fromC"] = links[0]["cardinality"]
      relation["to"] =  self.getNode(links[1]["from"],nodeData)
      relation["toC"] = links[1]["cardinality"]
    else:
      for link in links:
        if link["from"] != key:
          relation["from"] =  self.getNode(link["from"],nodeData)
          relation["fromC"] = link["cardinality"]
        if link["to"] != key:
          relation["to"] =  self.getNode(link["to"],nodeData)
          relation["toC"] = link["cardinality"]
    return relation 

  def parseAttribute(self, attribute):
    line = ''
    if attribute["unique"] == True:
      line = "id " + attribute["name"] + " unique"
    elif attribute["array"] == True:
      line = attribute["type"] + "[*] " + attribute["name"]
    else:
      line = attribute["type"] + " " + attribute["name"] 
    return "  " + line + "\n"

  def parseReference(self, reference):
    line = ""
    cardinality = "[*]" if reference["cardinality"] != "1" else "[1]"

    line = "ref " + reference["entity"] + cardinality + " " + reference["name"]
    return "  " + line + "\n"
  
  def toFirstLower(self, test_str):
    return test_str[0].lower() + test_str[1:]

  def main(self, diagram):
    Log.info("Ejecutando clase principal del parser er_to_gdm")
    nodeData = diagram['nodeDataArray']
    linkData = diagram['linkDataArray']

    # if not (nodeData or linkData):
    #   return
    
    entities = list(filter(lambda item: item['type'] == "entity",nodeData))


    entities2pair = list(map(lambda entity: (entity, self.getConnectedNodes(entity['key'], nodeData, linkData)),entities))
    count = 0
    for pair in entities2pair:
      entity = pair[0]
      features = pair[1]
      attributes = []
      references = []
      for feature in features:
        if (feature['type'] == "relation"):
          reference = {}
          relation = self.getRelationInfo( feature["key"], linkData, nodeData)

          if (relation["from"]["key"] != entity["key"]):
            reference["entity"] = relation["from"]["text"]
            reference["cardinality"] = relation["fromC"]
            if relation["fromC"] != '1':
              reference["name"] = feature["text"] + relation["from"]["text"]
            else:
              reference["name"] = self.toFirstLower(relation["from"]["text"])
          else:
            reference["entity"] = relation["to"]["text"]
            reference["cardinality"] = relation["toC"]
            # Si la relación es a N, va el nombre de la relación concatenado con el nombre de la entidad
            if relation["toC"] != '1':
                reference["name"] = feature["text"] + relation["to"]["text"]
            else:
                reference["name"] = self.toFirstLower(relation["to"]["text"])

          references.append(reference)
        if ( self.isAttribute(feature['type']) ):
          attribute = {}
          attribute["name"] = feature['text']
          attribute["type"] =  feature["gdmType"]
          attribute["array"] = True if feature["type"] == "multivalueAttribute" else False
          attribute["unique"] = True if feature["type"] == "keyAttribute" else False
          if attribute["unique"] == True:
            attribute["type"] = "id"
          attributes.append(attribute)
        
        # Escribimos el archivo de texto
      if count == 0:
        count += 1
        with open("salida.gdm", 'w') as output_file:
          output_file.write("entity " + entity["text"] + " {\n")
          for attribute in reversed(attributes):
            output_file.write(self.parseAttribute(attribute))
          for reference in reversed(references):
            output_file.write(self.parseReference(reference))
          output_file.write("}\n\n")
          output_file.close()
      else:
        with open("salida.gdm", 'a') as output_file:
          output_file.write("entity " + entity["text"] + " {\n")
          for attribute in reversed(attributes):
            output_file.write(self.parseAttribute(attribute))
          for reference in reversed(references):
            output_file.write(self.parseReference(reference))
          output_file.write("}\n\n")
          output_file.close()


if __name__ == '__main__':
    main()
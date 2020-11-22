
diagram = {
  "email": "omar@email.tv",
  "diagram": {
    "class": "GraphLinksModel",
    "modelData": {
      "position": "-435.4971485581509 -328.4277263020359"
    },
    "nodeDataArray": [
      {
        "type": "entity",
        "text": "Pedido",
        "figure": "Rectangle",
        "fill": "white",
        "key": -1,
        "loc": "-210 -110",
        "Comments": ""
      },
      {
        "type": "entity",
        "text": "Persona",
        "figure": "Rectangle",
        "fill": "white",
        "key": -13,
        "loc": "-110 -10",
        "Comments": ""
      },
      {
        "type": "keyAttribute",
        "text": "CURP",
        "figure": "Ellipse",
        "fill": "white",
        "key": -15,
        "loc": "-180 -60",
        "Comments": ""
      },
      {
        "type": "atribute",
        "text": "nombre",
        "figure": "Ellipse",
        "fill": "white",
        "key": -16,
        "loc": "-180 -60",
        "Comments": ""
      },
      {
        "type": "keyAttribute",
        "text": "idP",
        "figure": "Ellipse",
        "fill": "white",
        "key": -2,
        "loc": "-210 -210",
        "Comments": ""
      },
      {
        "type": "relation",
        "text": "realiza",
        "figure": "Diamond",
        "fill": "white",
        "key": -3,
        "loc": "20 -110",
        "Comments": ""
      },
      {
        "type": "entity",
        "text": "Cliente",
        "figure": "Rectangle",
        "fill": "white",
        "key": -4,
        "loc": "220 -120",
        "Comments": ""
      },
      {
        "type": "atribute",
        "text": "nombre",
        "figure": "Ellipse",
        "fill": "white",
        "key": -5,
        "loc": "250 -10",
        "Comments": ""
      },
      {
        "type": "keyAttribute",
        "text": "idC",
        "figure": "Ellipse",
        "fill": "white",
        "key": -6,
        "loc": "280 -210",
        "Comments": ""
      },
      {
        "type": "atribute",
        "text": "fecha",
        "figure": "Ellipse",
        "fill": "white",
        "key": -7,
        "loc": "-350 -110",
        "Comments": ""
      },
      {
        "type": "entity",
        "text": "articulo",
        "figure": "Rectangle",
        "fill": "white",
        "key": -8,
        "loc": "-210 130",
        "Comments": ""
      },
      {
        "type": "keyAttribute",
        "text": "sku",
        "figure": "Ellipse",
        "fill": "white",
        "key": -9,
        "loc": "-210 240",
        "Comments": ""
      },
      {
        "type": "atribute",
        "text": "num_serie",
        "figure": "Ellipse",
        "fill": "white",
        "key": -10,
        "loc": "-350 130",
        "Comments": ""
      },
      {
        "type": "relation",
        "text": "se compone",
        "figure": "Diamond",
        "fill": "white",
        "key": -11,
        "loc": "-210 10",
        "Comments": ""
      },
      {
        "type": "relation",
        "text": "es",
        "figure": "Diamond",
        "fill": "white",
        "key": -14,
        "loc": "-210 10",
        "Comments": ""
      },
      {
        "type": "atribute",
        "text": "cantidad",
        "figure": "Diamond",
        "fill": "white",
        "key": -12,
        "loc": "-180 200",
        "Comments": ""
      }
    ],
    "linkDataArray": [
      {
        "from": -2,
        "to": -1,
        "toText": "",
        "fromText": ""
      },
      {
        "from": -1,
        "to": -7
      },
      {
        "from": -1,
        "to": -3,
        "toText": "1",
        "fromText": "N"
      },
      {
        "from": -3,
        "to": -4,
        "toText": "1",
        "fromText": "N"
      },
      {
        "from": -6,
        "to": -4,
        "toText": "",
        "fromText": ""
      },
      {
        "from": -13,
        "to": -14,
        "toText": "1",
        "fromText": "1"
      },
      {
        "from": -14,
        "to": -4,
        "toText": "1",
        "fromText": "1"
      },
      {
        "from": -4,
        "to": -5
      },
      {
        "from": -16,
        "to": -13
      },
      {
        "from": -15,
        "to": -13
      },
      {
        "from": -8,
        "to": -9
      },
      {
        "from": -8,
        "to": -10
      },
      {
        "from": -12,
        "to": -11
      },
      {
        "from": -1,
        "to": -11,
        "toText": "N",
        "fromText": "M"
      },
      {
        "from": -11,
        "to": -8,
        "toText": "N",
        "fromText": "M"
      }
    ]
  }
}

class Relational():
  """
  Clase que implementa la obtención de sentencias SQL a partir de un diagrama ER generado por
  el proyecto: https://github.com/martinez-acosta/TT-2019-B052.git
  """

  def __init__(self,diagram, greet):
    self.diagram = diagram
    self.greet = greet


  def getSentencesSQL(self, project_name, entitiesWithAttrs, relations_NM_to_table_with_attr):
    database_template = """
  DROP DATABASE if exists {db_name};
  CREATE DATABASE {db_name};
  USE {db_name};
  """

    script_sentences = database_template.format(db_name=project_name)

    for table in entitiesWithAttrs:
      # get name table in dict with next(iter(table))
      script_sentences += self.build_table_sentence(table)

    script_sentences +="------- Table Relationships N:M -------------"

    for table in relations_NM_to_table_with_attr:
      # get name table in dict with next(iter(table))
      script_sentences += self.build_table_nm_sentence(table)

    return script_sentences

  def build_table_sentence(self, table_dict):

    table_template = """
  ---------------- CREATE TABLE ----------------
  -- step 1. drop table if exists
  DROP TABLE IF EXISTS {table_name} CASCADE;
  -- step 2. create table 
  CREATE TABLE IF NOT EXISTS {table_name} (
  {attrs_sentences},
  {primary_key}
  {foreing_keys}
  ) ENGINE=InnoDB;
  """
    attr_by_table = ""
    primarykey = next(iter(table_dict.values())).get('primary_key')
    attr_list = next(iter(table_dict.values())).get('attributes')
    foreingKeys = next(iter(table_dict.values())).get('foreing_keys')
    table_name = next(iter(table_dict))[0].replace(" ", "_")
    foreing_keys=""
    primary_key=""

    for table in table_dict:
      attr_by_table = self.build_columns_sentences(attr_list)
      primary_key = self.buildPrimaryKey(attr_list)
      if foreingKeys:
        primary_key += ","
        foreing_keys = self.buildForeingKeys(foreingKeys)

    return table_template.format(table_name=table_name, attrs_sentences=attr_by_table, primary_key=primary_key, foreing_keys=foreing_keys)

  def build_table_nm_sentence(self, table_dict):

    table_template = """
  ---------------- CREATE TABLE NM relationship----------------
  DROP TABLE IF EXISTS {table_name} CASCADE;
  CREATE TABLE IF NOT EXISTS {table_name} (
  {attrs_sentences},
  {primary_key}
  {foreing_keys}
  ) ENGINE=InnoDB;
  """
    attr_by_table = ""
    attr_primarykey_list = next(iter(table_dict.values())).get('primary_keys')
    attr_relation_list = next(iter(table_dict.values())).get('attr_relationship')
    foreingKeys_list = next(iter(table_dict.values())).get('foreing_keys')
    table_name = next(iter(table_dict))[0].replace(" ", "_")
    foreing_keys=""
    primary_key=""

    for table in table_dict:
      attr_by_table = self.build_columns_nm(attr_primarykey_list)
      if attr_relation_list:
        attr_by_table += ",\n"
        attr_by_table += self.build_columns_sentences(attr_relation_list)
      primary_key = "PRIMARY KEY ({})".format(",".join([attr for attr in attr_primarykey_list]))
      if foreingKeys_list:
        primary_key += ","
        foreing_keys = self.buildForeingKeys(attr_primarykey_list)

    return table_template.format(table_name=table_name, attrs_sentences=attr_by_table, primary_key=primary_key, foreing_keys=foreing_keys)

  def buildPrimaryKey(self, attr_list):
    primary_key_sentence = "PRIMARY KEY ({})"
    primary_key = [attr[0] for attr in attr_list if attr[2] == 'keyAttribute']
    return primary_key_sentence.format(",".join(primary_key))

  def buildForeingKeys(self, attr_list):
    foreing_key_sentence = "FOREIGN KEY ({attr_name}) REFERENCES {ref_table_name} ({attr_ref_table})"
    fk_list = []
    for attr in attr_list:
      attr_ref_table, ref_table = attr.split("_")
      fk_list.append(f"FOREIGN KEY ({attr}) REFERENCES {ref_table} ({attr_ref_table})")
    return ",\n".join(fk_list)

  def build_columns_sentences(self, attr_list):

    column_template= "{} varchar(255) NOT NULL DEFAULT ''"
    columns_script = []
    for column in attr_list:
      attr_name = column[0].replace(" ", "_")
      columns_script.append(column_template.format(attr_name))

    return ",\n".join(columns_script)

  def build_columns_nm(self, attr_list):

    column_template= "{} varchar(255) NOT NULL DEFAULT ''"
    columns_script = []
    for column in attr_list:
      attr_name = column.replace(" ", "_")
      columns_script.append(column_template.format(attr_name))

    return ",\n".join(columns_script)

  def getEntities(self, diagram):
    entities = []
    print(f"las keys del obj diagram {diagram.keys()}")
    for node in diagram['nodeDataArray']:
      if node['type'] == 'entity':
        entities.append(
          (node['text'], node['key'])
          )
    return entities

  def getAttrs(self, diagram):
    attrs = []
    for node in diagram['nodeDataArray']:
      if node['type'] in ['atribute', 'atributeDerived', 'keyAttribute', 'atributeComposite']:
        attrs.append(
          (node['text'], node['key'], node['type'])
          )
    return attrs

  def getRelationships(self, diagram):
    relationships = []
    for node in diagram['nodeDataArray']:
      if node['type'] in ['relation']:
        relationships.append(
          (node['text'], node['key'])
          )
    return relationships

  def validateOnlyBinarieRelationship(self, relationKey, diagram):
    count = 0
    for node in diagram['linkDataArray']:
      if node['from'] == relationKey and [entity for entity in entities if entity[1] == node['to']]:
        count += 1
      if node['to'] == relationKey and [entity for entity in entities if entity[1] == node['from']]:
        count += 1
    return True if count == 2 else False


  def getEntityWithAtributes(self, diagram, entity, attrs):
    diagramDict = diagram
    print(f" que paso {diagramDict['linkDataArray']}")
    entityWithAttr = []
    for node in diagramDict['linkDataArray']:  #pattern matching from & to
      if node['from'] == entity[1]:
        for attr in attrs:
          if attr[1] == node['to']:
            entityWithAttr.append(attr)
      if node['to'] == entity[1]:
        for attr in attrs:
          if attr[1] == node['from']:
            entityWithAttr.append(attr)
    primary_key = self.validateKeyAttibute({ entity : entityWithAttr })

    return { entity : {'attributes':entityWithAttr, 'primary_key': primary_key, 'foreing_keys':[] } }

  def getRelationsNM(self, diagram, relationship):
    attr_nm_relation = []
    diagramDict = diagram
    for node in diagramDict['linkDataArray']:
      if ('toText' in node and 'fromText' in node) and (node['toText'] and node['fromText']):
        if node['toText'] in ['N','M'] and node['fromText'] in ['N','M']:
          if node['to'] == relationship[1]:
            attr_nm_relation.append(node['from'])
          if node['from'] == relationship[1]:
            attr_nm_relation.append(node['to'])
    return {relationship :  attr_nm_relation} if attr_nm_relation else None

  def getRelations1M(self, diagram, relationship):
    """
    Función para obtener las relaciones 1 a muchos del diagrama entidad relación
    """
    attr_nm_relation = []
    diagramDict = diagram
    for node in diagramDict['linkDataArray']:
      if ('toText' in node and 'fromText' in node) and (node['toText'] and node['fromText']):
        if node['toText'] in ['1','N'] and node['fromText'] in ['N','1']:
          if node['to'] == relationship[1] :
            attr_nm_relation.append((node['from'], node['fromText']))
          if node['from'] == relationship[1] :
            attr_nm_relation.append((node['to'], node['toText']))
    return {relationship :  attr_nm_relation} if attr_nm_relation else None

  def getRelations11(self, diagram, relationship):
    """
    Función para obtener las relaciones 1 a 1 del diagrama entidad relación
    """
    attr_nm_relation = []
    diagramDict = diagram
    for node in diagramDict['linkDataArray']:
      if ('toText' in node and 'fromText' in node) and (node['toText'] and node['fromText']):
        if node['toText'] == '1' and node['fromText'] == '1':
          if node['to'] == relationship[1] :
            attr_nm_relation.append((node['from'], node['fromText']))
          if node['from'] == relationship[1] :
            attr_nm_relation.append((node['to'], node['toText']))
    return {relationship :  attr_nm_relation} if attr_nm_relation else None

  def setForeingKey(self, relations_1N_cardinality, entitiesWithAttrs):

    table_ref = ""
    attr_fk = ""
    table_fk = ""
    for key in next(iter(relations_1N_cardinality.values())):
      attributes_entity =  [entity for entity in entitiesWithAttrs if next(iter(entity))[1] == key[0]]
      if key[1] == '1':
        pk_ref = next(iter(attributes_entity[0].values()))['primary_key'][0]
        ref_table = next(iter(attributes_entity[0]))
        table_ref = ref_table[0]
        attr_fk = f"{pk_ref[0]}_{ref_table[0].lower()}"
      if key[1] == 'N':
        table_fk = [ entity for entity in entitiesWithAttrs if next(iter(entity))[1] == key[0]]
        ref_table = next(iter(table_fk[0]))
        table_fk = attributes_entity
    # obtenemos el indice del diccionario de la entidad a modificar
    index_entity = next(i for i,item in enumerate(entitiesWithAttrs) if item == table_fk[0])
    # agregamos el atributo a la lista de atributos de la entidad
    next(iter(entitiesWithAttrs[index_entity].values()))['attributes'].append((attr_fk, 0, 'fk_attribute'))
    # agregamos el atributo a las llaves foraneas de la entidad
    next(iter(entitiesWithAttrs[index_entity].values()))['foreing_keys'].append(attr_fk)
    
    return None

  def setForeingKey11(self, relations_1_1_cardinality, entitiesWithAttrs):

    l_table, r_table = next(iter(relations_1_1_cardinality.values()))
    print(f"LT {l_table} RL {r_table}")
    # obtenemos las entidades de la relacion con sus atributos
    attributes_l_entity =  [entity for entity in entitiesWithAttrs if next(iter(entity))[1] == l_table[0]]
    attributes_r_entity =  [entity for entity in entitiesWithAttrs if next(iter(entity))[1] == r_table[0]]
    ## obtener la llave primararia de la tabla 'izquierda'
    pk_l_entity = next(iter(attributes_l_entity[0].values()))['primary_key'][0]
    #formamos la llave forarea con la pk de la tabal izquierda concatenando el nombre de la entidad
    ref_table = next(iter(attributes_l_entity[0]))
    attr_fk = f"{pk_l_entity[0]}_{ref_table[0].lower()}"

    # recuperamos el indice de la tabla 'R' a modificar 
    index_entity = next(i for i,item in enumerate(entitiesWithAttrs) if item == attributes_r_entity[0])

    #Agregamos el atributo a la tabla R
    next(iter(entitiesWithAttrs[index_entity].values()))['attributes'].append((attr_fk, 0, 'fk_attribute'))
    # agregamos el atributo a las llaves foraneas de la entidad de la tabla R
    next(iter(entitiesWithAttrs[index_entity].values()))['foreing_keys'].append(attr_fk)

  def validateKeyAttibute(self, entity_with_attrs):
    attrs = next(iter(entity_with_attrs.values())) # get attributes in entinty_with_attr dictionary
    primary_key = [attr for attr in attrs if attr[2] == 'keyAttribute']
    
    return primary_key

  def greeting(self):
    print(type(self.diagram))
    return f"Saludos desde la clase relacional.py {self.greet}"

  def convertToSQLSenteneces(self, diagram):
    
    entities = self.getEntities(diagram)
    attrs = self.getAttrs(diagram)
    entitiesWithAttrs = [self.getEntityWithAtributes(diagram, entity, attrs) for entity in entities]
    entitiesWithAttrs_validation = [self.validateKeyAttibute(atributes) for atributes in entitiesWithAttrs]
    relations = self.getRelationships(diagram)
    relations_NM_to_table = [self.getRelationsNM(diagram, relationship ) for relationship in relations]
    relations_1M = [self.getRelations1M(diagram, relationship ) for relationship in relations]
    relations_1M = [ i for i in relations_1M if i]
    self.setForeingKey(relations_1M[0], entitiesWithAttrs)
    relations_1_1 = [self.getRelations11(diagram, relationship ) for relationship in relations]
    relations_1_1 = [i for i in relations_1_1 if i]
    self.setForeingKey11(relations_1_1[0], entitiesWithAttrs)
    relations_NM_to_table = [ i for i in relations_NM_to_table if i] #remove empty items
    relations_NM_to_table_with_attr = [self.getAttrsNMRelation(diagram, entitiesWithAttrs, relation_nm, attrs) for  relation_nm in relations_NM_to_table]

    return self.getSentencesSQL("prueba_sql", entitiesWithAttrs, relations_NM_to_table_with_attr)


  def getAttrsNMRelation(self, diagram, entitiesWithAttrs, relation_nm, attrs):
    attr_nm_relation = []
    primary_keys = []
    foreing_keys = []
    for entity_attrs in entitiesWithAttrs:
      if next(iter(entity_attrs))[1] in next(iter(relation_nm.values())):
        primary_key = next(iter(entity_attrs.values()))['primary_key'][0]
        ref_table = next(iter(entity_attrs))
        primary_keys.append(f"{primary_key[0]}_{ref_table[0].lower()}")
        foreing_keys.append(ref_table[0])
    attr_nm_relation = [self.getEntityWithAtributes(diagram, next(iter(relation_nm)), attrs)]
    return {next(iter(relation_nm)) : 
              {
                "primary_keys":primary_keys,
                "foreing_keys" : foreing_keys,
                "attr_relationship": next(iter(attr_nm_relation[0].values()))['attributes']
              }
            }

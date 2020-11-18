
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
        "from": -4,
        "to": -5
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

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def getSentencesSQL(project_name, entitiesWithAttrs, relations_NM_to_table_with_attr):
  database_template = """
DROP DATABASE if exists {db_name};
CREATE DATABASE {db_name};
USE {db_name};
"""

  script_sentences = database_template.format(db_name=project_name)

  for table in entitiesWithAttrs:
    # get name table in dict with next(iter(table))
    script_sentences += build_table_sentence(table)

  script_sentences +="------- Table Relationships N:M -------------"

  for table in relations_NM_to_table_with_attr:
    # get name table in dict with next(iter(table))
    script_sentences += build_table_nm_sentence(table)

  return script_sentences

def build_table_sentence(table_dict):

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
    attr_by_table = build_columns_sentences(attr_list)
    primary_key = buildPrimaryKey(attr_list)
    if foreingKeys:
      primary_key += ","
      foreing_keys = buildForeingKeys(foreingKeys)

  return table_template.format(table_name=table_name, attrs_sentences=attr_by_table, primary_key=primary_key, foreing_keys=foreing_keys)

def build_table_nm_sentence(table_dict):

  table_template = """
---------------- CREATE TABLE NM relationship----------------
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
  attr_primarykey_list = next(iter(table_dict.values())).get('primary_keys')
  attr_relation_list = next(iter(table_dict.values())).get('attr_relationship')
  foreingKeys_list = next(iter(table_dict.values())).get('foreing_keys')
  table_name = next(iter(table_dict))[0].replace(" ", "_")
  foreing_keys=""
  primary_key=""

  for table in table_dict:
    attr_by_table = build_columns_nm(attr_primarykey_list)
    if attr_relation_list:
      attr_by_table += ",\n"
      attr_by_table += build_columns_sentences(attr_relation_list)
    primary_key = "PRIMARY KEY ({})".format(",".join([attr for attr in attr_primarykey_list]))
    if foreingKeys_list:
      primary_key += ","
      foreing_keys = buildForeingKeys(attr_primarykey_list)

  return table_template.format(table_name=table_name, attrs_sentences=attr_by_table, primary_key=primary_key, foreing_keys=foreing_keys)

def buildPrimaryKey(attr_list):
  primary_key_sentence = "PRIMARY KEY ({})"
  primary_key = [attr[0] for attr in attr_list if attr[2] == 'keyAttribute']
  return primary_key_sentence.format(",".join(primary_key))

def buildForeingKeys(attr_list):
  foreing_key_sentence = "FOREIGN KEY ({attr_name}) REFERENCES {ref_table_name} ({attr_ref_table})"
  fk_list = []
  for attr in attr_list:
    attr_ref_table, ref_table = attr.split("_")
    fk_list.append(f"FOREIGN KEY ({attr}) REFERENCES {ref_table} ({attr_ref_table})")
  return ",\n".join(fk_list)

def build_columns_sentences(attr_list):

  # TODO: agregar relaciones a los atributos en caso de ser necesarias
  column_template= "{} varchar(255) NOT NULL DEFAULT ''"
  columns_script = []
  for column in attr_list:
    attr_name = column[0].replace(" ", "_")
    columns_script.append(column_template.format(attr_name))

  return ",\n".join(columns_script)

def build_columns_nm(attr_list):

  # TODO: agregar relaciones a los atributos en caso de ser necesarias
  column_template= "{} varchar(255) NOT NULL DEFAULT ''"
  columns_script = []
  for column in attr_list:
    attr_name = column.replace(" ", "_")
    columns_script.append(column_template.format(attr_name))

  return ",\n".join(columns_script)

def getEntities(diagram):
  entities = []
  for node in diagram['diagram']['nodeDataArray']:
    if node['type'] == 'entity':
      entities.append(
        (node['text'], node['key'])
        )
  return entities

def getAttrs(diagram):
  attrs = []
  for node in diagram['diagram']['nodeDataArray']:
    if node['type'] in ['atribute', 'atributeDerived', 'keyAttribute', 'atributeComposite']:
      attrs.append(
        (node['text'], node['key'], node['type'])
        )
  return attrs

def getRelationships(diagram):
  relationships = []
  for node in diagram['diagram']['nodeDataArray']:
    if node['type'] in ['relation']:
      relationships.append(
        (node['text'], node['key'])
        )
  return relationships

def validateOnlyBinarieRelationship(relationKey, diagram):
  count = 0
  for node in diagram['diagram']['linkDataArray']:
    if node['from'] == relationKey and [entity for entity in entities if entity[1] == node['to']]:
      count += 1
    if node['to'] == relationKey and [entity for entity in entities if entity[1] == node['from']]:
      count += 1
  return True if count == 2 else False


def getEntityWithAtributes(diagram, entity, attrs):
  diagramDict = diagram['diagram']
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
  primary_key = validateKeyAttibute({ entity : entityWithAttr })

  return { entity : {'attributes':entityWithAttr, 'primary_key': primary_key, 'foreing_keys':[] } }

def getRelationsNM(diagram, relationship):
  attr_nm_relation = []
  diagramDict = diagram['diagram']
  for node in diagramDict['linkDataArray']:
    if ('toText' in node and 'fromText' in node) and (node['toText'] and node['fromText']):
      if node['toText'] in ['N','M'] and node['fromText'] in ['N','M']:
        if node['to'] == relationship[1]:
          attr_nm_relation.append(node['from'])
        if node['from'] == relationship[1]:
          attr_nm_relation.append(node['to'])
  return {relationship :  attr_nm_relation} if attr_nm_relation else None

def getRelations1M(diagram, relationship):
  """
  Función para obtener las relaciones 1 a muchos del diagrama entidad relación
  """
  attr_nm_relation = []
  diagramDict = diagram['diagram']
  for node in diagramDict['linkDataArray']:
    if ('toText' in node and 'fromText' in node) and (node['toText'] and node['fromText']):
      if node['toText'] in ['1','N'] and node['fromText'] in ['N','1']:
        if node['to'] == relationship[1] :
          attr_nm_relation.append((node['from'], node['fromText']))
        if node['from'] == relationship[1] :
          attr_nm_relation.append((node['to'], node['toText']))
  return {relationship :  attr_nm_relation} if attr_nm_relation else None

def setForeingKey(relations_1N_cardinality):

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

def validateKeyAttibute(entity_with_attrs):
  attrs = next(iter(entity_with_attrs.values())) # get attributes in entinty_with_attr dictionary
  primary_key = [attr for attr in attrs if attr[2] == 'keyAttribute']
  # if primary_key:
  #   print(f"this attribute cointain primary key {bcolors.OKGREEN}CONTINUE{bcolors.ENDC}")
  # else:
  #   print(f"this NO attribute cointain primary key {bcolors.FAIL} ERROR {bcolors.ENDC}")

  return primary_key

def getAttrsNMRelation(entitiesWithAttrs, relation_nm):
  attr_nm_relation = []
  primary_keys = []
  foreing_keys = []
  for entity_attrs in entitiesWithAttrs:
    if next(iter(entity_attrs))[1] in next(iter(relation_nm.values())):
      primary_key = next(iter(entity_attrs.values()))['primary_key'][0]
      ref_table = next(iter(entity_attrs))
      primary_keys.append(f"{primary_key[0]}_{ref_table[0].lower()}")
      foreing_keys.append(ref_table[0])
  attr_nm_relation = [getEntityWithAtributes(diagram, next(iter(relation_nm)), attrs)]
  return {next(iter(relation_nm)) : {"primary_keys" : primary_keys, "foreing_keys" : foreing_keys, "attr_relationship": next(iter(attr_nm_relation[0].values()))['attributes']}}

projectName = "test_sql"

entities = getEntities(diagram)
attrs = getAttrs(diagram)
entitiesWithAttrs = [getEntityWithAtributes(diagram, entity, attrs) for entity in entities]
entitiesWithAttrs_validation = [validateKeyAttibute(atributes) for atributes in entitiesWithAttrs]
relations = getRelationships(diagram)
relations_NM_to_table = [getRelationsNM(diagram, relationship ) for relationship in relations]
relations_1M = [getRelations1M(diagram, relationship ) for relationship in relations]
relations_1M = [ i for i in relations_1M if i]
setForeingKey(relations_1M.pop())
relations_NM_to_table = [ i for i in relations_NM_to_table if i] #remove empty items
relations_NM_to_table_with_attr = [getAttrsNMRelation(entitiesWithAttrs, relation_nm) for  relation_nm in relations_NM_to_table]

script_sql_sentences = getSentencesSQL(projectName, entitiesWithAttrs, relations_NM_to_table_with_attr)

print("*"*20)
print(script_sql_sentences)

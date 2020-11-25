
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

    for table in relations_NM_to_table_with_attr:
      # get name table in dict with next(iter(table))
      script_sentences += self.build_table_nm_sentence(table)

    return script_sentences

  def build_table_sentence(self, table_dict):

    table_template = """
  ---------------- CREATE TABLE ----------------
  DROP TABLE IF EXISTS `{table_name}`;
  CREATE TABLE IF NOT EXISTS `{table_name}` (
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
  DROP TABLE IF EXISTS `{table_name}`;
  CREATE TABLE IF NOT EXISTS `{table_name}` (
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
      primary_key = "PRIMARY KEY ({})".format(",".join([f"`{attr}`" for attr in attr_primarykey_list]))
      if foreingKeys_list:
        primary_key += ","
        foreing_keys = self.buildForeingKeys(attr_primarykey_list)

    return table_template.format(table_name=table_name, attrs_sentences=attr_by_table, primary_key=primary_key, foreing_keys=foreing_keys)

  def buildPrimaryKey(self, attr_list):
    primary_key_sentence = "PRIMARY KEY ({})"
    primary_key = [f"`{attr[0]}`" for attr in attr_list if attr[2] == 'keyAttribute']
    return primary_key_sentence.format(",".join(primary_key))

  def buildForeingKeys(self, attr_list):
    foreing_key_sentence = "FOREIGN KEY ({attr_name}) REFERENCES {ref_table_name} ({attr_ref_table})"
    fk_list = []
    for attr in attr_list:
      attr_ref_table, ref_table = attr.rsplit("_",1)
      fk_list.append(f"FOREIGN KEY ({attr}) REFERENCES {ref_table} ({attr_ref_table})")
    return ",\n".join(fk_list)

  def build_columns_sentences(self, attr_list):

    column_template= "{name} {dt}{dt_s} {not_null} {auto_increment}"
    columns_script = []
    for column in attr_list:
      attrName = column[0].replace(" ", "_")
      dataType = column[3]
      dataSize = column[4]
      notNull = column[5]
      autoIncrement = column[6]
      columns_script.append(column_template.format(name=f"`{attrName}`", dt=dataType, dt_s=f"({dataSize})", not_null=notNull, auto_increment=autoIncrement).rstrip())

    return ",\n".join(columns_script)

  def build_columns_nm(self, attr_list):

    column_template= "{name} {dt}{dt_s} {not_null} {auto_increment}"
    columns_script = []
    for column in attr_list:
      attr_name = column[0].replace(" ", "_")
      dataType = column[3]
      dataSize = column[4]
      notNull = column[5]
      autoIncrement = column[6]
      columns_script.append(column_template.format(name=f"`{attrName}`", dt=dataType, dt_s=f"({dataSize})", not_null=notNull, auto_increment=autoIncrement).rstrip())

    return ",\n".join(columns_script)

  def getEntities(self, diagram):
    entities = []
    for node in diagram['nodeDataArray']:
      if node['type'] == 'entity':
        entities.append(
          (node['text'].replace(" ", "_"), node['key'])
          )
    return entities

  def getAttrs(self, diagram):
    attrs = []
    for node in diagram['nodeDataArray']:
      if node['type'] in ['atribute', 'atributeDerived', 'keyAttribute', 'atributeComposite']:
        attrs.append(
          (
            node['text'].replace(" ", "_"),
            node['key'],
            node['type'],
            node['dataType'],
            node['dataSize'] if 'dataSize' in node else 0,
            'NOT NULL' if 'notNull' in node else '',
            'AUTO_INCREMENT' if 'autoIncrement' in node else '',
          )
        ) 
    return attrs

  def getRelationships(self, diagram):
    relationships = []
    for node in diagram['nodeDataArray']:
      if node['type'] in ['relation']:
        relationships.append(
          (node['text'].replace(" ", "_"), node['key'])
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
      if ('cardinality' in node ) and (node['cardinality']):
        if node['cardinality'] in ['N','M']:
          if node['to'] == relationship[1]:
            attr_nm_relation.append(node['from'])
          if node['from'] == relationship[1]:
            attr_nm_relation.append(node['to'])
    return {relationship :  attr_nm_relation} if len(attr_nm_relation) == 2 else None

  def getRelations1M(self, diagram, relationship):
    """
    Función para obtener las relaciones 1 a muchos del diagrama entidad relación
    """
    attr_nm_relation = []
    diagramDict = diagram
    for node in diagramDict['linkDataArray']:
      if ('cardinality' in node ) and (node['cardinality']):
        if node['cardinality'] in ['1','N']:
          if node['to'] == relationship[1] :
            attr_nm_relation.append((node['from'], node['cardinality']))
          if node['from'] == relationship[1] :
            attr_nm_relation.append((node['to'], node['cardinality']))
    return {relationship :  attr_nm_relation} if len(attr_nm_relation) == 2 and attr_nm_relation[0][1] != attr_nm_relation[1][1] else None

  def getRelations11(self, diagram, relationship):
    """
    Función para obtener las relaciones 1 a 1 del diagrama entidad relación
    """
    attr_nm_relation = []
    diagramDict = diagram
    for node in diagramDict['linkDataArray']:
      if ('cardinality' in node ) and (node['cardinality']):
        if node['cardinality'] == '1':
          if node['to'] == relationship[1] :
            attr_nm_relation.append((node['from'], node['cardinality']))
          if node['from'] == relationship[1] :
            attr_nm_relation.append((node['to'], node['cardinality']))
    return {relationship :  attr_nm_relation} if len(attr_nm_relation) == 2 else None

  def setForeingKey(self, relations_1N_cardinality, entitiesWithAttrs):

    table_ref = ""
    attr_fk = ""
    table_fk = ""
    pk_ref = ()
    for key in next(iter(relations_1N_cardinality.values())):
      attributes_entity =  [entity for entity in entitiesWithAttrs if next(iter(entity))[1] == key[0]]
      if key[1] == '1':
        pk_ref = next(iter(attributes_entity[0].values()))['primary_key'][0]
        ref_table = next(iter(attributes_entity[0]))
        table_ref = ref_table[0]
        attr_fk = f"{pk_ref[0]}_{ref_table[0].lower()}"
        attr_tuple = list(pk_ref)
        attr_tuple[0] = attr_fk
        pk_ref = tuple(attr_tuple)
      if key[1] == 'N':
        table_fk = [ entity for entity in entitiesWithAttrs if next(iter(entity))[1] == key[0]]
        ref_table = next(iter(table_fk[0]))
        table_fk = attributes_entity
    # obtenemos el indice del diccionario de la entidad a modificar
    index_entity = next(i for i,item in enumerate(entitiesWithAttrs) if item == table_fk[0])
    # agregamos el atributo a la lista de atributos de la entidad
    # next(iter(entitiesWithAttrs[index_entity].values()))['attributes'].append((attr_fk, 0, 'fk_attribute', pk_ref[3], pk_ref[4], pk_ref[5], pk_ref[6]))
    next(iter(entitiesWithAttrs[index_entity].values()))['attributes'].append(pk_ref)
    # agregamos el atributo a las llaves foraneas de la entidad
    next(iter(entitiesWithAttrs[index_entity].values()))['foreing_keys'].append(attr_fk)
    
    return None

  def setForeingKey11(self, relations_1_1_cardinality, entitiesWithAttrs):

    l_table, r_table = next(iter(relations_1_1_cardinality.values()))
    # obtenemos las entidades de la relacion con sus atributos
    attributes_l_entity =  [entity for entity in entitiesWithAttrs if next(iter(entity))[1] == l_table[0]]
    attributes_r_entity =  [entity for entity in entitiesWithAttrs if next(iter(entity))[1] == r_table[0]]
    ## obtener la llave primararia de la tabla 'izquierda'
    pk_l_entity = next(iter(attributes_l_entity[0].values()))['primary_key'][0]
    #formamos la llave forarea con la pk de la tabal izquierda concatenando el nombre de la entidad
    ref_table = next(iter(attributes_l_entity[0]))
    attr_fk = f"{pk_l_entity[0]}_{ref_table[0].lower()}"
    pk_l = list(pk_l_entity)
    pk_l[0] = attr_fk
    pk_l_entity = tuple(pk_l)

    # recuperamos el indice de la tabla 'R' a modificar 
    index_entity = next(i for i,item in enumerate(entitiesWithAttrs) if item == attributes_r_entity[0])

    #Agregamos el atributo a la tabla R
    next(iter(entitiesWithAttrs[index_entity].values()))['attributes'].append((attr_fk, 0, 'fk_attribute', pk_l[3], pk_l[4], pk_l[5], pk_l[6]))
    next(iter(entitiesWithAttrs[index_entity].values()))['attributes'].append(pk_l)
    # agregamos el atributo a las llaves foraneas de la entidad de la tabla R
    next(iter(entitiesWithAttrs[index_entity].values()))['foreing_keys'].append(attr_fk)

  def validateKeyAttibute(self, entity_with_attrs):
    attrs = next(iter(entity_with_attrs.values())) # get attributes in entinty_with_attr dictionary
    primary_key = [attr for attr in attrs if attr[2] == 'keyAttribute']
    
    return primary_key

  def greeting(self):
    return f"Saludos desde la clase relacional.py {self.greet}"

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

  def convertToSQLSenteneces(self, diagram):
    
    entities = self.getEntities(diagram)
    attrs = self.getAttrs(diagram)
    entitiesWithAttrs = [self.getEntityWithAtributes(diagram, entity, attrs) for entity in entities]
    entitiesWithAttrs_validation = [self.validateKeyAttibute(atributes) for atributes in entitiesWithAttrs]
    relations = self.getRelationships(diagram)
    relations_NM_to_table = [self.getRelationsNM(diagram, relationship ) for relationship in relations]
    relations_1M = [self.getRelations1M(diagram, relationship ) for relationship in relations]
    relations_1M = [ i for i in relations_1M if i]
    relations_1_1 = [self.getRelations11(diagram, relationship ) for relationship in relations]
    relations_1_1 = [i for i in relations_1_1 if i]
    relations_NM_to_table = [ i for i in relations_NM_to_table if i] #remove empty items
    relations_NM_to_table_with_attr = [self.getAttrsNMRelation(diagram, entitiesWithAttrs, relation_nm, attrs) for  relation_nm in relations_NM_to_table]

    if relations_1M :
      for r in relations_1M:
        self.setForeingKey(r, entitiesWithAttrs) 
    if relations_1_1 :
      for r in relations_1_1:
        self.setForeingKey11(r, entitiesWithAttrs)

    return self.getSentencesSQL("prueba_sql", entitiesWithAttrs, relations_NM_to_table_with_attr)

  def validateDiagramStructure(self, diagram):
    errors = {}
    general_errors = self.generalValidations(diagram)
    if general_errors : errors['generalErrors'] = general_errors 
    return errors

  def generalValidations(self, diagram):
    general_errors = {}
    unary_links = self.getUniryLink(diagram['linkDataArray'])
    unconnected_items = self.getUnconnectedItems(diagram)
    if unary_links: general_errors['unary_links'] = unary_links
    if unconnected_items: general_errors['unconnected_items'] = unconnected_items
    return general_errors
  
  def getUniryLink(self, link_data_array):
    unary_links_list = []
    for link in link_data_array:
      if not all (k in link for k in ['from', 'to']) :
        unary_links_list.append(link)
        
    return unary_links_list
  
  def getUnconnectedItems(self, diagram):
    unconnected_list = []
    keys_list = [ item['key'] for item in diagram['nodeDataArray']]
    u_links = self.getUniryLink(diagram['linkDataArray'])
    # remove unary links to find unconnected items
    links_without_unary_link = [ link for link in diagram['linkDataArray'] if not link in u_links ]

    for key in keys_list:
      item_with_conexions = [item for item in links_without_unary_link if item['from'] == key or item['to'] == key ]
      if not item_with_conexions: unconnected_list.append(key)

    return unconnected_list 
        

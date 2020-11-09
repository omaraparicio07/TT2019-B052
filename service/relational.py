
diagram = {
  "email": "omar@email.tv",
  "diagram": {
    "class": "GraphLinksModel",
    "modelData": {
      "position": "-659.5028514418491 -993.572273697964"
    },
    "nodeDataArray": [
      {
        "type": "entity",
        "text": "Student",
        "figure": "Rectangle",
        "fill": "white",
        "key": -1,
        "loc": "-460 -760"
      },
      {
        "type": "atribute",
        "text": "id",
        "figure": "Ellipse",
        "fill": "white",
        "key": -3,
        "loc": "-610 -780"
      },
      {
        "type": "entity",
        "text": "Subject",
        "figure": "Rectangle",
        "fill": "white",
        "key": -4,
        "loc": "0 -760"
      },
      {
        "type": "atribute",
        "text": "Full_name",
        "figure": "Ellipse",
        "fill": "white",
        "key": -5,
        "loc": "-480 -590"
      },
      {
        "type": "relation",
        "text": "Have",
        "figure": "Diamond",
        "fill": "white",
        "key": -8,
        "loc": "-220 -760"
      },
      {
        "type": "atribute",
        "text": "id",
        "figure": "Ellipse",
        "fill": "white",
        "key": -6,
        "loc": "150 -800"
      },
      {
        "type": "atribute",
        "text": "Name_class",
        "figure": "Ellipse",
        "fill": "white",
        "key": -7,
        "loc": "100 -650"
      }
    ],
    "linkDataArray": [
      {
        "from": -1,
        "to": -3
      },
      {
        "from": -1,
        "to": -5
      },
      {
        "from": -6,
        "to": -4
      },
      {
        "from": -4,
        "to": -7
      },
      {
        "from": -1,
        "to": -8
      },
      {
        "from": -8,
        "to": -4
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
        (node['text'], node['key'])
        )
  return attrs

def getRelationships(diagram):
  relationships = []
  for node in diagram['diagram']['nodeDataArray']:
    if node['type'] in ['relation']:
      print(bcolors.OKGREEN + 'relationship correct' + bcolors.ENDC) if validateOnlyBinarieRelationship(node['key'], diagram) else print(bcolors.FAIL + 'relationship error' + bcolors.ENDC)
      relationships.append(
        (node['text'], node['key'])
        )
  return relationships

entities = getEntities(diagram)
attrs = getAttrs(diagram)
relations = getRelationships(diagram)
# entitiesWithAttrs = [getEntityWithAtributes(diagram, entity, attrs) for entity in entities]

print("*"*20)
print(entities)
print(attrs)
print(relations)
print(entitiesWithAttrs)
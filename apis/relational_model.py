from flask import current_app, json
from flask_restplus import Namespace, Resource, fields
from service.relational import Relational
import logging
import json

logging.basicConfig(level=logging.DEBUG)

api = Namespace('relational', description='Obtención de sentencias SQL')

diagram = api.model('diagram', {
  'db_name': fields.String(example="db_name.sql", required= True),
  'diagram': fields.String(example="{}", required= True)
})


@api.route("")
class Relatioral(Resource):
  """
  Clase para realizar la transformación del modelo er a sentencias SQL compatibles con mysql
  """
  @api.expect(diagram)
  @api.response(200, "Tranformación correcta")
  @api.response(401, 'No autorizado')
  @api.response(403, "Diagrama no encontrado en la petición")
  @api.response(500, "Error en el servidor")
  def post(self):
    """
    Método para realizar la tranformación a sentencias SQL
    """
    logging.info("Empezando la tranformación del diagrama er a sentencias SQL")
    diagram= json.loads(api.payload['diagram'])
    db_name = api.payload['dbName'] or "tt2019-B052"
    r = Relational(diagram, "Ya lleguee!!!!")
    if diagram['nodeDataArray']:
      test = r.convertToSQLSenteneces(diagram, db_name)
    else:
      return api.abort(403, "El diagrama se encuentra vacío.")
    
    return test

@api.route("/validate")
class ValidateDiagram(Resource):
  """
  Clase para realizar la validación estructural del diagrama entidad relación
  """
  @api.expect(diagram)
  @api.response(200, "Diagrama valido estructuralmente")
  @api.response(401, "No autorizado")
  @api.response(403, "Diagrama no entrado en la petición")
  @api.response(406, "Diagrama no valido")
  @api.response(500, "Error en el servidor")
  def post(self):
    """
    Método para validar la estructura del diagrama ER con los siguientes criterios:
     General :
      - No pueden existir elmentos sin conexión ✅
      - No pueden existir enlacen sin conexión ✅

    Entidades :
      - Debe tener al menos un atributo ✅
      - Debe tener al menos un atributo clave ✅
      - La clave primaria puede ser simple o compuesta(tener mas de un atributo clave) ✅
      - La clave primaria no es una una clave foránea ☑️
      - La clave primaria debe ser un atributo asociado a la entidad ✅
      - Dos entidades solo pueden conectarse entre si mediante una relación ✅

    Atributos :
      - Solo se puede asociar a un unico atributo o a una entidad ✅
      - Puede ser del tipo compuesto, derivado, multivalor, clave ✅
      - No puede conectarse a una relación ☑️
      - Los atributos compuestos y derivados solo pueden estar asociados a una entidad ✅

    Relaciones :
      - Solo pueden existir entre entidades ☑️
      - El grado máximo de participación es dos 
      - Una relación puede ser unaria ✅
      - No se permiten relaciones ternarias o de grado n ✅
    """
    logging.info("inicando la validación del diagrama")
    diagram = json.loads(api.payload['diagram'])
    validate_diagram = Relational(diagram, "Hi!")
    errors = {}
    if diagram['nodeDataArray']:
      errors = validate_diagram.validateDiagramStructure(diagram)
    else:
      return api.abort(400, "El diagrama se encuentra vacío.")

    if errors:
      logging.warn("diagrama no valido ")
      return errors, 406
    else:
      logging.info("diagrama valido en estructura")
      return "Diagrama valido",200
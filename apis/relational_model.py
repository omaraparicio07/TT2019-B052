from flask import current_app
from flask_restplus import Namespace, Resource, fields
import logging
from service.relational import Relational

logging.basicConfig(level=logging.DEBUG)

api = Namespace('relational', description='Obtención de sentencias SQL')

diagram = api.model('diagram', {
  # 'diagram': fields.String(example="{}", required= True),
})


@api.route("")
class Relatioral(Resource):
  """
  Clase para realizar la transformación del modelo er a sentencias SQL compatibles con mysql
  """
  @api.expect(diagram, validate=True)
  @api.response(200, "Tranformación correcta")
  @api.response(401, 'No autorizado')
  @api.response(403, "Diagrama no encontrado en la llamada")
  @api.response(500, "Error en el servidor")
  def post(self):
    """
    Método para realizar la tranformación a sentencias SQL
    """
    logging.info("Empezando la tranformación del diagrama er a sentencias SQL")
    diagram= api.payload['diagram']
    email= api.payload['email'].split("@")[0]
    r = Relational(diagram, "Ya lleguee!!!!")
    test = r.convertToSQLSenteneces(diagram)
    script_sql_out = open(f"script_sql_{email}.sql", "w")
    script_sql_out.write(test)
    script_sql_out.close()
    
    return r.greeting()

@api.route("/validate")
class ValidateDiagram(Resource):
  """
  Clase para realizar la validación estructural del diagrama entidad relación
  """
  @api.expect(diagram, validate=True)
  @api.response(200, "Diagrama valido estructuralmente")
  @api.response(401, "No autorizado")
  @api.response(403, "Diagrama no entrado en la petición")
  @api.response(500, "Error en el servidor")
  def post(self):
    """
    Método para validar la estructura del diagrama ER con los siguientes criterios:
     General :
      - No pueden existir elmentos sin conexión
      - No pueden existir enlacen sin conexión

    Entidades :
      - Debe tener al menos un atributo
      - Debe tener al menos un atributo clave
      - La clave primaria puede ser simple o compuesta(tener mas de un atributo clave)
      - La clave primaria no es una una clave foránea
      - La clave primaria debe ser un atributo asociado a la entidad
      - Dos entidades solo pueden estar conecatadas mediante una relación

    Atributos :
      - Solo se puede asociar a un unico atributo o a una entidad
      - Puede ser del tipo compuesto, derivado, multivalor, clave
      - No puede conectarse a una relación
      - Los atributos compuestos y derivados solo pueden estar asociados a una entidad

    Relaciones :
      - Solo pueden existir entre entidades
      - El grado máximo de participación es dos
      - Una relación puede ser unaria
      - No se permiten relaciones ternarias o de grado n
    """
    return 201
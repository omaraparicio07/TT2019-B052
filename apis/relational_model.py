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
    r = Relational(diagram, "Ya lleguee!!!!")
    test = r.convertToSQLSenteneces(diagram)
    print(test)
    
    return r.greeting()


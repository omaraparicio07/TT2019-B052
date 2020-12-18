from flask import current_app, json
from flask_restplus import Namespace, Resource, fields
from service.relational import Relational
from service.noSQL.parser_gdm_to_model import ParserGDM as gdmParser
import logging as Log
import json

Log.basicConfig(level=Log.DEBUG)

api = Namespace('noRelational', description='Modelo no relacional (NoSQL)')

gdmSimpleText = api.model('gdm', {
  'entidades': fields.String(required= True, example="entity { gdmType entityAttributeName propAttribute}"),
  'consultas': fields.String(required= True, example="query queryName: select alias.propsEntity from entity as alias including alias.prop  where alias.prop = '?'")
})

@api.route("")
class NoRelationa(Resource):
  """
  Clase para realizar la tranformación del modelo ER al modelo no relacional NoSQL
  """
  @api.expect(gdmSimpleText)
  @api.response(200, "Transformación del gdm exitosa")
  @api.response(401, "No autorizado")
  @api.response(403, "Entidades y consultas no entrados en la petición")
  @api.response(406, "Parámetos no validos")
  @api.response(500, "Error en el servidor")
  def post(self):
    """
    Método para realizar la tranformación  del gdm de texto simple al ddm
    """
    Log.info("Iniciando trasformación al GDM de texto simple")
    entities_gdm_input = api.payload['entidades']
    queries_gdm_input = api.payload['consultas']

    if entities_gdm_input and queries_gdm_input:
      Log.info("Procedemos al Crear el archivo .gdm")
      with open("venues.gdm","w+") as gdmFile:
        gdmFile.write("*"*23+ "\n"+"* Entities definition *"+ "\n"+"*"*23 + "\n\n")
        gdmFile.write(entities_gdm_input)
        gdmFile.write("\n\n")
        gdmFile.write("*"*22+ "\n"+"* Queries definition *"+ "\n"+"*"*22 +"\n\n")
        gdmFile.write(queries_gdm_input)
      gdm_parse = gdmParser()
      gdm_parse.main("venues.gdm")
      return "Todo cool!!."
    else:
      return api.abort(400, "Las entidades o consultas se encuentran vacios.")

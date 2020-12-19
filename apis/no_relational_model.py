from flask import current_app, json
from flask_restplus import Namespace, Resource, fields
from service.relational import Relational
from service.noSQL.parser_gdm_to_model import ParserGDM as gdmParser
from service.noSQL.gdm_to_ddm import ParserDDM as ddmParser
from service.noSQL.document_model_to_gojs import ParserDiagramNoSQL as gojsParser
from service.noSQL.er_to_gdm_entities import GDMEntities as gdmEntities
import logging as Log
import json
import os

Log.basicConfig(level=Log.DEBUG)

api = Namespace('noRelational', description='Modelo no relacional (NoSQL)')

gdmSimpleText = api.model('gdm', {
  'entities': fields.String(required= True, example="entity { gdmType entityAttributeName propAttribute}"),
  'queries': fields.String(required= True, example="query queryName: select alias.propsEntity from entity as alias including alias.prop  where alias.prop = '?'")
})

diagram = api.model('diagram', {
  'diagram': fields.String(example="{}", required= True),
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
    Log.info("Iniciando trasformación del GDM de texto simple")
    entities_gdm_input = api.payload['entities']
    queries_gdm_input = api.payload['queries']

    if entities_gdm_input and queries_gdm_input:
      Log.info("Procedemos al crear el archivo .gdm")
      with open("venues.gdm","w+") as gdmFile:
        gdmFile.write("*"*23+ "\n"+"* Entities definition *"+ "\n"+"*"*23 + "\n\n")
        gdmFile.write(entities_gdm_input)
        gdmFile.write("\n\n")
        gdmFile.write("*"*22+ "\n"+"* Queries definition *"+ "\n"+"*"*22 +"\n\n")
        gdmFile.write(queries_gdm_input)
        gdmFile.write("\n  ")
        Log.info("archivo creado con exitp")
      try:
        gdm_parse = gdmParser()
        gdm_parse.main("venues.gdm")
        ddm_parser = ddmParser()
        ddm_parser.main("venues")
        gojs_parser = gojsParser()
        gojsDiagram = gojs_parser.main("prueba_ddm.xmi")
        if gojsDiagram:
          response = {
            'diagram':gojsDiagram
          }
          return response
        else:
          return api.abort(500, "Ocurrio un error con los datos del diagrama al modelo NoSQL.")
      except Exception as ex :
        Log.exception("Algo ocurrio!")
        return api.abort(500, "Ocurrio un error en la tranformación al modelo NoSQL.")
      finally:
        # eliminar archivos del servidor
        if os.path.exists("venues.gdm"):
          os.remove("venues.gdm")
        if os.path.exists("venues.xmi"):
          os.remove("venues.xmi")
        pass
    else:
      return api.abort(400, "Las entidades o consultas se encuentran vacios.")
  

  @api.expect(diagram)
  @api.response(200, "Entidades obtenidas con exito.")
  @api.response(400, "Diagrama no encontrado en la petición.")
  @api.response(500, "Error en el servidor.")
  def put(Resource):
    """
    Obtener las entidades del diagrama ER y parsearlas a las entidades de gdm
    """
    Log.info("Obteniendo las entidades del GDM de texto simple")
    if api.payload['diagram']:
      diagram = json.loads(api.payload['diagram'])
      gdm_entities = gdmEntities()
      gdm_entities.main(diagram)
      entities = ""
      try:
        with open("salida.gdm", "r") as f:
          entities = f.read()
        return entities
      except Exception :
        Log.exception("Algo ocurrio!")
        return api.abort(500, "Ocurrio un error al obtener las entidades del diagrama ER.")
      finally:
        if os.path.exists("salida.gdm"):
          os.remove("salida.gdm")
    else:
      return api.abort(400, "Diagrama no encontrado en la petición.")


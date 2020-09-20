from flask_restplus import Namespace, Resource, fields
from config.database import db
from bson import json_util, objectid

api = Namespace('user', description='Cats related operations')

user = api.model('User', {
  '_id': fields.String,
  'name': fields.String,
  'username': fields.String,
  'email': fields.String(required=True),
  'password': fields.String(required=True),
  'diagram': fields.String,
})


@api.route('/')
class CatList(Resource):
  @api.doc('list_cats')
  @api.marshal_list_with(user)
  def get(self):
    '''List all cats'''
    users = db.db.users.find()
    response = list(users)
    return response


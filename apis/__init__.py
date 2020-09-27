from flask_restplus import Api

from .user import api as ns_user
from .login import api as ns_login


api = Api(
    title='API TT 2019-B052',
    version='1.0',
    description='A description',
    # All API metadatas
)

api.add_namespace(ns_user)
api.add_namespace(ns_login)
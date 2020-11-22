from flask_restplus import Api

from .user import api as ns_user
from .login import api as ns_login
from .diagram import api as ns_diagram
from .relational_model import api as ns_relational

# Bases Authorization
authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


api = Api(
    title='API TT 2019-B052',
    version='0.10.0',
    description='api de servicios para el trabajo termnal 2019-B052',
    contact="Omar Aparicio Quiroz, Eduardo Acosta Martinez",
    contact_email="omaraparicio07@gmail.com, fx2013630461@gmail.com",
    security='Bearer Auth',
    authorizations=authorizations,
    RESTPLUS_MASK_SWAGGER=False
    # All API metadatas
)


api.add_namespace(ns_user)
api.add_namespace(ns_login)
api.add_namespace(ns_diagram)
api.add_namespace(ns_relational)
import falcon
from falcon_swagger_ui import register_swaggerui_app

from api.resources.predict_resource import PredictResource
from api.resources.reset_resource import ResetResource
from api.resources.retrain_resource import RetrainResource
from api.resources.healthcheck_resource import HealthCheckResource

from falcon.http_status import HTTPStatus

from middleware.cors_middleware import CORSComponent


api = falcon.API(middleware=[CORSComponent()])
api.add_route("/", HealthCheckResource())
api.add_route('/predict', PredictResource())
api.add_route('/reset', ResetResource())
api.add_route('/reset/data', ResetResource(), suffix='data')
api.add_route('/reset/model', ResetResource(), suffix='model')
api.add_route('/retrain', RetrainResource())
api.add_route('/retrain/data', RetrainResource(), suffix='add_data')

SWAGGERUI_URL = '/swagger'  # without trailing slash
SCHEMA_URL = 'http://petstore.swagger.io/v2/swagger.json'

page_title = 'Falcon Swagger Doc'
favicon_url = 'https://falconframework.org/favicon-32x32.png'

register_swaggerui_app(
    api, SWAGGERUI_URL, SCHEMA_URL,
    page_title=page_title,
    favicon_url=favicon_url,
    config={'supportedSubmitMethods': ['post'], }
)

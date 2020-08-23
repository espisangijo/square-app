import falcon


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

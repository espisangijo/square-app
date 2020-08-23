import falcon

class HealthCheckResource(object):
    def on_get(self, req, resp):
        """
        Check healthstatus of service.
        """
        resp.status = falcon.HTTP_200

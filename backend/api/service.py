import socket

from flask_restful import Resource

from backend.core.schema import HostSchema
from backend.helpers import success_response


class ServiceStatus(Resource):
    def get(self):
        """
        ---
        summary: Service status
        description: Method to test that service is working, always returns success
        responses:
            200:
                description: OK
        """

        return success_response()


class CurrentServer(Resource):
    def get(self):
        """
        ---
        summary: Host info
        description: Returns information about the host that handles current request
        responses:
            200:
                description: OK
                content:
                    application/json:
                        schema: HostSchema
        """

        hostname = socket.gethostname()
        lhostname = socket.getfqdn()

        return HostSchema().dump({
            'host': hostname,
            'host_full': lhostname,
        })

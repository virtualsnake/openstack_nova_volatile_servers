import functools

from flask_restful import Resource, reqparse, marshal_with, fields
from flask_restful import abort
from openstack.exceptions import HttpException, SDKException
from werkzeug.exceptions import HTTPException

from volatile_api.openstack_api import client as os_client, ServerTypes, extractServerType

server_types = [e.value for e in ServerTypes]

response_server_fields = {
    'name': fields.String,
    'id': fields.String,
    'type': fields.String(attribute=extractServerType)
}


def handleExceptions(func):
    # convert OpenStack HttpExceptions to Flask Response (4xx or 5xx)
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPException:
            raise
        except HttpException as e:
            abort(e.status_code, message=e.details)
        except SDKException as e:
            abort(400, message=e.message)
        except Exception as e:
            abort(400, message=str(e))

    return wrapped


class Server(Resource):
    @handleExceptions
    @marshal_with(response_server_fields, envelope="servers")
    def get(self, server_id):
        return os_client.getServer(server_id)

    @handleExceptions
    def delete(self, server_id):
        # HTTP 204 (No content)
        # indicate a successful deletion with no additional information (response body is empty).
        return os_client.deleteServer(server_id), 204


class ServerList(Resource):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._post_parser = reqparse.RequestParser()
        self._post_parser.add_argument('server_name', required=True, type=str)
        self._post_parser.add_argument('server_type',
                                       required=True,
                                       choices=server_types,
                                       help='{error_msg}. Supported values ' + str(server_types))

    @handleExceptions
    @marshal_with(response_server_fields, envelope="servers")
    def get(self):
        return os_client.getServers()

    @handleExceptions
    @marshal_with(response_server_fields, envelope="servers")
    def post(self):
        args = self._post_parser.parse_args()
        server = os_client.createServer(name=args['server_name'], server_type=args['server_type'])
        return server, 201

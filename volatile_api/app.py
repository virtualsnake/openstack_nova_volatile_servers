from flask import Flask
from flask_restful import Api

from volatile_api.resources.server import Server, ServerList

app = Flask(__name__)
api = Api(app)

api.add_resource(ServerList, '/servers')
api.add_resource(Server, '/servers/<string:server_id>')

if __name__ == '__main__':
    app.run(debug=True)

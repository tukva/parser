from sanic import Sanic

from config import PARSER_API_PORT, PARSER_API_HOST
from routes import add_routes

app = Sanic(name=__name__)
add_routes(app)

if __name__ == '__main__':
    app.run(host=PARSER_API_HOST, port=PARSER_API_PORT)

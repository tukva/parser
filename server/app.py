from sanic import Sanic

from config import PARSER_API_PORT
from routes import add_routes

app = Sanic(name=__name__)
add_routes(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PARSER_API_PORT)

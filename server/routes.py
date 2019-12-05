from services.views.parse import parse_team


def add_routes(app):
    app.add_route(parse_team, '/parse', methods=["POST"])

from listeners import acquire_con, close_con
from services.views.parse_link import ParserLinkView, ParserAllLinksView, RealTeamView


def add_routes(app):
    app.register_listener(acquire_con, "before_server_start")
    app.register_listener(close_con, "after_server_stop")

    app.add_route(ParserAllLinksView.as_view(), '/parse-links/teams')
    app.add_route(ParserLinkView.as_view(), '/parse-links/<link_id:int>/teams')

    app.add_route(RealTeamView.as_view(), '/real-team')

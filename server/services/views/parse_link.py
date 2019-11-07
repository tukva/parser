from sanic.views import HTTPMethodView
from engine import Connection
from models import tb_team, tb_real_team

from services.utils import get_all_teams, get_teams_by_link, refresh_teams_by_link, \
    refresh_real_teams, delete_teams_by_link


class ParserLinkView(HTTPMethodView):

    async def get(self, request, link_id):
        async with Connection() as conn:
            return await get_teams_by_link(conn, link_id)

    async def put(self, request, link_id):
        async with Connection() as conn:
            return await refresh_teams_by_link(conn, link_id)

    async def delete(self, request, link_id):
        async with Connection() as conn:
            return await delete_teams_by_link(conn, link_id)


class ParserAllLinksView(HTTPMethodView):

    async def get(self, request):
        async with Connection() as conn:
            return await get_all_teams(conn, tb_team)


class RealTeamView(HTTPMethodView):

    async def get(self, request):
        async with Connection() as conn:
            return await get_all_teams(conn, tb_real_team)

    async def put(self, request):
        async with Connection() as conn:
            return await refresh_real_teams(conn)

from sanic.views import HTTPMethodView
from engine import Connection
from models import _Parser as Parser

from services.decorators import mapp_func_by_link, mapp_func_by_all_links
from services.utils import ParserRealTeams, ParserAllTeams


class ParserLinkView(HTTPMethodView):

    @mapp_func_by_link()
    async def get(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.get(conn, link_id)

    @mapp_func_by_link()
    async def put(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.put(conn, link_id)

    @mapp_func_by_link()
    async def delete(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.delete(conn, link_id)


class ParserAllLinksView(HTTPMethodView):

    @mapp_func_by_all_links()
    async def get(self, request, cls):
        async with Connection() as conn:
            return await cls.get(conn, Parser.team)


class RealTeamView(HTTPMethodView):

    async def get(self, request):
        async with Connection() as conn:
            return await ParserAllTeams.get(conn, Parser.real_team)

    async def put(self, request):
        async with Connection() as conn:
            return await ParserRealTeams.put(conn)

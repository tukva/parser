from sanic.views import HTTPMethodView
from engine import Connection

from services.decorators import mapp_func
from services.utils import ParserRealTeams, ParserAllTeams


class ParserLinkView(HTTPMethodView):
    decorators = [mapp_func()]

    async def get(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.get(conn, link_id)

    async def put(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.put(conn, link_id)

    async def delete(self, request, link_id, cls):
        async with Connection() as conn:
            return await cls.delete(conn, link_id)


class ParserAllLinksView(HTTPMethodView):
    decorators = [mapp_func()]

    async def get(self, request, cls):
        async with Connection() as conn:
            return await cls.get(conn)


class RealTeamView(HTTPMethodView):

    async def get(self, request):
        async with Connection() as conn:
            return await ParserRealTeams.get(conn)

    async def put(self, request):
        async with Connection() as conn:
            return await ParserRealTeams.put(conn)

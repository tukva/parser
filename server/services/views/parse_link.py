from datetime import datetime

from sanic.views import HTTPMethodView
from sanic.response import text, json
from sqlalchemy import and_

from engine import Connection
from models import tb_link, tb_team
from services.parsers import team_parser
from services.forms import TeamResponseSchema


class ParserLinkView(HTTPMethodView):

    async def get(self, request, link_id, name):
        if name == 'teams':
            async with Connection() as conn:
                teams = await conn.execute(tb_team.select().where(tb_team.c.link_id == link_id))
                res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
                return json(res, 200)

    async def put(self, request, link_id, name):
        if name == 'teams':
            async with Connection() as conn:
                select_tb_link = await conn.execute(tb_link.select().where(tb_link.c.link_id == link_id))
                link = await select_tb_link.fetchone()

                teams = team_parser(link.link, link.attributes["cls"], link.attributes["elem"])
                for team in teams:
                    select_tb_team = await conn.execute(tb_team.select().where(and_(
                        tb_team.c.name == team,
                        tb_team.c.link_id == link_id
                    )))
                    exist_record = await select_tb_team.fetchone()

                    if exist_record:
                        await conn.execute(tb_team.update().where(and_(
                            tb_team.c.name == team, tb_team.c.link_id == link_id)).values(
                            name=team, site_name=link.site_name, created_on=datetime.utcnow(), link_id=link_id)
                        )
                        break
                    else:
                        await conn.execute(tb_team.insert().values(
                            name=team, site_name=link.site_name, created_on=datetime.utcnow(), link_id=link_id)
                        )
                return text("Ok", 200)

    async def delete(self, request, link_id, name):
        if name == 'teams':
            async with Connection() as conn:
                await conn.execute(tb_team.delete().where(tb_team.c.link_id == link_id))
                return text("Ok", 200)


class ParserAllLinksView(HTTPMethodView):

    async def get(self, request, name):
        if name == 'teams':
            async with Connection() as conn:
                teams = await conn.execute(tb_team.select())
                res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
                return json(res, 200)
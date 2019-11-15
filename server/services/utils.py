from datetime import datetime

from sanic.response import text, json

from models import _Parser as Parser
from services.forms import TeamResponseSchema
from services.parsers import team_parser
from sqlalchemy import and_


async def get_all_teams(conn, table_name):
    teams = await conn.execute(table_name.select())
    res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
    return json(res, 200)


async def get_teams_by_link(conn, link_id):
    teams = await conn.execute(Parser.team.select().where(Parser.team.c.link_id == link_id))
    result = await teams.fetchall()
    if not result:
        return text("Not Found", 404)
    res = TeamResponseSchema().dump(result, many=True)
    return json(res, 200)


async def refresh_teams_by_link(conn, link_id):
    select_tb_link = await conn.execute(Parser.link.select().where(Parser.link.c.link_id == link_id))
    link = await select_tb_link.fetchone()
    if not link or link.site_name == "UEFA":
        return text("Not Found", 404)
    teams = team_parser(link.link, link.attributes["cls"], link.attributes["elem"])
    for team in teams:
        select_tb_team = await conn.execute(Parser.team.select().where(and_(
            Parser.team.c.name == team,
            Parser.team.c.link_id == link_id
        )))
        exist_record = await select_tb_team.fetchone()

        if exist_record:
            await conn.execute(Parser.team.update().where(and_(
                Parser.team.c.name == team, Parser.team.c.link_id == link_id)).values(
                name=team, site_name=link.site_name, created_on=datetime.utcnow(), link_id=link_id)
            )
            break
        else:
            await conn.execute(Parser.team.insert().values(
                name=team, site_name=link.site_name, created_on=datetime.utcnow(), link_id=link_id)
            )
    return text("Ok", 200)


async def delete_teams_by_link(conn, link_id):
    select_tb_link = await conn.execute(Parser.link.select().where(Parser.link.c.link_id == link_id))
    link = await select_tb_link.fetchone()
    if not link:
        return text("Not Found", 404)
    await conn.execute(Parser.team.delete().where(Parser.team.c.link_id == link_id))
    return text("Ok", 200)


async def refresh_real_teams(conn):
    select_tb_link = await conn.execute(Parser.link.select().where(Parser.link.c.site_name == 'UEFA'))
    link = await select_tb_link.fetchone()

    teams = team_parser(link.link, link.attributes["cls"], link.attributes["elem"])

    for team in teams:
        select_tb_team = await conn.execute(Parser.real_team.select().where(
            Parser.real_team.c.name == team
        ))
        exist_record = await select_tb_team.fetchone()

        if exist_record:
            await conn.execute(Parser.real_team.update().where(Parser.real_team.c.name == team).values(
                name=team, created_on=datetime.utcnow())
            )
        else:
            await conn.execute(Parser.real_team.insert().values(
                name=team, created_on=datetime.utcnow())
            )
    return text("Ok", 200)

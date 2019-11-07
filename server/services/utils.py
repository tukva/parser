from datetime import datetime

from marshmallow.exceptions import ValidationError
from sanic.response import text, json

from models import tb_link, tb_team, tb_real_team
from services.forms import TeamResponseSchema
from services.parsers import team_parser
from sqlalchemy import and_


async def get_all_teams(conn, table_name):
    try:
        teams = await conn.execute(table_name.select())
        res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
        return json(res, 200)
    except ValidationError as e:
        return json(e, 400)


async def get_teams_by_link(conn, link_id):
    try:
        teams = await conn.execute(tb_team.select().where(tb_team.c.link_id == link_id))
        res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
        return json(res, 200)
    except ValidationError as e:
        return json(e, 400)


async def refresh_teams_by_link(conn, link_id):
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


async def refresh_real_teams(conn):
    select_tb_link = await conn.execute(tb_link.select().where(tb_link.c.site_name == 'UEFA'))
    link = await select_tb_link.fetchone()

    teams = team_parser(link.link, link.attributes["cls"], link.attributes["elem"])

    for team in teams:
        select_tb_team = await conn.execute(tb_real_team.select().where(
            tb_real_team.c.name == team
        ))
        exist_record = await select_tb_team.fetchone()

        if exist_record:
            await conn.execute(tb_real_team.update().where(tb_real_team.c.name == team).values(
                name=team, created_on=datetime.utcnow())
            )
        else:
            await conn.execute(tb_real_team.insert().values(
                name=team, created_on=datetime.utcnow())
            )
    return text("Ok", 200)


async def delete_teams_by_link(conn, link_id):
    await conn.execute(tb_team.delete().where(tb_team.c.link_id == link_id))
    return text("Ok", 200)

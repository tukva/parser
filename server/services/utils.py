from datetime import datetime

from sanic.log import logger
from sanic.response import json
from psycopg2 import DatabaseError

from models import _Parser as Parser
from services.forms import TeamResponseSchema
from services.parsers import team_parser
from sqlalchemy import and_

from abc import ABC, abstractmethod


class ParserByLink(ABC):

    @staticmethod
    @abstractmethod
    async def get(conn, link_id):
        pass

    @staticmethod
    @abstractmethod
    async def put(conn, link_id):
        pass

    @staticmethod
    @abstractmethod
    async def delete(conn, link_id):
        pass


class ParserByAllLinks(ABC):

    @staticmethod
    @abstractmethod
    async def get(conn):
        pass

    @staticmethod
    async def put(conn):
        pass

    @staticmethod
    async def delete(conn):
        pass


class ParserTeamsByLink(ParserByLink):

    @staticmethod
    async def get(conn, link_id):
        teams = await conn.execute(Parser.team.select().where(Parser.team.c.link_id == link_id))
        result = await teams.fetchall()
        if not result:
            return json("Not Found", 404)
        res = TeamResponseSchema().dump(result, many=True)
        return json(res, 200)

    @staticmethod
    async def put(conn, link_id):
        select_tb_link = await conn.execute(Parser.link.select().where(Parser.link.c.link_id == link_id))
        link = await select_tb_link.fetchone()
        if not link or link.site_name == "UEFA":
            return json("Not Found", 404)
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
        return json("Ok", 200)

    @staticmethod
    async def delete(conn, link_id):
        select_tb_link = await conn.execute(Parser.link.select().where(Parser.link.c.link_id == link_id))
        link = await select_tb_link.fetchone()
        if not link:
            return json("Not Found", 404)
        await conn.execute(Parser.team.delete().where(Parser.team.c.link_id == link_id))
        return json("Ok", 200)


class ParserAllTeams(ParserByAllLinks):

    @staticmethod
    async def get(conn):
        teams = await conn.execute(Parser.team.select())
        res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
        return json(res, 200)

    @staticmethod
    async def put(conn):
        select_tb_link = await conn.execute(Parser.link.select())
        all_links = await select_tb_link.fetchall()
        for link in all_links:
            if not link or link.site_name == "UEFA":
                continue
            teams = team_parser(link.link, link.attributes["cls"], link.attributes["elem"])
            for team in teams:
                select_tb_team = await conn.execute(Parser.team.select().where(and_(
                    Parser.team.c.name == team,
                    Parser.team.c.link_id == link.link_id
                )))

                if select_tb_team.rowcount:
                    await conn.execute(Parser.team.update().where(and_(
                        Parser.team.c.name == team, Parser.team.c.link_id == link.link_id)).values(
                        name=team, site_name=link.site_name, created_on=datetime.utcnow(), link_id=link.link_id)
                    )
                    break
                else:
                    await conn.execute(Parser.team.insert().values(
                        name=team, site_name=link.site_name, created_on=datetime.utcnow(), link_id=link.link_id)
                    )
        return json("Ok", 200)


class ParserRealTeams(ParserByAllLinks):

    @staticmethod
    async def get(conn):
        teams = await conn.execute(Parser.real_team.select())
        res = TeamResponseSchema().dump(await teams.fetchall(), many=True)
        return json(res, 200)

    @staticmethod
    async def put(conn):
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
        return json("Ok", 200)


async def set_real_team(conn, team_id, real_team_id):
    try:
        result = await conn.execute(Parser.team.update().values(real_team_id=real_team_id).where(
            Parser.team.c.team_id == team_id))
    except DatabaseError as e:
        logger.error(f"DB Update error: {e}")
        return json("Not found", 404)

    if not result.rowcount:
        return json("Bad request", 400)

    return json("Ok", 204)

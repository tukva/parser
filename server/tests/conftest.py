from datetime import datetime

import pytest
from sanic import Sanic
from sqlalchemy.schema import CreateTable, DropTable

from routes import add_routes
from engine import Connection, Engine
from models import tb_team, tb_real_team, tb_link


def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: smoke tests")
    config.addinivalue_line("markers", "parser: parser tests")
    config.addinivalue_line("markers", "real_teams: real_teams tests")
    config.addinivalue_line("markers", "parse_links: parse_links tests")


async def drop_tables():
    async with Connection() as conn:
        await conn.execute(DropTable(tb_team))
        await conn.execute(DropTable(tb_real_team))
        await conn.execute(DropTable(tb_link))


async def create_tables():
    async with Connection() as conn:
        await conn.execute(CreateTable(tb_link))
        await conn.execute(CreateTable(tb_real_team))
        await conn.execute(CreateTable(tb_team))

        await conn.execute(tb_link.insert().values(site_name="bwin",
                                                   link="https://sports.bwin.com/en/sports",
                                                   created_on=datetime.utcnow(),
                                                   attributes={"elem": "a", "cls": "js-mg-tooltip"}))

        await conn.execute(tb_link.insert().values(site_name="UEFA",
                                                   link="https://en.competitions.uefa.com/"
                                                        "memberassociations/uefarankings/club/libraries//years/2020/",
                                                   created_on=datetime.utcnow(),
                                                   attributes={"elem": "a", "cls": "team-name visible-md visible-lg"}))


@pytest.fixture
def test_cli(loop, sanic_client):
    app = Sanic()
    add_routes(app)
    return loop.run_until_complete(sanic_client(app))


@pytest.fixture
async def tables(test_cli):
    await create_tables()

    yield

    await drop_tables()


@pytest.fixture
async def add_team(tables):
    async with Connection() as conn:
        await conn.execute(tb_team.insert().values(name="Chelsea", created_on='2019-11-07T14:13:44.041152',
                                                   site_name="bwin", link_id=1))


@pytest.fixture
async def add_real_team(tables):
    async with Connection() as conn:
        await conn.execute(tb_real_team.insert().values(name="Chelsea", created_on='2019-11-07T14:13:44.041152'))


@pytest.fixture
async def connection():
    await Engine.init()

    yield

    await Engine.close()

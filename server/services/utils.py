import asyncio

from common.rest_client.base_client_betting_data import BaseClientBettingData

from services import parsers
from constants import PeriodForCreation


async def parse_teams_by_link(link):
    site_name = link["site_name"]
    parser = parsers.PARSER_TYPES.get(site_name)

    if not parser:
        return [], link

    attr = { 'class': link["attributes"]["class"]}
    url = link["link"]
    tag = link["attributes"]["elem"]

    teams = await parser(url=url, tag=tag, attr=attr)

    return teams, link


async def create_real_teams():
    client = BaseClientBettingData()
    link = await client.get_links(where="type:eq:real_team")
    real_teams, _ = await parse_teams_by_link(link)
    for real_team in real_teams:
        await client.create_real_teams(json={"name": real_team})
    await asyncio.sleep(PeriodForCreation.REAL_TEAMS)
    await create_real_teams()


async def create_teams():
    client = BaseClientBettingData()
    links = await client.get_links(where="type:eq:team")
    futures = [parse_teams_by_link(link) for link in links]
    for future in asyncio.as_completed(futures):
        teams, link = await future
        for team in teams:
            await client.create_team(json={"name": team, "site_name": link["site_name"], "link_id": link["link_id"]})
    await asyncio.sleep(PeriodForCreation.TEAMS)
    await create_teams()

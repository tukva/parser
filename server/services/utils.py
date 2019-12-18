import asyncio
from datetime import datetime

from common.rest_client.base_client_betting_data import BaseClientBettingData

from services.parsers import team_parser


async def parse_teams_by_link(link):
    teams = await team_parser(link["link"], link["attributes"]["class"], link["attributes"]["elem"])
    return link, teams


async def update_teams():
    client = BaseClientBettingData()
    links = await client.get_links()
    futures = [parse_teams_by_link(link) for link in links]
    for future in asyncio.as_completed(futures):
        link, teams = await future
        tasks = []
        if link["type"] == "real_team":
            for team in teams:
                tasks.append(asyncio.ensure_future(client.create_real_teams(json={"name": team})))
        else:
            for team in teams:
                tasks.append(asyncio.ensure_future(client.create_team(
                    json={"name": team, "site_name": link["site_name"], "link_id": link["link_id"]})))
        await asyncio.wait(tasks)
    await asyncio.sleep(7200)
    await update_teams()

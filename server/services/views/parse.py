from marshmallow.exceptions import ValidationError
from sanic.response import json

from services.parsers import team_parser
from services.forms import RequestParseSchema


async def parse_team(request):
    try:
        data = RequestParseSchema().load(request.json)
    except ValidationError as e:
        return json(e.messages, 422)
    teams = team_parser(data["url"], data["cls"], data["elem"])
    return json(teams, 200)

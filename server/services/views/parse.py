from http import HTTPStatus

from marshmallow.exceptions import ValidationError
from sanic.response import json

from services.parsers import team_parser
from services.forms import RequestParseSchema


async def parse_team(request):
    try:
        data = RequestParseSchema().load(request.json)
    except ValidationError as e:
        return json(e.messages, HTTPStatus.UNPROCESSABLE_ENTITY)
    teams = team_parser(data["url"], data["class_"], data["elem"])
    return json(teams, HTTPStatus.OK)

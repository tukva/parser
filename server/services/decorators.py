from collections import namedtuple
from functools import wraps

from sanic.response import json
from sanic.log import logger

from services.utils import ParserTeamsByLink, ParserAllTeams

Parse_by = namedtuple('Parse_by', ['name', 'cls_parse_by_link', 'cls_parse_by_all_links'])
parser_teams = Parse_by("teams", ParserTeamsByLink, ParserAllTeams)

VALID_PARSER_BY_FIELDS = [parser_teams]


def mapp_func():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            req_json = request.json
            parse_by_field = req_json["parse_by"] if req_json and "parse_by" in req_json else None

            if not parse_by_field:
                logger.error("Not correct request field")
                return json({"Bad request"}, 400)

            parser_by = None
            for field in VALID_PARSER_BY_FIELDS:
                if field.name == parse_by_field:
                    parser_by = field

            if not parser_by:
                logger.error("order_by field is invalid")
                return json({"Locked"}, 423)

            if kwargs.get("link_id"):
                cls = parser_by.cls_parse_by_link
                return await f(request=request, cls=cls, *args, **kwargs)

            cls = parser_by.cls_parse_by_all_links
            return await f(request, cls, *args, **kwargs)
        return decorated_function
    return decorator

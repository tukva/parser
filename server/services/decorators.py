from collections import namedtuple
from functools import wraps

from sanic.response import json

from services.utils import ParserTeamsByLink, ParserAllTeams

Parse_by = namedtuple('Parse_by', ['name', 'cls_parse_by_link', 'cls_parse_by_all_links'])
parser_teams = Parse_by("teams", ParserTeamsByLink, ParserAllTeams)

VALID_PARSER_BY_FIELDS = [parser_teams]


def mapp_func():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            parse_by_field = request.json.get("parse_by") if request.json else None

            if not parse_by_field:
                return json({"Bad request"}, 400)

            parser_by = None
            for field in VALID_PARSER_BY_FIELDS:
                if field.name == parse_by_field:
                    parser_by = field

            if not parser_by:
                return json({f"Can not parse by '{parse_by_field}'. "
                             f"Valid values: {[field.name for field in VALID_PARSER_BY_FIELDS]}"}, 422)

            if kwargs.get("link_id"):
                cls = parser_by.cls_parse_by_link
                return await f(request=request, cls=cls, *args, **kwargs)

            cls = parser_by.cls_parse_by_all_links
            return await f(request, cls, *args, **kwargs)
        return decorated_function
    return decorator

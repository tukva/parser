from collections import namedtuple
from functools import wraps

from sanic.response import json

from services.utils import ParserTeamsByLink, ParserAllTeams, ParserRealTeams

Parse_by = namedtuple('Parse_by', ['name', 'cls_parse_by_link', 'cls_parse_by_all_links'])
parser_teams = Parse_by("teams", ParserTeamsByLink, ParserAllTeams)
parser_real_teams = Parse_by("real_teams", None, ParserRealTeams)

VALID_PARSER_BY_FIELDS = [parser_teams, parser_real_teams]


def mapp_func():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            parse_by_field = request.args.get("parse_by")

            if not parse_by_field:
                return json("Type the parse_by parameter if you want to parse something", 200)

            parser_by = None
            for field in VALID_PARSER_BY_FIELDS:
                if field.name == parse_by_field:
                    parser_by = field

            if not parser_by:
                return json(f"Can not parse by '{parse_by_field}'. "
                            f"Valid values: {[field.name for field in VALID_PARSER_BY_FIELDS]}", 422)

            if kwargs.get("link_id"):
                if not parser_by.cls_parse_by_link:
                    return json("Can not parse by link", 422)

                cls = parser_by.cls_parse_by_link
                return await f(request=request, cls=cls, *args, **kwargs)

            if not parser_by.cls_parse_by_all_links:
                return json("Can not parse by all links", 422)

            cls = parser_by.cls_parse_by_all_links

            return await f(request, cls, *args, **kwargs)
        return decorated_function
    return decorator

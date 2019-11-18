from functools import wraps
from sanic.response import json

from services.utils import ParserTeamsByLink, ParserAllTeams

VALID_FIELDS = {"teams": {"by_link": ParserTeamsByLink, "all_teams": ParserAllTeams}}


def mapp_func_by_link():
    def decorator(f):
        @wraps(f)
        async def decorated_function(self, request, link_id, *args, **kwargs):
            req_json = request.json
            parse_by = req_json["parse_by"] if req_json and "parse_by" in req_json else None

            if not parse_by or parse_by not in VALID_FIELDS:
                return json({"'parse_by' field wrong"}, 423)

            cls = VALID_FIELDS[parse_by]["by_link"]
            return await f(self, request, link_id, cls, *args, **kwargs)
        return decorated_function
    return decorator


def mapp_func_by_all_links():
    def decorator(f):
        @wraps(f)
        async def decorated_function(self, request, *args, **kwargs):
            req_json = request.json
            parse_by = req_json["parse_by"] if req_json and "parse_by" in req_json else None

            if not parse_by or parse_by not in VALID_FIELDS:
                return json({"'parse_by' field wrong"}, 423)

            cls = VALID_FIELDS[parse_by]["all_teams"]
            return await f(self, request, cls, *args, **kwargs)
        return decorated_function
    return decorator

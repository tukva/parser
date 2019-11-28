from sanic.response import json

from engine import Connection
from services.utils import set_real_team


async def change_status_team(request, team_id):
    if not request.json:
        return json("Bad request", 400)
    real_team_id = request.json.get('real_team_id')
    status = request.json.get('status')
    async with Connection() as conn:
        return await set_real_team(conn, team_id, real_team_id, status)

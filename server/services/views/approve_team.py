from engine import Connection
from services.utils import set_real_team


async def approve_team(request, team_id):
    real_team_id = request.json.get('real_team_id') if request.json else None
    async with Connection() as conn:
        return await set_real_team(conn, team_id, real_team_id)

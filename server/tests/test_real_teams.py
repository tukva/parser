import pytest


@pytest.mark.real_teams
@pytest.mark.parser
async def test_get_real_teams(test_cli, add_real_team):
    resp = await test_cli.get('/real-teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'real_team_id': 1, 'name': 'Chelsea', }]

    assert resp.status == 200
    assert await resp.json() == response_json


@pytest.mark.real_teams
@pytest.mark.parser
async def test_refresh_real_teams(test_cli, tables):
    resp = await test_cli.put('/real-teams')

    assert resp.status == 200

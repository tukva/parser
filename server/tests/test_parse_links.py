import pytest


@pytest.mark.parse_links
@pytest.mark.parser
async def test_get_teams_by_all_link(test_cli, add_team):
    resp = await test_cli.get('/parse-links/teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin'}]

    assert resp.status == 200
    assert await resp.json() == response_json


@pytest.mark.parse_links
@pytest.mark.parser
async def test_get_teams_by_link(test_cli, add_team):
    resp = await test_cli.get('/parse-links/1/teams')

    response_json = [{'created_on': '2019-11-07T14:13:44.041152', 'link_id': 1, 'team_id': 1,
                      'name': 'Chelsea', 'real_team_id': None, 'site_name': 'bwin'}]

    assert resp.status == 200
    assert await resp.json() == response_json

    resp = await test_cli.get('/parse-links/3/teams')

    assert resp.status == 404
    assert await resp.text() == "Not Found"


@pytest.mark.parse_links
@pytest.mark.parser
async def test_refresh_teams_by_link(test_cli, tables):
    resp = await test_cli.put('/parse-links/1/teams')

    assert resp.status == 200
    assert await resp.text() == "Ok"

    resp = await test_cli.put('/parse-links/3/teams')

    assert resp.status == 404
    assert await resp.text() == "Not Found"


@pytest.mark.parse_links
@pytest.mark.parser
async def test_delete_teams_by_link(test_cli, add_team):
    resp = await test_cli.put('/parse-links/1/teams')

    assert resp.status == 200
    assert await resp.text() == "Ok"

    resp = await test_cli.put('/parse-links/3/teams')

    assert resp.status == 404
    assert await resp.text() == "Not Found"

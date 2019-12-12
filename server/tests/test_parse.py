from unittest import mock
from http import HTTPStatus

async def test_parse_team(test_cli):
    with mock.patch("services.views.parse.team_parser", return_value="mock_data"):
        resp = await test_cli.post('/parse', json={"url": "test_data", "cls": "test_data", "elem": "test_data"})

        assert resp.status == HTTPStatus.OK
        assert await resp.json() == "mock_data"

        resp = await test_cli.post('/parse', json={"wrong_key1": "test_data",
                                                   "wrong_key2": "test_data",
                                                   "wrong_key3": "test_data"})

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert await resp.json() == {'url': ['Missing data for required field.'],
                                     'cls': ['Missing data for required field.'],
                                     'elem': ['Missing data for required field.'],
                                     'wrong_key1': ['Unknown field.'],
                                     'wrong_key2': ['Unknown field.'],
                                     'wrong_key3': ['Unknown field.']}

        resp = await test_cli.post('/parse', json={"url": "", "cls": "test_data",  "elem": "test_data"})

        assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
        assert await resp.json() == {'url': ['Length must be between 4 and 255.']}

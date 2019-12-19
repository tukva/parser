import unittest


from unittest import mock
from bs4 import BeautifulSoup
from http import HTTPStatus

<<<<<<< Updated upstream

async def test_parse_team(test_cli):
    with mock.patch("services.views.parse.team_parser", return_value="mock_data"):
        resp = await test_cli.post('/parse', json={"url": "test_data", "cls": "test_data", "elem": "test_data"})
=======
from server.services import parsers


html = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>Document</title>
</head>
<body>
	<ul>
		<li class="item_base"><a class="title">Oxford Utd</a></li>
		<li class="item_base"><a class="title">Man City</a></li>
		<li class="item_sep"><a class="title">Oxford Utd vs Man City</a></li>
	</ul>
</body>
</html>
"""
class MockRequestResponse:
    @classmethod
    @property
    def text(cls):
        return html


# async def test_parse_team(test_cli):
#     with mock.patch("services.views.parse.team_parser", return_value="mock_data"):
#         resp = await test_cli.post('/parse', json={"url": "test_data", "cls": "test_data", "elem": "test_data"})
#
#         assert resp.status == HTTPStatus.OK
#         assert await resp.json() == "mock_data"
#
#         resp = await test_cli.post('/parse', json={"wrong_key1": "test_data",
#                                                    "wrong_key2": "test_data",
#                                                    "wrong_key3": "test_data"})
#
#         assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
#         assert await resp.json() == {'url': ['Missing data for required field.'],
#                                      'cls': ['Missing data for required field.'],
#                                      'elem': ['Missing data for required field.'],
#                                      'wrong_key1': ['Unknown field.'],
#                                      'wrong_key2': ['Unknown field.'],
#                                      'wrong_key3': ['Unknown field.']}
#
#         resp = await test_cli.post('/parse', json={"url": "", "cls": "test_data",  "elem": "test_data"})
#
#         assert resp.status == HTTPStatus.UNPROCESSABLE_ENTITY
#         assert await resp.json() == {'url': ['Length must be between 4 and 255.']}
>>>>>>> Stashed changes


class TestBaseParserType(unittest.TestCase):
    @mock.patch('requests.get', mock.Mock(side_effect = lambda url, headers: {'url_true': html}.get(url, f'unhandled request {url}')))
    def test_get_page(self):
        base_parser = parsers.BaseParserType
        page = base_parser.get_page(url='url_true')

        self.assertEqual(page, html)

if __name__ == '__main__':
    unittest.main()


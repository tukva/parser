from os import getenv

PARSER_API_PORT = int(getenv('PARSER_API_PORT', 5000))
PARSER_API_HOST = getenv('PARSER_API_HOST', "localhost")

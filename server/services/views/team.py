from sanic.views import HTTPMethodView
from sanic.response import text


class SimpleView(HTTPMethodView):

    async def get(self, request):
        return text('I am get method')

    async def post(self, request):
        return text('I am post method')

    async def put(self, request):
        return text('I am put method')

    async def patch(self, request):
        return text('I am patch method')

    async def delete(self, request):
        return text('I am delete method')

# -!- coding: utf-8 -!-

from sanic import Sanic
from sanic.response import json


app = Sanic(__name__)

@app.route("/")
async def index(request):
    return json({'msg':"fuck"})
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=9000)

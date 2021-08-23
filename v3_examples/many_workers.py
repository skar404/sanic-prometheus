from sanic import Sanic
from sanic.response import json

from v3 import Monitor, Mode, MetricsStruct

app = Sanic(name='tmp')


async def ping(_request):
    return json({'success': 'you are home'})


async def hone(_request):
    return json({'success': 'you are home'})


async def user(_request):
    return json({'success': 'you are home'})


if __name__ == "__main__":
    Monitor(
        app=app,
        mode=Mode.MULTIPROCESSING,
    )

    app.run(host="127.0.0.1", port=8000, workers=2)

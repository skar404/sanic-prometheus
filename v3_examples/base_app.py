from prometheus_client import Counter
from sanic import Sanic
from sanic.response import json

from v3 import Monitor, MetricsStruct

app = Sanic(name='tmp')


async def ping(_request):
    return json({'success': 'you are home'})


async def hone(_request):
    return json({'success': 'you are home'})


async def user(_request):
    return json({'success': 'you are home'})


if __name__ == "__main__":
    m = Monitor(app=app)
    m.add_metric(MetricsStruct(
        key='list',
        metric=Counter(
            name='list',
            documentation='',
            labelnames=['label_1', 'label_2'],
        )
    ))
    m._metrics['list'].labels('123', '123123').inc(1)

    app.run(host="127.0.0.1", port=8000, workers=1)

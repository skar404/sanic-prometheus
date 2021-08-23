from typing import List, Optional, Dict

from prometheus_client import CollectorRegistry, multiprocess, CONTENT_TYPE_LATEST
from prometheus_client.exposition import generate_latest
from prometheus_client.metrics import MetricWrapperBase
from sanic import Sanic
from sanic.response import raw

from .structs import Mode, MetricsStruct


class Monitor:
    __registry = CollectorRegistry(auto_describe=True)

    _metrics: Dict[str, MetricWrapperBase]

    def __init__(self, app: Sanic, uri: Optional[str] = None, mode: Mode = None):
        self.app: Sanic = app
        self.uri: str = uri or '/metrics'

        self.mode: Mode = mode or Mode.SINGLE
        self._metrics = {}

        self.sync_path = '.'

        self.app.metrics = self
        self.app.add_route(self._expose_metrics, self.uri, methods=('GET',))

    def add_metric(self, metric: MetricsStruct):
        self.__registry.register(metric.metric)
        self._metrics[metric.key] = metric.metric

    def add_metrics(self, metrics: List[MetricsStruct]):
        for m in metrics:
            self._metrics[m.key] = m.metric

    async def _expose_metrics(self, _request):
        return raw(self._get_metrics_data(),
                   content_type=CONTENT_TYPE_LATEST)

    def _get_metrics_data(self):
        if self.mode == Mode.SINGLE:
            registry = self.__registry
        elif self.mode.MULTIPROCESSING:
            registry = CollectorRegistry()
            multiprocess.MultiProcessCollector(registry, path=self.sync_path)
        else:
            raise
        data = generate_latest(registry)
        return data

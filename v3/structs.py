from dataclasses import dataclass
from enum import IntEnum
from typing import Type

from prometheus_client.metrics import MetricWrapperBase


@dataclass
class MetricsStruct:
    key: str
    metric: MetricWrapperBase


class Mode(IntEnum):
    # use prometheus_client.registry.CollectorRegistry
    #   create tmp file in sync metrics in all workers
    MULTIPROCESSING = 1
    # use in one WORKER
    SINGLE = 2

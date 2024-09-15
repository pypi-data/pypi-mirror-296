from aiovk.mixins import LimitRateDriverMixin
from aiovk.drivers import HttpDriver


class DefaultDriver(LimitRateDriverMixin, HttpDriver):
    requests_per_period = 2
    period = 1
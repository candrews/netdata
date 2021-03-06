# -*- coding: utf-8 -*-
# Description: nginx netdata python.d plugin
# Author: Pawel Krupa (paulfantom)

from base import UrlService

# default module values (can be overridden per job in `config`)
# update_every = 2
priority = 60000
retries = 5

# default job configuration (overridden by python.d.plugin)
# config = {'local': {
#             'update_every': update_every,
#             'retries': retries,
#             'priority': priority,
#             'url': 'http://localhost/stub_status'
#          }}

# charts order (can be overridden if you want less charts, or different order)
ORDER = ['connections', 'requests', 'connection_status', 'connect_rate']

CHARTS = {
    'connections': {
        'options': "'' 'nginx Active Connections' 'connections' nginx nginx.connections line",
        'lines': [
            {"name": "active",
             "options": "'' absolute 1 1"}
        ]},
    'requests': {
        'options': "'' 'nginx Requests' 'requests/s' nginx nginx.requests line",
        'lines': [
            {"name": "requests",
             "options": "'' incremental 1 1"}
        ]},
    'connection_status': {
        'options': "'' 'nginx Active Connections by Status' 'connections' nginx nginx.connection.status line",
        'lines': [
            {"name": "reading",
             "options": "'' absolute 1 1"},
            {"name": "writing",
             "options": "'' absolute 1 1"},
            {"name": "waiting",
             "options": "idle absolute 1 1"}
        ]},
    'connect_rate': {
        'options': "'' 'nginx Connections Rate' 'connections/s' nginx nginx.performance line",
        'lines': [
            {"name": "accepts",
             "options": "accepted incremental 1 1"},
            {"name": "handled",
             "options": "'' incremental 1 1"}
        ]}
}


class Service(UrlService):
    def __init__(self, configuration=None, name=None):
        UrlService.__init__(self, configuration=configuration, name=name)
        if len(self.url) == 0:
            self.url = "http://localhost/stub_status"
        self.order = ORDER
        self.charts = CHARTS

    def _formatted_data(self):
        """
        Format data received from http request
        :return: dict
        """
        try:
            raw = self._get_data().split(" ")
            return {'active': int(raw[2]),
                    'requests': int(raw[7]),
                    'reading': int(raw[11]),
                    'writing': int(raw[13]),
                    'waiting': int(raw[15]),
                    'accepts': int(raw[8]),
                    'handled': int(raw[9])}
        except (ValueError, AttributeError):
            return None

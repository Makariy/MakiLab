import json
import requests
from typing import List, Dict

from .models import Proxy
from .exceptions import NoMoreProxiesException


class FreeProxier:
    def __init__(self, url='https://www.proxy-list.download/api/v1/get?type=http'):
        self.url = url
        self.used_proxies = []
        self.proxies = self.make_proxies()

    def make_proxies(self) -> List[Proxy]:
        proxies = []

        response = requests.get(self.url)
        for raw_proxy in filter(lambda a: a, response.text.split('\r\n')):
            ip, port = raw_proxy.split(':')
            proxies.append(
                Proxy(
                    ip=ip,
                    port=port,
                    speed=100,
                )
            )
        return proxies

    def add_used_proxy(self, proxy: Proxy):
        self.proxies.remove(proxy)
        self.used_proxies.append(proxy)

    def get_proxy(self) -> Proxy:
        if len(self.proxies) == 0:
            self.make_proxies()
            if not self.proxies:
                raise NoMoreProxiesException()
            return self.get_proxy()
        return self.proxies[0]


class Proxier:
    def __init__(self, url='https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=speed&sort_type=desc'):
        self.url = url
        self.used_proxies = []
        self.proxies = self.make_proxies()

    def _make_proxies_from_data(self, data: Dict[str, List[Dict[str, str]]]) -> List[Proxy]:
        proxies = []
        for proxy_data in data['data']:
            proxy = Proxy(
                ip=proxy_data['ip'],
                port=int(proxy_data['port']),
                speed=int(proxy_data['speed'])
            )
            if proxy not in self.used_proxies:
                proxies.append(proxy)
        return proxies

    def make_proxies(self):
        response = requests.get(self.url)
        data = json.loads(response.text)
        return self._make_proxies_from_data(data)

    def add_used_proxy(self, proxy):
        self.proxies.remove(proxy)
        self.used_proxies.append(proxy)

    def get_proxy(self) -> Proxy:
        if len(self.proxies) == 0:
            self.make_proxies()
            if not self.proxies:
                raise NoMoreProxiesException()
            return self.get_proxy()
        return self.proxies[0]


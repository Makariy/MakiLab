import json
import requests
from .models import Proxy
from typing import List, Dict, Union
from .exceptions import NoMoreProxiesException


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
                port=proxy_data['port'],
                speed=proxy_data['speed']
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
        try:
            proxy = self.proxies.pop()
        except IndexError:
            self.make_proxies()
            return self.get_proxy()
            
        self.used_proxies.append(proxy)
        return proxy

    def get_proxies(self, count=8) -> List[Proxy]:
        return [self.get_proxy() for i in range(count)]



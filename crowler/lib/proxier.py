import json
import requests
from typing import List, Dict, Union


class Proxy:
    ip: str
    port: int
    speed: int

    def __init__(self, proxy_data: Dict[str, Union[str, int]]):
        self.ip = proxy_data['ip']
        self.port = proxy_data['port']
        self.speed = proxy_data.get('speed') or 0

    def __cmp__(self, other):
        return self.ip == other.ip and self.port == other.port

    def __str__(self):
        return json.dumps({
            'ip': self.ip,
            'port': self.port,
            'speed': self.speed
        })


class Proxier:
    def __init__(self, url='https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=speed&sort_type=desc'):
        self.url = url
        self.used_proxies = []
        self.proxies = self.make_proxies()

    def _make_proxies_from_data(self, data: Dict[str, List[Dict[str, str]]]) -> List[Proxy]:
        proxies = []
        for proxy_data in data['data']:
            proxy = Proxy(proxy_data)
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
        proxy = self.proxies.pop()
        self.used_proxies.append(proxy)
        return proxy

    def get_proxies(self, count=8) -> List[Proxy]:
        return [self.get_proxy() for i in range(count)]



import json
import requests
from typing import List, Dict, Union
from crowler import config


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
        with open(config.USER_PROXIES_FILE_NAME, 'r') as file:
            data = json.loads(file.read())
            for proxy_data in data['proxies']:
                self.used_proxies.append(Proxy(proxy_data))
        self.proxies = self._get_proxies()

    def __del__(self):
        with open(config.USER_PROXIES_FILE_NAME, 'w') as file:
            file.write(json.dumps({
                'proxies': [str(proxy) for proxy in self.used_proxies]
            }))

    def _make_proxies_from_data(self, data: Dict[str, List[Dict[str, str]]]) -> List[Proxy]:
        proxies = []
        for proxy_data in data['data']:
            proxy = Proxy(proxy_data)
            if proxy not in self.used_proxies:
                proxies.append(proxy)
        return proxies

    def _get_proxies(self):
        response = requests.get(self.url)
        data = json.loads(response.text)
        return self._make_proxies_from_data(data)

    def get_proxy(self) -> Proxy:
        proxy = self.proxies.pop()
        self.used_proxies.append(proxy)
        return proxy



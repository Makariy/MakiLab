from dataclasses import dataclass


@dataclass
class Proxy:
    ip: str
    port: int
    speed: int

    def __cmp__(self, other):
        return self.ip == other.ip and self.port == other.port

    def __str__(self):
        return f'https://{self.ip}:{self.port}'


@dataclass
class HLS:
    name: str
    resolution: str
    bandwidth: int
    url: str


@dataclass
class QUALITY:
    BEST = 1
    NORMAL = 2
    WORST = 3


@dataclass
class Video:
    title: str
    url: str
    preview_url: str
    uuid: str


import pydantic
from typing import List, Dict, Union, Optional


class Proxy(pydantic.BaseModel):
    ip: str
    port: int
    speed: int

    def __cmp__(self, other):
        return self.ip == other.ip and self.port == other.port


class HLS(pydantic.BaseModel):
    name: str
    resolution: str
    bandwidth: int
    url: str


class QUALITY:
    BEST = 1
    NORMAL = 2
    WORST = 3


class Video(pydantic.BaseModel):
    title: str
    url: str
    preview_url: str
    uuid: str


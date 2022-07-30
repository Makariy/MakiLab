from abc import abstractmethod, ABC
from typing import Optional

import aioredis
from utils.utils import singleton
import config


class CacheBase(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[str]:
        pass

    @abstractmethod
    async def set(self, key: str, value: str):
        pass

    @abstractmethod
    async def delete(self, key: str):
        pass

@singleton
class RedisCache(CacheBase):
    def __init__(self, *args, **kwargs):
        host = config.CACHE_HOST
        port = config.CACHE_PORT
        self._redis = aioredis.from_url(f"redis://{host}:{port}")

    async def get(self, key: str) -> Optional[str]:
        return await self._redis.get(key)

    async def set(self, key: str, value: str):
        return await self._redis.set(key, value)

    async def delete(self, key: str):
        return await self._redis.delete(key)


@singleton
class DummyCache(CacheBase):
    def __init__(self, *args, **kwargs):
        self._db = {}

    async def get(self, key: str) -> Optional[str]:
        return self._db.get(key)

    async def set(self, key: str, value: str):
        self._db[key] = value

    async def delete(self, key: str):
        self._db.pop(key)


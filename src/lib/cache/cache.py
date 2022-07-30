import config
from .caches import CacheBase

Cache: CacheBase = config.CACHE_CLASS()

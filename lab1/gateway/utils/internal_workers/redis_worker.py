import json

import redis.asyncio as redis

from config import app_settings


class RedisWorker:
    def __init__(self, dsn: str):
        self._client = redis.from_url(dsn, decode_responses=True)

    async def set(self, key: str, value: dict, ex: int | None = None) -> None:
        await self._client.set(key, json.dumps(value), ex=ex)

    async def get(self, key: str) -> dict | None:
        value = await self._client.get(key)
        if value is None:
            return None
        return json.loads(value)

    async def delete(self, key: str) -> None:
        await self._client.delete(key)


redis_worker = RedisWorker(app_settings.REDIS_DSN)

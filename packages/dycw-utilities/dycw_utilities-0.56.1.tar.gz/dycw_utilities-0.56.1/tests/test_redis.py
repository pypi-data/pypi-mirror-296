from __future__ import annotations

import redis
import redis.asyncio
from hypothesis import given
from hypothesis.strategies import DataObject, booleans, data

from tests.conftest import SKIPIF_CI_AND_NOT_LINUX
from utilities.hypothesis import redis_cms
from utilities.redis import RedisKey, yield_client, yield_client_async


class TestRedisKey:
    @given(data=data(), value=booleans())
    @SKIPIF_CI_AND_NOT_LINUX
    async def test_main(self, *, data: DataObject, value: bool) -> None:
        async with redis_cms(data) as container:
            key = RedisKey(name=container.key, type=bool)
            match container.client:
                case redis.Redis():
                    assert key.get() is None
                    _ = key.set(value)
                    assert key.get() is value
                case redis.asyncio.Redis():
                    assert await key.get_async() is None
                    _ = await key.set_async(value)
                    assert await key.get_async() is value


class TestYieldClient:
    def test_sync_default(self) -> None:
        with yield_client() as client:
            assert isinstance(client, redis.Redis)

    def test_sync_client(self) -> None:
        with yield_client() as client1, yield_client(client=client1) as client2:
            assert isinstance(client2, redis.Redis)

    async def test_async_default(self) -> None:
        async with yield_client_async() as client:
            assert isinstance(client, redis.asyncio.Redis)

    async def test_async_client(self) -> None:
        async with (
            yield_client_async() as client1,
            yield_client_async(client=client1) as client2,
        ):
            assert isinstance(client2, redis.asyncio.Redis)

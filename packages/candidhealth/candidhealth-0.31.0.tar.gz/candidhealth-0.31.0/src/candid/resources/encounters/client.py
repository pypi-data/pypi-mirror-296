# This file was auto-generated by Fern from our API Definition.

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .resources.v_4.client import AsyncV4Client, V4Client


class EncountersClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper
        self.v_4 = V4Client(client_wrapper=self._client_wrapper)


class AsyncEncountersClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper
        self.v_4 = AsyncV4Client(client_wrapper=self._client_wrapper)

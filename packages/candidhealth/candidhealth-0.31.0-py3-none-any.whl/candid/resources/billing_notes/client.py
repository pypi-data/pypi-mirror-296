# This file was auto-generated by Fern from our API Definition.

from ...core.client_wrapper import AsyncClientWrapper, SyncClientWrapper
from .resources.v_2.client import AsyncV2Client, V2Client


class BillingNotesClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper
        self.v_2 = V2Client(client_wrapper=self._client_wrapper)


class AsyncBillingNotesClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper
        self.v_2 = AsyncV2Client(client_wrapper=self._client_wrapper)

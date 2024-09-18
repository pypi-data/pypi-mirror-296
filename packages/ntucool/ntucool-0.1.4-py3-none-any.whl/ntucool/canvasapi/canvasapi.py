import asyncio

import awaitlet
import httpx
from rich import print

from ..requestor import Requestor
from ._canvasapi import Canvas
from ._canvasapi.requester import Requester


class _RequesterWrapped(Requester):
    def __init__(self, base_url, access_token, requestor: Requestor, is_async: bool):
        super().__init__(base_url, access_token)

        self.requestor = requestor
        self.is_async = is_async

    def _delete_request(self, url, headers, data=None, **kwargs):
        if kwargs.pop("is_async", False):
            return self.requestor.async_delete(url, headers=headers, **kwargs)
        assert data is None
        return self.requestor.delete(url, headers=headers, **kwargs)

    def _get_request(self, url, headers, params=None, **kwargs):
        if kwargs.pop("is_async", False):
            return self.requestor.async_get(url, headers=headers, **kwargs)
        return self.requestor.get(url, headers=headers, params=params, **kwargs)

    def _patch_request(self, url, headers, data=None, **kwargs):
        if kwargs.pop("is_async", False):
            return self.requestor.async_patch(url, headers=headers, data=data, **kwargs)
        return self.requestor.patch(url, headers=headers, data=data, **kwargs)

    def _post_request(self, url, headers, data=None, json=False):
        if data and data.get("is_async", False):
            return self.requestor.async_post(url, headers=headers, data=data, json=json)

        return self.requestor.post(url, headers=headers, data=data, json=json)

    def _put_request(self, url, headers, data=None, **kwargs):
        if kwargs.pop("is_async", False):
            return self.requestor.async_put(url, headers=headers, data=data, **kwargs)
        return self.requestor.put(url, headers=headers, data=data, **kwargs)

    def request(
        self,
        method,
        endpoint=None,
        headers=None,
        use_auth=True,
        _url=None,
        _kwargs=None,
        json=False,
        **kwargs,
    ) -> httpx.Response:
        use_auth = False
        return super().request(
            method, endpoint, headers, use_auth, _url, _kwargs, json, **kwargs
        )

    async def request_async(
        self,
        method,
        endpoint=None,
        headers=None,
        use_auth=True,
        _url=None,
        _kwargs=None,
        json=False,
        **kwargs,
    ) -> httpx.Response:
        use_auth = False
        return await awaitlet.async_def(
            super().request,
            method,
            endpoint,
            headers,
            use_auth,
            _url,
            _kwargs,
            json,
            is_async=True,
            **kwargs,
        )


class CanvasAPI(Canvas):
    def __init__(self, requestor: Requestor, is_async=False):
        base_url = "https://cool.ntu.edu.tw"
        access_token = ""

        super().__init__(base_url, access_token)

        # overwrite the requester
        self._Canvas__requester = _RequesterWrapped(
            base_url, access_token, requestor, is_async
        )



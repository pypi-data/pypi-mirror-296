from contextlib import asynccontextmanager
from typing import Any, Literal, overload
from urllib.parse import unquote

import httpx
from httpx._client import UseClientDefault
from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    ProxyTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestExtensions,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

from ntucool.auth import async_get_auth_cookies, get_auth_cookies

DEFAULT_TIMEOUT_CONFIG = httpx.Timeout(timeout=0.5)

USE_CLIENT_DEFAULT = UseClientDefault()

# def wrap_request[**P1, T1, S, **P2](f: Callable[Concatenate[P1], T1]) -> Callable[
#     [Callable[Concatenate[S, P2], object]],
#     # Callable[Concatenate[Requestor, bool, str, P1], T1],
#     Callable[..., T1],
# ]:


def wrap_request(method: str):
    """
    For type hint.
    """

    # def wrap_request(f: Callable[..., Any]):
    def dec(_):
        def _f(self: "Requestor", url: str, **kwargs):
            return self.request(method, url, **kwargs)

        return _f

    return dec  # type: ignore


def wrap_async_request(method: str):
    """
    For type hint.
    """

    # def wrap_request(f: Callable[..., Any]):
    def dec(_):
        async def _f(self: "Requestor", url: str, **kwargs):
            return await self.async_request(method, url, **kwargs)

        return _f

    return dec  # type: ignore


DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Origin": "https://cool.ntu.edu.tw",
    # "X-Requested-With": "XMLHttpRequest",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
}


class Requestor:
    __BASE__ = "https://cool.ntu.edu.tw"
    __MERGE_KEYS__ = ["headers", "cookies"]

    account: str
    password: str

    headers: dict[str, str] = DEFAULT_HEADERS
    cookies: dict[str, str]

    has_auth = False
    client: httpx.Client
    async_client: httpx.AsyncClient

    def __init__(self, account: str, password: str, is_async: bool) -> None:
        self.account = account
        self.password = password

        # TODO: maybe don't need this
        self.is_async = is_async

        self.client = httpx.Client()
        self.async_client = httpx.AsyncClient()

    def _merge_args(self, kwargs: dict[str, Any]):
        if token := self.cookies.get("_csrf_token", None):
            self.headers["X-CSRF-Token"] = unquote(token)

        new_kwargs = kwargs.copy()
        for key in self.__MERGE_KEYS__:
            new_kwargs[key] = (kwargs.get(key, {}) or {}) | getattr(self, key)
        return new_kwargs

    def _process_args(
        self,
        url: str,
        is_xhr: bool = False,
        referrer: str = "",
        **kwargs,
    ):
        if url.startswith("/"):
            url = self.__BASE__ + url

        headers = kwargs.get("headers", {})
        if is_xhr:
            headers["X-Requested-With"] = "XMLHttpRequest"
        if referrer:
            if referrer.startswith("/"):
                referrer = self.__BASE__ + referrer
                print(referrer)
            headers["Referer"] = referrer
        kwargs["headers"] = headers
        kwargs = self._merge_args(kwargs)

        return url, kwargs

    def update_cookies(self, response: httpx.Response):
        self.cookies |= response.cookies

    def request(
        self: "Requestor",
        method: str,
        url: str,
        stream: bool = False,
        **kwargs,
    ):
        assert not self.is_async

        if not self.has_auth:
            self.cookies = get_auth_cookies(self.client, self.account, self.password)
            self.has_auth = True

        url, kwargs = self._process_args(url, **kwargs)
        if not stream:
            response: httpx.Response = self.client.request(method, url, **kwargs)
            if not response.has_redirect_location:
                # todo: disable
                response.raise_for_status()
            self.update_cookies(response)
            return response

        return httpx.stream(method, url, **kwargs)

    async def async_request(
        self: "Requestor",
        method: str,
        url: str,
        **kwargs,
    ):
        assert self.is_async

        if not self.has_auth:
            self.cookies = await async_get_auth_cookies(
                self.async_client, self.account, self.password
            )
            self.has_auth = True

        url, kwargs = self._process_args(url, **kwargs)
        response: httpx.Response = await self.async_client.request(
            method, url, **kwargs
        )
        self.update_cookies(response)
        return response

    def stream(
        self,
        method: str,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | None = None,
        proxy: ProxyTypes | None = None,
        proxies: ProxiesTypes | None = None,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        follow_redirects: bool = False,
        verify: VerifyTypes = True,
        cert: CertTypes | None = None,
        trust_env: bool = True,
    ):
        def f(url, **kwargs):
            url, kwargs = self._process_args(url, **kwargs)
            return httpx.stream(url=url, **kwargs)

        return f(
            url,
            method=method,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
            cookies=cookies,
            proxy=proxy,
            proxies=proxies,
            cert=cert,
            verify=verify,
            timeout=timeout,
            trust_env=trust_env,
        )

    @asynccontextmanager
    async def async_stream(
        self,
        method: str,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ):
        def f(url, **kwargs):
            url, kwargs = self._process_args(url, **kwargs)
            return self.async_client.stream(
                url=url,
                **kwargs,
            )

        async with f(
            url,
            method=method,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
            cookies=cookies,
            timeout=timeout,
        ) as r:
            yield r

    @wrap_request("GET")
    def get(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | None = None,
        proxy: ProxyTypes | None = None,
        proxies: ProxiesTypes | None = None,
        follow_redirects: bool = False,
        cert: CertTypes | None = None,
        verify: VerifyTypes = True,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        trust_env: bool = True,
        #
        stream: bool = False,
        is_xhr: bool = False,
        referrer: str = "",
    ) -> httpx.Response: ...

    @wrap_request("POST")
    def post(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | None = None,
        proxy: ProxyTypes | None = None,
        proxies: ProxiesTypes | None = None,
        follow_redirects: bool = False,
        cert: CertTypes | None = None,
        verify: VerifyTypes = True,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        trust_env: bool = True,
        #
        stream: bool = False,
        is_xhr: bool = False,
        referrer: str = "",
    ) -> httpx.Response: ...

    @wrap_request("DELETE")
    def delete(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | None = None,
        proxy: ProxyTypes | None = None,
        proxies: ProxiesTypes | None = None,
        follow_redirects: bool = False,
        cert: CertTypes | None = None,
        verify: VerifyTypes = True,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        trust_env: bool = True,
    ) -> httpx.Response: ...

    @wrap_request("PUT")
    def put(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | None = None,
        proxy: ProxyTypes | None = None,
        proxies: ProxiesTypes | None = None,
        follow_redirects: bool = False,
        cert: CertTypes | None = None,
        verify: VerifyTypes = True,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
        trust_env: bool = True,
        #
        stream: bool = False,
        is_xhr: bool = False,
        referrer: str = "",
    ) -> httpx.Response: ...

    @wrap_request("PATCH")
    def patch(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> httpx.Response: ...

    @wrap_async_request("GET")
    async def async_get(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        #
        is_xhr: bool = False,
        referrer: str = "",
    ) -> httpx.Response: ...


    @wrap_async_request("POST")
    async def async_post(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        #
        is_xhr: bool = False,
        referrer: str = "",
    ) -> httpx.Response: ...

    @wrap_async_request("DELETE")
    async def async_delete(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> httpx.Response: ...

    @wrap_async_request("PUT")
    async def async_put(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
        #
        is_xhr: bool = False,
        referrer: str = "",
    ) -> httpx.Response: ...

    @wrap_async_request("PATCH")
    async def async_patch(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
        follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
        timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
        extensions: RequestExtensions | None = None,
    ) -> httpx.Response: ...



def is_logged_in(requestor: Requestor):
    res = requestor.get("https://cool.ntu.edu.tw/")
    try:
        res.raise_for_status()
        return True
    except:
        return False

import httpx
import asyncio
from typing import Optional, Union, List

class HttpClient:
    _client: Optional[httpx.AsyncClient] = None
    _proxy: Optional[Union[str, List[str]]] = None
    _proxy_index: int = 0

    @classmethod
    def _resolve_proxy(cls) -> Optional[str]:
        if cls._proxy is None:
            return None

        if isinstance(cls._proxy, str):
            return cls._proxy

        if isinstance(cls._proxy, list) and cls._proxy:
            proxy = cls._proxy[cls._proxy_index % len(cls._proxy)]
            cls._proxy_index += 1
            return proxy

        return None

    @classmethod
    def get(cls, proxy: Optional[Union[str, List[str]]] = None) -> httpx.AsyncClient:
        if proxy is not None:
            cls._proxy = proxy
            cls._client = None

        if cls._client is None:
            final_proxy = cls._resolve_proxy()
            transport = httpx.AsyncHTTPTransport(
                retries=3,
                proxy=final_proxy
            )
            cls._client = httpx.AsyncClient(
                transport=transport,
                http2=True,
                timeout=httpx.Timeout(3.0, connect=1.0),
                limits=httpx.Limits(max_keepalive_connections=100, max_connections=300),
            )
        return cls._client


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

getClient = HttpClient.get()
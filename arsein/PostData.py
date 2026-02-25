import asyncio
import base64
import io
import sys
import nest_asyncio
from base64 import b64decode
from json import JSONDecodeError, dumps, loads
from random import choice, choices, randint

import aiohttp
import httpx
import httpcore
from typing import Optional, Callable, Union, List

from .Clien import clien
from .Device import DeviceTelephone
from .Encoder import encoderjson
from .Error import AuthError, ErrorPrivatyKey, ErrorServer, Connection_Error
from .ErrorRubika import ErrorRubika
from .GetDataMethod import GetDataMethod
from .GtM import set_server
from .http_client import getClient, loop, HttpClient

nest_asyncio.apply()


async def download(
    auth: str,
    dc_id: int,
    file_id: str,
    size: int,
    access_hash: str,
    chunk_size: int = 131072,
    retries: int = 3,
    delay: float = 1.0,
    cdn_tag: str = None,
    dc_url: str = None,
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    sink: str = None,
    progress=None,
):
    url = f"https://messenger{dc_id}.iranlms.ir/GetFile.ashx"
    base_headers = {
        "auth": auth,
        "file-id": str(file_id),
        "access-hash-rec": access_hash,
        "user-agent": user_agent,
    }
    if cdn_tag:
        base_headers["cdn-tag"] = cdn_tag
    if dc_url:
        base_headers["dc-url"] = dc_url

    buf = io.BytesIO()
    writer = None
    if sink:
        writer = open(sink, "wb")

    async def fetch_chunk(client, start, end):
        headers = {**base_headers, "start-index": str(start), "last-index": str(end)}
        for attempt in range(retries):
            try:
                resp = await client.post(url, headers=headers)
                if resp.status_code == 200:
                    return resp.content
            except Exception:
                pass
            await asyncio.sleep(delay * (2**attempt))
        return b""

    transport = httpx.AsyncHTTPTransport(retries=retries)
    async with httpx.AsyncClient(transport=transport, http2=True, timeout=20) as client:
        downloaded = 0
        for pos in range(0, int(size), chunk_size):
            end = min(pos + chunk_size, size)
            chunk = await fetch_chunk(client, pos, end)
            if not chunk:
                break
            if writer:
                writer.write(chunk)
            else:
                buf.write(chunk)
            downloaded += len(chunk)
            if progress:
                await progress(size, downloaded)

    if writer:
        writer.flush()
        writer.close()
        return sink

    buf.seek(0)
    return [buf.getvalue(), downloaded == size]


class method_Rubika:
    def __init__(
        self,
        plat: str = None,
        OrginalAuth: str = None,
        auth: str = None,
        keyAccount: str = None,
        tokenBot: str = None,
        Proxy: Optional[Union[str, List[str]]] = None,
    ):
        self.Plat = plat
        self.Proxy = Proxy
        self.Auth = auth
        self.OrginalAuth = OrginalAuth
        self.keyAccount = keyAccount
        self.Token = tokenBot
        if keyAccount != None:
            self.enc = encoderjson(
                self.Auth if plat == "web" else self.OrginalAuth, self.keyAccount
            )

    async def http(
        self,
        plat: str = None,
        js: dict = None,
        OrginalAuth: str = None,
        auth: str = None,
        key: str = None,
        api_version: str = "6",
        tmp_session: str = None,
    ):
        ence = encoderjson(
            auth=(
                tmp_session
                if tmp_session
                else (auth if plat in ("web") else OrginalAuth)
            ),
            private_key=key if auth else None,
        )
        servers = set_server.get_api_server()
        data_js = {
            "api_version": api_version,
            "auth": (OrginalAuth if plat in ("web") else auth) if auth else None,
            "tmp_session": tmp_session if tmp_session else None,
            "data_enc": ence.encrypt(dumps(js)),
            "sign": (
                None if tmp_session else ence.makeSignFromData(ence.encrypt(dumps(js)))
            ),
        }
        data_headers = (
            {
                "Referer": f'https://{("web" if plat in ("web") else "m" )}.rubika.ir/',
                "Content-Type": "application/json; charset=utf-8",
            }
            if plat in ("web", "pwa")
            else None if auth else None
        )
        if self.Proxy:
            Client__ = HttpClient.get(self.Proxy)
        else:
            Client__ = getClient

        response = await Client__.post(
            servers, data=dumps(data_js), headers=data_headers
        )
        return response.text

    async def httpfiles(self, serversfile: str, dade: dict, head: dict):
        response = await getClient.post(serversfile, data=dade, headers=head)
        return response.text

    async def Rubino(self, api_version: str = "0", auth: str = None, js: dict = None):
        if self.Proxy:
            Client__ = HttpClient.get(self.Proxy)
        else:
            Client__ = getClient

        servers = set_server.get_api_server_rubino()
        response = await Client__.post(
            servers,
            json=js,
            headers={
                "User-Agent": "okhttp/3.12.1",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Content-Type": "application/json; charset=UTF-8",
            },
        )

        return response.text

    async def Bot(self, methodeBot: str, js: dict = None):
        response = await getClient.post(
            f"https://botapi.rubika.ir/v3/{self.Token}/{methodeBot}",
            json=js,
            headers={"Content-Type": "application/json"},
        )

        return response.text

    async def methodsRubika(
        self,
        types: str = None,
        methode: str = None,
        indata: dict = None,
        wn: dict = None,
        downloads: list = None,
        server: str = None,
        podata: bin = None,
        header: dict = None,
    ):
        self.Type: str = types
        self.inData: dict = (
            {"method": methode, "input": indata, "client": wn}
            if types != "Rubino"
            else {
                "auth": self.OrginalAuth,
                "api_version": "0",
                "client": wn,
                "data": indata,
                "method": methode,
            }
        )
        self.download: list = downloads
        self.serverfile: str = str(server)
        self.datafile: bin = podata
        self.headerfile: dict = header

        if self.Type == "json":
            resp_jso = await self.http(
                plat=self.Plat,
                js=self.inData,
                OrginalAuth=self.OrginalAuth,
                auth=self.Auth,
                key=self.keyAccount,
            )
            sendJS = loads(self.enc.decrypt(loads(resp_jso).get("data_enc")))
            if sendJS.get("status") != "OK":
                ErrorRubika(sendJS)
            else:
                return sendJS

        elif self.Type == "file":
            sendFILE = await self.httpfiles(
                serversfile=self.serverfile,
                dade=self.datafile,
                head=self.headerfile,
            )
            return sendFILE

        elif self.Type == "login":
            authrnd = encoderjson.changeAuthType(
                "".join(choices("abcdefghijklmnopqrstuvwxyz", k=32))
            )
            self.enc = encoderjson(auth=authrnd)
            sendLOGIN: dict = loads(
                self.enc.decrypt(
                    loads(
                        await self.http(
                            plat=self.Plat, tmp_session=authrnd, js=self.inData
                        )
                    ).get("data_enc")
                )
            )

            return (
                ErrorRubika(sendLOGIN) if sendLOGIN.get("status") != "OK" else sendLOGIN
            )

        elif self.Type == "download":
            sendDOWNLOAD = await download(
                auth=self.download[0],
                dc_id=self.download[1],
                file_id=self.download[2],
                size=int(self.download[3]),
                access_hash=self.download[4],
                sink=self.download[5],
            )
            return (
                ErrorRubika(sendDOWNLOAD)
                if sendDOWNLOAD.get("status") != "OK"
                else sendDOWNLOAD
            )

        elif self.Type == "Bot":
            sendBot = loads(await self.Bot(methodeBot=methode, js=indata))
            return ErrorRubika(sendBot) if sendBot.get("status") != "OK" else sendBot

        elif self.Type == "Rubino":
            sendRubino = loads(await self.Rubino(js=self.inData))
            if sendRubino.get("status") != "OK":
                ErrorRubika(sendRubino)
            else:
                return sendRubino

    def run(
        self,
        types: str = None,
        methode: str = None,
        indata: dict = None,
        wn: dict = None,
        downloads: list = None,
        server: str = None,
        podata: bin = None,
        header: dict = None,
    ):
        try:
            run_method = self.methodsRubika(
                types=types,
                methode=methode,
                indata=indata,
                wn=wn,
                downloads=downloads,
                server=server,
                podata=podata,
                header=header,
            )
            return loop.run_until_complete(run_method)
        except (httpx.ConnectError, httpx.HTTPError, httpx.TimeoutException):
            raise Connection_Error(
                {
                    "status": "Not_Connected",
                    "detail": "No internet connectivity detected...",
                }
            )

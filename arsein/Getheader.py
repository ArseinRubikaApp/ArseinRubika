import os
import math
import asyncio
import aiohttp
import aiofiles
import base64
from json import loads

from .Encoder import encoderjson
from .PostData import method_Rubika
from .GetDataMethod import GetDataMethod
from .Clien import clien
from .http_client import getClient, loop


def get_ext(path):
    return os.path.splitext(path)[1].lower().strip(".") or "bin"


class Upload:
    def __init__(self, plat=None, OrginalAuth=None, Sh_account=None, keyAccount=None):
        self.Auth = OrginalAuth
        self.Sh_account = Sh_account
        self.keyAccount = keyAccount
        self.Platform = plat
        self.enc = (
            encoderjson(self.Sh_account if plat == "web" else self.Auth, keyAccount)
            if keyAccount
            else None
        )
        self.methodUpload = method_Rubika(
            plat=plat,
            OrginalAuth=self.Auth,
            auth=self.Sh_account,
            keyAccount=keyAccount,
        )
        self.cli = clien(plat).platform
        self.progressFiles = {}
        self.uploadQueue = type(
            "UploadQueue", (object,), {"next": lambda self, msg: None}
        )()

    async def _safe(self, resp):
        try:
            return await resp.json(content_type=None)
        except:
            try:
                t = await resp.text()
                return loads(t) if t else {}
            except:
                return {}

    def _normalize(self, raw):
        if raw is None:
            raise RuntimeError("Init failed: None response")
        if isinstance(raw, dict):
            return raw.get("data") or raw
        raise RuntimeError(f"Init failed: {type(raw).__name__}")

    def _require(self, data, keys):
        for k in keys:
            if not data.get(k):
                raise RuntimeError(f"Missing required field: {k}")
        return data

    def _extract_access_hash_rec(self, res, res_type=None):
        if not isinstance(res, dict):
            return None
        if res_type in ("rubino", "rubika"):
            target_key = "hash_file_receive"
        else:
            target_key = "access_hash_rec"
        paths = [
            ["data", target_key],
            [target_key],
            ["status_det", target_key],
            ["data", "data", target_key],
            ["result", "data", target_key],
        ]
        for p in paths:
            cur = res
            ok = True
            for k in p:
                if isinstance(cur, dict) and k in cur:
                    cur = cur[k]
                else:
                    ok = False
                    break
            if ok:
                return cur
        return None

    def requestSendFile(self, path, *, rubino=False, file_type=None, profile_id=None):
        ext = get_ext(path)
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        if rubino:
            payload = {
                "file_name": os.path.basename(path),
                "file_size": os.path.getsize(path),
                "file_type": file_type,
                "profile_id": profile_id,
            }
            return GetDataMethod(
                target=self.methodUpload.run,
                args=("Rubino", "requestUploadFile", payload, self.cli),
            ).show()
        payload = {
            "file_name": os.path.basename(path),
            "size": os.path.getsize(path),
            "mime": ext,
        }
        return GetDataMethod(
            target=self.methodUpload.run,
            args=("json", "requestSendFile", payload, self.cli),
        ).show()

    def uploadFile(self, path):
        async def wrap():
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=300),
                connector=aiohttp.TCPConnector(force_close=True, limit=10),
            ) as session:
                return await self._uploadRubika(path, session)

        return asyncio.run(wrap())

    def uploadFileRubino(self, path, Type="Picture", profile_id=None):
        async def wrap():
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=300),
                connector=aiohttp.TCPConnector(force_close=True, limit=10),
            ) as session:
                return await self._uploadRubino(path, Type, profile_id, session)

        return asyncio.run(wrap())

    async def _uploadRubika(self, path, session):
        init_raw = self.requestSendFile(path)
        init = self._require(
            self._normalize(init_raw), ["id", "access_hash_send", "upload_url"]
        )
        file_id = init["id"]
        access_hash_send = init["access_hash_send"]
        url = init["upload_url"]
        size = os.path.getsize(path)
        chunk = 131072
        total = math.ceil(size / chunk)
        self.uploadQueue.next(
            {"file_id": file_id, "uploaded_size": 0, "percent": 0, "total_size": size}
        )
        base = {
            "auth": self.Sh_account if self.Platform == "web" else self.Auth,
            "file-id": str(file_id),
            "access-hash-send": access_hash_send,
        }
        access_hash_rec = ""
        reinit = 0
        with open(path, "rb") as f:
            index = 0
            while index < total:
                offset = index * chunk
                f.seek(offset)
                data = f.read(min(chunk, size - offset))
                headers = base.copy()
                headers["part-number"] = str(index + 1)
                headers["total-part"] = str(total)
                headers["chunk-size"] = str(len(data))
                result = None
                for attempt in range(3):
                    try:
                        async with session.post(url, data=data, headers=headers) as r:
                            r.raise_for_status()
                            result = await self._safe(r)
                            break
                    except:
                        await asyncio.sleep(1 * (2**attempt))
                result = result or {}
                acc = self._extract_access_hash_rec(result, "rubika")
                if acc:
                    access_hash_rec = acc
                status = result.get("status")
                if status == "ERROR_TRY_AGAIN" and reinit < 3:
                    init_raw = self.requestSendFile(path)
                    init = self._require(
                        self._normalize(init_raw),
                        ["id", "access_hash_send", "upload_url"],
                    )
                    file_id = init["id"]
                    access_hash_send = init["access_hash_send"]
                    url = init["upload_url"]
                    base["access-hash-send"] = access_hash_send
                    index = 0
                    reinit += 1
                    continue
                uploaded = min((index + 1) * chunk, size)
                percent = min(100, uploaded * 100 // size)
                self.progressFiles[file_id] = {"percent": percent}
                self.uploadQueue.next(
                    {
                        "file_id": file_id,
                        "uploaded_size": uploaded,
                        "percent": percent,
                        "total_size": size,
                    }
                )
                index += 1
        if file_id in self.progressFiles:
            del self.progressFiles[file_id]
        self.uploadQueue.next({"file_id": file_id, "percent": 100, "is_done": True})
        return [init, access_hash_rec]

    async def _uploadRubino(self, path, Type, profile_id, session):
        try:
            decodect = base64.b64decode(path, validate=True)
            async with aiofiles.open(decodect, "rb") as f:
                bytef = await f.read()
        except Exception:
            async with aiofiles.open(path, "rb") as f:
                bytef = await f.read()

        init_raw = self.requestSendFile(
            path, rubino=True, file_type=Type, profile_id=profile_id
        )
        init = self._require(
            self._normalize(init_raw), ["file_id", "hash_file_request", "server_url"]
        )

        file_id = init["file_id"]
        hash_send = init["hash_file_request"]
        url = init["server_url"]

        chunk = 1048576
        size = len(bytef)
        total = int(size / chunk + 1)

        self.uploadQueue.next(
            {"file_id": file_id, "uploaded_size": 0, "percent": 0, "total_size": size}
        )

        index = 0
        last_response = None

        while index < total:
            data = bytef[index * chunk : index * chunk + chunk]

            headers = {
                "auth": str(self.Auth or ""),
                "file-id": str(file_id),
                "total-part": str(total),
                "part-number": str(index + 1),
                "chunk-size": str(len(data)),
                "hash-file-request": str(hash_send),
                "content-type": "application/octet-stream",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.12.1",
            }

            result = None
            for attempt in range(3):
                try:
                    async with session.post(url, data=data, headers=headers) as r:
                        r.raise_for_status()
                        result = await self._safe(r)
                        break
                except:
                    await asyncio.sleep(1 * (2**attempt))

            result = result or {}
            last_response = result

            if result.get("status") == "ERROR_TRY_AGAIN":
                init_raw = self.requestSendFile(
                    path, rubino=True, file_type=Type, profile_id=profile_id
                )
                init = self._require(
                    self._normalize(init_raw),
                    ["file_id", "hash_file_request", "server_url"],
                )
                file_id = init["file_id"]
                hash_send = init["hash_file_request"]
                url = init["server_url"]
                index = 0
                continue

            uploaded = min((index + 1) * chunk, size)
            percent = min(100, uploaded * 100 // size)

            self.progressFiles[file_id] = {"percent": percent}
            self.uploadQueue.next(
                {
                    "file_id": file_id,
                    "uploaded_size": uploaded,
                    "percent": percent,
                    "total_size": size,
                }
            )

            index += 1

        if file_id in self.progressFiles:
            del self.progressFiles[file_id]

        self.uploadQueue.next({"file_id": file_id, "percent": 100, "is_done": True})

        if (
            last_response.get("status") == "OK"
            and last_response.get("status_det") == "OK"
        ):
            return [init, last_response.get("data", {}).get("hash_file_receive")]
        return [init, None]


class UploadBot:
    def __init__(self, url=None, type_file=None, address=None):

        self.files = {
            "file": (
                os.path.basename(address),
                open(address, "rb"),
                (
                    ("audio/ogg" if address.endswith(".ogg") else "audio/mpeg")
                    if type_file == "Music"
                    else "application/octet-stream"
                ),
            )
        }
        self.Url = url

    async def Upload_(self):
        pos_data_file = await getClient.post(self.Url, files=self.files)
        return pos_data_file.json()

    @property
    def File_Id(self):
        return loop.run_until_complete(self.Upload_())

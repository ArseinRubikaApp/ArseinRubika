import httpx
import time
from random import randint
from .Error import Connection_Error


class defaultServer:
    def __init__(self, refresh_interval: int = 900, timeout: float = 1.0):
        self.refresh_interval = refresh_interval
        self.timeout = timeout
        self.last_update = 0
        self.api_servers = []
        self.socket_servers = []
        self.current_index_api = 0
        self.current_index_socket = 0
        self.client = httpx.Client(timeout=timeout)
        self.fallback_servers = [
            "https://messengerg2c1.iranlms.ir",
            "https://messengerg2c2.iranlms.ir",
            "https://messengerg2c3.iranlms.ir",
        ]
        self.online = True

    def warmup(self):
        try:
            r = self.client.get("https://getdcmess.iranlms.ir/")
            r.raise_for_status()
            data = r.json().get("data") or {}
            api = list((data.get("API") or {}).values())
            socket = list((data.get("socket") or {}).values())
            self.api_servers = api if api else self.fallback_servers
            self.socket_servers = socket if socket else []
            self.online = True
        except Exception as err:
            self.api_servers = []
            self.socket_servers = []
            self.online = False
            raise Connection_Error({"status":"Not_Connected","detail":"No internet connectivity detected..."}) from err
        self.last_update = time.time()

    def get_api_server(self):
        if not self.api_servers or (time.time() - self.last_update > self.refresh_interval):
            self.warmup()
        server = self.api_servers[self.current_index_api]
        self.current_index_api = (self.current_index_api + 1) % len(self.api_servers)
        return server

    def get_socket_server(self):
        if not self.socket_servers or (time.time() - self.last_update > self.refresh_interval):
            self.warmup()
        server = self.socket_servers[self.current_index_socket]
        self.current_index_socket = (self.current_index_socket + 1) % len(self.socket_servers)
        return server

    def get_api_server_rubino(self):
        if not self.online or (time.time() - self.last_update > self.refresh_interval):
            self.warmup()
        if not self.online:
            raise Connection_Error({"status":"Not_Connected","detail":"No internet connectivity detected..."})
        server = f"https://rubino{randint(1, 67)}.iranlms.ir/"
        return server


set_server = defaultServer(refresh_interval=86400, timeout=1.0)
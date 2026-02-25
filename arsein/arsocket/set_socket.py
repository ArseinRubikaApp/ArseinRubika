import websocket, json, time, threading
from ..GtM import set_server
from ..Arsein import Messenger
from ..Encoder import encoderjson
from .get_Message import Message_socket
from ..filters.userbot import *


handlers, handlers_on, online = [], [], False
auth, key, enc, change_auth = None, None, None, None
build_deco = False
ping_timer = None
ws = None


def ChatUpdate(filters):

    if not isinstance(filters, Operators):
        filters = Operators(filters)

    def warmup(func):
        global auth, key, enc, build_deco, change_auth
        handlers.append((filters, func))
        if not build_deco:
            print("connecting ...\n")
            auth, key = Messenger._getDataUser()
            enc = encoderjson(encoderjson.changeAuthType(auth), key)
            change_auth = encoderjson.changeAuthType(auth)
            threading.Thread(target=_listen, args=()).start()
            build_deco = True
        return func

    return warmup


def _listen():
    global online, auth, ws, change_auth
    handshake = {
        "api_version": "5",
        "auth": change_auth,
        "data": "",
        "method": "handShake",
    }

    while True:
        try:
            ws = websocket.create_connection(set_server.get_socket_server(), timeout=5)
            ws.settimeout(60)
            ws.send(json.dumps(handshake))
            print("connected\n")
            online = True

            while online:
                try:
                    msg = json.loads(ws.recv())
                    reset_ping()
                    if not msg:
                        print("disconnected\n")
                        online = False
                        ws.close()
                        break

                    elif "type" in msg.keys() and msg.get("type") == "messenger":
                        get_data = enc.decrypt(msg.get("data_enc"))
                        get_obj = Message_socket(json.loads(get_data))
                        for Filt, methods in handlers:
                            if Filt(get_obj):
                                methods(get_obj)

                    elif "status" in msg.keys():
                        print(msg)

                except websocket._exceptions.WebSocketTimeoutException:
                    online = False
                    ws.close()
                    break
                except (websocket.WebSocketConnectionClosedException, OSError):
                    print(
                        f"connection error: WebSocket connection to the server failed."
                    )
                    online = False
                    ws.close()
                    break

        except Exception as e:
            online = False
            if ws:
                ws.close()
                print("disconnected error\n\n")
                build_deco = False
                raise
                break


def reset_ping():
    global ping_timer, ws, online

    if ping_timer:
        ping_timer.cancel()

    def _send():
        global online
        if online and ws:
            try:
                ws.send("{}")
            except:
                online = False

    ping_timer = threading.Timer(10.5, _send)
    ping_timer.start()

import asyncio
import base64
import datetime
import io
import os
import re
import sys
import time
from base64 import b64decode
from json import dump, loads, load
from random import choice, randint
from re import findall

import aiohttp
import httpx
import mutagen
import tinytag
import threading
from mutagen.mp3 import MP3
from tinytag import TinyTag
from .GtM import set_server
from .GetDataMethod import GetDataMethod
from .PostData import method_Rubika

from .Clien import clien
from .Copyright import copyright
from .Device import DeviceTelephone
from .Encoder import encoderjson, getThumbInline
from .Error import AuthError, ErrorMethod, ErrorPrivatyKey, TypeMethodError
from .Getheader import Upload, UploadBot
from .TypeText import parse_text, deleteRSAset, makeJsonResend
from typing import Union, Optional, Any, Dict, List
from .utils import auto_delete_time

handlers, next_offset_id, build_deco = [], None, False

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Messenger:
    def __init__(
        self,
        Sh_account: str = None,
        keyAccount: str = None,
        TypePlat: str = None,
        session_file: str = None,
        Proxy: Optional[Union[str, List[str]]] = None,
    ):

        if session_file:
            with open(
                session_file.rsplit(".", 1)[0] + ".json", "r", encoding="utf-8"
            ) as f:
                data = load(f)

            Sh_account = data.get("Auth")
            keyAccount = data.get("Key")

        keyAccount, Sh_account = deleteRSAset(keyAccount), "".join(
            findall(r"\w{32}", Sh_account)
        )

        self.keyUser, status_platform = keyAccount, ""

        # check Auth Account
        if Sh_account.__len__() != 32:
            raise AuthError("The Auth entered is incorrect")

        # check PrivatyKey Account
        if self.keyUser.startswith("eyJ") or str(TypePlat) in ("web", "pwa"):

            status_platform = TypePlat
            self.cli = clien(TypePlat).platform
            self.keyUser = (
                loads(b64decode(self.keyUser).decode("utf-8"))["d"]
                if self.keyUser.startswith("eyJ")
                else f"-----BEGIN RSA PRIVATE KEY-----\n{self.keyUser}\n-----END RSA PRIVATE KEY-----"
            )

        elif self.keyUser[:3] == "MII" or str(TypePlat) in ("android"):
            status_platform = "android"
            self.cli = clien("android").platform
            self.keyUser = f"-----BEGIN RSA PRIVATE KEY-----\n{self.keyUser}\n-----END RSA PRIVATE KEY-----"
        elif status_platform not in ("android", "web", "pwa"):
            raise ErrorPrivatyKey("Your account private key is incorrect")

        # get Data
        self.servers = set_server.warmup()
        self.CopyRight = copyright.CopyRight
        self.Auth = encoderjson.changeAuthType(Sh_account)
        self.OrginalAuth = Sh_account
        self.TypePlatform = status_platform
        self.handlers = []
        Messenger.OrginalAuth, Messenger.keyUser = self.OrginalAuth, self.keyUser

        self.methods = method_Rubika(
            plat=status_platform,
            OrginalAuth=Sh_account,
            auth=self.Auth,
            keyAccount=self.keyUser,
            Proxy=Proxy,
        )
        self.Upload = Upload(status_platform, self.OrginalAuth, self.Auth, self.keyUser)

    def __repr__(self):
        return f"Auth your Account: {self.Auth} and PrivateKey: {self.keyUser.replace('-----BEGIN RSA PRIVATE KEY-----', '').replace('-----END RSA PRIVATE KEY-----', '')[:50]} ...."

    @property
    def thumb_inline(self):
        return "iVBORw0KGgoAAAANSUhEUgAAACgAAAAoCAYAAACM/rhtAAAHl0lEQVR4nO2Ye3BU1R3Hv+eeu+9HdjebB5uEvCBAIiG0daBijAidtiTWR1leHWqV0mE67R9l0FqJbiLychqZtkwsD1vr1D4itbWt0JGXvCqVIVAq1QZBQyTZrEkgz929e8/5de4SFBwLK49O/uA7e2bvnT3n3M/9/e7ve89Z4KZGkIjAjIYRKBZsCvILJ8PHIwM0eDHYg1/JmP+dGv+n/Xa1uuq7DIWgoA6oZ5BBhMx5W458T/XLH4IYtAhbs29u9vrD2JgwIEuPl1J9fb38vwASwF4PVfHp9Xt043zpr+6tkemJJ20eNvnvG8+AETBlSQ7iZ8Vhvcv++Ppv/WGb0a9q9251z53TBZgxxQ0CpKYgZ3NeEsbxs2urx54qYSsTbhk0qRLRXqFveahFgQS+/stx0ublKuI6tEHv74d6K5/Y/MD3W4xxwaYm/tKcOeK6AhrprKsDMQZ66OGHXY8VHlqq2geX7smxu9+OKeIcOOwuVWl9/RwkKRgz3YFYv5Aaz4Z0jeNx2+f7zQOywbz7bw2N9Y0DISIFdXVIJe2pALLhzKK58c4FoyzRULZdlpyJCexPs+gmq8ojXEXEbcOp41EoDCy9PBO9g/mkkxeJWEJQRoVqS/NDP3u2xXS2L7Tpy/N+l1L4rgR4IXI71n71lhJf/zOZ9vhMkgLRmEwIt4nvsDL2/vv90PokdBtH84kEPuRZcE8YC13jsLo4fEUBWLOmkhaVwuSwmriRhnMD29EWXvqLuYuOh+rq2OUieVlAIiiMQZ7YMGXvmCxR2RMRmiBwj4Mru97pwfPv5WNi6Uz4/dlQCFCgQGcMDAIEwgedHTjw7lGYqmcgt/wWxHsHJOOKsORnmmPvtO399R33VBnprmfsfwKqV4hvsuL4QWnVxkshsqA4zVzZ/68evNI5Az9++mmWE/BcdorO1nY8umottTMzsiaNUbR4nEw724Rjb6vD+L3+ClV9ecBhyW6F5D7O1Tyhi5IhNJ0swMrNP2M+lwX/PHqMunu6jWgnQ55MivFhgM/nQ0XFJPz0qRDuX/4omC+ArNfCzHUixuMUHwZTrh2QVMaYZECbCXObwvjiskXwuSz0+PInsXLVOkaIwcSddB7tvDQxCAYzLX9sGVasrEVlbiFeWFCPBdO+CbKqkEIZ7mtMbLjnp0tJBVDXFbKoDIfiUWztjqNiwjiEw2GsWbOOFRcW4RvzF5LbnQan051sLlca5s+bT8VFxUYfhDvCqJhUjpORI+jUIrCoZpCUKRl2SoCqQtQb5TjZxcGZAq5yRCJdEDRElXdMpQ2bGmC1mCCETDaLxUQbNq5DZeUUCBpAJPIhGFPAmAmRMxEM9Rt2xJOAV6JMKcWnu6U8l+Do01SI4dI2GiMH27Z1FyaWTqNYPM4SehRGDcfjnJWXTaNYLMEYOUnhHFJKEAlAS1DH6R5ETdGUjDglwK39hbLK3I8yu4Z0RUHnuT5UVt2Ogvw8nGo9bVyGTZ5USrOqZyYd/a9/3o5jb73NAIHiwnwUFxeh+fARWJkHzJKBLLUbpfxdGG49XFZXC3h++An4lbCWg1tNHQjl96Ll4AHYF8zGi7/dRLW1K9DV1Q1JEofebIY0VqxMoqJ8PPkz0rFiRS1sNivbe+AIVeXNwN3uM2yWpQVxJIavwa49gjapSSh27IoFUJTuxYmX/4E99+5D1V2V2LHzL0zTNCiKAuPbuKDZbDJSysxmc/IuX929nwa278Mz47zIZJ0wwYoeaU6pSC4LWIe65HtYGl7AGRy6xjq6FcbLp9Mjz/0cPzjTjrvvryGHw5EMg6peOt3g4CD9ZsurePO5p9BQDpgGiA1JM0szG7eR2oImpQgygkBfnISbE80uIEvNWATst6H2Jxuxek0DfBmZlDTpC8sKBnCuoqMjjLmBNjz7JQf6hYpYO5HaZpEyzpnhrNcNkMyKg6aNZuK+XCFHOTlnKvoPvoWBnafQ0dqDxH9aP3phMcaQEAkQhshq8uCPQ3bcXqxgakBCBOJg/oTuDNvUznZuuWYf/HdTmXFhJmYXNWrfLR1UCjMsiEkZD3fLY7WbMXCyC1aHjbmcTrhcTnK7XWSxmlE2oYQWf3sxXE47jnyQwOI/xdE5xIRJgNxOZh0oEL19xdSQjHkoxK4a8PzKl/Dyjx55Xn2j5QuyrXOL1Z/GI3uO8qH2iO4JeEnoetLjjKIwAjg4NEgTJ43HqtVPQDVz5GXY5ckeiK0tuup0mJRT/bYXtoUzPzelsfnF5ONwlXuVSxQMfrw7W9T82qyye+5rdllGUU11kLxpBZrHWSA9rgL6qLnzZUb6GJHuKdC+Vj2XrJY8mn9ryRsdqyvvujBPUxDXvOO7RKFQSDH2E8ZxKWDOzi5e9uADS8JZ/hJyO/INwITHlQSVac78hMOSSznZZbRw4aL3vO7AEuD8WAqCJ3eEN0pJSKNMAcybNy+Q6S9a73GP1rzuZPR0j6tAeN1F5E0bHc3OKl4XDAZ9Rl9jRNNFmbjRYhc7QMAfmOxNy3nFgPS6R5PXk78lNzN34md1i+suImMJ+PGz5PUGbvP5Mqde1GXE/AWifMIRPnk+YsQvjuhN3dRN3RRGvv4LqYA1uYzHX8wAAAAASUVORK5CYII="

    @classmethod
    def _getDataUser(cls):
        return cls.OrginalAuth, cls.keyUser

    # MentionText Mono Bold Italic Strike Underline Spoiler hyperlink
    def sendMessage(
        self,
        guid: str,
        text: str,
        link: str = None,
        Guid_mention: str = None,
        message_id: str = None,
    ):
        def check_marks(t):
            return any(
                m in t for m in ["@@", "##", "$$", "**", "~~", "__", "||", "|", "``"]
            )

        def texts(t):
            return re.sub(
                r"\s+", " ", re.sub(r"(?:\$\$|\*\*|~~|__|\|\||@@|##|``)", "", t)
            ).strip()

        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "sendMessage",
                {
                    "object_guid": guid,
                    "rnd": f"{randint(100000, 999999)}",
                    "text": texts(text) if check_marks(text) else text,
                    "metadata": (
                        {
                            "meta_data_parts": parse_text(
                                text,
                                guid=Guid_mention if Guid_mention else None,
                                link=link if link else None,
                            )
                        }
                        if check_marks(text)
                        else None
                    ),
                    "reply_to_message_id": message_id,
                },
                self.cli,
            ),
        ).show()

    def editMessage(self, guid: str, new: str, message_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editMessage",
                {"message_id": message_id, "object_guid": guid, "text": new},
                self.cli,
            ),
        ).show()

    def deleteMessages(self, guid: str, message_ids: str, All: bool = False):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "deleteMessages",
                {
                    "object_guid": guid,
                    "message_ids": message_ids,
                    "type": "Global" if All else "Local",
                },
                self.cli,
            ),
        ).show()

    def getMessagefilter(self, guid: str, filter_whith: str, sort: str = "FromMax"):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "getMessages",
                    {
                        "filter_type": filter_whith,
                        "max_id": "NaN",
                        "object_guid": guid,
                        "sort": sort,
                    },
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("messages")
        )

    def getMessages(self, guid: str, min_id: int):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "getMessagesInterval",
                    {"object_guid": guid, "middle_message_id": min_id},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("messages")
        )

    def getMessagesbySort(self, guid: str, message_id: list, Type: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getMessages",
                {
                    "object_guid": guid,
                    "sort": "FromMax" if Type == "max" else "FromMin",
                    "max_id" if Type == "max" else "min_id": message_id,
                },
                self.cli,
            ),
        ).show()

    def searchMessages(self, guid: str, text: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "searchChatMessages",
                {
                    "search_text": text.replace("#", ""),
                    "type": "Hashtag" if text.startswith("#") else "Text",
                    "object_guid": guid,
                },
                self.cli,
            ),
        ).show()

    # Hashtag #Text.....

    def getChats(self, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getChats", {"start_id": start_id}, self.cli),
        ).show()

    def getMapView(self, latitude, longitude):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getMapView",
                {"location": {"latitude": latitude, "longitude": longitude}},
                self.cli,
            ),
        ).show()

    def sendMap(self, guid: str, latitude: float, longitude: float):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "sendMessage",
                {
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "location": {"latitude": latitude, "longitude": longitude},
                },
                self.cli,
            ),
        ).show()

    def getMessagesUpdates(self, guid: str):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getMessagesUpdates",
                {"object_guid": guid, "state": state},
                self.cli,
            ),
        ).show()

    @property
    def getChatsUpdate(self):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getChatsUpdates", {"state": state}, self.cli),
        ).show()

    def deleteUserChat(self, user_guid: str, last_message: list):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "deleteUserChat",
                {"last_deleted_message_id": last_message, "user_guid": user_guid},
                self.cli,
            ),
        ).show()

    def startSupperBot(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "sendMessage",
                {"object_guid": guid, "rnd": randint(100000, 999999), "text": "/start"},
                self.cli,
            ),
        ).show()

    def stoptSupperBot(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "stopBot", {"bot_guid": guid}, self.cli),
        ).show()

    def getBotInfo(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getBotInfo", {"bot_guid": guid}, self.cli),
        ).show()

    def sendChatActivity(self, user_guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "sendChatActivity",
                {"object_guid": user_guid, "activity": "Typing"},
                self.cli,
            ),
        ).show()

    def getInfoByUsername(self, username: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getObjectByUsername",
                {"username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def banGroupMember(self, guid_gap: str, user_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "banGroupMember",
                {"group_guid": guid_gap, "member_guid": user_id, "action": "Set"},
                self.cli,
            ),
        ).show()

    def unbanGroupMember(self, guid_gap: str, user_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "banGroupMember",
                {"group_guid": guid_gap, "member_guid": user_id, "action": "Unset"},
                self.cli,
            ),
        ).show()

    def banChannelMember(self, guid_channel: str, user_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "banChannelMember",
                {"channel_guid": guid_channel, "member_guid": user_id, "action": "Set"},
                self.cli,
            ),
        ).show()

    def unbanChannelMember(self, guid_channel: str, user_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "banChannelMember",
                {
                    "channel_guid": guid_channel,
                    "member_guid": user_id,
                    "action": "Unset",
                },
                self.cli,
            ),
        ).show()

    def getGroupMentionList(self, guid_group: str, text: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getGroupMentionList",
                {"group_guid": guid_group, "search_mention": text},
                self.cli,
            ),
        ).show()

    def shaireContect(
        self, guid: str, phone_number: str, first_name: str, last_name: str = None
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "sendMessage",
                {
                    "object_guid": "u09pbi05e46fa119166489d14a3f0562",
                    "type": "ContactMessage",
                    "message_contact": {
                        "first_name": first_name,
                        "last_name": last_name,
                        "phone_number": f"98{phone_number[1:]}",
                        "user_guid": guid,
                    },
                    "rnd": randint(100000, 999999),
                },
                self.cli,
            ),
        ).show()

    # report account or channell or group
    def report(self, guid: str, reportType: int):
        if not reportType in [102, 101, 104, 103, 105, 106, 100]:
            raise ErrorMethod("the numerTypeReport is wrong! ")
        else:
            return GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "reportObject",
                    {
                        "object_guid": guid,
                        "report_type": reportType,
                        "report_type_object": "Object",
                    },
                    self.cli,
                ),
            ).show()

    def reportPost(self, guid: str, reportType: int, message_id: str):
        if not reportType in [102, 101, 104, 103, 105, 106, 100]:
            raise ErrorMethod("the numerTypeReport is wrong ! ")
        else:
            return GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "reportObject",
                    {
                        "object_guid": guid,
                        "message_id": message_id,
                        "report_type": reportType,
                        "report_type_object": "Message",
                    },
                    self.cli,
                ),
            ).show()

    def otherReport(self, TYPE: str, guid: str, text: str, message_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "reportObject",
                {
                    "object_guid": guid,
                    "message_id": message_id if message_id else None,
                    "report_type": 100,
                    "report_type_object": "Message" if TYPE == "message" else "Object",
                    "report_description": text,
                },
                self.cli,
            ),
        ).show()

    def getbanGroupUsers(self, guid_gap: str, text: str = None, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getBannedGroupMembers",
                {"group_guid": guid_gap, "search_text": text, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def getbanChannelUsers(
        self, guid_channel: str, text: str = None, start_id: str = None
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getBannedChannelMembers",
                {
                    "channel_guid": guid_channel,
                    "search_text": text,
                    "start_id": start_id,
                },
                self.cli,
            ),
        ).show()

    def getGroupInfo(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getGroupInfo", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getChannelInfo(self, guid_channel: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getChannelInfo", {"channel_guid": guid_channel}, self.cli),
        ).show()

    def addMemberGroup(self, guid_gap: str, user_ids: list):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "addGroupMembers",
                {"group_guid": guid_gap, "member_guids": user_ids},
                self.cli,
            ),
        ).show()

    def addMemberChannel(self, guid_channel: str, user_ids: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "addChannelMembers",
                {"channel_guid": guid_channel, "member_guids": user_ids},
                self.cli,
            ),
        ).show()

    def getGroupAdmins(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getGroupAdminMembers", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getChannelAdmins(self, guid_channel: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getChannelAdminMembers",
                {"channel_guid": guid_channel},
                self.cli,
            ),
        ).show()

    def AddNumberPhone(self, first_num: str, numberPhone: str, last_num: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "addAddressBook",
                {
                    "phone": numberPhone.replace("+98", ""),
                    "first_name": first_num,
                    "last_name": last_num,
                },
                self.cli,
            ),
        ).show()

    def getMessagesInfo(self, guid: str, message_ids: list):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getMessagesByID",
                {"object_guid": guid, "message_ids": message_ids},
                self.cli,
            ),
        ).show()

    def getGroupMembers(self, guid_gap, text=None, start_id=None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getGroupAllMembers",
                {"group_guid": guid_gap, "search_text": text, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def getChannelMembers(
        self, channel_guid: str, text: str = None, start_id: str = None
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getChannelAllMembers",
                {
                    "channel_guid": channel_guid,
                    "search_text": text.replace("@", ""),
                    "start_id": start_id,
                },
                self.cli,
            ),
        ).show()

    def lockGroup(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setGroupDefaultAccess",
                {"access_list": ["AddMember"], "group_guid": guid_gap},
                self.cli,
            ),
        ).show()

    def unlockGroup(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setGroupDefaultAccess",
                {"access_list": ["SendMessages", "AddMember"], "group_guid": guid_gap},
                self.cli,
            ),
        ).show()

    def getGroupAccess(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getGroupDefaultAccess", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getGroupLink(self, guid_gap):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getGroupLink", {"group_guid": guid_gap}, self.cli),
        ).show()

    def GroupOnlineCount(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getGroupOnlineCount", {"group_guid": guid_gap}, self.cli),
        ).show()

    def getChannelLink(self, guid_channel: str):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "getChannelLink",
                    {"channel_guid": guid_channel},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("join_link")
        )

    def changeGroupLink(self, guid_gap: str):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=("json", "setGroupLink", {"group_guid": guid_gap}, self.cli),
            )
            .show()
            .get("data")
            .get("join_link")
        )

    def changeChannelLink(self, guid_channel: str):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "setChannelLink",
                    {"channel_guid": guid_channel},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("join_link")
        )

    def setGroupTimer(self, guid_gap: str, time: int):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editGroupInfo",
                {
                    "group_guid": guid_gap,
                    "slow_mode": time,
                    "updated_parameters": ["slow_mode"],
                },
                self.cli,
            ),
        ).show()

    def limit_storage_Group(self, guid_gap: str, active: bool):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editGroupInfo",
                {
                    "group_guid": guid_gap,
                    "is_restricted_content": active,
                    "updated_parameters": ["is_restricted_content"],
                },
                self.cli,
            ),
        ).show()

    def limit_storage_Channel(self, guid_channel: str, active: bool):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editChannelInfo",
                {
                    "channel_guid": guid_channel,
                    "is_restricted_content": active,
                    "updated_parameters": ["is_restricted_content"],
                },
                self.cli,
            ),
        ).show()

    def getGroupMessageReadParticipants(self, guid_gap: str, message_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getGroupMessageReadParticipants",
                {"group_guid": guid_gap, "message_id": message_id},
                self.cli,
            ),
        ).show()

    def setGroupAdmin(self, guid_gap: str, guid_member: str, access_admin: list = None):
        access_admin = (
            access_admin
            if access_admin != None
            else [
                "ChangeInfo",
                "SetJoinLink",
                "SetAdmin",
                "BanMember",
                "DeleteGlobalAllMessages",
                "PinMessages",
                "SetMemberAccess",
            ]
        )
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setGroupAdmin",
                {
                    "group_guid": guid_gap,
                    "access_list": access_admin,
                    "action": "SetAdmin",
                    "member_guid": guid_member,
                },
                self.cli,
            ),
        ).show()

    def deleteGroupAdmin(self, guid_gap: str, guid_admin: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setGroupAdmin",
                {
                    "group_guid": guid_gap,
                    "action": "UnsetAdmin",
                    "member_guid": guid_admin,
                },
                self.cli,
            ),
        ).show()

    def deleteGroup(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "removeGroup", {"group_guid": guid_gap}, self.cli),
        ).show()

    def setChannelAdmin(
        self, guid_channel: str, guid_member: str, access_admin: list = None
    ):
        access_admin = (
            access_admin
            if access_admin != None
            else [
                "SetAdmin",
                "SetJoinLink",
                "AddMember",
                "DeleteGlobalAllMessages",
                "EditAllMessages",
                "SendMessages",
                "PinMessages",
                "ViewAdmins",
                "ViewMembers",
                "ChangeInfo",
            ]
        )
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setChannelAdmin",
                {
                    "channel_guid": guid_channel,
                    "access_list": access_admin,
                    "action": "SetAdmin",
                    "member_guid": guid_member,
                },
                self.cli,
            ),
        ).show()

    def deleteChannelAdmin(self, guid_channel: str, guid_admin: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setChannelAdmin",
                {
                    "channel_guid": guid_channel,
                    "action": "UnsetAdmin",
                    "member_guid": guid_admin,
                },
                self.cli,
            ),
        ).show()

    def getStickersByEmoji(self, emojee: str):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "getStickersByEmoji",
                    {"emoji_character": emojee, "suggest_by": "All"},
                    self.cli,
                ),
            )
            .show()
            .get("data")
        )

    def searchStickerSets(self, text: str, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "searchStickerSets",
                {"search_text": text, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def getTrendStickerSets(self, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getTrendStickerSets", {"start_id": start_id}, self.cli),
        ).show()

    def getStickerSetByID(self, sticker_set_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getStickerSetByID",
                {"sticker_set_id": sticker_set_id},
                self.cli,
            ),
        ).show()

    def actionStickerSet(self, action: int, sticker_set_id: str = None):
        Action = ["Add", "Remove"]
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "actionOnStickerSet",
                {"sticker_set_id": sticker_set_id, "action": Action[action]},
                self.cli,
            ),
        ).show()

    def activenotification(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setActionChat",
                {"action": "Unmute", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def offnotification(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setActionChat",
                {"action": "Mute", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def sendPoll(self, guid: str, question: str, options: list):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "createPoll",
                {
                    "object_guid": guid,
                    "options": options,
                    "rnd": f"{randint(100000, 999999999)}",
                    "question": question,
                    "type": "Regular",
                    "is_anonymous": False,
                    "allows_multiple_answers": True,
                },
                self.cli,
            ),
        ).show()

    def sendPollExam(
        self,
        guid: str,
        question: str,
        options: list,
        explanation: str,
        correct_option_index: int,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "createPoll",
                {
                    "object_guid": guid,
                    "options": options,
                    "rnd": f"{randint(100000, 999999999)}",
                    "question": question,
                    "type": "Quiz",
                    "is_anonymous": False,
                    "allows_multiple_answers": False,
                    "explanation": explanation,
                    "correct_option_index": correct_option_index,
                },
                self.cli,
            ),
        ).show()

    def getPollStatus(self, poll_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getPollStatus", {"poll_id": poll_id}, self.cli),
        ).show()

    def getVoters(self, poll_id: str, index: Union[str, int]):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getPollOptionVoters",
                {"poll_id": poll_id, "selection_index": index},
                self.cli,
            ),
        ).show()

    def votePoll(self, poll_id: str, index: Union[str, int]):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "votePoll",
                {"poll_id": poll_id, "selection_index": index},
                self.cli,
            ),
        ).show()

    def forwardMessages(self, From: str, message_ids: Union[str, int, list], to: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "forwardMessages",
                {
                    "from_object_guid": From,
                    "message_ids": message_ids,
                    "rnd": f"{randint(100000, 999999999)}",
                    "to_object_guid": to,
                },
                self.cli,
            ),
        ).show()

    def VisitChatGroup(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editGroupInfo",
                {
                    "chat_history_for_new_members": "Visible",
                    "group_guid": guid_gap,
                    "updated_parameters": ["chat_history_for_new_members"],
                },
                self.cli,
            ),
        ).show()

    def HideChatGroup(self, guid_gap: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editGroupInfo",
                {
                    "chat_history_for_new_members": "Hidden",
                    "group_guid": guid_gap,
                    "updated_parameters": ["event_messages"],
                },
                self.cli,
            ),
        ).show()

    def pin(self, guid: str, message_id: Union[str, int]):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setPinMessage",
                {"action": "Pin", "message_id": message_id, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def unpin(self, guid: str, message_id: Union[str, int]):
        return self.methods.run(
            "json",
            methode="setPinMessage",
            indata={"action": "Unpin", "message_id": message_id, "object_guid": guid},
            wn=self.cli,
        )

    @property
    def logout(self):
        return GetDataMethod(
            target=self.methods.run, args=("json", "logout", {}, self.cli)
        ).show()

    def joinGroup(self, link: str):
        hashLink = link.split("/")[-1]
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "joinGroup", {"hash_link": hashLink}, self.cli),
        ).show()

    def getJoinLinkUserJoined(
        self, object_guid: str, join_link: str, start_id: str = None
    ):
        hashLink = join_link.split("/")[-1]
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getJoinLinkUserJoined",
                {
                    "object_guid": object_guid,
                    "join_link": hashLink,
                    "start_id": start_id,
                },
                self.cli,
            ),
        ).show()

    def joinChannelAll(self, guid: str):
        def check_(v):
            return (
                "link"
                if re.fullmatch(r"https?://rubika\.ir/joinc/\w+", v)
                else (
                    "@"
                    if re.fullmatch(r"@\w+", v)
                    else "guid" if v.startswith("c0") else "invalid"
                )
            )

        guid = (
            guid
            if guid.startswith("c0")
            else (
                guid.split("/")[-1]
                if "/" in guid
                else self.getInfoByUsername(guid.replace("@", ""))["data"]["channel"][
                    "channel_guid"
                ]
            )
        )
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "joinChannelByLink" if check_ == "link" else "joinChannelAction",
                (
                    {"hash_link": guid}
                    if check_ == "link"
                    else {"action": "Join", "channel_guid": guid}
                ),
            ),
        ).show()

    def joinChannelByLink(self, link: str):
        hashLink = link.split("/")[-1]
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "joinChannelByLink", {"hash_link": hashLink}, self.cli),
        ).show()

    def joinChannelByID(self, ide: str):
        IDE = ide.replace("@", "")
        GUID = self.getInfoByUsername(IDE)["data"]["channel"]["channel_guid"]
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "joinChannelAction",
                {"action": "Join", "channel_guid": GUID},
                self.cli,
            ),
        ).show()

    def joinChannelByGuid(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "joinChannelAction",
                {"action": "Join", "channel_guid": guid},
                self.cli,
            ),
        ).show()

    def leaveGroup(self, guid_gap: str):
        guid = guid if guid.startswith("g0") else guid.split("/")[-1]
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "leaveGroup", {"group_guid": guid}, self.cli),
        ).show()

    def leaveChannel(self, guid_channel: str):
        guid_channel = (
            self.joinChannelByLink(guid_channel)["data"]["chat_update"]["object_guid"]
            if guid_channel.startswith("https://rubika.ir/joinc/")
            else (
                self.joinChannelByID(guid_channel)["data"]["chat_update"]["object_guid"]
                if guid_channel.startswith("@")
                else guid_channel
            )
        )
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "joinChannelAction",
                {"action": "Leave", "channel_guid": guid_channel},
                self.cli,
            ),
        ).show()

    def EditNameGroup(self, groupgu: str, namegp: str):
        biogp = self.getGroupInfo(groupgu).get("data").get("group").get("description")
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editGroupInfo",
                {
                    "group_guid": groupgu,
                    "title": namegp,
                    "description": biogp,
                    "updated_parameters": ["title", "description"],
                },
                self.cli,
            ),
        ).show()

    def EditBioGroup(self, groupgu: str, biogp: str):
        namegp = self.getGroupInfo(groupgu).get("data").get("group").get("group_title")
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editGroupInfo",
                {
                    "group_guid": groupgu,
                    "title": namegp,
                    "description": biogp,
                    "updated_parameters": ["title", "description"],
                },
                self.cli,
            ),
        ).show()

    def block(self, guid_user: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setBlockUser",
                {"action": "Block", "user_guid": guid_user},
                self.cli,
            ),
        ).show()

    def unblock(self, guid_user: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setBlockUser",
                {"action": "Unblock", "user_guid": guid_user},
                self.cli,
            ),
        ).show()

    # startVoiceChat channel or group
    def startVoiceChat(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "createGroupVoiceChat", {"chat_guid": guid}, self.cli),
        ).show()

    def addUserContact(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setAskSpamAction",
                {"object_guid": guid, "action": "AddToContact"},
                self.cli,
            ),
        ).show()

    def getVoiceChatId(self, guid: str):
        return (
            self.getGroupInfo(guid)["data"]["chat"]["group_voice_chat_id"]
            if guid.startswith("g0")
            else (
                self.getGroupInfo(guid)["data"]["chat"]["group_voice_chat_id"]
                if guid.startswith("c0")
                else "error only guid channel or group"
            )
        )

    def joinGroupVoiceChat(self, guid_g_ch: str, guid_user: str):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                f"joinGroupVoiceChat",
                {
                    "chat_guid": guid_g_ch,
                    "voice_chat_id": voice_chat_id,
                    "sdp_offer_data": sdp_offer_data,
                    "self_object_guid": guid_user,
                },
                self.cli,
            ),
        ).show()

    def getGroupVoiceChat(self, guid: str):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                f"getGroupVoiceChat",
                {"voice_chat_id": voice_chat_id, "chat_guid": guid},
                self.cli,
            ),
        ).show()

    # getGroupVoiceChatParticipants channel or group
    def getGroupVoiceChatParticipants(self, guid: str, start_id: str = None):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                f"getGroupVoiceChatParticipants",
                {
                    f"chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "start_id": start_id,
                },
                self.cli,
            ),
        ).show()

    # *
    #  join_muted = true  Members can speak join_muted = false Members can not speak  channel or group
    def editVoiceChat(self, guid: str, bol: bool = True):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setGroupVoiceChatSetting",
                {
                    "chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "join_muted": bol,
                    "updated_parameters": ["join_muted"],
                },
                self.cli,
            ),
        ).show()

    # changeTitleVoiceChat channel or group
    def changeTitleVoiceChat(self, guid: str, title: str):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setGroupVoiceChatSetting",
                {
                    f"chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "title": title,
                    "updated_parameters": ["title"],
                },
                self.cli,
            ),
        ).show()

    # finishVoiceChat channel or group
    def finishVoiceChat(self, guid: str):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "discardGroupVoiceChat",
                {"chat_guid": guid, "voice_chat_id": voice_chat_id},
                self.cli,
            ),
        ).show()

    # leaveGroupVoiceChat group or channel
    def leaveGroupVoiceChat(self, guid: str):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "leaveGroupVoiceChat",
                {"chat_guid": guid, "voice_chat_id": voice_chat_id},
                self.cli,
            ),
        ).show()

    def getDisplayAsInGroupVoiceChat(self, guid: str, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getDisplayAsInGroupVoiceChat",
                {"chat_guid": guid, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def sendGroupVoiceChatActivity(
        self, guid: str, guiduser: str = None, activity: str = "Speaking"
    ):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getGroupVoiceChatActivity",
                {
                    "group_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "activity": activity,
                    "participant_object_guid": guiduser,
                },
                self.cli,
            ),
        ).show()

    def getGroupVoiceChatUpdates(self, guid: str):
        voice_chat_id, state = self.getVoiceChatId(guid), str(
            round(datetime.datetime.today().timestamp()) - 200
        )
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getGroupVoiceChatUpdates",
                {"chat_guid": guid, "voice_chat_id": voice_chat_id, "state": state},
                self.cli,
            ),
        ).show()

    def setGroupVoiceChatState(self, guid: str, state: bool, guid_member: str = None):
        voice_chat_id = self.getVoiceChatId(guid)
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setGroupVoiceChatState",
                {
                    "chat_guid": guid,
                    "voice_chat_id": voice_chat_id,
                    "action": "Mute" if state == False else "Unmute",
                    "participant_object_guid": guid_member,
                },
                self.cli,
            ),
        ).show()

    def getUserInfo(self, guid_user: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getUserInfo", {"user_guid": guid_user}, self.cli),
        ).show()

    def getUserInfoByIDE(self, IDE_user: str):
        guiduser = self.getInfoByUsername(IDE_user.replace("@", ""))["data"]["user"][
            "user_guid"
        ]
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getUserInfo", {"user_guid": guiduser}, self.cli),
        ).show()

    def seeGroupbyLink(self, link_gap: str):
        link = link_gap.replace("https://rubika.ir/joing/", "")
        return (
            GetDataMethod(
                target=self.methods.run,
                args=("json", "groupPreviewByJoinLink", {"hash_link": link}, self.cli),
            )
            .show()
            .get("data")
        )

    def seeChannelbyLink(self, link_channel: str):
        link = link_channel.replace("https://rubika.ir/joinc/", "")
        return (
            GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "channelPreviewByJoinLink",
                    {"hash_link": link},
                    self.cli,
                ),
            )
            .show()
            .get("data")
        )

    def getAvatars(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getAvatars", {"object_guid": guid}, self.cli),
        ).show()

    def uploadAvatar_replay(self, files_ide: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "uploadAvatar",
                {
                    "thumbnail_file_id": files_ide,
                    "main_file_id": files_ide,
                },
                self.cli,
            ),
        ).show()

    def uploadAvatar(self, main: str, thumbnail: str = None):
        mainID = str(self.Upload.uploadFile(main)[0]["id"])
        thumbnailID = str(self.Upload.uploadFile(thumbnail or main)[0]["id"])
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "uploadAvatar",
                {
                    "thumbnail_file_id": thumbnailID,
                    "main_file_id": mainID,
                },
                self.cli,
            ),
        ).show()

    def removeAvatar(self, guid: str):
        avatar_id = self.getAvatars(guid)["data"]["avatars"][0]["avatar_id"]
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "deleteAvatar",
                {"object_guid": guid, "avatar_id": avatar_id},
                self.cli,
            ),
        ).show()

    def removeAllAvatars(self, guid: str):
        while 1:
            try:
                avatar = self.getAvatars(guid)["data"]["avatars"]
                if avatar != []:
                    avatar_id = self.getAvatars(guid)["data"]["avatars"][0]["avatar_id"]
                    GetDataMethod(
                        target=self.methods.run,
                        args=(
                            "json",
                            "deleteAvatar",
                            {"object_guid": guid, "avatar_id": avatar_id},
                            self.cli,
                        ),
                    ).show()
                else:
                    return "Ok remove Avatars"
                    break
            except:
                continue

    def Devicesrubika(self, service_guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getServiceInfo", {"service_guid": service_guid}, self.cli),
        ).show()

    def getPaymentInfo(self, payment_id: Union[str, int]):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getPaymentInfo", {"payment_id": payment_id}, self.cli),
        ).show()

    def deleteChatHistory(self, guid: str, last_message_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "deleteChatHistory",
                {"last_message_id": last_message_id, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def addFolder(
        self,
        Name="Arsein",
        include_chat: list[str] = None,
        include_object: list[str] = None,
        exclude_chat: list[str] = None,
        exclude_object: list[str] = None,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "addFolder",
                {
                    "exclude_chat_types": exclude_chat,
                    "exclude_object_guids": exclude_object,
                    "include_chat_types": include_chat,
                    "include_object_guids": include_object,
                    "is_add_to_top": True,
                    "name": Name,
                },
                self.cli,
            ),
        ).show()

    def deleteFolder(self, folder_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "deleteFolder", {"folder_id": folder_id}, self.cli),
        ).show()

    def addGroup(self, title: str, guidsUser: list):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "addGroup",
                {"member_guids": guidsUser, "title": title},
                self.cli,
            ),
        ).show()

    def deleteGroup(self, guid_group: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "deleteNoAccessGroupChat",
                {"group_guid": guid_group},
                self.cli,
            ),
        ).show()

    def addChannel(self, title: str, typeChannell: int, bio: str, guidsUser: list):
        TypeChannell = ["Private", "Public"]
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "addChannel",
                {
                    "channel_type": TypeChannell[typeChannell],
                    "description": bio,
                    "member_guids": guidsUser,
                    "title": title,
                },
                self.cli,
            ),
        ).show()

    def editUser(self, first_name: str = None, last_name: str = None, bio: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "updateProfile",
                {
                    "bio": bio,
                    "first_name": first_name,
                    "last_name": last_name,
                    "updated_parameters": ["first_name", "last_name", "bio"],
                },
                self.cli,
            ),
        ).show()

    def editUsername(self, username: str):
        ide = username.replace("@", "")
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "updateUsername", {"username": ide}, self.cli),
        ).show()

    def editDate_birth(self, birth_date: str):  # "2026-01-27"
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "updateProfile",
                {"birth_date": birth_date, "updated_parameters": ["birth_date"]},
                self.cli,
            ),
        ).show()

    def Postion(self, guid, guiduser):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "requestChangeObjectOwner",
                {"new_owner_user_guid": guiduser, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def getPostion(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getPendingObjectOwner", {"object_guid": guid}, self.cli),
        ).show()

    def AcceptPostion(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "replyRequestObjectOwner",
                {"action": "Accept", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def RejectPostion(self, guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "replyRequestObjectOwner",
                {"action": "Reject", "object_guid": guid},
                self.cli,
            ),
        ).show()

    def sendLive(self, guid: str, titlelive: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "sendLive",
                {
                    "object_guid": guid,
                    "title": titlelive,
                    "device_type": "Software",
                    "thumb_inline": self.thumb_inline,
                    "rnd": randint(100000, 999999),
                },
                self.cli,
            ),
        ).show()

    @property
    def ClearAccounts(self):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "terminateOtherSessions", {}, self.cli),
        ).show()

    @property
    def DeleteAccount(self):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "requestDeleteAccount", {}, self.cli),
        ).show()

    def selectionClearAccount(self, session_key: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "terminateSession", {"session_key": session_key}, self.cli),
        ).show()

    def HidePhone(self, **kwargs: dict):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setSetting",
                {"settings": kwargs, "update_parameters": ["show_my_phone_number"]},
                self.cli,
            ),
        ).show()

    def HideOnline(self, **kwargs: dict):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setSetting",
                {"settings": kwargs, "update_parameters": ["show_my_last_online"]},
                self.cli,
            ),
        ).show()

    def search_inaccount(self, text: str):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=(
                    "json",
                    "searchGlobalMessages",
                    {"search_text": text, "start_id": None, "type": "Text"},
                    self.cli,
                ),
            )
            .show()
            .get("data")
            .get("messages")
        )

    def search_inrubika(self, text: str):
        return (
            GetDataMethod(
                target=self.methods.run,
                args=("json", "searchGlobalObjects", {"search_text": text}, self.cli),
            )
            .show()
            .get("data")
            .get("objects")
        )

    def getAbsObjects(self, guids: list[str]):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getAbsObjects", {"objects_guids": guids}, self.cli),
        ).show()

    def Infolinkpost(self, linkpost: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getLinkFromAppUrl", {"app_url": linkpost}, self.cli),
        ).show()

    # THERE IS A PROBLEM RIGHT NOW.
    # def setAutoDelete(self, chat_guid: str, object_guids: list, auto_delete_value: str):
    #     self.cli = clien("android").platform
    #     return GetDataMethod(
    #         target=self.methods.run,
    #         args=("json", "setAutoDelete", {"object_guid": chat_guid,"object_guids": object_guids,"auto_delete": auto_delete_value}, self.cli),
    #     ).show()

    def addToMyGifSet(self, guid: str, message_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "addToMyGifSet",
                {"message_id": message_id, "object_guid": guid},
                self.cli,
            ),
        ).show()

    def deleteMyGifSet(self, file_id: Union[str, int, list]):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "removeFromMyGifSet", {"file_id": file_id}, self.cli),
        ).show()

    def getContactsLastOnline(self, user_guids: list[str]):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getContactsLastOnline",
                {"user_guids": user_guids},
                self.cli,
            ),
        ).show()

    def SignMessageChannel(self, guid_channel: str, sign: bool = False):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editChannelInfo",
                {
                    "channel_guid": guid_channel,
                    "sign_messages": sign,
                    "updated_parameters": ["sign_messages"],
                },
                self.cli,
            ),
        ).show()

    @property
    def ActiveContectJoin(self):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setSetting",
                {
                    "settings": {"can_join_chat_by": "MyContacts"},
                    "update_parameters": ["can_join_chat_by"],
                },
                self.cli,
            ),
        ).show()

    @property
    def ActiveEverybodyJoin(self):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setSetting",
                {
                    "settings": {"can_join_chat_by": "Everybody"},
                    "update_parameters": ["can_join_chat_by"],
                },
                self.cli,
            ),
        ).show()

    def CalledBy(self, typeCall: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setSetting",
                {
                    "settings": {"can_called_by": typeCall},
                    "update_parameters": ["can_called_by"],
                },
                self.cli,
            ),
        ).show()

    def changeChannelID(self, guid_channel: str, username: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "updateChannelUsername",
                {"channel_guid": guid_channel, "username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def getMessageShareUrl(self, guid: str, messageId: Union[str, list]):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getMessageShareUrl",
                {"object_guid": guid, "messageId": messageId},
                self.cli,
            ),
        ).show()

    def getBlockedUsers(self, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getBlockedUsers", {"start_id": start_id}, self.cli),
        ).show()

    def deleteContact(self, guid_user: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "deleteContact", {"user_guid": guid_user}, self.cli),
        ).show()

    def checkUserUsername(self, username: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "checkUserUsername",
                {"username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def checkChannelUsername(self, username: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "checkChannelUsername",
                {"username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def getContacts(self, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getContacts", {"start_id": start_id}, self.cli),
        ).show()

    def getLiveStatus(
        self, live_id: Optional[Union[str, int]], token_live: Optional[Union[str, int]]
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getLiveStatus",
                {"live_id": live_id, "access_token": token_live},
                self.cli,
            ),
        ).show()

    def getLiveComments(
        self, live_id: Optional[Union[str, int]], token_live: Optional[Union[str, int]]
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "getLiveComments",
                {"live_id": live_id, "access_token": token_live},
                self.cli,
            ),
        ).show()

    @property
    def getdatabaseReaction(self):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getAvailableReactions", {}, self.cli),
        ).show()

    def Reaction(self, guid: str, typeReaction: str, reaction: str, message_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "actionOnMessageReaction",
                {
                    "action": "Add" if typeReaction == "add" else "Remove",
                    "reaction_id": reaction,
                    "message_id": message_id,
                    "object_guid": guid,
                },
                self.cli,
            ),
        ).show()

    def commonGroup(self, guid_user: str):
        IDE = guid_user.replace("@", "")
        GUID = self.getInfoByUsername(IDE)["data"]["user"]["user_guid"]
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getCommonGroups", {"user_guid": GUID}, self.cli),
        ).show()

    def setTypeChannel(self, guid_channel: str, Private: bool = False):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "editChannelInfo",
                {
                    "channel_guid": guid_channel,
                    "channel_type": ("Private" if type_Channel else "Public"),
                    "updated_parameters": ["channel_type"],
                },
                self.cli,
            ),
        ).show()

    def getChatAds(self, user_guids: list):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getChatAds", {"state": state}, self.cli),
        ).show()

    def clickMessageUrl(
        self, guid: str, message_id: Optional[Union[str, int, list]], link: str
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "clickMessageUrl",
                {"object_guid": guid, "message_id": message_id, "link_url": link},
                self.cli,
            ),
        ).show()

    def seenChat(self, guid: str, message_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "seenChat",
                {"seen_list": {f"{guid}": f"{message_id}"}},
                self.cli,
            ),
        ).show()

    @property
    def getContactsUpdates(self):
        state = str(round(datetime.datetime.today().timestamp()) - 200)
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getContactsUpdates", {"state": state}, self.cli),
        ).show()

    def twolocks(self, ramz: str, hide: str):
        locked = GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "setupTwoStepVerification",
                {"hint": hide, "password": ramz},
                self.cli,
            ),
        ).show()
        if locked["status"] == "ERROR_GENERIC":
            return locked["self.client_show_message"]["link"]["alert_data"]["message"]
        else:
            return locked

    def deletetwolocks(self, password: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "turnOffTwoStep", {"password": password}, self.cli),
        ).show()

    def checkPassword(self, password: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "checkTwoStepPasscode", {"password": password}, self.cli),
        ).show()

    def passwordChange(self, password: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "resendCodeRecoveryEmail", {"password": password}, self.cli),
        ).show()

    def loginforgetPassword(
        self,
        emailCode: Optional[Union[str, int]],
        password: str,
        phone_number: Optional[Union[str, int]],
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "loginDisableTwoStep",
                {
                    "email_code": emailCode,
                    "forget_password_code_hash": password,
                    "phone_number": phone_number,
                },
                self.cli,
            ),
        ).show()

    def ProfileEdit(
        self,
        first_name: str = None,
        last_name: str = None,
        bio: str = None,
        username: str = None,
    ):
        while 1:
            try:
                for tekrar in range(1):
                    self.editUser(first_name=first_name, last_name=last_name, bio=bio)
                    if username != None:
                        self.editusername(username.replace("@", ""))
                    return "Profile edited"
                break
            except:
                continue

    def getChatGroup(self, guid_gap: str):
        while 1:
            try:
                for tekrar in range(1):
                    lastmessages = self.getGroupInfo(guid_gap)["data"]["chat"][
                        "last_message_id"
                    ]
                    messages = self.getMessages(guid_gap, lastmessages)
                    return messages
                break
            except:
                continue

    def getChatChannel(self, guid_channel: str):
        while 1:
            try:
                for tekrar in range(1):
                    lastmessages = self.getChannelInfo(guid_channel)["data"]["chat"][
                        "last_message_id"
                    ]
                    messages = self.getMessages(guid_channel, lastmessages)
                    return messages
                break
            except:
                continue

    def getChatUser(self, guid_User: str):
        while 1:
            try:
                for tekrar in range(1):
                    lastmessages = self.getUserInfo(guid_User)["data"]["chat"][
                        "last_message_id"
                    ]
                    messages = self.getMessages(guid_User, lastmessages)
                    return messages
                break
            except:
                continue

    @property
    def Authrandom(self):
        auth = ""
        meghdar = "qwertyuiopasdfghjklzxcvbnm0123456789"
        for string in range(32):
            auth += choice(meghdar)
        return auth

    # method send Files

    def requestSendFile(self, addressfile: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "requestSendFile",
                {
                    "file_name": os.path.basename(addressfile),
                    "size": os.path.getsize(addressfile),
                    "mime": os.path.splitext(addressfile)[1].strip("."),
                },
                self.cli,
            ),
        ).show()

    def resend(self, guid: str, message_id: list[str]):
        datamsg = self.getMessagesInfo(guid, message_id).get("data").get("messages")[0]
        resend = makeJsonResend(guid, datamsg.get("file_inline"))
        if "text" in datamsg.keys():
            resend["text"] = datamsg.get("text")
        else:
            resend["text"] = None
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "sendMessage", resend, self.cli),
        ).show()

    def downloadFiles(
        self,
        guid: str,
        message_id: list[str, int],
        save: str = None,
        link: bool = False,
    ):
        getdatafile = (
            self.getMessagesInfo(guid, message_id)
            .get("data")
            .get("messages")[0]
            .get("file_inline")
        )

        if link == False:
            return self.methods.run(
                "download",
                downloads=[
                    self.Auth,
                    getdatafile.get("dc_id"),
                    getdatafile.get("file_id"),
                    getdatafile.get("size"),
                    getdatafile.get("access_hash_rec"),
                    save,
                ],
            )
        elif link == True:
            Link: str = (
                f"https://messenger{getdatafile.get('dc_id')}.iranlms.ir/InternFile.ashx?id={getdatafile.get('file_id')}&ach={getdatafile.get('access_hash_rec')}"
            )
            file: bin = httpx.get(Link).content
            return (
                (open(save, "wb").write(file), [save, True])[1]
                if save
                else [file, True]
            )

    def Http(self, link: str, formats: str):
        while True:
            try:
                for tek in range(1):

                    async def download_file(link, formatt):
                        async with aiohttp.ClientSession() as session:
                            async with session.get(link) as response:
                                if response.status == 200:
                                    while True:
                                        buildnamefiles = f"LibraryArseinRubika{randint(0, 1000)}.{formatt}"
                                        checkname = os.path.exists(buildnamefiles)
                                        if checkname == False:
                                            for tek in range(1):
                                                with open(buildnamefiles, "wb") as file:
                                                    content = await response.read()
                                                    file.write(content)
                                                return buildnamefiles
                                            break
                                        else:
                                            continue
                                else:
                                    return 404

                    loop = asyncio.get_event_loop()
                    return loop.run_until_complete(download_file(link, formats))
                break
            except Exception as Error:
                continue

    def SendSticker(
        self,
        guid: str,
        emoji_character: str,
        w_h_ratio: str,
        sticker_id: str,
        sticker_set_id: str,
        file_id: str = None,
        dc_id: str = None,
        access_hash_rec: str = None,
    ):
        return self.methods.run(
            "json",
            methode="sendMessage",
            indata={
                "object_guid": guid,
                "rnd": randint(100000, 999999999),
                "sticker": {
                    "emoji_character": emoji_character,
                    "w_h_ratio": w_h_ratio,
                    "sticker_id": sticker_id,
                    "file": {
                        "file_id": file_id,
                        "mime": "png",
                        "dc_id": dc_id,
                        "access_hash_rec": access_hash_rec,
                        "file_name": "sticker.png",
                        "cdn_tag": "PR5",
                        "size": 0,
                    },
                    "sticker_set_id": sticker_set_id,
                },
            },
            wn=self.cli,
        )

    def SendImage(
        self,
        guid: str,
        addressfile: str,
        spoil: bool = False,
        thumbinline: str = None,
        caption: str = None,
        message_id: str = None,
    ):
        from PIL import Image

        addressfile: str = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "png")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getphoto = Image.open(addressfile)
            up = self.Upload.uploadFile(addressfile)
            width, height = getphoto.size
            thumbinline = (
                self.thumb_inline
                if thumbinline == None
                else str(getThumbInline(open(addressfile, "rb").read()))
            )
            getphoto.close()
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "json",
                methode="sendMessage",
                indata={
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "Image",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "is_spoil": spoil,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "thumb_inline": thumbinline,
                        "width": width,
                        "height": height,
                        "access_hash_rec": up[1],
                    },
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error sendPhoto"

    def SendFile(
        self,
        guid: str,
        addressfile: str,
        formats: str = None,
        caption: str = None,
        message_id: str = None,
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, formats)
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            up = self.Upload.uploadFile(addressfile)
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "json",
                methode="sendMessage",
                indata={
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "File",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "access_hash_rec": up[1],
                    },
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendFile"

    def SendVideo(
        self,
        guid: str,
        addressfile: str,
        spoil: bool = False,
        thumbinline: str = None,
        caption: str = None,
        message_id: str = None,
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp4")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getvideo = TinyTag.get(addressfile)
            width, height = [100, 100]
            up = self.Upload.uploadFile(addressfile)
            thumbinline = (
                self.thumb_inline
                if thumbinline == None
                else str(getThumbInline(open(addressfile, "rb").read()))
            )
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "json",
                methode="sendMessage",
                indata={
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "Video",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "is_spoil": spoil,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "thumb_inline": thumbinline,
                        "width": width,
                        "height": height,
                        "time": int(getvideo.duration * 1000),
                        "access_hash_rec": up[1],
                    },
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendVideo"

    def SendGif(
        self,
        guid: str,
        addressfile: str,
        thumbinline: str = None,
        caption: str = None,
        message_id: str = None,
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp4")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getvideo = TinyTag.get(addressfile)
            width, height = [100, 100]
            up = self.Upload.uploadFile(addressfile)
            thumbinline = (
                self.thumb_inline
                if thumbinline == None
                else str(getThumbInline(open(addressfile, "rb").read()))
            )
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "json",
                methode="sendMessage",
                indata={
                    "file_inline": {
                        "access_hash_rec": up[1],
                        "auto_play": False,
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "file_name": os.path.basename(addressfile),
                        "height": height,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "size": getSize,
                        "thumb_inline": thumbinline,
                        "time": int(getvideo.duration * 1000),
                        "type": "Gif",
                        "width": width,
                    },
                    "is_mute": False,
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendGif"

    def SendVoice(
        self,
        guid: str,
        addressfile: str,
        timevoice: Optional[Union[str, int]] = None,
        caption: str = None,
        message_id: str = None,
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp3")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getMP3 = MP3(addressfile)
            time = getMP3.info.length if timevoice == None else timevoice
            up = self.Upload.uploadFile(addressfile)
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "json",
                methode="sendMessage",
                indata={
                    "file_inline": {
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "type": "Voice",
                        "file_name": os.path.basename(addressfile),
                        "size": getSize,
                        "time": time,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "access_hash_rec": up[1],
                    },
                    "object_guid": guid,
                    "rnd": f"{randint(100000, 999999999)}",
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendVoice"

    def SendMusic(
        self, guid: str, addressfile: str, caption: str = None, message_id: str = None
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp3")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getMP3 = MP3(addressfile)
            width, height, time = (
                getMP3.info.channels,
                getMP3.info.sample_rate,
                getMP3.info.length,
            )
            up = self.Upload.uploadFile(addressfile)
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "json",
                methode="sendMessage",
                indata={
                    "file_inline": {
                        "access_hash_rec": up[1],
                        "auto_play": False,
                        "dc_id": up[0]["dc_id"],
                        "file_id": up[0]["id"],
                        "file_name": os.path.basename(addressfile),
                        "height": height,
                        "mime": os.path.splitext(addressfile)[1].strip("."),
                        "music_performer": "library ArseinRubika",
                        "size": getSize,
                        "time": time,
                        "type": "Music",
                        "width": width,
                    },
                    "is_mute": False,
                    "object_guid": guid,
                    "rnd": randint(100000, 999999999),
                    "text": caption,
                    "reply_to_message_id": message_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendMusic"

    def getJoinRequests(self, object_guid: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("json", "getJoinRequests", {"object_guid": object_guid}, self.cli),
        ).show()

    def AcceptJoinRequest(self, object_guid: str, user_guid: str):
        object_type = "Group" if object_guid.startswith("g0") else "Channel"
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "actionOnJoinRequest",
                {
                    "object_guid": object_guid,
                    "object_type": object_type,
                    "user_guid": user_guid,
                    "action": "Accept",
                },
                self.cli,
            ),
        ).show()

    def RejectJoinRequest(self, object_guid: str, user_guid: str):
        object_type = "Group" if object_guid.startswith("g0") else "Channel"
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "actionOnJoinRequest",
                {
                    "object_guid": object_guid,
                    "object_type": object_type,
                    "user_guid": user_guid,
                    "action": "Reject",
                },
                self.cli,
            ),
        ).show()

    def run(self):
        while True:
            try:
                time.sleep(3600)
            except KeyboardInterrupt:
                ...

    # method logins

    def register(self, typeauth: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "registerDevice",
                DeviceTelephone(typeauth.lower()).Device,
                self.cli,
            ),
        ).show()


def sendCode(
    platforms: str, numberphone: str, send_type: bool = False, password: str = None
):
    cli, method = clien(platforms).platform, method_Rubika(platforms)
    send_type = "Internal" if send_type != False else "SMS"
    return method.run(
        "login",
        methode="sendCode",
        indata={
            "phone_number": (
                f"98{numberphone[3:]}" if numberphone.startswith("98") else numberphone
            ),
            "send_type": send_type,
            "pass_key": password,
        },
        wn=cli,
    )


def signIn(
    platforms: str, numberphone: str, codehash: str, phone_code: str, save: str = None
):
    publicKey, privateKey = encoderjson.rsaKeyGenerate()
    method, cli = method_Rubika(platforms), clien(platforms).platform
    if platforms and numberphone and codehash and phone_code:
        GetDataSignIn = method.run(
            "login",
            methode="signIn",
            indata={
                "phone_number": (
                    f"98{numberphone[3:]}"
                    if numberphone.startswith("98")
                    else numberphone
                ),
                "phone_code_hash": codehash,
                "phone_code": phone_code,
                "public_key": publicKey,
                "private_key": privateKey,
            },
            wn=cli,
        )
        if GetDataSignIn.get("data").get("status") == "OK":
            data_account = dict(
                Auth=encoderjson.changeAuthType(
                    encoderjson.decryptRsaOaep(
                        privateKey, GetDataSignIn.get("data").get("auth")
                    )
                ),
                Key=privateKey,
            )
            if save != None:
                with open(save.rsplit(".", 1)[0] + ".json", "w") as f:
                    dump(data_account, f)
            return data_account

        elif GetDataSignIn.get("data").get("status") == "CodeIsInvalid":
            raise ErrorMethod("Invalid Rubika login code")
    elif not platforms or numberphone or codehash or phone_code:
        raise ErrorMethod("Enter the complete values ​​into the method")


class Robot_Rubika(Messenger): ...


class Bot:
    def __init__(self, token: str):
        self.methods = method_Rubika(tokenBot=token)

    @property
    def getMe(self):
        return GetDataMethod(
            target=self.methods.run,
            args=("Bot", "getMe"),
        ).show()

    def getUpdates(self, offset_id: str = None, limit: int = None):
        return GetDataMethod(
            target=self.methods.run,
            args=("Bot", "getUpdates", {"offset_id": offset_id, "limit": limit}),
        ).show()

    def requestSendFile(self, type: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("Bot", "requestSendFile", {"type": type}),
        ).show()

    def getUpdate(self, filters):
        def warmup(func):
            handlers.append((filters, func))
            if not hasattr(self, "_update_thread"):
                self._update_thread = threading.Thread(target=self.__getupdate)
                self._update_thread.start()
            return func

        return warmup

    def __getupdate(self):
        from .arsocket.get_Message import Bot_Updates

        global get_update
        while True:
            try:
                get_update = self.getUpdates(limit=100)

                if len(get_update.get("data").get("updates")) == 100:
                    next_offset_id = get_update.get("data").get("next_offset_id")
                    get_update = self.getUpdates(next_offset_id, 100)

                if get_update.get("data").get("updates"):
                    msg = Bot_Updates(get_update.get("data").get("updates")[-1])

                    for Flt, methods in handlers:
                        if Flt(msg):
                            threading.Thread(
                                target=methods, args=(msg,), daemon=True
                            ).start()
                    time.sleep(1)

            except Exception as e:
                import traceback

                print("Update error:", repr(e))
                traceback.print_exc()
                time.sleep(3)
                continue

    def run(self):
        while True:
            try:
                time.sleep(3600)
            except KeyboardInterrupt:
                ...

    def sendMessage(
        self,
        chat_id: str,
        text: str,
        chat_keypad_type: str = None,
        keypad: Optional[Dict[str, Any]] = None,
        notification: bool = False,
        inline_keypad: Optional[Dict[str, Any]] = None,
        reply_to_message_id: str = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):
        data = {"chat_id": chat_id, "text": text, "disable_notification": notification}

        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendMessage", data)
        ).show()

    def sendPoll(self, chat_id: str, question: str, items: list[str]):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "sendPoll",
                {"chat_id": chat_id, "question": question, "options": items},
            ),
        ).show()

    def sendLocation(
        self,
        chat_id: str,
        latitude: str,
        longitude: str,
        chat_keypad_type: str = None,
        keypad: Optional[Dict[str, Any]] = None,
        notification: str = "false",
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
        reply_to_message_id: str = None,
    ):

        data = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "disable_notification": notification,
        }

        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendLocation", data)
        ).show()

    def sendContact(
        self,
        chat_id: str,
        first_name: str,
        last_name: str,
        phone_number: str,
        chat_keypad_type: str = None,
        keypad: Optional[Dict[str, Any]] = None,
        notification: str = "false",
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
        reply_to_message_id: str = None,
    ):

        data = {
            "chat_id": chat_id,
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
        }

        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type
        if notification:
            data["disable_notification"] = notification

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendContact", data)
        ).show()

    def getChat(self, chat_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("Bot", "getChat", {"chat_id": chat_id}),
        ).show()

    def forwardMessage(
        self, chat_id: str, message_id: str, to_chat_id: str, notification: bool = False
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "forwardMessage",
                {
                    "from_chat_id": chat_id,
                    "message_id": message_id,
                    "to_chat_id": to_chat_id,
                    "disable_notification": notification,
                },
            ),
        ).show()

    def editMessageText(self, chat_id: str, message_id: str, text: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "editMessageText",
                {"chat_id": chat_id, "message_id": message_id, "text": text},
            ),
        ).show()

    def getChatAdmins(self, chat_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "getChatAdmins",
                {"chat_id": chat_id},
            ),
        ).show()

    def getChatMembers(self, chat_id: str, start_id: str = ""):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "getChatMembers",
                {"chat_id": chat_id, "start_id": start_id},
            ),
        ).show()

    def getChatInfo(self, chat_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "getChatInfo",
                {"chat_id": chat_id},
            ),
        ).show()

    def editChatTitle(self, chat_id: str, title: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "editChatTitle",
                {"chat_id": chat_id, "title": title},
            ),
        ).show()

    def editChatDescription(self, chat_id: str, description: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "editChatDescription",
                {"chat_id": chat_id, "description": description},
            ),
        ).show()

    def editChatPhoto(self, chat_id: str, file_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "editChatPhoto",
                {"chat_id": chat_id, "file_id": file_id},
            ),
        ).show()

    def addChatMembers(self, chat_id: str, member_ids: list[str]):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "addChatMembers",
                {"chat_id": chat_id, "member_ids": member_ids},
            ),
        ).show()

    def banChatMember(self, chat_id: str, user_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "banChatMember",
                {"chat_id": chat_id, "user_id": user_id},
            ),
        ).show()

    def unbanChatMember(self, chat_id: str, member_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "unbanChatMember",
                {"chat_id": chat_id, "member_id": member_id},
            ),
        ).show()

    def restrictChatMember(self, chat_id: str, member_id: str, until_date: int = 0):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "restrictChatMember",
                {"chat_id": chat_id, "member_id": member_id, "until_date": until_date},
            ),
        ).show()

    def getChatAdministrators(self, chat_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "getChatAdministrators",
                {"chat_id": chat_id},
            ),
        ).show()

    def getChatMemberCount(self, chat_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "getChatMemberCount",
                {"chat_id": chat_id},
            ),
        ).show()

    def promoteChatMember(self, chat_id: str, member_id: str, rights: dict = {}):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "promoteChatMember",
                {"chat_id": chat_id, "member_id": member_id, "rights": rights},
            ),
        ).show()

    def pinChatMessage(self, chat_id: str, member_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "pinChatMessage",
                {"chat_id": chat_id, "message_id": message_id},
            ),
        ).show()

    def unpinChatMessage(self, chat_id: str, member_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "unpinChatMessage",
                {"chat_id": chat_id, "message_id": message_id},
            ),
        ).show()

    def exportChatInviteLink(self, chat_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "exportChatInviteLink",
                {"chat_id": chat_id},
            ),
        ).show()

    def revokeChatInviteLink(self, chat_id: str, invite_link: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "revokeChatInviteLink",
                {"chat_id": chat_id, "invite_link": invite_link},
            ),
        ).show()

    def editMessageKeypad(
        self,
        chat_id: str,
        message_id: str,
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "editMessageKeypad",
                {
                    "chat_id": chat_id,
                    "message_id": message_id,
                    "inline_keypad": (
                        inline_keypad.to_dict(resize_keyboard, on_time_keyboard)
                        if inline_keypad
                        else None
                    ),
                },
            ),
        ).show()

    def deleteMessage(self, chat_id: str, message_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "deleteMessage",
                {"chat_id": chat_id, "message_id": message_id},
            ),
        ).show()

    def setCommands(self, bot_commands: list[str]):
        return GetDataMethod(
            target=self.methods.run,
            args=("Bot", "setCommands", {"bot_commands": bot_commands.to_dict()}),
        ).show()

    def updateBotEndpoints(self, url: str, TypeEndpoin: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("Bot", "updateBotEndpoints", {"url": url, "type": TypeEndpoin}),
        ).show()

    def editChatKeypad(
        self,
        chat_id: str,
        chat_keypad_type: str = None,
        keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Bot",
                "editChatKeypad",
                {
                    "chat_id": chat_id,
                    "chat_keypad": (
                        keypad.to_dict(resize_keyboard, on_time_keyboard)
                        if keypad
                        else None
                    ),
                    "chat_keypad_type": chat_keypad_type,
                },
            ),
        ).show()

    def getLinkDownload(self, file_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("Bot", "getFile", {"file_id": file_id}),
        ).show()

    def sendFile(
        self,
        chat_id: str,
        file: str,
        caption: str = None,
        chat_keypad_type: str = None,
        reply_to_message_id: str = None,
        notification: str = "false",
        keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):

        upload_url = self.requestSendFile("File").get("data").get("upload_url")
        Upload_file_id = UploadBot(upload_url, file).File_Id["data"]["file_id"]

        data = {"chat_id": chat_id, "file_id": Upload_file_id}

        if caption:
            data["text"] = caption
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if notification:
            data["disable_notification"] = notification
        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendFile", data)
        ).show()

    def sendImage(
        self,
        chat_id: str,
        file: str,
        caption: str = None,
        chat_keypad_type: str = None,
        reply_to_message_id: str = None,
        notification: str = "false",
        keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):

        upload_url = self.requestSendFile("Image").get("data").get("upload_url")
        Upload_file_id = UploadBot(upload_url, file).File_Id["data"]["file_id"]

        data = {"chat_id": chat_id, "file_id": Upload_file_id}

        if caption:
            data["text"] = caption
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if notification:
            data["disable_notification"] = notification
        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendFile", data)
        ).show()

    def sendVoice(
        self,
        chat_id: str,
        file: str,
        caption: str = None,
        chat_keypad_type: str = None,
        reply_to_message_id: str = None,
        notification: str = "false",
        keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):

        upload_url = self.requestSendFile("Voice").get("data").get("upload_url")
        Upload_file_id = UploadBot(upload_url, file).File_Id["data"]["file_id"]

        data = {"chat_id": chat_id, "file_id": Upload_file_id}

        if caption:
            data["text"] = caption
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if notification:
            data["disable_notification"] = notification
        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendFile", data)
        ).show()

    def sendVideo(
        self,
        chat_id: str,
        file: str,
        caption: str = None,
        chat_keypad_type: str = None,
        reply_to_message_id: str = None,
        notification: str = "false",
        keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):

        upload_url = self.requestSendFile("Video").get("data").get("upload_url")
        Upload_file_id = UploadBot(upload_url, file).File_Id["data"]["file_id"]

        data = {"chat_id": chat_id, "file_id": Upload_file_id}

        if caption:
            data["text"] = caption
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if notification:
            data["disable_notification"] = notification
        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendFile", data)
        ).show()

    def sendGif(
        self,
        chat_id: str,
        file: str,
        caption: str = None,
        chat_keypad_type: str = None,
        reply_to_message_id: str = None,
        notification: str = "false",
        keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):

        upload_url = self.requestSendFile("Gif").get("data").get("upload_url")
        Upload_file_id = UploadBot(upload_url, file).File_Id["data"]["file_id"]

        data = {"chat_id": chat_id, "file_id": Upload_file_id}

        if caption:
            data["text"] = caption
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if notification:
            data["disable_notification"] = notification
        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendFile", data)
        ).show()

    def sendMusic(
        self,
        chat_id: str,
        file: str,
        caption: str,
        chat_keypad_type: str = None,
        reply_to_message_id: str = None,
        notification: str = "false",
        keypad: Optional[Dict[str, Any]] = None,
        inline_keypad: Optional[Dict[str, Any]] = None,
        resize_keyboard: bool = True,
        on_time_keyboard: bool = False,
    ):

        upload_url = self.requestSendFile("Music").get("data").get("upload_url")
        Upload_file_id = UploadBot(upload_url, "Music", file).File_Id["data"]["file_id"]

        data = {"chat_id": chat_id, "file_id": Upload_file_id}

        if caption:
            data["text"] = caption
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if reply_to_message_id:
            data["reply_to_message_id"] = str(reply_to_message_id)
        if notification:
            data["disable_notification"] = notification
        if keypad:
            data["chat_keypad"] = keypad.to_dict(resize_keyboard, on_time_keyboard)
        if inline_keypad:
            data["inline_keypad"] = inline_keypad.to_dict(
                resize_keyboard, on_time_keyboard
            )
        if chat_keypad_type:
            data["chat_keypad_type"] = chat_keypad_type

        return GetDataMethod(
            target=self.methods.run, args=("Bot", "sendFile", data)
        ).show()


class Rubino:
    def __init__(self, auth: str, Proxy: Optional[Union[str, List[str]]] = None):
        self.methods = method_Rubika(OrginalAuth=auth, Proxy=Proxy)
        self.cli = clien("android").platform
        self.Upload = Upload(OrginalAuth=auth)

    def addPostVideo(
        self,
        addressfile: str,
        profile_id: str,
        caption: str,
        sizes: list[str] = ["1293", "1080"],
        thumbinline: str = None,
    ):
        addressfile = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "mp4")
        )

        if addressfile != 404 and os.path.exists(addressfile):
            thumbinline_ = (
                "arsein/logo/logo_arsein.jpg" if not thumbinline else thumbinline
            )
            getSize = str(os.path.getsize(addressfile))
            getvideo = TinyTag.get(addressfile)
            height, width = sizes
            up = self.Upload.uploadFileRubino(addressfile, "Video", profile_id)
            thumbinline_Up = self.Upload.uploadFileRubino(
                thumbinline_, "Picture", profile_id
            )
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "Rubino",
                methode="addPost",
                indata={
                    "caption": caption,
                    "file_id": up[0]["file_id"],
                    "hash_file_receive": up[1],
                    "height": height,
                    "width": width,
                    "is_multi_file": False,
                    "post_type": "Video",
                    "rnd": randint(100000, 999999999),
                    "tagged_profiles": [],
                    "thumbnail_file_id": thumbinline_Up[0]["file_id"],
                    "thumbnail_hash_file_receive": thumbinline_Up[1],
                    "profile_id": profile_id,
                    "duration": f"{int(getvideo.duration * 1000)}",
                    "snapshot_file_id": thumbinline_Up[0]["file_id"],
                    "snapshot_hash_file_receive": thumbinline_Up[1],
                },
                wn=self.cli,
            )
        else:
            return "error SendPostVideo_Rubino"

    def addPostImage(
        self, addressfile: str, profile_id: str, caption: str, sizes: list[str] = None
    ):
        from PIL import Image

        addressfile: str = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "png")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            getSize = str(os.path.getsize(addressfile))
            getphoto = Image.open(addressfile)
            up = self.Upload.uploadFileRubino(addressfile, "Picture", profile_id)
            width, height = getphoto.size if not sizes else sizes
            getphoto.close()
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "Rubino",
                methode="addPost",
                indata={
                    "caption": caption,
                    "file_id": up[0]["file_id"],
                    "hash_file_receive": up[1],
                    "height": height,
                    "width": width,
                    "is_multi_file": False,
                    "post_type": "Picture",
                    "rnd": randint(100000, 999999999),
                    "tagged_profiles": [],
                    "thumbnail_file_id": up[0]["file_id"],
                    "thumbnail_hash_file_receive": up[1],
                    "profile_id": profile_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendPostImage_Rubino"

    def addStoryVideo(
        self,
        addressfile: str,
        profile_id: str,
        sizes: list[str] = ["1280", "720"],
        thumbinline: str = None,
    ):

        addressfile: str = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "png")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            thumbinline_ = (
                "arsein/logo/logo_arsein.jpg" if not thumbinline else thumbinline
            )
            getSize = str(os.path.getsize(addressfile))
            getvideo = TinyTag.get(addressfile)
            height, width = sizes
            up = self.Upload.uploadFileRubino(addressfile, "Video", profile_id)
            thumbinline_Up = self.Upload.uploadFileRubino(
                thumbinline_, "Picture", profile_id
            )
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "Rubino",
                methode="addStory",
                indata={
                    "duration": f"{int(getvideo.duration * 1000)}",
                    "file_id": up[0]["file_id"],
                    "hash_file_receive": up[1],
                    "height": height,
                    "story_type": "Video",
                    "rnd": randint(100000, 999999999),
                    "snapshot_file_id": thumbinline_Up[0]["file_id"],
                    "snapshot_hash_file_receive": thumbinline_Up[1],
                    "thumbnail_file_id": thumbinline_Up[0]["file_id"],
                    "thumbnail_hash_file_receive": thumbinline_Up[1],
                    "width": width,
                    "profile_id": profile_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendStoryVideo_Rubino"

    def addStoryImage(
        self,
        addressfile: str,
        profile_id: str,
        sizes: list[str] = None,
        thumbinline: str = None,
    ):
        from PIL import Image

        addressfile: str = (
            addressfile
            if not addressfile.startswith("https://" or "http://")
            else self.Http(addressfile, "png")
        )
        if addressfile != 404 and os.path.exists(addressfile):
            thumbinline_ = (
                "arsein/logo/logo_arsein.jpg" if not thumbinline else thumbinline
            )
            getSize = str(os.path.getsize(addressfile))
            getphoto = Image.open(addressfile)
            width, height = getphoto.size if not sizes else sizes
            up = self.Upload.uploadFileRubino(addressfile, "Picture", profile_id)
            thumbinline_Up = self.Upload.uploadFileRubino(
                thumbinline_, "Picture", profile_id
            )
            getphoto.close()
            if addressfile.startswith("LibraryArseinRubika"):
                os.remove(addressfile)
            return self.methods.run(
                "Rubino",
                methode="addStory",
                indata={
                    "file_id": up[0]["file_id"],
                    "hash_file_receive": up[1],
                    "height": height,
                    "story_type": "Picture",
                    "rnd": randint(100000, 999999999),
                    "thumbnail_file_id": thumbinline_Up[0]["file_id"],
                    "thumbnail_hash_file_receive": thumbinline_Up[1],
                    "width": width,
                    "profile_id": profile_id,
                },
                wn=self.cli,
            )
        else:
            return "error SendStoryVideo_Rubino"

    # action_type Like - Unlike
    # track_id  Explore:two_tower - Feed - Explore

    def likePostAction(
        self, post_id: str, post_profile_id: str, action_type: str, profile_id: str
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "likePostAction",
                {
                    "action_type": action_type,
                    "post_id": post_id,
                    "post_profile_id": post_profile_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def getMyProfileInfo(self, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("Rubino", "getMyProfileInfo", {"profile_id": profile_id}, self.cli),
        ).show()

    def getProfileHighlights(self, target_profile_id: str, profile_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getProfileHighlights",
                {"target_profile_id": target_profile_id, "profile_id": profile_id},
                self.cli,
            ),
        ).show()

    def getMyProfilePosts(
        self, limit, profile_id: str, max_id: str = None, sort: str = "FromMax"
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getMyProfilePosts",
                {
                    "limit": limit,
                    "sort": sort,
                    "max_id": None,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def updateProfile(
        self,
        profile_id: str,
        username: str = None,
        name: str = None,
        bio: str = None,
        email: str = None,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "updateProfile",
                {
                    "profile_id": profile_id,
                    "username": username.replace("@", "") if username else None,
                    "name": name,
                    "bio": bio,
                    "email": email,
                },
                self.cli,
            ),
        ).show()

    def private_page(self, profile_id: str, profile_status: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "updateProfile",
                {"profile_id": profile_id, "profile_status": profile_status},
                self.cli,
            ),
        ).show()

    def getProfileList(self, limit: int, sort: str = "FromMax"):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getProfileList",
                {"limit": limit, "sort": sort},
                self.cli,
            ),
        ).show()

    def getNewEvents(self, profile_id: str, limit: int, sort: str = "FromMax"):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getNewEvents",
                {"profile_id": profile_id, "limit": limit, "sort": sort},
                self.cli,
            ),
        ).show()

    def getProfileInfo(self, target_profile_id: str, track_id: str = ""):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getProfileInfo",
                {"target_profile_id": target_profile_id, "track_id": track_id},
                self.cli,
            ),
        ).show()

    def getProfilePosts(
        self,
        limit: int,
        target_profile_id: str,
        profile_id: str,
        max_id: str = None,
        sort: str = "FromMax",
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getProfilePosts",
                {
                    "limit": limit,
                    "sort": sort,
                    "target_profile_id": target_profile_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    # 'max_id':max_id

    def getRecentFollowingPosts(
        self, profile_id: str, limit: int, max_id: str, sort: str = "FromMax"
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getRecentFollowingPosts",
                {
                    "profile_id": profile_id,
                    "limit": limit,
                    "sort": sort,
                    "max_id": max_id,
                },
                self.cli,
            ),
        ).show()

    def getProfilesStories(self, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=("Rubino", "getProfilesStories", {"profile_id": profile_id}, self.cli),
        ).show()

    def sendRubinoPost(self, object_guid: str, post_id: str, post_profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "json",
                "sendRubinoPost",
                {
                    "object_guid": object_guid,
                    "post_id": post_id,
                    "post_profile_id": post_profile_id,
                    "is_mute": false,
                    "rnd": f"{randint(100000, 999999)}",
                },
                self.cli,
            ),
        ).show()

    # action_type  Bookmark - Unbookmark
    # track_id  Explore - Feed

    def postBookmarkAction(
        self, post_id: str, post_profile_id: str, action_type: str, track_id: str = None
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "postBookmarkAction",
                {
                    "post_id": post_id,
                    "post_profile_id": post_profile_id,
                    "action_type": action_type,
                    "track_id": track_id,
                },
                self.cli,
            ),
        ).show()

    # f_type Follower - Following
    # track_id  Explore - Feed

    def requestFollow(
        self, followee_id: str, f_type: str, post_track_id: str, profile_id: str
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "requestFollow",
                {
                    "followee_id": followee_id,
                    "f_type": f_type,
                    "post_track_id": post_track_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def getComments(
        self,
        profile_id: str,
        post_id: str,
        post_profile_id: str,
        limit: int,
        min_id: Optional[Union[str, int]] = None,
        sort: str = "FromMax",
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getComments",
                {
                    "profile_id": profile_id,
                    "post_id": post_id,
                    "post_profile_id": post_profile_id,
                    "limit": limit,
                    "sort": sort,
                    "min_id": min_id,
                },
                self.cli,
            ),
        ).show()

    def addComment(
        self, text: str, post_id: str, post_profile_id: str, profile_id: str
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "addComment",
                {
                    "content": text,
                    "post_id": post_id,
                    "post_profile_id": post_profile_id,
                    "profile_id": profile_id,
                    "track_id": "Feed",
                },
                self.cli,
            ),
        ).show()

    # action_type Unlike - Like
    # track_id  Explore - Feed

    def likeCommentAction(
        self,
        post_id: str,
        comment_id: str,
        action_type: str,
        profile_id: str,
        track_id: str,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "likeCommentAction",
                {
                    "post_id": post_id,
                    "comment_id": comment_id,
                    "action_type": action_type,
                    "profile_id": profile_id,
                    "track_id": track_id,
                },
                self.cli,
            ),
        ).show()

    def getPostLikes(
        self,
        profile_id: str,
        post_id: str,
        post_profile_id: str,
        limit: int,
        max_id: str = None,
        sort: str = "FromMax",
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getPostLikes",
                {
                    "profile_id": profile_id,
                    "post_id": post_id,
                    "post_profile_id": post_profile_id,
                    "limit": limit,
                    "sort": sort,
                    "max_id": max_id,
                },
                self.cli,
            ),
        ).show()

    # model  Post - Profile
    # reason 1 - 2

    def setReportRecord(
        self,
        model: str,
        reason: Optional[int],
        record_id: str,
        post_profile_id: str = None,
        profile_id: str = None,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "setReportRecord",
                {
                    "model": model,
                    "reason": reason,
                    "record_id": record_id,
                    "post_profile_id": post_profile_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def isExistUsername(self, username: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "isExistUsername",
                {"username": username.replace("@", "")},
                self.cli,
            ),
        ).show()

    def getHighlightStoryIds(
        self,
        profile_id: str,
        target_profile_id: str,
        highlight_id: str,
        story_ids: list = None,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getHighlightStoryIds",
                {
                    "profile_id": profile_id,
                    "target_profile_id": target_profile_id,
                    "highlight_id": highlight_id,
                    "story_ids": story_ids,
                },
                self.cli,
            ),
        ).show()

    # f_type Follower - Following

    def getFollowers(
        self,
        profile_id: str,
        limit: int,
        target_profile_id: str,
        f_type: str,
        max_id: str = None,
        sort: str = "FromMax",
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getProfileFollowers",
                {
                    "profile_id": profile_id,
                    "limit": limit,
                    "sort": sort,
                    "max_id": max_id,
                    "target_profile_id": target_profile_id,
                    "f_type": f_type,
                },
                self.cli,
            ),
        ).show()

    def searchFollower(
        self,
        username: str,
        limit: int,
        search_type: str,
        target_profile_id: str,
        profile_id: str,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "searchFollower",
                {
                    "username": username.replace("@", ""),
                    "limit": limit,
                    "search_type": search_type,
                    "target_profile_id": target_profile_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def getExplorePosts(
        self,
        profile_id: str,
        limit,
        max_id: str,
        topic_id: str = None,
        sort: str = "FromMax",
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getExplorePosts",
                {
                    "profile_id": profile_id,
                    "limit": limit,
                    "sort": sort,
                    "max_id": f"v6-ai-{max_id}",
                    "topic_id": topic_id,
                },
                self.cli,
            ),
        ).show()

    # start_id - AI_RE_2
    # track_id  Explore:two_tower - Feed

    def getRelatedExplorePost(
        self,
        profile_id: str,
        post_id: str,
        post_profile_id: str,
        limit: int,
        track_id: str,
        start_id: str = None,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getRelatedExplorePost",
                {
                    "profile_id": profile_id,
                    "post_id": post_id,
                    "post_profile_id": post_profile_id,
                    "start_id": start_id,
                    "limit": limit,
                    "track_id": track_id,
                },
                self.cli,
            ),
        ).show()

    def getStory(self, profile_id: str, story_profile_id: str, story_ids: list):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getStory",
                {
                    "profile_id": profile_id,
                    "story_profile_id": story_profile_id,
                    "story_ids": story_ids,
                },
                self.cli,
            ),
        ).show()

    def getStoryIds(self, profile_id: str, target_profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getStoryIds",
                {"profile_id": profile_id, "target_profile_id": target_profile_id},
                self.cli,
            ),
        ).show()

    def getSuggested(
        self, profile_id: str, limit: int, max_id: str, sort: str = "FromMax"
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getSuggested",
                {
                    "profile_id": profile_id,
                    "limit": limit,
                    "sort": sort,
                    "max_id": max_id,
                },
                self.cli,
            ),
        ).show()

    def searchProfile(self, username: str, limit: str, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "searchProfile",
                {
                    "username": username.replace("@", ""),
                    "limit": limit,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def getHashTagTrend(self, limit: int, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getHashTagTrend",
                {"limit": limit, "profile_id": profile_id},
                self.cli,
            ),
        ).show()

    def searchHashTag(self, text: str, limit: int, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "searchHashTag",
                {"content": text, "limit": limit, "profile_id": profile_id},
                self.cli,
            ),
        ).show()

    def getPostsByHashTag(self, text: str, start_id: str = None):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getPostsByHashTag",
                {"hashtag": text, "start_id": start_id},
                self.cli,
            ),
        ).show()

    def getTaggedPosts(
        self, target_profile_id: str, profile_id: str, start_id: str = None
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getTaggedPosts",
                {
                    "start_id": start_id,
                    "target_profile_id": target_profile_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def getExplorePostTopics(self, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getExplorePostTopics",
                {"profile_id": profile_id},
                self.cli,
            ),
        ).show()

    def create_page(
        self,
        username: str,
        name: str,
        bio: str = None,
        phone: str = None,
        email: str = None,
        website: str = None,
    ):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "createPage",
                {
                    "username": username,
                    "name": name,
                    "bio": bio,
                    "phone": phone,
                    "email": email,
                    "website": website,
                },
                self.cli,
            ),
        ).show()

    def unblock_page(self, target_profile_id: str, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "setBlockProfile",
                {
                    "action": "Unblock",
                    "blocked_id": target_profile_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def block_page(self, target_profile_id: str, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "setBlockProfile",
                {
                    "action": "Block",
                    "blocked_id": target_profile_id,
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

    def block_page(
        self, limit: int, max_id: str, profile_id: str, sort: str = "FromMax"
    ):
        data = {"limit": limit, "max_id": max_id, "sort": sort}
        if profile_id:
            data["profile_id"] = profile_id

        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getBookmarkedPosts",
                data,
                self.cli,
            ),
        ).show()

    def getInfoPost(self, url: str, profile_id: str):
        return GetDataMethod(
            target=self.methods.run,
            args=(
                "Rubino",
                "getPostByShareLink",
                {
                    "share_string": url.replace("https://rubika.ir/post/", ""),
                    "profile_id": profile_id,
                },
                self.cli,
            ),
        ).show()

class photo_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.file_name = data.get("message").get("file_inline").get("file_name")
        self.file_format = (
            data.get("message").get("file_inline").get("file_name").split(".")[1]
        )
        self.thumb_inline = data.get("message").get("file_inline").get("thumb_inline")
        self.width = data.get("message").get("file_inline").get("width")
        self.height = data.get("message").get("file_inline").get("height")
        self.size = data.get("message").get("file_inline").get("size")


class file_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.file_id = data.get("message").get("file_inline").get("file_id")
        self.mime = data.get("message").get("file_inline").get("mime")
        self.dc_id = data.get("message").get("file_inline").get("dc_id")
        self.access_hash_rec = (
            data.get("message").get("file_inline").get("access_hash_rec")
        )
        self.file_name = data.get("message").get("file_inline").get("file_name")
        self.file_format = (
            data.get("message").get("file_inline").get("file_name").split(".")[1]
        )
        self.size = data.get("message").get("file_inline").get("size")


class voice_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.file_id = data.get("message").get("file_inline").get("file_id")
        self.mime = data.get("message").get("file_inline").get("mime")
        self.dc_id = data.get("message").get("file_inline").get("dc_id")
        self.access_hash_rec = (
            data.get("message").get("file_inline").get("access_hash_rec")
        )
        self.file_name = data.get("message").get("file_inline").get("file_name")
        self.file_format = (
            data.get("message").get("file_inline").get("file_name").split(".")[1]
        )
        self.size = data.get("message").get("file_inline").get("size")
        self.time = data.get("message").get("file_inline").get("time")


class video_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.file_id = data.get("message").get("file_inline").get("file_id")
        self.mime = data.get("message").get("file_inline").get("mime")
        self.dc_id = data.get("message").get("file_inline").get("dc_id")
        self.access_hash_rec = (
            data.get("message").get("file_inline").get("access_hash_rec")
        )
        self.file_name = data.get("message").get("file_inline").get("file_name")
        self.file_format = (
            data.get("message").get("file_inline").get("file_name").split(".")[1]
        )
        self.size = data.get("message").get("file_inline").get("size")
        self.time = data.get("message").get("file_inline").get("time")
        self.width = data.get("message").get("file_inline").get("width")
        self.height = data.get("message").get("file_inline").get("height")


class music_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.file_id = data.get("message").get("file_inline").get("file_id")
        self.mime = data.get("message").get("file_inline").get("mime")
        self.dc_id = data.get("message").get("file_inline").get("dc_id")
        self.access_hash_rec = (
            data.get("message").get("file_inline").get("access_hash_rec")
        )
        self.file_name = data.get("message").get("file_inline").get("file_name")
        self.file_format = (
            data.get("message").get("file_inline").get("file_name").split(".")[1]
        )
        self.size = data.get("message").get("file_inline").get("size")
        self.time = data.get("message").get("file_inline").get("time")


class gif_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.file_id = data.get("message").get("file_inline").get("file_id")
        self.mime = data.get("message").get("file_inline").get("mime")
        self.dc_id = data.get("message").get("file_inline").get("dc_id")
        self.access_hash_rec = (
            data.get("message").get("file_inline").get("access_hash_rec")
        )
        self.file_name = data.get("message").get("file_inline").get("file_name")
        self.file_format = (
            data.get("message").get("file_inline").get("file_name").split(".")[1]
        )
        self.size = data.get("message").get("file_inline").get("size")
        self.time = data.get("message").get("file_inline").get("time")
        self.width = data.get("message").get("file_inline").get("width")
        self.height = data.get("message").get("file_inline").get("height")


class sticker_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.emoji_character = data.get("message").get("sticker").get("emoji_character")
        self.w_h_ratio = data.get("message").get("sticker").get("w_h_ratio")
        self.sticker_id = data.get("message").get("sticker").get("sticker_id")
        self.sticker_set_id = data.get("message").get("sticker").get("sticker_set_id")
        self.file_id = data.get("message").get("sticker").get("file").get("file_id")
        self.dc_id = data.get("message").get("sticker").get("file").get("dc_id")
        self.access_hash_rec = (
            data.get("message").get("sticker").get("file").get("access_hash_rec")
        )


class location_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.longitude = data.get("message").get("location").get("longitude")
        self.latitude = data.get("message").get("location").get("latitude")
        self.tile_side_count = (
            data.get("message").get("location").get("map_view").get("tile_side_count")
        )
        self.tile_urls = (
            data.get("message").get("location").get("map_view").get("tile_urls")
        )
        self.x_loc = data.get("message").get("location").get("map_view").get("x_loc")
        self.y_loc = data.get("message").get("location").get("map_view").get("y_loc")


class poll_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.poll_id = data.get("message").get("poll").get("poll_id")
        self.question = data.get("message").get("poll").get("question")
        self.options = data.get("message").get("poll").get("options")
        self.state = data.get("message").get("poll").get("state")


class live_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.live_id = data.get("message").get("live_data").get("live_id")
        self.thumb_inline = data.get("message").get("live_data").get("thumb_inline")
        self.access_token = data.get("message").get("live_data").get("access_token")
        self.live_status = (
            data.get("message").get("live_data").get("live_status").get("status")
        )
        self.play_count = (
            data.get("message").get("live_data").get("live_status").get("play_count")
        )
        self.allow_comment = (
            data.get("message").get("live_data").get("live_status").get("allow_comment")
        )
        self.can_play = (
            data.get("message").get("live_data").get("live_status").get("can_play")
        )
        self.timestamp = (
            data.get("message").get("live_data").get("live_status").get("timestamp")
        )


class contact_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.phone_number = (
            data.get("message").get("contact_message").get("phone_number")
        )
        self.first_name = data.get("message").get("contact_message").get("first_name")
        self.last_name = data.get("message").get("contact_message").get("last_name")
        self.vcard = data.get("message").get("contact_message").get("vcard")
        self.allow_transcription = (
            data.get("message").get("contact_message").get("allow_transcription")
        )


class forward_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.from_title = data.get("message").get("forwarded_no_link").get("from_title")
        self.time = data.get("message").get("time")
        self.count_seen = data.get("message").get("count_seen")
        self.is_edited = data.get("message").get("is_edited")
        self.type_from = data.get("message").get("forwarded_from").get("type_from")
        self.message_id_from = (
            data.get("message").get("forwarded_from").get("message_id")
        )
        self.object_guid = data.get("message").get("forwarded_from").get("object_guid")


class reply_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.text = data.get("message").get("text")
        self.reply_to_message_id = data.get("message").get("reply_to_message_id")
        self.time = data.get("message").get("time")
        self.is_edited = data.get("message").get("is_edited")
        self.type = data.get("message").get("type")
        self.author_object_guid = data.get("message").get("author_object_guid")
        self.allow_transcription = data.get("message").get("allow_transcription")


class bot_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.text = data.get("message").get("text")
        self.time = data.get("message").get("time")
        self.is_edited = data.get("message").get("is_edited")
        self.inline_keypad = data.get("message").get("inline_keypad")
        self.type = data.get("message").get("type")
        self.author_object_guid = data.get("message").get("author_object_guid")
        self.allow_transcription = data.get("message").get("allow_transcription")


class event_:
    def __init__(self, data: dict):
        self.message_id = data.get("message_id")
        self.type_activity = data.get("message").get("event_data").get("type")
        self.performer_type = (
            data.get("message").get("event_data").get("performer_object").get("type")
        )
        self.performer_object_guid = (
            data.get("message")
            .get("event_data")
            .get("performer_object")
            .get("object_guid")
        )
        self.performer_type = (
            data.get("message").get("event_data").get("peer_objects")[0].get("type")
            if "peer_objects" in data.get("message").get("event_data").keys()
            else False
        )
        self.performer_object_guid = (
            data.get("message")
            .get("event_data")
            .get("peer_objects")[0]
            .get("object_guid")
            if "peer_objects" in data.get("message").get("event_data").keys()
            else False
        )


class voice_chat_:
    def __init__(self, data: dict):
        self._type_voice_chat = (
            data.get("group_voice_chat_updates")
            if "group_voice_chat_updates" in data.keys()
            else data.get("channel_voice_chat_updates")
        )
        self._info_voice_chat = (
            self._type_voice_chat[0].get("group_voice_chat")
            if "group_voice_chat" in self._type_voice_chat[0].keys()
            else self._type_voice_chat[0].get("channel_voice_chat")
        )
        self.voice_chat_id = self._type_voice_chat[0].get("voice_chat_id")
        self.state = (
            self._info_voice_chat.get("state")
            if "state" in self._info_voice_chat.keys()
            else False
        )
        self.join_muted = (
            self._info_voice_chat.get("state")
            if "join_muted" in self._info_voice_chat.keys()
            else False
        )
        self.participant_count = (
            self._info_voice_chat.get("participant_count")
            if "participant_count" in self._info_voice_chat.keys()
            else False
        )
        self.title = (
            self._info_voice_chat.get("title")
            if "title" in self._info_voice_chat.keys()
            else False
        )
        self.version = (
            self._info_voice_chat.get("version")
            if "version" in self._info_voice_chat.keys()
            else False
        )


class pin_:
    def __init__(self, data: dict):
        self.pinned_message_ids = (
            data.get("chat_updates")[0].get("chat").get("pinned_message_ids")
        )


class Message_socket:
    def __init__(self, data: dict):

        message_updates, show_activities = (
            data["message_updates"][0]
            if "message_updates" in data.keys() and data["message_updates"] != []
            else dict()
        ), (
            data["show_activities"][0]
            if "show_activities" in data.keys() and data["show_activities"] != []
            else dict()
        )

        if message_updates:
            self.action = message_updates["action"]
            self.text = (
                message_updates["message"]["text"]
                if "message" in message_updates.keys()
                and "text" in message_updates["message"].keys()
                else False
            )
            self.time = (
                message_updates["message"]["time"]
                if "message" in message_updates.keys()
                and "time" in message_updates["message"].keys()
                else False
            )
            self.is_edited = (
                message_updates["message"]["is_edited"]
                if "message" in message_updates.keys()
                else False
            )
            self.type_send = (
                message_updates["message"]["type"]
                if "message" in message_updates.keys()
                and "type" in message_updates["message"].keys()
                else False
            )
            self.author_type = (
                message_updates["message"]["author_type"]
                if "message" in message_updates.keys()
                and "author_type" in message_updates["message"].keys()
                else False
            )
            self.author_object_guid = (
                message_updates["message"]["author_object_guid"]
                if "message" in message_updates.keys()
                and "author_object_guid" in message_updates["message"].keys()
                else False
            )
            self.allow_transcription = (
                message_updates["message"]["allow_transcription"]
                if "message" in message_updates.keys()
                and "allow_transcription" in message_updates["message"].keys()
                else False
            )
            self.timestamp = message_updates["timestamp"]
            self.prev_message_id = (
                message_updates["prev_message_id"]
                if "prev_message_id" in message_updates.keys()
                else False
            )
            self.object_guid = message_updates["object_guid"]
            self.object_guid_user_service = (
                message_updates["message"]["event_data"]["performer_object"][
                    "object_guid"
                ]
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self.type_chat_service = (
                message_updates["message"]["event_data"]["performer_object"]["type"]
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self.chat_type = message_updates["type"]
            self.state = message_updates["state"]
            self.is_scheduled = message_updates["is_scheduled"]

            self._is_pv = message_updates["type"] == "User"
            self._is_gap = message_updates["type"] == "Group"
            self._is_channel = message_updates["type"] == "Channel"
            self._is_bot = message_updates["type"] == "Bot"
            self._is_text = (
                message_updates["message"]["type"] == "Text"
                if "message" in message_updates.keys()
                and "type" in message_updates["message"].keys()
                else False
            )
            self._is_location = (
                message_updates["message"]["type"] == "Location"
                if "message" in message_updates.keys()
                and "type" in message_updates["message"].keys()
                else False
            )
            self._is_image = (
                message_updates["message"]["file_inline"]["type"] == "Image"
                if "message" in message_updates.keys()
                and "file_inline" in message_updates["message"].keys()
                else False
            )
            self._is_video = (
                message_updates["message"]["file_inline"]["type"] == "Video"
                if "message" in message_updates.keys()
                and "file_inline" in message_updates["message"].keys()
                else False
            )
            self._is_voice = (
                message_updates["message"]["file_inline"]["type"] == "Voice"
                if "message" in message_updates.keys()
                and "file_inline" in message_updates["message"].keys()
                else False
            )
            self._is_music = (
                message_updates["message"]["file_inline"]["type"] == "Music"
                if "message" in message_updates.keys()
                and "file_inline" in message_updates["message"].keys()
                else False
            )
            self._is_gif = (
                message_updates["message"]["file_inline"]["type"] == "Gif"
                if "message" in message_updates.keys()
                and "file_inline" in message_updates["message"].keys()
                else False
            )
            self._is_file = (
                message_updates["message"]["file_inline"]["type"] == "File"
                if "message" in message_updates.keys()
                and "file_inline" in message_updates["message"].keys()
                else False
            )
            self._is_sticker = (
                message_updates["message"]["type"] == "Sticker"
                if "message" in message_updates.keys()
                and "type" in message_updates["message"].keys()
                else False
            )
            self._is_poll = (
                message_updates["message"]["type"] == "Poll"
                if "message" in message_updates.keys()
                and "type" in message_updates["message"].keys()
                else False
            )
            self._is_live = (
                message_updates["message"]["type"] == "Live"
                if "message" in message_updates.keys()
                and "type" in message_updates["message"].keys()
                else False
            )
            self._is_contact = (
                message_updates["message"]["type"] == "ContactMessage"
                if "message" in message_updates.keys()
                and "type" in message_updates["message"].keys()
                else False
            )
            self._is_spoil = (
                message_updates["message"]["file_inline"]["is_spoil"]
                if "message" in message_updates.keys()
                and "file_inline" in message_updates["message"].keys()
                else False
            )

            self._is_service = (
                True
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._new_member_gap = (
                message_updates["message"]["event_data"]["type"] == "JoinedGroupByLink"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._left_member_gap = (
                message_updates["message"]["event_data"]["type"] == "LeaveGroup"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._remove_member_gap = (
                message_updates["message"]["event_data"]["type"] == "RemoveGroupMembers"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._add_member_gap = (
                message_updates["message"]["event_data"]["type"] == "AddedGroupMembers"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._change_title = (
                message_updates["message"]["event_data"]["type"] == "TitleUpdate"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._change_photo = (
                message_updates["message"]["event_data"]["type"] == "PhotoUpdate"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._delete_photo = (
                message_updates["message"]["event_data"]["type"] == "RemovePhoto"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )

            self._message_pinned = (
                message_updates["message"]["event_data"]["type"]
                == "PinnedMessageUpdated"
                if "message" in message_updates.keys()
                and "event_data" in message_updates["message"].keys()
                else False
            )
            self._Stop_VoiceChat = (
                "message" in message_updates
                and "event_data" in message_updates["message"]
                and "type" in message_updates["message"]["event_data"]
                and message_updates["message"]["event_data"]["type"]
                in ("StopGroupVoiceChat", "StopChannelVoiceChat")
            )
            self._start_VoiceChat = (
                "message" in message_updates
                and "event_data" in message_updates["message"]
                and "type" in message_updates["message"]["event_data"]
                and message_updates["message"]["event_data"]["type"]
                in ("CreateGroupVoiceChat", "CreateChannelVoiceChat")
            )

            self._is_forwarded = "message" in message_updates and (
                "forwarded_from" in message_updates["message"]
                or "forwarded_no_link" in message_updates["message"]
            )
            self._is_reply = (
                "message" in message_updates.keys()
                and "reply_to_message_id" in message_updates["message"].keys()
            )
            self._is_deleted_message = message_updates["action"] == "Delete"
            self._is_edit_message = message_updates["action"] == "Edit"
            self._forwarded_from_channel = (
                message_updates["message"]["forwarded_from"]["type_from"] == "Channel"
                if "message" in message_updates.keys()
                and "forwarded_from" in message_updates["message"].keys()
                else False
            )
            self._forwarded_from_pv = (
                message_updates["message"]["forwarded_from"]["type_from"] == "User"
                if "message" in message_updates.keys()
                and "forwarded_from" in message_updates["message"].keys()
                else (
                    message_updates["message"]["type"] == "User"
                    if "forwarded_no_link" in message_updates["message"].keys()
                    else False
                )
            )
            self._forwarded_from_gap = (
                message_updates["message"]["forwarded_from"]["type_from"] == "Group"
                if "message" in message_updates.keys()
                and "forwarded_from" in message_updates["message"].keys()
                else False
            )
            self._forwarded_message_id = (
                message_updates["message"]["forwarded_from"]["message_id"]
                if "message" in message_updates.keys()
                and "forwarded_from" in message_updates["message"].keys()
                else False
            )
            self._forwarded_object_guid = (
                message_updates["message"]["forwarded_from"]["object_guid"]
                if "message" in message_updates.keys()
                and "forwarded_from" in message_updates["message"].keys()
                else False
            )
            self._is_fance_font = (
                "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
            )
            self._is_font_bold = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "Bold"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )
            self._is_font_MentionText = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "MentionText"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )
            self._is_font_Mono = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "Mono"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )
            self._is_font_Italic = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "Italic"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )
            self._is_font_Strike = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "Strike"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )
            self._is_font_Underline = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "Underline"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )
            self._is_font_Spoiler = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "Spoiler"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )
            self._is_font_Link = (
                message_updates["message"]["metadata"]["meta_data_parts"][0]["type"]
                == "Link"
                if "message" in message_updates.keys()
                and "metadata" in message_updates["message"].keys()
                else False
            )

        elif show_activities:
            self.is_typing = (
                show_activities["object_type"] == "Typing"
                if "show_activities" in data.keys()
                else False
            )
            self.type_activity = show_activities["type"]
            self.object_guid = show_activities["object_guid"]
            self.user_activity_guid = show_activities["user_activity_guid"]

        if self._is_image:
            self.Photo = photo_(message_updates)

        elif self._is_video:
            self.Video = video_(message_updates)

        elif self._is_voice:
            self.Voice = voice_(message_updates)

        elif self._is_music:
            self.Music = music_(message_updates)

        elif self._is_poll:
            self.Poll = poll_(message_updates)

        elif self._is_location:
            self.Location = location_(message_updates)

        elif self._is_sticker:
            self.Sticker = sticker_(message_updates)

        elif self._is_live:
            self.Live = live_(message_updates)

        elif self._is_contact:
            self.Contact = contact_(message_updates)

        elif self._is_forwarded:
            self.Forwarded = forward_(message_updates)

        elif self._is_reply:
            self.Reply = reply_(message_updates)

        elif self._is_bot:
            self.Bot = bot_(message_updates)

        elif self._is_service:
            self.Service = event_(message_updates)

        elif self._is_gif:
            self.Gif = gif_(message_updates)

        elif self._start_VoiceChat or self._Stop_VoiceChat:
            self.Voice_Chat = voice_chat_(data)

        elif self._message_pinned:
            self.Pin = pin_(message_updates)

        elif self._is_file:
            self.File = file_(message_updates)

    def __getattr__(self, item):
        return False


class photo_bot:
    def __init__(self, data: dict):
        self.file_id = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_id")
        )
        self.file_name = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
        )
        self.file_format = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
            .split(".")[1]
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.size = (
            data.get("new_message", data.get("updated_message")).get("file").get("size")
        )
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )


class file_bot:
    def __init__(self, data: dict):
        self.file_id = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_id")
        )
        self.file_name = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
        )
        self.file_format = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
            .split(".")[1]
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.size = (
            data.get("new_message", data.get("updated_message")).get("file").get("size")
        )
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )


class voice_bot:
    def __init__(self, data: dict):
        self.file_id = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_id")
        )
        self.file_name = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
        )
        self.file_format = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
            .split(".")[1]
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.size = (
            data.get("new_message", data.get("updated_message")).get("file").get("size")
        )
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )


class video_bot:
    def __init__(self, data: dict):
        self.file_id = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_id")
        )
        self.file_name = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
        )
        self.file_format = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
            .split(".")[1]
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.size = (
            data.get("new_message", data.get("updated_message")).get("file").get("size")
        )
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )


class music_bot:
    def __init__(self, data: dict):
        self.file_id = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_id")
        )
        self.file_name = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
        )
        self.file_format = (
            data.get("new_message", data.get("updated_message"))
            .get("file")
            .get("file_name")
            .split(".")[1]
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.size = (
            data.get("new_message", data.get("updated_message")).get("file").get("size")
        )
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )


class sticker_bot:
    def __init__(self, data: dict):
        self.file_id = (
            data.get("new_message", data.get("updated_message"))
            .get("sticker")
            .get("file")
            .get("file_id")
        )
        self.file_name = (
            data.get("new_message", data.get("updated_message"))
            .get("sticker")
            .get("file")
            .get("file_name")
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.size = (
            data.get("new_message", data.get("updated_message"))
            .get("sticker")
            .get("file")
            .get("size")
        )
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )
        self.emoji_character = (
            data.get("new_message", data.get("updated_message"))
            .get("sticker")
            .get("emoji_character")
        )
        self.sticker_id = (
            data.get("new_message", data.get("updated_message"))
            .get("sticker")
            .get("sticker_id")
        )


class location_bot:
    def __init__(self, data: dict):
        self.longitude = (
            data.get("new_message", data.get("updated_message"))
            .get("location")
            .get("longitude")
        )
        self.longitude = (
            data.get("new_message", data.get("updated_message"))
            .get("location")
            .get("longitude")
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )


class poll_bot:
    def __init__(self, data: dict):
        self.question = (
            data.get("new_message", data.get("updated_message"))
            .get("poll")
            .get("question")
        )
        self.options = (
            data.get("new_message", data.get("updated_message"))
            .get("poll")
            .get("options")
        )
        self.time = data.get("new_message", data.get("updated_message")).get("time")
        self.message_id = data.get("new_message", data.get("updated_message")).get(
            "message_id"
        )
        self.is_edited = data.get("new_message", data.get("updated_message")).get(
            "is_edited"
        )
        self.chat_id = data.get("chat_id")
        self.sender_type = data.get("sender_type")
        self.sender_id = data.get("new_message", data.get("updated_message")).get(
            "sender_id"
        )
        self.state = data.get("new_message").get("poll").get("poll_status").get("state")


class forward_bot:
    def __init__(self, data: dict):
        self.type_from = (
            data.get("new_message", data.get("updated_message"))
            .get("forwarded_from")
            .get("type_from")
        )
        self.message_id = (
            data.get("new_message", data.get("updated_message"))
            .get("forwarded_from")
            .get("message_id")
        )
        self.from_chat_id = (
            data.get("new_message", data.get("updated_message"))
            .get("forwarded_from")
            .get("from_chat_id")
        )
        self.from_sender_id = (
            data.get("new_message", data.get("updated_message"))
            .get("forwarded_from")
            .get("from_sender_id")
        )


class contact_bot:
    def __init__(self, data: dict):
        self.phone_number = (
            data.get("new_message", data.get("updated_message"))
            .get("ContactMessage")
            .get("phone_number")
        )
        self.first_name = (
            data.get("new_message", data.get("updated_message"))
            .get("ContactMessage")
            .get("first_name")
        )
        self.last_name = (
            data.get("new_message", data.get("updated_message"))
            .get("ContactMessage")
            .get("last_name")
        )


class Bot_Updates:
    def __init__(self, data: dict):
        new_message, RemovedMessage = (
            data.get("new_message", data.get("updated_message"))
            if "new_message" in data.keys() or "updated_message" in data.keys()
            else dict()
        ), (data if "removed_message_id" in data.keys() else dict())

        image_formats = [
            "JPEG",
            "PNG",
            "GIF",
            "BMP",
            "TIFF",
            "WebP",
            "SVG",
            "ICO",
            "HEIF",
            "RAW",
            "JPG",
        ]
        all_audio_formats = [
            "MP3",
            "WAV",
            "FLAC",
            "AAC",
            "OGG",
            "M4A",
            "WMA",
            "ALAC",
            "AIFF",
            "DSD",
            "APE",
            "MIDI",
            "MOD",
            "OPUS",
            "AMR",
            "3GP",
            "GSM",
            "VOX",
            "DSS",
            "DVF",
            "RA",
            "VQF",
            "AU",
            "VOC",
            "CAF",
            "A Law",
            "MU Law",
            "S3M",
            "XM",
            "MPC",
            "IVS",
        ]
        video_formats = [
            "MP4",
            "AVI",
            "MKV",
            "MOV",
            "WMV",
            "FLV",
            "WebM",
            "MPEG",
            "3GP",
            "M4V",
            "TS",
            "MTS",
            "VOB",
            "DAT",
            "RMVB",
            "ASF",
            "DIVX",
            "XVID",
            "H264",
            "HEVC",
            "AVCHD",
            "MXF",
            "OGV",
            "SWF",
            "F4V",
            "MPG",
            "M2TS",
            "M2V",
            "MPE",
            "MPV",
            "3G2",
            "QT",
            "YUV",
            "CRM",
            "RM",
            "AVS",
            "MK3D",
            "WEBM",
            "VIVO",
            "FLIC",
        ]
        file_formats = [
            "zip",
            "rar",
            "7z",
            "tar",
            "gz",
            "bz2",
            "xz",
            "exe",
            "msi",
            "bat",
            "cmd",
            "sh",
            "apk",
            "jar",
            "bin",
            "com",
            "pdf",
            "doc",
            "docx",
            "txt",
            "rtf",
            "odt",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "csv",
        ]

        if new_message:

            self.type_send = data["type"]
            self.chat_id = data["chat_id"]
            self.message_id = (
                new_message["message_id"]
                if "message_id" in new_message.keys()
                else False
            )
            self.text = new_message["text"] if "text" in new_message.keys() else False

            self._aux_data_button_id = (
                new_message["aux_data"]["button_id"]
                if "aux_data" in new_message.keys()
                and "button_id" in new_message["aux_data"].keys()
                else False
            )

            self._is_image = (
                "file" in new_message.keys()
                and "file_name" in new_message["file"].keys()
                and new_message["file"]["file_name"].split(".")[1].upper()
                in image_formats
            )
            self._is_music = (
                "file" in new_message.keys()
                and "file_name" in new_message["file"].keys()
                and new_message["file"]["file_name"].split(".")[1].upper()
                in all_audio_formats
            )
            self._is_voice = (
                "file" in new_message.keys()
                and "file_name" in new_message["file"].keys()
                and new_message["file"]["file_name"].split(".")[1].upper()
                in all_audio_formats
            )
            self._is_video = (
                "file" in new_message.keys()
                and "file_name" in new_message["file"].keys()
                and new_message["file"]["file_name"].split(".")[1].upper()
                in video_formats
            )
            self._is_file = (
                "file" in new_message.keys()
                and "file_name" in new_message["file"].keys()
                and new_message["file"]["file_name"].split(".")[1].upper()
                in file_formats
            )
            self._is_poll = "poll" in new_message.keys()
            self._is_location = "location" in new_message.keys()
            self._is_forwarded = "forwarded_from" in new_message.keys()
            self._is_forwarded_no_link = "forwarded_no_link" in new_message.keys()
            self._is_contact = "ContactMessage" in new_message.keys()
            self._is_text = (
                "text" in new_message.keys() and "file" not in new_message.keys()
            )
            self._is_sticker = "sticker" in new_message.keys()
            self._is_stopped = "StoppedBot" in data["type"]
            self._is_user = data.get("chat_id").startswith("b0") and new_message.get(
                "sender_id"
            ).startswith("u0")
            self._is_gap = data.get("chat_id").startswith("g0")
            self._is_channel = data.get("chat_id").startswith("c0")
            self._is_bot = new_message.get("sender_id").startswith("b0")

            if "reply_to_message_id" in new_message.keys():
                self.reply_to_message_id = new_message.get("reply_to_message_id")
            elif (
                "aux_data" in new_message.keys()
                and "start_id" in new_message["aux_data"].keys()
            ):
                self.aux_data_start_id = new_message.get("aux_data").get("start_id")

            if self._is_image:
                self.Photo = photo_bot(data)

            elif self._is_video:
                self.Video = video_bot(data)

            elif self._is_voice:
                self.Voice = voice_bot(data)

            elif self._is_music:
                self.Music = music_bot(data)

            elif self._is_poll:
                self.Poll = poll_bot(data)

            elif self._is_location:
                self.Location = location_bot(data)

            elif self._is_sticker:
                self.Sticker = sticker_bot(data)

            elif self._is_file:
                self.File = file_bot(data)

            elif self._is_forwarded:
                self.Forwarded = forward_bot(data)

            elif self._is_contact:
                self.Contact = contact_bot(data)

        elif RemovedMessage:

            self.type_send = RemovedMessage["type"]
            self.chat_id = RemovedMessage["chat_id"]
            self.removed_message_id = (
                RemovedMessage["removed_message_id"]
                if "removed_message_id" in RemovedMessage.keys()
                else False
            )

    def __getattr__(self, item):
        return False

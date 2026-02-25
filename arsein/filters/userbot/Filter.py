import re


class Operators:
    def __init__(self, func):
        self.func = func

    def __call__(self, message):
        return self.func(message)

    def __eq__(self, other):
        return Operators(lambda msg: self.func(msg) == other)

    def __lt__(self, other):
        return Operators(lambda msg: self.func(msg) < other)

    def __gt__(self, other):
        return Operators(lambda msg: self.func(msg) > other)

    def __ne__(self, other):
        return Operators(lambda msg: self.func(msg) != other)

    def __le__(self, other):
        return Operators(lambda msg: self.func(msg) <= other)

    def __ge__(self, other):
        return Operators(lambda msg: self.func(msg) >= other)

    def __and__(self, other):
        return Operators(lambda msg: self.func(msg) and other(msg))

    def __or__(self, other):
        return Operators(lambda msg: self.func(msg) or other(msg))

    def __rand__(self, other):
        return Operators(lambda msg: other(msg) and self.func(msg))

    def __ror__(self, other):
        return Operators(lambda msg: other(msg) or self.func(msg))


is_pv = Operators(lambda msg: msg._is_pv)
is_gap = Operators(lambda msg: msg._is_gap)
is_channel = Operators(lambda msg: _msg.is_channel)
is_bot = Operators(lambda msg: msg._is_bot)
is_image = Operators(lambda msg: msg._is_image)
is_video = Operators(lambda msg: msg._is_video)
is_gif = Operators(lambda msg: msg._is_gif)
is_file = Operators(lambda msg: msg._is_file)
is_voice = Operators(lambda msg: msg._is_voice)
is_music = Operators(lambda msg: msg._is_music)
is_sticker = Operators(lambda msg: msg._is_sticker)
is_location = Operators(lambda msg: msg._is_location)
is_text = Operators(lambda msg: msg.text)
is_forwarded = Operators(lambda msg: msg._is_forwarded)
forwarded_from_channel = Operators(lambda msg: msg._forwarded_from_channel)
forwarded_from_pv = Operators(lambda msg: msg._forwarded_from_pv)
forwarded_from_gap = Operators(lambda msg: msg._forwarded_from_gap)
forwarded_message_id = Operators(lambda msg: msg._forwarded_message_id)
forwarded_object_guid = Operators(lambda msg: msg._forwarded_object_guid)
is_fance_font = Operators(lambda msg: msg._is_fance_font)
is_font_bold = Operators(lambda msg: msg._is_font_bold)
is_font_MentionText = Operators(lambda msg: msg._is_font_MentionText)
is_font_Mono = Operators(lambda msg: msg._is_font_Mono)
is_font_Italic = Operators(lambda msg: msg._is_font_Italic)
is_font_Strike = Operators(lambda msg: msg._is_font_Strike)
is_font_Underline = Operators(lambda msg: msg._is_font_Underline)
is_font_Spoiler = Operators(lambda msg: msg._is_font_Spoiler)
is_font_Link = Operators(lambda msg: msg._is_font_Link)
is_deleted_message = Operators(lambda msg: msg._is_deleted_message)
is_edit_message = Operators(lambda msg: msg._is_edit_message)
is_spoil = Operators(lambda msg: msg._is_spoil)
is_service = Operators(lambda msg: msg._is_service)
new_member_gap = Operators(lambda msg: msg._new_member_gap)
left_member_gap = Operators(lambda msg: msg._left_member_gap)
remove_member_gap = Operators(lambda msg: msg._remove_member_gap)
add_member_gap = Operators(lambda msg: msg._add_member_gap)
message_pinned = Operators(lambda msg: msg._message_pinned)
start_VoiceChat = Operators(lambda msg: msg._start_VoiceChat)
Stop_VoiceChat = Operators(lambda msg: msg._Stop_VoiceChat)
is_change_title = Operators(lambda msg: msg._change_title)
is_change_photo = Operators(lambda msg: msg._change_photo)
is_delete_photo = Operators(lambda msg: msg._delete_photo)
is_poll = Operators(lambda msg: msg._is_poll)
is_live = Operators(lambda msg: msg._is_live)
is_contact = Operators(lambda msg: msg._is_contact)
is_reply = Operators(lambda msg: msg._is_reply)
is_link = Operators(
    lambda msg: (
        True
        if isinstance(msg.text, str)
        and bool(
            re.search(
                r"\b((?:https?|ftp):\/\/[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/[^\s]*)?)",
                msg.text,
            )
        )
        else False
    )
)
is_ID = Operators(
    lambda msg: (
        True
        if isinstance(msg.text, str)
        and bool(re.search(r"(?<!\w)@([a-zA-Z0-9_\.]{3,32})(?!\w)", msg.text))
        else False
    )
)


def text_startswith(matn):
    return Operators(
        lambda msg: isinstance(msg.text, str) and msg.text.startswith(matn)
    )


def text_endswith(matn):
    return Operators(lambda msg: isinstance(msg.text, str) and msg.text.endswith(matn))


def text_keywords(*matn):
    matns = list(matn)
    return Operators(
        lambda msg: (
            any(word.lower() in msg.text.lower() for word in matns)
            if isinstance(msg.text, str)
            else False
        )
    )


def regex(matn, flags=0):
    regexs = re.compile(matn, flags)
    return Operators(
        lambda msg: (
            bool(regexs.search(msg.text)) if isinstance(msg.text, str) else False
        )
    )

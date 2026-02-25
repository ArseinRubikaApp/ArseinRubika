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


is_image = Operators(lambda msg: msg._is_image)
is_music = Operators(lambda msg: msg._is_music)
is_voice = Operators(lambda msg: msg._is_voice)
is_video = Operators(lambda msg: msg._is_video)
is_poll = Operators(lambda msg: msg._is_poll)
is_location = Operators(lambda msg: msg._is_location)
is_text = Operators(lambda msg: msg._is_text)
is_sticker = Operators(lambda msg: msg._is_sticker)
is_file = Operators(lambda msg: msg._is_file)
is_stopped = Operators(lambda msg: msg._is_stopped)
is_user = Operators(lambda msg: msg._is_user)
is_gap = Operators(lambda msg: msg._is_gap)
is_channel = Operators(lambda msg: _msg.is_channel)
is_bot = Operators(lambda msg: msg._is_bot)
is_forwarded = Operators(lambda msg: msg._is_forwarded)
is_forwarded_no_link = Operators(lambda msg: msg._is_forwarded_no_link)
is_contact = Operators(lambda msg: msg._is_contact)

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


def on_chatkeypad(button__id):
    if isinstance(button__id, str):
        return Operators(lambda msg: bool(button__id == msg._aux_data_button_id))
    else:
        return False


def on_command(name_command):
    if isinstance(name_command, str):
        if not name_command.startswith("/"):
            name_command = f"/{name_command}"
        return Operators(lambda msg: bool(name_command.strip() == msg.text.strip()))
    else:
        return False

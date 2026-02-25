from random import randint
import re


def parse_text(text: str, guid: str = None, link: str = None):
    markers = [
        ("@@", "MentionText"),
        ("``", "Mono"),
        ("**", "Bold"),
        ("$$", "Italic"),
        ("~~", "Strike"),
        ("__", "Underline"),
        ("||", "Spoiler"),
        ("##", "Link"),
    ]
    markers.sort(key=lambda x: -len(x[0]))
    result = []
    clean_parts = []
    pos = 0
    i = 0
    n = len(text)
    stack = []
    while i < n:
        matched = False
        for marker, mtype in markers:
            ml = len(marker)
            if text.startswith(marker, i):
                if stack and stack[-1][0] == marker:
                    open_marker, open_type, start_pos, raw_start = stack.pop()
                    segment_raw = text[raw_start + ml : i]
                    length = pos - start_pos
                    if length > 0:
                        if open_type == "MentionText" and guid:
                            mt = (
                                "User"
                                if guid.startswith("u0")
                                else ("Group" if guid.startswith("g0") else "User")
                            )
                            result.append(
                                {
                                    "type": "MentionText",
                                    "mention_text_object_guid": guid,
                                    "from_index": start_pos,
                                    "length": length,
                                    "mention_text_object_type": mt,
                                }
                            )
                        elif open_type == "Link":
                            url_value = link or segment_raw
                            result.append(
                                {
                                    "type": "Link",
                                    "from_index": start_pos,
                                    "length": length,
                                    "link": {
                                        "type": "hyperlink",
                                        "hyperlink_data": {"url": url_value},
                                    },
                                }
                            )
                        else:
                            result.append(
                                {
                                    "type": open_type,
                                    "from_index": start_pos,
                                    "length": length,
                                }
                            )
                    i += ml
                    matched = True
                    break
                else:
                    if text.find(marker, i + ml) == -1:
                        clean_parts.append(marker)
                        pos += ml
                        i += ml
                        matched = True
                        break
                    stack.append((marker, mtype, pos, i))
                    i += ml
                    matched = True
                    break
        if matched:
            continue
        clean_parts.append(text[i])
        pos += 1
        i += 1
    while stack:
        marker, _, _, _ = stack.pop()
        clean_parts.append(marker)
        pos += len(marker)
    clean_text = "".join(clean_parts)
    L = len(clean_text)
    safe = []
    for part in result:
        fi = part["from_index"]
        ln = part["length"]
        if fi < 0 or fi >= L:
            continue
        if fi + ln > L:
            ln = L - fi
        if ln <= 0:
            continue
        part["length"] = ln
        safe.append(part)
    return safe


def makeJsonResend(guid, file_inline):
    return {
        "object_guid": guid,
        "rnd": randint(100000, 999999999),
        "file_inline": file_inline,
        "text": "868937185613347",
    }


def deleteRSAset(key):
    return key.replace("-----BEGIN RSA PRIVATE KEY-----\n", "").replace(
        "\n-----END RSA PRIVATE KEY-----", ""
    )

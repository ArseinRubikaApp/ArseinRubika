from enum import Enum


class Enums(str, Enum):
    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)


class ButtonTypeEnum(str, Enum):
    Simple = "Simple"
    Selection = "Selection"
    Calendar = "Calendar"
    NumberPicker = "NumberPicker"
    StringPicker = "StringPicker"
    Location = "Location"
    CameraImage = "CameraImage"
    CameraVideo = "CameraVideo"
    GalleryImage = "GalleryImage"
    GalleryVideo = "GalleryVideo"
    File = "File"
    Audio = "Audio"
    RecordAudio = "RecordAudio"
    Textbox = "Textbox"
    Link = "Link"
    AskMyPhoneNumber = "AskMyPhoneNumber"
    AskMyLocation = "AskMyLocation"
    Barcode = "Barcode"


class ChatTypeEnum(Enums):
    User = "User"
    Bot = "Bot"
    Group = "Group"
    Channel = "Channel"


class FileTypeEnum(Enums):
    File = "File"
    Image = "Image"
    Voice = "Voice"
    Video = "Video"
    Music = "Music"
    Gif = "Gif"


class ForwardedFromEnum(Enums):
    User = "User"
    Channel = "Channel"
    Bot = "Bot"


class PollStatusEnum(Enums):
    Open = "Open"
    Closed = "Closed"


class ButtonSelectionTypeEnum(Enums):
    TextOnly = "TextOnly"
    TextImgBig = "TextImgBig"
    TextImgThu = "TextImgThu"


class ButtonSelectionSearchEnum(Enums):
    Local = "Local"
    Api = "Api"


class ButtonSelectionGetEnum(Enums):
    Local = "Local"
    Api = "Api"


class ButtonCalendarTypeEnum(Enums):
    DatePersian = "DatePersian"
    DateGregorian = "DateGregorian"


class ButtonTextboxTypeKeypadEnum(Enums):
    String = "String"
    Number = "Number"


class ButtonTextboxTypeLineEnum(Enums):
    SingleLine = "SingleLine"
    MultiLine = "MultiLine"


class ButtonLocationTypeEnum(Enums):
    Picker = "Picker"
    View = "View"


class MessageSenderEnum(str, Enum):
    User = "User"
    Bot = "Bot"


class UpdateTypeEnum(Enums):
    UpdatedMessage = "UpdatedMessage"
    NewMessage = "NewMessage"
    RemovedMessage = "RemovedMessage"
    StartedBot = "StartedBot"
    StoppedBot = "StoppedBot"


class ChatKeypadTypeEnum(Enums):
    New = "New"
    Remove = "Remove"


class UpdateEndpointTypeEnum(Enums):
    ReceiveUpdate = "ReceiveUpdate"
    ReceiveInlineMessage = "ReceiveInlineMessage"
    ReceiveQuery = "ReceiveQuery"
    GetSelectionItem = "GetSelectionItem"
    SearchSelectionItems = "SearchSelectionItems"

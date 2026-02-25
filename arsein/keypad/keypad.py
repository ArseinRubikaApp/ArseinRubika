from dataclasses import dataclass, asdict
from typing import List, Optional
from ..enums import *


@dataclass
class Location:
    longitude: str
    latitude: str

    def to_dict(self):
        return asdict(self)


@dataclass
class ButtonSelectionItem:
    text: str
    image_url: Optional[str] = None
    type: Optional[ButtonSelectionTypeEnum] = None

    def to_dict(self):
        data = asdict(self)
        if self.type:
            data["type"] = (
                self.type.value if not isinstance(self.type, str) else self.type
            )
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class ButtonSelection:
    selection_id: str
    search_type: ButtonSelectionSearchEnum
    get_type: ButtonSelectionGetEnum
    items: List[ButtonSelectionItem]
    is_multi_selection: bool
    columns_count: str
    title: str

    def to_dict(self):
        data = asdict(self)
        data["search_type"] = (
            self.search_type.value
            if not isinstance(self.search_type, str)
            else self.search_type
        )
        data["get_type"] = (
            self.get_type.value if not isinstance(self.get_type, str) else self.get_type
        )
        data["items"] = [item.to_dict() for item in self.items]
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class ButtonCalendar:
    type: ButtonCalendarTypeEnum
    min_year: str
    max_year: str
    title: str
    default_value: Optional[str] = None

    def to_dict(self):
        data = asdict(self)
        data["type"] = self.type.value if not isinstance(self.type, str) else self.type
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class ButtonNumberPicker:
    min_value: str
    max_value: str
    title: str
    default_value: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ButtonStringPicker:
    items: List[str]
    default_value: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class ButtonLocation:
    default_pointer_location: Location
    default_map_location: Location
    type: ButtonLocationTypeEnum
    title: Optional[str] = None

    def to_dict(self):
        data = asdict(self)
        data["type"] = self.type.value if not isinstance(self.type, str) else self.type
        data["default_pointer_location"] = self.default_pointer_location.to_dict()
        data["default_map_location"] = self.default_map_location.to_dict()
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class ButtonTextbox:
    type_line: ButtonTextboxTypeLineEnum
    type_keypad: ButtonTextboxTypeKeypadEnum
    place_holder: Optional[str] = None
    title: Optional[str] = None
    default_value: Optional[str] = None

    def to_dict(self):
        data = asdict(self)
        data["type_line"] = (
            self.type_line.value
            if not isinstance(self.type_line, str)
            else self.type_line
        )
        data["type_keypad"] = (
            self.type_keypad.value
            if not isinstance(self.type_keypad, str)
            else self.type_keypad
        )
        return {k: v for k, v in data.items() if v is not None}


@dataclass
class Button:
    id: str
    type: ButtonTypeEnum
    button_text: str
    button_selection: Optional[ButtonSelection] = None
    button_calendar: Optional[ButtonCalendar] = None
    button_number_picker: Optional[ButtonNumberPicker] = None
    button_string_picker: Optional[ButtonStringPicker] = None
    button_location: Optional[ButtonLocation] = None
    button_textbox: Optional[ButtonTextbox] = None

    def to_dict(self):
        data = asdict(self)
        data["type"] = self.type.value if not isinstance(self.type, str) else self.type

        if self.button_selection:
            data["button_selection"] = self.button_selection.to_dict()
        if self.button_calendar:
            data["button_calendar"] = self.button_calendar.to_dict()
        if self.button_number_picker:
            data["button_number_picker"] = self.button_number_picker.to_dict()
        if self.button_string_picker:
            data["button_string_picker"] = self.button_string_picker.to_dict()
        if self.button_location:
            data["button_location"] = self.button_location.to_dict()
        if self.button_textbox:
            data["button_textbox"] = self.button_textbox.to_dict()

        return {k: v for k, v in data.items() if v is not None}


@dataclass
class KeypadRow:
    buttons: List[Button]

    def to_dict(self):
        return {"buttons": [btn.to_dict() for btn in self.buttons]}


@dataclass
class ChatKeypad:
    rows: List[KeypadRow]

    def to_dict(self, resize_keyboard: bool = True, one_time_keyboard: bool = False):
        return {
            "rows": [row.to_dict() for row in self.rows],
            "resize_keyboard": resize_keyboard,
            "one_time_keyboard": one_time_keyboard,
        }

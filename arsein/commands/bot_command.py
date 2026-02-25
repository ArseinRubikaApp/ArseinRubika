from dataclasses import dataclass, asdict
from typing import List


@dataclass
class BotCommand:
    command: str
    description: str

    def to_dict(self):
        return asdict(self)


@dataclass
class BotCommands:
    commands: List[BotCommand]

    def to_dict(self):
        return [cmd.to_dict() for cmd in self.commands]

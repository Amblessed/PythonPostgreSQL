from typing import List
from models.option import Option

from database import create_poll, get_poll_options, get_latest_poll, get_poll, get_polls


class Poll:
    def __init__(self, title: str, owner: str, _id: int = None):
        self.id = _id
        self.title = title
        self.owner = owner

    def __repr__(self):
        return f"Poll({self.title!r}, {self.owner!r}, {self.id!r})"

    def save(self):
        new_poll_id = create_poll(self.title, self.owner)
        self.id = new_poll_id

    def add_option(self, option_text:str):
        Option(option_text, self.id).save()

    @property
    def options(self) -> List[Option]:
        options = get_poll_options(self.id)
        return [Option(option[1], option[2], option[0]) for option in options]

    @classmethod
    def get(cls, poll_id: int) -> "Poll":
        poll = get_poll(poll_id)
        return cls(poll[1], poll[2], poll[0])

    @classmethod
    def all(cls) -> List["Poll"]:
        polls = get_polls()
        return [cls(poll[1], poll[2], poll[0]) for poll in polls]

    @classmethod
    def latest(cls) -> "Poll":
        poll = get_latest_poll()
        return cls(poll[1], poll[2], poll[0])


from typing import List

from database import add_poll_vote, Vote, add_option, get_option, get_votes_for_option


class Option:
    def __init__(self, option_text: str, poll_id: int, _id: int = None):
        self.id = _id
        self.text = option_text
        self.poll_id = poll_id

    def __repr__(self):
        return f"Poll({self.text!r}, {self.poll_id!r}, {self.id!r})"

    def save(self):
        new_option_id = add_option(self.text, self.poll_id)
        self.id = new_option_id

    @classmethod
    def get(cls, option_id: int) -> "Option":
        option = get_option(option_id)
        return cls(option[1], option[2], option[0])

    def vote(self, username: str):
        add_poll_vote(username, self.id)

    @property
    def votes(self) -> List[Vote]:
        votes = get_votes_for_option(self.id)
        return votes

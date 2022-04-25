from database import create_tables
from models.poll import Poll

NEW_OPTION_PROMPT: str = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll():
    create_tables()
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    poll = Poll(poll_title, poll_owner)
    poll.save()

    while new_option := input(NEW_OPTION_PROMPT):
        poll.add_option(new_option)


prompt_create_poll()

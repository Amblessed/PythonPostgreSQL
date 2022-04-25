import random
from typing import List

from models.poll import Poll
from models.option import Option

from database import create_tables

MENU_PROMPT = """--- Menu ----
1) Vote on a poll
2) Show poll votes
3) Select a random winner from a poll option
4) Exit. 

Enter your choice: """


def list_open_polls():
    polls = Poll.all()
    print()
    for poll in polls:
        print(f"{poll.id}: {poll.title} (created by {poll.owner})")
    print()


def _print_poll_options(options: List[Option]):
    for option in options:
        print(f"{option.id}: {option.text}")


def prompt_vote_poll() -> None:
    list_open_polls()
    poll_id = int(input("\nEnter poll you would like to vote on: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    Option.get(option_id).vote(username)


def show_poll_votes() -> None:
    list_open_polls()
    poll_id = int(input("Enter poll you would like to see votes for: "))
    print()
    options = Poll.get(poll_id).options
    votes_per_option = [len(option.votes) for option in options]
    total_votes = sum(votes_per_option)

    try:
        for option, votes in zip(options, votes_per_option):
            percentage = votes / total_votes * 100
            print(f"{option.text} got {votes} ({percentage:.2f}% of total)")
        print()
    except ZeroDivisionError:
        print("No votes cast for this poll yet")


def randomize_poll_winner() -> None:
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    _print_poll_options(Poll.get(poll_id).options)

    option_id = int(input("Enter which is the winning option, we'll pick a random winner from voters: "))
    votes = Option.get(option_id).votes
    winner = random.choice(votes)
    print(f"The randomly selected winner is {winner[0]}.")


MENU_OPTIONS = {"1": prompt_vote_poll, "2": show_poll_votes, "3": randomize_poll_winner}


def menu():
    create_tables()
    while (selection := input(MENU_PROMPT)) != "4":
        try:
            MENU_OPTIONS[selection]()
        except KeyError:
            print("Invalid input selected. Please try again")


menu()

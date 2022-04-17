# from databaseList import add_entry, get_entries
from database import add_entry, create_table, get_entries

menu = """Please select one of the following options:
1) Add new entry for today.
2) View Entries.
3) Exit.

Your selection: """

welcome = "Welcome to the programming diary"


def add_new_entry():
    entry_content = input("What have you learned today?")
    entry_date = input("Enter the date(or hit enter for today's date): ")
    add_entry(entry_content, entry_date)


def view_entries(entries) -> None:
    for entry in entries:
        print(f"{entry['date']}: {entry['content']}\n")


print(welcome)
create_table()

while (user_input := input(menu)) != "3":
    if user_input == "1":
        add_new_entry()
    elif user_input == "2":
        view_entries(get_entries())
    else:
        print("Invalid option, please try again")

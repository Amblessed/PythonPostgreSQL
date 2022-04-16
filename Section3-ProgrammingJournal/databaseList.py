from datetime import datetime
from typing import List

entries = list()


def add_entry(entry_content: str, entry_date: str):
    if not entry_date:
        entry_date = datetime.today().strftime('%d-%m-%Y')
    entries_dict = {"content": entry_content, "date": entry_date}
    entries.append(entries_dict)


def get_entries() -> List:
    return entries

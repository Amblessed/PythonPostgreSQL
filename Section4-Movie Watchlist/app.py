# from databaseList import add_entry, get_entries
from datetime import datetime

from database import create_tables, add_movie, get_watched_movies, get_movies, watch_movie, add_user, search_movies

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies.
4) Watch a movie
5) View watched movies.
6) Add User to the app.
7) Search for a movie.
8) Exit. 

Your selection: """


def add_new_movie() -> None:
    title: str = input("Movie title: ")
    release_date: str = input("Release date (dd-mm-YYYY): ")
    timestamp = datetime.strptime(release_date, "%d-%m-%Y").timestamp()
    add_movie(title, timestamp)


def add_new_user() -> None:
    user: str = input("Username: ")
    add_user(user)


def print_movies(heading: str, movies) -> None:
    print(f"---- {heading} Movies ----")
    for movie in movies:
        movie_date = datetime.fromtimestamp(movie[2]).strftime("%d %b %Y")
        print(f"{movie[0]}: {movie[1]} released on {movie_date}\n")


def print_watched_movies(user_name: str, watched) -> None:
    print(f" --- {user_name}'s watched movies ---")
    for watch in watched:
        print(f" {watch[1]}\n")


def prompt_watch_movie() -> None:
    user_name = input("Enter your username: ")
    movie_id = input("Movie ID: ")
    watch_movie(user_name, int(movie_id))


def prompt_show_watched_movies():
    username = input("Enter your username: ")
    movies = get_watched_movies(username)
    if movies:
        print_movies(f"Watched", movies)
    else:
        print("That user has no watched movies.")


def prompt_search_movies():
    search_term: str = input("Enter the partial movie title: ")
    movies = search_movies(search_term)
    if movies:
        print_movies("Movies found", movies)
    else:
        print("Found no movies for that search term")


welcome = "Welcome to the watchlist app!"
print(welcome)
create_tables()

while (user_input := input(menu)) != "8":
    if user_input == "1":
        add_new_movie()
    elif user_input == "2":
        print_movies("Upcoming", get_movies(True))
    elif user_input == "3":
        print_movies("All", get_movies())
    elif user_input == "4":
        prompt_watch_movie()
    elif user_input == "5":
        prompt_show_watched_movies()
    elif user_input == "6":
        add_new_user()
    elif user_input == "7":
        prompt_search_movies()
    else:
        print("Invalid input, please try again")

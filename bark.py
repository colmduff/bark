
import commands
from options import Option
import os

def print_options(options):
    for shortcut, option in options.items():
        print(f"({shortcut}) {option}")

def option_choice_is_valid(choice, options):
    return choice in options or choice.upper() in options

def get_option_choice(options):
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid Selection")

        choice = input("Choose an option: ")

    return options[choice.upper()]

def get_user_input(label, required=True):
    value = input(f"{label}: ") or None

    while required and not value:
        value = input(f"{label}: ") or None
    
    return value

def get_new_bookmark_data():
    return{
        "title": get_user_input("Title"),
        "url": get_user_input("URL"),
        "notes": get_user_input("Notes", required=False)
    }

def get_bookmark_id_for_deletion():
    return get_user_input("Enter bookmark ID for deletion")

def clear_screen():
    clear = "cls" if os.name =="nt" else "clear"
    os.system(clear)


def loop():
    options = {
        "A": Option("Add a bookmark", commands.AddBookmarkCommand(),
                    prep_call=get_new_bookmark_data),
        "B": Option("List bookmarks by date", commands.ListBookmarksCommand()),
        "T": Option("List bookmarks by title", commands.ListBookmarksCommand(order_by="title")),
        "D": Option("Delete a bookmark", commands.DeleteBookmarkCommand(),
                    prep_call=get_bookmark_id_for_deletion),
        "Q": Option("Quit", commands.QuitCommand())
    }

    clear_screen()

    print_options(options)
    choose_option = get_option_choice(options)

    clear_screen()
    choose_option.choose()

    _ = input("Press ENTER to return to menu")
    

if __name__ == "__main__":
    commands.CreateBookmarksTableCommand().execute()

    while True:
        loop()




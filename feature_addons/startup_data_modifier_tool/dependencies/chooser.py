# Dependency to store the helper functions that display a menu
# and require the user to make a choice

import sys
from tkinter import filedialog as file_chooser


def user_menu_chooser(menu_choices: str, total_menu_choices: int):
    """Helper function for displaying a menu with choices for the user

    This function is called by a few other functions that need to display
    a menu to the user for them to make a choice. The function just prints

    Args:
        menu_choices (str): A formatted string of how the choices should be
        displayed
        total_menu_choices (int): The maximum number of choices there are

    Returns:
        int: _description_
    """
    # Set the user choice as default to 0 meaning no valid choice was made
    user_choice = 0

    # Create option to quit the whole program and add it to the end of the passed
    # in menu
    total_menu_choices += 1
    quit_choice = total_menu_choices

    # Create menu header and footers
    menu_header = "Please choose one of the following:\n"
    menu_footer = f"[{quit_choice}] Quit the program\n"
    menu_choices = menu_header + menu_choices + menu_footer

    print("\n" + menu_choices)
    user_input = input("What would you like to do? ")

    if (
        not user_input.isnumeric()
        or int(user_input) < 1
        or int(user_input) > total_menu_choices
    ):
        # User didn't choose a valid option
        print("\nThat choice is invalid!")
    else:
        # User chose a valid option, process accordingly
        user_choice = int(user_input)

        # Check if user chose to quit the program
        if user_choice == quit_choice:
            print("\nThank you for using Demord. Have a wonderful day.")
            sys.exit()

    return user_choice


def new_file_chooser():
    """Helper function to have the user choose what type of new file to create

    This function will ask the user to choose whether to create a new startup file with
    default data or with values the user decides

    Args:
        None

    Returns:
        bool: True if the startup file should contain default data, False if not
    """
    # Loop through until user makes a valid choice
    is_default = False
    menu_choices = (
        "[1] Create a new startup file with some default values\n"
        "[2] Create a new startup file with programs that you choose\n"
    )
    total_menu_choices = 2
    quit_loop = False

    while not quit_loop:
        # Ask user what type of new file they want
        user_choice = user_menu_chooser(menu_choices, total_menu_choices)

        if user_choice in range(1, total_menu_choices + 1):
            quit_loop = True
            if user_choice == 1:
                is_default = True

    return is_default


def edit_file_chooser(item_name: str):
    """Helper function to show a file dialog box

    Args:
        item_name: The existing startup item name

    Returns:
        str: The full path of the file that was selected
    """
    file_name = file_chooser.askopenfilename(
        initialdir="C:/Program Files/",
        title="Choose the program executable for {}".format(item_name),
    )
    return file_name

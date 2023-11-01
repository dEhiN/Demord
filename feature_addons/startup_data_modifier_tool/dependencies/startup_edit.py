# Dependency to store the helper functions that are used when
# editing a startup item

from dependencies.chooser import user_menu_chooser, edit_file_chooser
from dependencies.pretty import prettify_startup_item
from dependencies.startup_add import save_startup_item, add_startup_item_arguments


def edit_startup_item(startup_item: dict, json_path: list, json_filename: str):
    """Helper function to edit a single startup item

    This function will take the specific startup item passed in, display it and
    allow the user to edit any part of that item

    Args:
        startup_item (dict): A dictionary with the single startup item

        json_path (list): A list containing the relative or absolute path to
        the JSON file with each list item representing one subfolder from
        Current Working Directory (CWD)

        json_filename (str): The filename of the JSON file

    Returns:
        list: A list containing the updated startup items.
    """
    # Show startup item selected
    prettified_item = prettify_startup_item(startup_item)
    print(prettified_item)
    input("\nPress any key to continue...")

    # Loop through to and ask the user what they want to do
    menu_choices = (
        "[1] Edit item name\n"
        "[2] Edit item description\n"
        "[3] Edit item program path\n"
        "[4] Edit or add item arguments\n"
        "[5] Show startup data\n"
        "[6] Save startup data to disk\n"
        "[7] Return to the previous menu\n"
    )
    total_menu_choices = 7
    quit_loop = False

    while not quit_loop:
        user_choice = user_menu_chooser(menu_choices, total_menu_choices)

        match user_choice:
            case 1:
                startup_item["Name"] = edit_startup_item_name(startup_item["Name"])
            case 2:
                startup_item["Description"] = edit_startup_item_description(
                    startup_item["Description"]
                )
            case 3:
                startup_item["FilePath"] = edit_startup_item_program_path(
                    startup_item["Name"], startup_item["FilePath"]
                )
            case 4:
                arg_count = startup_item["ArgumentCount"]
                temp_arg_list = []

                # Check if startup item has arguments
                if arg_count > 0:
                    temp_arg_list = edit_startup_item_arguments_list(
                        True, arg_count, startup_item["ArgumentList"]
                    )
                else:
                    temp_arg_list = edit_startup_item_arguments_list(False)

                # Update the startup_item dictionary
                startup_item["ArgumentCount"] = len(temp_arg_list)
                startup_item["ArgumentList"] = temp_arg_list.copy()
            case 5:
                print(prettify_startup_item(startup_item))
            case 6:
                write_status, return_message = save_startup_item(
                    startup_item, json_path, json_filename
                )

                print("\nAttempt to read in startup data from file was...")
                if write_status:
                    print("...successful!")
                else:
                    print("...not successful!")
                print(
                    "This functionality is still under construction...nothing was saved...try again later..."
                )
            case 7:
                quit_loop = True

    return startup_item


def edit_startup_item_name(item_name: str):
    """Helper function to change the name of a startup item

    Args:
        item_name (str): The existing startup item name

    Returns:
        str: The new startup item name
    """
    print("\nThe current name for this startup item is:", item_name)
    new_name = input(
        "Please enter a new name or press enter to leave the existing name: "
    )

    if not new_name:
        print("\nNo change was made...")
        new_name = item_name

    return new_name


def edit_startup_item_description(item_description: str):
    """Helper function to change the description of a startup item

    Args:
        item_description (str): The existing startup item description

    Returns:
        str: The new startup item description
    """
    print("\nThe current description for this startup item is:", item_description)
    new_description = input(
        "Please enter a new description or press enter to leave the existing"
        " description: "
    )

    if not new_description:
        print("\nNo change was made...")
        new_description = item_description

    return new_description


def edit_startup_item_program_path(item_name: str, item_path: str):
    """Helper function to change the path of a startup item

    Args:
        item_name (str): The existing startup item name
        item_path (str): The existing startup item absolute path

    Returns:
        str: The new startup item absolute path
    """
    new_path = ""
    print("\nThe current file path for this startup item is:", item_path)
    user_choice = input(
        "Would you like to use the file chooser window to select the new file"
        " path [Y/N]? "
    )

    if user_choice.isalpha():
        if user_choice.upper() == "Y":
            new_path = edit_file_chooser(item_name)
        elif user_choice.upper() == "N":
            input_msg = (
                "Please enter the new path to the program executable in full"
                " or press enter to use the existing path: "
            )
            new_path = input(input_msg)

    if not new_path:
        print("\nNo change was made...")
        new_path = item_path

    return new_path


def edit_startup_item_arguments_list(
    args_exist: bool, arg_count: int = 0, arg_list: list = []
):
    """Helper function to change the arguments list of a
    startup item

    If there are no arguments, this function will ask the
    user if they want to add arguments. If there are
    arguments, this function will allow the user to edit,
    delete, or add arguments. It does so all within this
    function and only calls add_startup_arguments if there
    are no arguments and the user wants to add some.

    Args:
        args_exist (bool): Required to let the function
        know if there are arguments.

        arg_count (int, optional): The number of arguments. Defaults to 0.
        arg_list (list, optional): A list of the arguments. Defaults to [].

    Returns:
        list: A list containing the edited or added
        startup items. If there aren't any arguments, an
        empty list is returned
    """
    new_arg_list = arg_list.copy()
    new_argument = ""

    # Check if there are existing arguments
    if args_exist and arg_count > 0:
        # Initialize all the variables pertaining to the full user menu
        menu_header = ""
        menu_footer = ""
        menu_choices = "[0] Return to previous menu"
        add_choice, delete_choice, cancel_choice, total_menu_choices = (
            0,
            0,
            0,
            0,
        )

        # Loop through the menu until the user cancels
        quit_loop = False
        while not quit_loop:
            # Create a menu listing all the arguments
            arg_items_menu = []
            for index in range(0, arg_count):
                arg_items_menu.append(
                    f"[{index + 1}] Edit argument {index + 1}: {new_arg_list[index]}\n"
                )

            # Generate the full menu
            add_choice = arg_count + 1
            delete_choice = arg_count + 2
            cancel_choice = arg_count + 3
            total_menu_choices = cancel_choice
            menu_footer = (
                f"[{add_choice}] Add a new argument\n"
                + f"[{delete_choice}] Delete an argument\n"
                + f"[{cancel_choice}] Return to the previous menu\n"
            )

            menu_choices = "".join(arg_items_menu) + menu_footer

            user_choice = user_menu_chooser(menu_choices, total_menu_choices)

            if user_choice == cancel_choice:
                quit_loop = True
            elif user_choice == delete_choice:
                # Generate delete menu
                menu_header = "Please specify which argument you want to delete:\n"

                # Create a menu listing all the arguments
                arg_delete_menu = []
                for index in range(0, arg_count):
                    arg_delete_menu.append(
                        f"[{index + 1}] Argument {index + 1}: {new_arg_list[index]}\n"
                    )

                cancel_choice = arg_count + 1
                menu_footer = f"[{cancel_choice}] Cancel deletion\n"
                menu_choices = "".join(arg_delete_menu) + menu_footer
                total_menu_choices = cancel_choice
                user_choice = 0

                while user_choice == 0:
                    user_choice = user_menu_chooser(menu_choices, total_menu_choices)

                if user_choice < cancel_choice:
                    # Calculate which list index we're working with
                    changed_argument_index = user_choice - 1
                    try:
                        deleted_arg = new_arg_list.pop(changed_argument_index)
                        arg_count = len(new_arg_list)
                        print('\nSuccessfully deleted "' + deleted_arg + '"!')
                    except IndexError:
                        print(
                            "\nUnable to delete argument "
                            + deleted_arg
                            + ". Encountered an IndexError."
                        )
            elif user_choice > 0:
                new_argument = input(
                    "Please enter the new argument or press enter to cancel: "
                )

                if not new_argument:
                    print("\nNo change was made...")
                    continue

                # Calculate which list index we're working with
                changed_argument_index = user_choice - 1

                # Determine if user added a new argument or edited an existing one
                if user_choice == add_choice:
                    # Add the new argument to the argument list and update the
                    # argument list menu
                    new_arg_list.append(new_argument)
                    arg_count = len(new_arg_list)
                    print('\nSuccessfully added "' + new_argument + '"!')
                else:
                    # Edit the existing argument and update the argument list menu
                    new_arg_list[changed_argument_index] = new_argument
    else:
        # Check if user wants to add arguments
        user_choice = input(
            "There are currently no arguments. Would you like to add some"
            " arguments (Y/[N])? "
        )

        if user_choice.isalpha() and user_choice.upper() == "Y":
            new_arg_list = add_startup_item_arguments().copy()
        else:
            print("\nNo change was made...")
            new_arg_list = arg_list.copy()

    return new_arg_list
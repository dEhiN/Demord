# Dependency to store the helper functions that print out data
# structures, such as errors or JSON data, in a prettified way
# to the screen


def prettify_json(json_data: dict):
    """Helper function to prettify the passed-in JSON data

    This function will go through the JSON data dictionary and format the data
    to display it in a human readable manner

    Args:
        json_data (dict): The JSON data to prettify

    Returns:
        str: The JSON data in a nicely formatted manner as a string
    """
    # Create and initialize our function variables
    pretty_data = "\n"
    total_items = json_data["TotalItems"]
    items_list = json_data["Items"]

    # Check edge case where total_items > 0 but items_list is blank
    if total_items > 0 and len(items_list) == 0:
        total_items = 0

    # Start populating pretty_data
    pretty_data += "Number of startup items: " + str(total_items)

    # Go through all the startup items
    for i in range(total_items):
        # Get the specific startup item
        item = items_list[i]

        # Prettify the startup item data
        pretty_data += prettify_startup_item(item)

    # If there are no startup items, display a different message
    if total_items == 0:
        pretty_data = "There are no startup items to display!"

    return pretty_data


def prettify_startup_item(startup_item: dict):
    """Helper function to prettify the passed-in JSON data

    This function will go through the JSON data dictionary and format the data
    to display it in a human readable manner

    Args:
        startup_item (dict): A dictionary representing the JSON data for one startup
        item.

    Returns:
        str: The startup item JSON data in a nicely formatted manner as a string
    """
    # Used to add a new line or tab
    line = "\n"
    tab = "\t"

    startup_data = ""

    # Add the startup item number
    startup_data += line + line + "Startup item #" + str(startup_item["ItemNumber"])

    # Add the startup item name
    startup_data += line + tab + "Item name: " + startup_item["Name"]

    # Add the startup description
    startup_data += line + tab + "Item description: " + startup_item["Description"]

    # Add the file path
    startup_data += line + tab + "Item program path: " + startup_item["FilePath"]

    # Add any argument information
    startup_data += line + tab + "Does this item use arguments: "
    arg_count = startup_item["ArgumentCount"]
    if arg_count > 0:
        startup_data += "Yes"

        # Get the total number of arguments
        startup_data += line + tab + "Total number of arguments used: " + str(arg_count)
        arg_list = startup_item["ArgumentList"]

        # Go through each argument
        if arg_count >= 2:
            counter = 0
            for argument in arg_list:
                counter += 1
                if type(argument) == list:
                    argument = " ".join(argument)

                startup_data += (
                    line
                    + tab
                    + tab
                    + "Argument "
                    + str(counter)
                    + ": "
                    + '"'
                    + argument
                    + '"'
                )
        else:
            startup_data += line + tab + tab + "Argument: " + '"' + arg_list + '"'
    else:
        startup_data += "No"

    return startup_data


def prettify_error(error: Exception, file_mode: str = ""):
    """Helper function to prettify an error or exception

    This function will take an Exception and create a more human-readable
    output for the error

    Args:
        error (Exception): The Exception that was caught (might be most likely
        through a try-except block).

        file_mode (str, optional): If the Exception was caught while working
        with files, this parameter will tell which file mode or what action was
        being taken. Acceptable values are "r" for reading, "w" for writing.
        Defaults to "". If the default value is used or a non-acceptable value
        is used, only the Exception will be returned without any extra
        messaging.

    Returns:
        str: The Exception printed out in a way that makes sense
    """
    return_message = ""
    match file_mode:
        case "r":
            return_message += (
                "Unable to read startup data. Error information is below:\n"
            )
        case "w":
            return_message += (
                "Unable to write startup data. Error information is below:\n"
            )
        case _:
            pass
    return_message += str(type(error).__name__) + " - " + str(error)
    return return_message
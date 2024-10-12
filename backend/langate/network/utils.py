import random
import json

def generate_dev_name():
    """
        Generate a random device name based on a list of names
    """
    # prevent circular import
    from langate.network.models import Device

    try:
        with open("assets/misc/device_names.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            taken_names = Device.objects.values_list("name", flat=True)

            if len(taken_names) < len(lines) :
                n = random.choice(lines)
                while n in taken_names:
                    n = random.choice(lines)
                return n

            else:
                return random.choice(lines)

    except FileNotFoundError:
        return "MISSINGNO"

def get_mark(user=None):
    """
        Get a mark from the settings based on random probability
    """
    # prevent circular import
    from langate.settings import SETTINGS

    # If the user is not None, get the mark from the user's game
    if user:
        if user.tournament:
            if SETTINGS["games"] and SETTINGS["games"][user.tournament]:
                return SETTINGS["games"][user.tournament]

    # Get random between 0 and 1
    random_choice = random.random()

    # for each mark in the settings
    total = 0
    for mark in SETTINGS["marks"]:
        if random_choice <= mark["priority"] + total:
            return mark["value"]
        total += mark["priority"]

    # It should never reach this point but if it does, return the first mark
    return SETTINGS["marks"][0]["value"]

def validate_marks(marks):
    """
    Validate the marks data
    """
    # Check if the marks are not empty
    if not marks:
        return False

    # Check if the marks are a list
    if not isinstance(marks, list):
        return False

    # Check if the marks are a list of dictionaries
    for mark in marks:
        if not isinstance(mark, dict):
            return False

    # Check if the marks have the right keys
    for mark in marks:
        if "name" not in mark or "value" not in mark or "priority" not in mark:
            return False

    # Check if the marks have the right types
    for mark in marks:
        if not isinstance(mark["name"], str) or not isinstance(mark["value"], int) or not (isinstance(mark["priority"], int) or isinstance(mark["priority"], float)):
            return False

    # Check if the marks have the right values
    sum = 0
    for mark in range(len(marks)):
        sum += marks[mark]["priority"]
    if sum != 1:
        return False

    return True

def validate_games(games):
    """
    Validate the games data
    """
    # Check if the games are not empty
    if not games:
        return False

    # Check if the games are a dictionary
    if not isinstance(games, dict):
        return False

    # Check if the games have the right keys
    for game in games:
        if not isinstance(game, str):
            return False
        if not isinstance(games[game], int):
            return False

    return True

def save_settings(new_settings):
    """
    Save the settings to the settings.json file
    """
    with open("assets/misc/settings.json", "w") as f:
        json.dump(new_settings, f, indent=2)

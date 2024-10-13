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

                existing_marks = [
                  mark
                  for mark in SETTINGS["games"][user.tournament]
                  if mark in [x["value"] for x in SETTINGS["marks"]]
                ]

                mark_proba = [
                  mark_data["priority"]
                  for mark in existing_marks
                  for mark_data in SETTINGS["marks"]
                  if mark_data["value"] == mark
                ]

                # Chose a random mark from the user's tournament based on the probability
                return random.choices(existing_marks, weights=mark_proba)[0]

    # Get a random mark from the settings based on the probability
    return random.choices(
      [mark["value"] for mark in SETTINGS["marks"]],
      weights=[mark["priority"] for mark in SETTINGS["marks"]]
    )[0]

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
    Validate the games data.
    The games data is a dictionary with the tournament name as key and a list of marks as value.
    For example:
    {
        "tournament1": [100, 101, 102],
        "tournament2": [100, 103]
    }
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
        if not isinstance(games[game], list):
            return False
        for mark in games[game]:
            if not isinstance(mark, int):
                return False

    return True

def save_settings(new_settings):
    """
    Save the settings to the settings.json file
    """
    with open("assets/misc/settings.json", "w") as f:
        json.dump(new_settings, f, indent=2)

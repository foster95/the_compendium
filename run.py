"""
Dependencies imports
"""
from dataclasses import field
import gspread
from google.oauth2.service_account import Credentials

import random

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

"""Code from Love Sandwiches Walkthrough"""
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD.open('the_compendium')

""" Global variables to be used to validate race, class,
allignment, proficiencies"""

ALLOWED_RACES = [
    "Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Tiefling",
    "Gnome", "Half-Elf", "Half-Orc"
]

ALLOWED_CLASSES = [
    "Fighter", "Wizard", "Rogue", "Cleric", "Paladin", "Druid", "Barbarian",
    "Bard", "Monk", "Ranger", "Sorcerer", "Warlock"
]

ALLOWED_ALIGNMENTS = [
    "Lawful Good", "Neutral Good", "Chaotic Good",
    "Lawful Neutral", "True Neutral", "Chaotic Neutral",
    "Lawful Evil", "Neutral Evil", "Chaotic Evil"
]

ALLOWED_PROFICIENCIES = [
    "Athletics", "Acrobatics", "Stealth", "Perception",
    "Arcana", "History", "Insight", "Medicine",
    "Nature", "Religion", "Deception", "Intimidation",
    "Performance", "Persuasion", "Sleight Of Hand", "Investigation",
    "Animal Handling", "Survival"
]
"""
Global variables for the stat keys to be used in the ammend
stats section of compendium
"""
STAT_KEYS = [
    "Strength", "Dexterity", "Constitution", "Intelligence",
    "Wisdom", "Charisma"
    ]


# Code assistance from mentor Spencer Barribal
def parse_stats_string(stats_str: str) -> dict:
    """
    Convert 'Strength: 12, Dexterity: 10, ...' etc into a dictionary
    with proper keys/ints. Missing stats are filled with 10 by default.
    """
    result = {k: 10 for k in STAT_KEYS}
    if not stats_str:
        return result
    for chunk in stats_str.split(","):
        if ":" not in chunk:
            continue
        key, val = chunk.split(":", 1)
        key = key.strip().title()
        try:
            result[key] = int(val.strip())
        except ValueError:
            pass  # ignore bad values
    return result


def format_stats_string(stats: dict) -> str:
    """
    Shows character's statistics in a formatted string.
    """
    return ", ".join(f"{k}: {int(stats.get(k, 10))}" for k in STAT_KEYS)


def format_modifiers_string(stats: dict) -> str:
    """
    Shows character's ability score modifiers in a formatted string.
    """
    mods = calculate_modifiers(stats)
    return ", ".join(f"{k}: {mods.get(k, 0):+d}" for k in STAT_KEYS)


def update_row_fields(sheet, row: int, fields: dict) -> None:
    """
    Update specific named columns in a row by header name.
    """
    headers = sheet.row_values(1)
    for name, value in fields.items():
        if name in headers:
            col_idx = headers.index(name) + 1
            sheet.update_cell(row, col_idx, value)


def calculate_modifiers(stats):
    """
    Function to calculate ability score modifiers
    """
    modifiers = {}
    for stat, value in stats.items():
        modifiers[stat] = (value - 10) // 2
    return modifiers


def get_stored_characters():
    """
    Function to get stored characters from the Google Sheet
    and show in terminal
    """
    try:
        sheet = SHEET.worksheet('Stored Characters')
        characters = sheet.get_all_records()
        if characters:
            for character in characters:
                print(f"\nName: {character.get('Name', '')}")
                print(f"Race/Species: {character.get('Race/Species', '')}")
                print(f"Class: {character.get('Class', '')}")
                stats_str = character.get('Statistics', '')
                stats_dict = parse_stats_string(stats_str)
                print("Statistics:")
                for stat, value in stats_dict.items():
                    modifier = calculate_modifiers(stats_dict)[stat]
                    sign = "+" if modifier >= 0 else ""
                    print(f"  {stat}: {value} ({sign}{modifier})")
                modifiers = character.get('Modifiers', '')
                if modifiers:
                    print(f"Modifiers:")
                    for mod in modifiers.split(','):
                        print(f"  {mod.strip()}")
                proficiencies = character.get('Proficiencies', '')
                if proficiencies:
                    print(f"Proficiencies: {proficiencies}")
                print(f"Alignment: {character.get('Alignment', '')} \n")

            while True:
                choice = input(
                    "Please choose an option from the below:\n"
                    "[1] Amend a character in The Compendium \n"
                    "[0] Return to main menu \n"
                    "\nEnter your choice: \n"
                    ).strip()
                if choice == "1":
                    exit_to_main_menu = amend_stored_character(characters)
                    if exit_to_main_menu:
                        break
                elif choice == "0":
                    print("\nReturning to main menu...\n")
                    break
                else:
                    print(
                        "Invalid choice. You must choose from the"
                        " options above.\n"
                        )
        return characters
    except Exception as e:
        print(
            f"Oh no! An error occurred while"
            f" fetching: {e}. Returning to main menu... \n"
            )
        return


def amend_stored_character(characters):
    """
    Function to amend a character stored in The Compendium
    """
    print("Choose a character from The Compendium to amend.\n")

    name = input(
        "Enter the name of the character"
        " you want to amend. To return to "
        "the main menu type 0: \n"
        ).strip()
    character = next((c for c in characters if c.get('Name', '').strip().lower() == name.lower()), None)

    if name == "0":
        print("\nReturning to main menu...")
        return True

    if not character:
        print(f"Character not found: {name}")
        return

    try:
        sheet = SHEET.worksheet('Stored Characters')
    except Exception as e:
        print(f"Oh no! Could not open worksheet: {e}")
        return

    cell = sheet.find(character['Name'])
    if not cell:
        print(f"Character {name} not found in the sheet.")
        return
    row = cell.row

    while True:
        print(f"Amending: {character.get('Name','(unknown)')}")
        print("\nFields you can amend:\n"
              "[1] Class\n"
              "[2] Statistics\n"
              "[3] Proficiencies\n"
              "[4] Alignment\n"
              "[0] Return to main menu\n"
              )

        # Allows user to choose field to ammend or breakout to main menu
        choice = input("Enter your choice:\n").strip()
        if choice == "1":
            amend_class(character, sheet, row)

        elif choice == "2":
            amend_statistics(character, sheet, row)

        elif choice == "3":
            amend_proficiencies(character, sheet, row)

        elif choice == "4":
            amend_alignment(character, sheet, row)

        elif choice == "0":
            print("\nReturning to main menu...")
            return True

        else:
            print("Invalid choice. You must choose either 0, 1, 2, 3 or 4")


def amend_class(character, sheet, row):
    """
    Function to allow user to ammend class
    """
    current_class = [c.strip() for c in character.get('Class', '').split(',') if c.strip()]
    print(f"\nCurrent Class: {', '.join(current_class) if current_class else '(none)'}")
    print("Allowed Classes: ", ", ".join(ALLOWED_CLASSES))

    while True:
        action = input(
            "\nDo you want to add a class? \n"
            "[1] Yes \n"
            "[0] Return to character amendment choices \n"
            "Enter your choice: \n"
            ).strip()

        if action == "0":
            print("Returning to character amendment choices...\n")
            return

        elif action == "1":
            new_class = input(
                "Enter new class or type 0 to return"
                " to character amendment choices: \n"
                ).strip().title()
            if new_class == "0":
                print("Returning to character amendment choices...\n")
                return
            if not new_class:
                continue
            if new_class not in ALLOWED_CLASSES:
                print("Not an allowed class. Try again.")
                continue
            if new_class in current_class:
                print("Character already has this class.")
                continue
            current_class.append(new_class)
            character['Class'] = ', '.join(current_class)
            try:
                update_row_fields(sheet, row, {"Class": character['Class']})
                print(f"\nUpdated Class to {character['Class']}.\n")
            except Exception as e:
                print(f"\nOh no! Error updating sheet: {e}")
        else:
            print("Invalid choice. Please choose from the options above.")


def amend_statistics(character, sheet, row):
    """
    Function to allow user to ammend character statistics
    """
    current_stats_str = character.get('Statistics', '')
    stats = parse_stats_string(current_stats_str)

    while True:
        print("\nWhich statistic do you want to change?")
        for k in STAT_KEYS:
            print(f"{k} (current {stats.get(k, 10)})")

        # Prompt user for which stat to change
        chosen_key = input(
            "\nType the statistic name exactly as shown above."
            " To return back to the character amendment"
            " choices, type 0: \n"
            ).strip().title()
        if chosen_key == "0":
            print("Returning to character amendment choices...\n")
            return
        if chosen_key not in STAT_KEYS:
            print("Invalid statistic. Please enter one from the list above.")
            continue

        # Ask for new value
        try:
            new_val = int(input(
                f"\nEnter new value for {chosen_key} (1-20): \n"
                ).strip())
            if not 1 <= new_val <= 20:
                print("\nValue must be between 1 and 20.")
                continue
            if new_val == stats.get(chosen_key, 10):
                print(f"\nCharacter already has {chosen_key} = {new_val}. Try again.")
                continue
        except ValueError:
            print("Please enter a whole number between 1 and 20.")
            continue

        # Apply change
        stats[chosen_key] = new_val
        new_stats_str = format_stats_string(stats)
        new_mods_str = format_modifiers_string(stats)
        character['Statistics'] = new_stats_str
        character['Modifiers'] = new_mods_str

        try:
            update_row_fields(sheet, row, {"Statistics": new_stats_str, "Modifiers": new_mods_str})
            print(f"\nUpdated {chosen_key} and recalculated modifiers.\n")
        except Exception as e:
            print(f"\nOh no! Error updating sheet: {e}")

        more_updates = input(
            "Do you want to amend another statistic? (yes/no): \n"
            ).strip().lower()
        if more_updates != "yes":
            break


def amend_proficiencies(character, sheet, row):
    """
    Function to allow user to ammend character proficiency
    """
    current_proficiencies = [p.strip() for p in character.get('Proficiencies', '').split(',') if p.strip()]
    print(f"\nCurrent Proficiencies: {', '.join(current_proficiencies) if current_proficiencies else '(none)'}")
    print("Allowed Proficiencies: ", ", ".join(ALLOWED_PROFICIENCIES))

    while True:
        action = input(
            "\nDo you want to add or remove a proficiency? \n"
            "[1] Add a proficiency \n"
            "[2] Remove a proficiency \n"
            "[0] Return to character amendment choices \n"
            "\nEnter your choice: \n"
            ).strip()

        if action == "0":
            # Correctly exits the while loop, not the whole function
            print("Returning to character amendment choices...\n")
            return

        elif action == "1":
            # Launch proficiency addition. If character already
            # has 4 proficiencies, they cannot add more and
            # are prompted to remove a proficiency instead
            if len(current_proficiencies) >= 4:
                print(
                    "\nMaximum of 4 proficiencies reached."
                    " Remove one first if you want to add another."
                    )
                continue

            print(
                f"\nCurrent Proficiencies: {', '.join(current_proficiencies)}"
                )
            new_proficiency = input(
                "Enter a proficiency to add, with a comma"
                " between each proficiency"
                " or type 0 to return to character amendment choices: \n"
            ).strip().title()

            if not new_proficiency:
                continue

            added_proficiency = [p.strip() for p in new_proficiency.split(",") if p.strip()]

            for new_proficiency in added_proficiency:
                if len(current_proficiencies) >= 4:
                    print(
                        "\nMaximum of 4 proficiencies reached."
                        " You cannot add another proficiency."
                        )
                    break
                if new_proficiency == "0":
                    print("Returning to character amendment choices...\n")
                    return
                if new_proficiency not in ALLOWED_PROFICIENCIES:
                    print("Not an allowed proficiency. Try again.")
                    continue
                if new_proficiency in current_proficiencies:
                    print(f"Character already has {new_proficiency}.")
                    continue
                current_proficiencies.append(new_proficiency)
                print(f"{new_proficiency} added to proficiencies.")

            character['Proficiencies'] = ", ".join(current_proficiencies)
            try:
                update_row_fields(sheet, row, {"Proficiencies": character['Proficiencies']})
            except Exception as e:
                print(f"Error updating sheet: {e}")

        elif action == "2":
            # Launch proficiency removal. If character has no proficiencies,
            # they cannot remove any and are prompted to add a
            # proficiency instead
            if not current_proficiencies:
                print(
                    "No proficiencies to remove."
                    " Please add a proficiency first."
                    )
                continue

            print(
                f"\nCurrent Proficiencies: {', '.join(current_proficiencies)}"
                )
            proficiency_to_remove = input(
                "Enter a proficiency to remove, with a"
                " comma between each proficiency or type"
                " 0 to return to character amendment choices): \n"
                ).strip().title()
            if proficiency_to_remove == "0":
                print("Returning to character amendment choices...\n")
                continue

            removed_proficiencies = [p.strip() for p in proficiency_to_remove.split(",") if p.strip()]
            for proficiency_to_remove in removed_proficiencies:
                if proficiency_to_remove not in current_proficiencies:
                    print(
                        f"{proficiency_to_remove} is not in"
                        " current proficiencies."
                        )
                    continue
                current_proficiencies.remove(proficiency_to_remove)
                print(f"{proficiency_to_remove} removed from proficiencies.")

                character['Proficiencies'] = ", ".join(current_proficiencies)
                try:
                    update_row_fields(sheet, row, {"Proficiencies": character['Proficiencies']})
                except Exception as e:
                    print(f"Error updating sheet: {e}")


def amend_alignment(character, sheet, row):
    current_alignment = character.get('Alignment', '')
    print(f"\nCurrent Alignment: {current_alignment}")
    print("Allowed Alignments: ", ", ".join(ALLOWED_ALIGNMENTS))
    while True:
        new_alignment = input(
            "\nEnter new alignment or type 0 to return"
            " to character ammendment choices: \n"
            ).strip().title()
        if new_alignment == "0":
            print("Returning to character amendment choices...\n")
            return
        if not new_alignment:
            print("No changes made to alignment.")
            break
        if new_alignment not in ALLOWED_ALIGNMENTS:
            print("Not an allowed alignment. Try again.")
            continue
        if new_alignment == current_alignment:
            print("Alignment is already set to this value.")
            continue
        character['Alignment'] = new_alignment
        try:
            update_row_fields(sheet, row, {"Alignment": character['Alignment']})
            print(f"\nUpdated Alignment to {character['Alignment']}.\n")
        except Exception as e:
            print(f"\nOh no! Error updating sheet: {e}")
        break
    return character


def create_randomised_character():
    """
    Function to create a new character using prompts from The Compendium.
    At the end of the prompts the user will be given the option to
    add the character to The Compendium and the character will be added
    to the Google Sheet.
    """

    randomised_proficiencies = random.sample(ALLOWED_PROFICIENCIES, 4)
    stats = {
        "Strength": random.randint(1, 20),
        "Dexterity": random.randint(1, 20),
        "Constitution": random.randint(1, 20),
        "Intelligence": random.randint(1, 20),
        "Wisdom": random.randint(1, 20),
        "Charisma": random.randint(1, 20)
    }
    while True:
        # Code to require user to provide required first name
        first_name = input(
            "\nEnter character first name (required): \n"
            ).strip()
        # Code to validate that user has entered a name
        if len(first_name) == 0:
            print(
                "Character name must contain at least one character,"
                " please try again."
                )
            continue
        # Code to validate that user has entered text
        # and not numbers or special characters
        if not first_name.isalpha():
            print(
                "Character name must contain only letters, please try again."
                )
            continue
        break
    while True:
        # Code for user to provide optional last name
        last_name = input("Enter character surname (optional): \n")
        if last_name and not last_name.isalpha():
            print("Surname must contain only letters, please try again.")
            continue
        break
    # Combine first name and last name (if provided)
    character_name = f"{first_name} {last_name}" if last_name else first_name

    randomised_character = {
        "Name": character_name,
        "Race/Species": random.choice(ALLOWED_RACES),
        "Class": random.choice(ALLOWED_CLASSES),
        "Statistics": stats,
        "Proficiencies": randomised_proficiencies,
        "Alignment": random.choice(ALLOWED_ALIGNMENTS),
    }
    return randomised_character


def add_character_to_compendium(character):
    """
    Function to add the randomised character to The Compendium.
    This will add the character to the Google Sheet.
    """
    try:
        sheet = SHEET.worksheet('Stored Characters')

        # Change dictionary stats to a list of
        # values so it can be added to Google Sheet
        stats_dict = character["Statistics"]
        stats_string = ", ".join(f"{stat}: {value}" for stat, value in stats_dict.items())

        # Change proficiencies to a string so it can be
        # added to Google Sheet
        proficiencies_string = ", ".join(character["Proficiencies"])

        # Change modifiers to a string so it can be added to Google Sheet
        # Thanks to RealPython for explaining the +d function in Python
        modifiers = calculate_modifiers(character["Statistics"])
        modifiers_string = ", ".join(f"{stat}: {modifier:+d}" for stat, modifier in modifiers.items())

        # Create a new row in Google Sheet with new generated character data
        new_row = [
            character["Name"],
            character["Race/Species"],
            character["Class"],
            stats_string,
            modifiers_string,
            proficiencies_string,
            character["Alignment"],
        ]
        sheet.append_row(new_row)
        print(
            f"\nCharacter '{character['Name']}' added to The Compendium!"
            " Returning to main menu... \n"
            )
    except Exception as e:
        print(f"Oh no! An error occurred while adding the character: {e}")


def add_premade_character_to_compendium():
    """
    Function to add a character made outside of The Compendium to
    the Google Sheet.
    """

    print("Add your own existing character to The Compendium. \n"
          "Please provide the character's details as prompted. \n"
          "\nTo go back to the main menu at any time, type 0")
    while True:
        # Code for user to provide required first name
        pre_made_first_name = input(
            "Enter character first name (required): \n"
            ).strip()

        # Go back to main menu
        if pre_made_first_name == "0":
            print("Returning to main menu...\n")
            return

        # Code to validate that user has entered a name
        if len(pre_made_first_name) == 0:
            print(
                "Character name must contain"
                " at least one character, please try again."
            )
            continue

        # Code to validate that user has entered text
        # and not numbers or special characters
        if not pre_made_first_name.isalpha():
            print(
                "Character name must contain"
                " only letters, please try again."
            )
            continue
        break
    while True:
        # Code for user to provide optional last name
        pre_made_last_name = input("Enter character surname (optional): \n")

        # Go back to main menu
        if pre_made_last_name == "0":
            print("Returning to main menu...\n")
            return
        if pre_made_last_name and not pre_made_last_name.isalpha():
            print("Surname must contain only letters, please try again.")
            continue
        break

    # Code to combine first name and last name (if provided)
    pre_made_character_name = f"{pre_made_first_name} {pre_made_last_name}" if pre_made_last_name else pre_made_first_name

    # Code for user to provide pre-made base characterists
    # ie race, class, alignment with validation
    while True:
        pre_made_race = input(
            f"\nEnter race/species from the following"
            f" list - \n{', '.join(ALLOWED_RACES)}: \n"
            ).strip().title()
        # Go back to main menu
        if pre_made_race == "0":
            print("Returning to main menu...\n")
            return
        if pre_made_race not in ALLOWED_RACES:
            print("Invalid race. Please choose one from the list.")
        else:
            break

    # Validation for pre-made character class
    while True:
        pre_made_character_class = input(
            f"\nEnter class from the following"
            f" list -\n{', '.join(ALLOWED_CLASSES)}: \n"
            ).strip().title()
        # Go back to main menu
        if pre_made_character_class == "0":
            print("Returning to main menu...\n")
            return
        if pre_made_character_class not in ALLOWED_CLASSES:
            print("Invalid class. Please choose one from the list.")
        else:
            break

    # Validation for pre-made character alignment
    while True:
        pre_made_alignment = input(
            f"\nEnter alignment from the following"
            f" list - \n{', '.join(ALLOWED_ALIGNMENTS)}: \n"
            ).strip().title()
        # Go back to main menu
        if pre_made_alignment == "0":
            print("Returning to main menu...\n")
            return
        if pre_made_alignment not in ALLOWED_ALIGNMENTS:
            print("Invalid alignment. Please choose one from the list.")
        else:
            break

    # Code for user to provide pre-made proficiencies
    pre_made_proficiencies = []
    print(
        f"\nEnter up to 4 proficiencies from the following"
        " list. \nWhen you are done, hit Enter - "
        f"\n{', '.join(ALLOWED_PROFICIENCIES)}:")

    while len(pre_made_proficiencies) < 4:
        raw_input = input("Enter proficiencies (comma-separated): \n").strip()
        # Go back to main menu
        if raw_input == "0":
            print("Returning to main menu...\n")
            return
        if raw_input == "":
            if not pre_made_proficiencies:
                print("You must add four proficiencies.")
                continue
            break
        entries = [item.strip().title() for item in raw_input.split(',')]

        # Warn user if they have entered more than 4 proficiencies
        if len(entries) + len(pre_made_proficiencies) > 4:
            print(
                "You can only add up to 4 proficiencies in total. "
                "Please try again.")
            continue

        for proficiency in entries:
            if len(pre_made_proficiencies) >= 4:
                break
            if proficiency in ALLOWED_PROFICIENCIES:
                if proficiency not in pre_made_proficiencies:
                    pre_made_proficiencies.append(proficiency)
                    print(f"Added: {proficiency} to proficiencies.")
                else:
                    print(f"{proficiency} is already added.\n")
            else:
                print(f"{proficiency} is not a valid proficiency.\n")

    # Code for user to provide pre-made stats
    pre_made_statistics = {}
    for statistic in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
        while True:
            raw_input_val = input(
                f"Enter {statistic} (1-20) or 0 to"
                " return to main menu: "
                ).strip()
            if raw_input_val == "0":
                print("Returning to main menu...\n")
                return None
            try:
                value = int(raw_input_val)
                if 1 <= value <= 20:
                    pre_made_statistics[statistic] = value
                    break
                else:
                    print("Value must be between 1 and 20, please try again.")
            except ValueError:
                print("Please enter a valid statistic number.")
    return {
        "Name": pre_made_character_name,
        "Race/Species": pre_made_race,
        "Class": pre_made_character_class,
        "Alignment": pre_made_alignment,
        "Proficiencies": pre_made_proficiencies,
        "Statistics": pre_made_statistics,
    }


def main():
    """
    Function to launch The Compendium, allowing users to select options.
    To exit the compendium the player should type 0
    """
    print(
            "\nWelcome to the Compendium! \n"
            "Your one stop shop for all your"
            " Dungeons & Dragons character needs! \n")
    while True:
        try:
            print(
                "Please select an option by typing the relevant number into"
                " the terminal: \n"
                "[1] View all characters logged to The Compendium \n"
                "[2] Create a new character using The Compendium's"
                " character generator \n"
                "[3] Add your own existing character to The Compendium \n"
                "[0] Exit\n"
            )

            choice = int(input("Enter your choice: \n"))
            if choice == 1:
                print("Viewing all characters logged to The Compendium...")
                # Code to view all characters loaded to The Compendium
                get_stored_characters()

            elif choice == 2:
                print("Create a new character using The Compendium...")
                # Code to create a new character using
                # The Compendium randomiser
                randomised_character = create_randomised_character()
                # Code to print new randomised character
                print("\nYour new character:")
                for key, value in randomised_character.items():
                    if isinstance(value, dict):
                        print(f"{key}:")
                        for stat, stat_value in value.items():
                            modifier = calculate_modifiers(value)[stat]
                            sign = "+" if modifier >= 0 else ""
                            print(f"  {stat}: {stat_value} ({sign}{modifier})")
                    elif isinstance(value, list):
                        print(f"{key}: {', '.join(value)}")
                    else:
                        print(f"{key}: {value}")
                # Code to add the new randomised character to The Compendium.
                # This will add the character to the Google Sheet.
                add_character_to_compendium(randomised_character)

            elif choice == 3:
                print(
                    "Loading choices to add an existing"
                    " character to The Compendium..."
                )
                pre_made_character = add_premade_character_to_compendium()
                if pre_made_character:
                    print(
                        "\nPlease ensure that the below characteristics are"
                        " correct before adding to The Compendium\n"
                    )
                    print(f"Name: {pre_made_character['Name']}")
                    print(
                        "Race/Species:"
                        f" {pre_made_character['Race/Species']}")
                    print(f"Class: {pre_made_character['Class']}")
                    print(f"Statistics:")
                    for stat, value in pre_made_character['Statistics'].items():
                        modifier = calculate_modifiers(pre_made_character['Statistics'])[stat]
                        sign = "+" if modifier >= 0 else ""
                        print(f" {stat}: {value} ({sign}{modifier})")
                    print(
                        f"Proficiencies: {', '.join(pre_made_character['Proficiencies'])}")
                    print(f"Alignment: {pre_made_character['Alignment']}")
                    confirm = input(
                        "\nDo you want to add this character to"
                        " The Compendium? (type yes or no): \n"
                        ).strip().lower()
                    if confirm == "yes":
                        add_character_to_compendium(pre_made_character)
                        print(
                            "Character added to The Compendium!"
                            " Returning to main menu...\n"
                        )
                    elif confirm == "no":
                        print(
                            "Character not added to The Compendium."
                            " Returning to main menu...\n"
                        )
                    else:
                        print(
                            "Invalid option. You must choose either yes or no."
                            " Character not added to The Compendium."
                        )

            elif choice == 0:
                print("Exiting The Compendium. Goodbye!")
                break
            else:
                print(
                    "Invalid choice, please only enter"
                    " a number between 0 and 3."
                )
        except ValueError:
            print("Please enter a valid number.")


# Launch the program
main()

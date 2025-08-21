"""Dependencies imports"""
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

""" Global variables to be used to validate race, class, allignment, proficiencies"""

ALLOWED_RACES = [
    "Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Tiefling", "Gnome",
    "Half-Elf", "Half-Orc"
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

STAT_KEYS = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

# Code assistance from mentor Spencer Barribal
def parse_stats_string(stats_str: str) -> dict:
    """
    Convert 'Strength: 12, Dexterity: 10, ...' etc into a dictionary with proper keys/ints.
    Missing stats are filled with 10 by default.
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
    """Dict -> 'Strength: 12, Dexterity: 10, ...' in fixed, neat order."""
    return ", ".join(f"{k}: {int(stats.get(k, 10))}" for k in STAT_KEYS)

def format_modifiers_string(stats: dict) -> str:
    """Build the Modifiers string from stats using your calculate_modifiers()."""
    mods = calculate_modifiers(stats)
    return ", ".join(f"{k}: {mods.get(k, 0):+d}" for k in STAT_KEYS)

def update_row_fields(sheet, row: int, fields: dict) -> None:
    """
    Update specific named columns in a row by header name.
    Example: update_row_fields(ws, 5, {"Statistics": "...", "Modifiers": "..."})
    """
    headers = sheet.row_values(1)
    for name, value in fields.items():
        if name in headers:
            col_idx = headers.index(name) + 1
            sheet.update_cell(row, col_idx, value)

def calculate_modifiers(stats):
    """Function to calculate ability score modifiers"""
    modifiers = {}
    for stat, value in stats.items():
        modifiers[stat] = (value - 10) // 2
    return modifiers

def get_stored_characters():
    """Function to get stored characters from the Google Sheet"""
    try:
        sheet = SHEET.worksheet('Stored Characters')
        characters = sheet.get_all_records()
        if characters:
            print("Stored Characters:")
            for character in characters:
                print(f"Name: {character.get('Name', '')}")
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
                choice = input("Please choose an option from the below:\n"
                           "[1] Amend a character in The Compendium \n"
                           "[2] Remove a character from The Compendium \n"
                           "[0] Return to main menu \n"
                           "\nEnter your choice: ").strip()
                if choice == "1":
                    amend_stored_character(characters)
                elif choice == "2":
                    remove_stored_character(character)    
                elif choice == "0":
                    print("\nReturning to main menu...\n")
                    return
                else:
                    print("Invalid choice. You must choose from the options above.\n")
        return characters
    except Exception as e:
        print(f"Oh no! An error occurred while fetching: {e}. Returning to main menu... \n")
        return
    
def amend_stored_character(characters):
    """Amend a character in 'Stored Characters'. Supports targeted Statistics edit."""
    print("Choose a character from The Compendium to amend.\n")

    name = input("Enter the name of the character you want to amend: ").strip()
    character = next((c for c in characters if c.get('Name', '').strip().lower() == name.lower()), None)

    if not character:
        print(f"Character not found: {name}")
        return

    print(f"Amending character: {character.get('Name','(unknown)')}")
    print("Fields you can amend: Name, Race/Species, Class, Statistics, Proficiencies, Alignment")
    field = input("Enter the field you want to amend: ").strip()

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

    #Update statistics 
    if field.lower() in {"statistics", "stats"}:
        current_stats_str = character.get('Statistics', '')
        stats = parse_stats_string(current_stats_str)

        while True:
            print("\nWhich statistic do you want to change?")
            for k in STAT_KEYS:
                print(f"- {k} (current {stats.get(k, 10)})")

            # Ask user for stat to change
            chosen_key = input("Type the statistic name exactly as shown above: ").strip().title()
            if chosen_key not in STAT_KEYS:
                print("Invalid statistic. Please enter one from the list above.")
                continue

            # Ask for new value
            try:
                new_val = int(input(f"Enter new value for {chosen_key} (1-20): ").strip())
                if not 1 <= new_val <= 20:
                    print("Value must be between 1 and 20.")
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
                print(f"Updated {chosen_key} and recalculated modifiers.")
            except Exception as e:
                print(f"Oh no! Error updating sheet: {e}")

            more_updates = input("Do you want to amend another statistic? (yes/no): ").strip().lower()
            if more_updates != "yes":
                break
        return

    if field not in character:
        print(f"Field not found on record: {field}")
        return

    new_value = input(f"Enter the new value for {field}: ").strip()
    character[field] = new_value
    try:
        update_row_fields(sheet, row, {field: new_value})
        print(f"Updated {field} for {character.get('Name','(unknown)')}.")
        print("Returning to main menu \n")
    except Exception as e:
        print(f"Oh no! Error updating sheet: {e}")

def remove_stored_character(character):
    """Function to remove a character from The Compendium. This will also remove
    the character from the Google Sheet"""




def create_randomised_character():
    """
    Function to create a new character using prompts from The Compendium.
    At the end of the prompts the user will be given the option to 
    add the character to The Compendium and the character will be added
    to the Google Sheet.
    """

    print("Create a new character here using The Compendium to provide you your baseline character traits")

    randomised_proficiencies = random.sample(allowed_proficiencies, 4)

    stats = {
        "Strength": random.randint(1, 20),
        "Dexterity": random.randint(1, 20),
        "Constitution": random.randint(1, 20),
        "Intelligence": random.randint(1, 20),
        "Wisdom": random.randint(1, 20),
        "Charisma": random.randint(1, 20)
    }

    while True:
        #Code to require user to provide required first name
        first_name = input("Enter character first name (required): ").strip()
        #Code to validate that user has entered a name
        if len(first_name) == 0:
            print("Character name must contain at least one character, please try again.")
            continue
        #Code to validate that user has entered text and not numbers or special characters
        if not first_name.isalpha():
            print("Character name must contain only letters, please try again.")
            continue
        break

    while True:
        #Code for user to provide optional last name
        last_name = input("Enter character surname (optional): ")
        if last_name and not last_name.isalpha():
            print("Surname must contain only letters, please try again.")
            continue
        break

    #Combine first name and last name (if provided)
    character_name = f"{first_name} {last_name}" if last_name else first_name

    randomised_character = {
        "Name": character_name,
        "Race/Species": random.choice(ALLOWED_RACES),
        "Class": random.choice(ALLOWED_CLASSES  ),
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

        #Change dictionary stats to a list of values so it can be added to Google Sheet
        stats_dict = character["Statistics"]
        stats_string = ", ".join(f"{stat}: {value}" for stat, value in stats_dict.items())

        #Change proficiencies to a string so it can be added to Google Sheet
        proficiencies_string = ", ".join(character["Proficiencies"])

        #Change modifiers to a string so it can be added to Google Sheet
        #Thanks to RealPython for explaining the +d function in Python
        modifiers = calculate_modifiers(character["Statistics"])
        modifiers_string = ", ".join(f"{stat}: {modifier:+d}" for stat, modifier in modifiers.items())

        #Create a new row in Google Sheet with new generated character data
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
        print(f"Character '{character['Name']}' added to The Compendium!")
    except Exception as e:
        print(f"Oh no! An error occurred while adding the character: {e}")

def add_premade_character_to_compendium():
    """Function to add a character made outside of The Compendium to the Google Sheet."""

    print("Add your own existing character to The Compendium. \n" \
          "Please provide the character's details as prompted. \n")

    while True:
        #Code for user to provide required first name
        pre_made_first_name = input("Enter character first name (required): ").strip()
        #Code to validate that user has entered a name
        if len(pre_made_first_name) == 0:
            print("Character name must contain at least one character, please try again.")
            continue
        #Code to validate that user has entered text and not numbers or special characters
        if not pre_made_first_name.isalpha():
            print("Character name must contain only letters, please try again.")
            continue
        break

    while True:
        #Code for user to provide optional last name    
        pre_made_last_name = input("Enter character surname (optional): ")
        if pre_made_last_name and not pre_made_last_name.isalpha():
            print("Surname must contain only letters, please try again.")
            continue
        break

    #Code to combine first name and last name (if provided)
    pre_made_character_name = f"{pre_made_first_name} {pre_made_last_name}" if pre_made_last_name else pre_made_first_name

    #Code for user to provide pre-made base characterists ie race, class, alignment
    #Validation for pre-made character race
    while True:
        pre_made_race = input(f"\nEnter race/species from the following list - {', '.join(ALLOWED_RACES)}: ").strip().title()
        if pre_made_race not in ALLOWED_RACES:
            print("Invalid race. Please choose one from the list.")
        else:
            break

    #Validation for pre-made character class
    while True:
        pre_made_character_class = input(f"\nEnter class from the following list - {', '.join(ALLOWED_CLASSES)}: ").strip().title()
        if pre_made_character_class not in ALLOWED_CLASSES:
            print("Invalid class. Please choose one from the list.")
        else:
            break

    #Validation for pre-made character alignment
    while True:
        pre_made_alignment = input(f"\nEnter alignment from the following list - {', '.join(ALLOWED_ALIGNMENTS)}: ").strip().title()
        if pre_made_alignment not in ALLOWED_ALIGNMENTS:
            print("Invalid alignment. Please choose one from the list.")
        else:
            break

    #Code for user to provide pre-made proficiencies
    pre_made_proficiencies = []
    print(f"\nEnter up to 4 proficiencies from the following list. When you are done, hit Enter - {', '.join(allowed_proficiencies)}:")

    while len(pre_made_proficiencies) < 4:
        raw_input = input("Enter proficiencies (comma-separated): ").strip()

        if raw_input == "":
            if not pre_made_proficiencies:
                print("You must add four proficiencies.")
                continue
            break

        entries = [item.strip().title() for item in raw_input.split(',')]

        #Warn user if they have entered more than 4 proficiencies
        if len(entries) + len(pre_made_proficiencies) > 4:
            print("You can only add up to 4 proficiencies in total. Please try again.")
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

    #Code for user to provide pre-made stats
    pre_made_statistics = {}
    for statistic in ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]:
        while True:
            try:
                value = int(input(f"Enter {statistic} (1-20): "))
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

def launch():
    """
    Function to launch The Compendium, allowing users to select options. 
    To exit the compendium the player should type 0
    """
    print(
            "\nWelcome to the Compendium! \n" \
            "Your one stop shop for all your Dungeon's and Dragon's character needs! \n")
   
    while True:
        try:
            print("Please select an option by typing the relevant number into the terminal: \n" \
            "[1] View all characters logged to The Compendium \n" 
            "[2] Create a new character using The Compendium's character generator \n" 
            "[3] Add your own existing character to The Compendium \n" 
            "[0] Exit\n")

            choice = int(input("Enter your choice: "))
            if choice == 1:
                print("Viewing all characters logged to The Compendium...")

                #Code to view all characters loaded to The Compendium
                get_stored_characters()
            elif choice == 2:
                print("Create a new character using The Compendium...")

                #Code to create a new character using The Compendium as a randomiser
                randomised_character=create_randomised_character()

                #Code to print new randomised character
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
                #Code to add the new randomised character to The Compendium.
                # This will add the character to the Google Sheet.
                add_character_to_compendium(randomised_character)
            elif choice == 3:
                print("Loading choices to add an existing character to The Compendium...")
                pre_made_character=add_premade_character_to_compendium()
                if pre_made_character:
                    print("\nPlease ensure that the below characteristics are correct before adding to The Compendium")
                    print(f"  Name: {pre_made_character['Name']}")
                    print(f"  Race/Species: {pre_made_character['Race/Species']}")
                    print(f"  Class: {pre_made_character['Class']}")
                    print(f"  Statistics:")
                    for stat, value in pre_made_character['Statistics'].items():
                        modifier = calculate_modifiers(pre_made_character['Statistics'])[stat]
                        sign = "+" if modifier >= 0 else ""
                        print(f"    {stat}: {value} ({sign}{modifier})")
                    print(f"  Proficiencies: {', '.join(pre_made_character['Proficiencies'])}")
                    print(f"  Alignment: {pre_made_character['Alignment']}")
                    confirm = input("Do you want to add this character to The Compendium? (type yes or no): ").strip().lower()
                    if confirm == "yes":
                        add_character_to_compendium(pre_made_character)
                        print("Character added to The Compendium!")
                    elif confirm == "no":
                        print("Character not added to The Compendium.")
                    else:
                        print("Invalid option. You must choose either yes or no. Character not added to The Compendium.")
            elif choice == 0:
                print("Exiting The Compendium. Goodbye!")
                break
            else:
                print("Invalid choice, please only enter a number between 0 and 3.")
        except ValueError:
            print("Please enter a valid number.")


launch()
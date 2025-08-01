"""Dependencies imports"""
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

def get_stored_characters():
    """Function to get stored characters from the Google Sheet"""
    try:
        sheet = SHEET.worksheet('Stored Characters')
        characters = sheet.get_all_records()
        if characters:
            print("Stored Characters:")
            for character in characters:
                print(character)
        else:
            print("Oh no! No characters found.")
        return characters
    except Exception as e:
        print(f"Oh no! An error occurred while fetching characters: {e}")
        return []
    
def create_randomised_character():
    """
    Function to create a new character using prompts from The Compendium.
    At the end of the prompts the user will be given the option to add the character to The Compendium
    and the character will be added to the Google Sheet.
    """

    print("Create a new character here using The Compendium to provide you your baseline character traits")

    races = ["Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Tiefling"]
    classes = ["Fighter", "Wizard", "Rogue", "Cleric", "Paladin", "Druid"]
    alignments = ["Lawful Good", "Neutral Good", "Chaotic Good", 
                   "Lawful Neutral", "True Neutral", "Chaotic Neutral",
                   "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
    proficiencies = ["Athletics", "Acrobatics", "Stealth", "Perception",
                    "Arcana", "History", "Insight", "Medicine",
                    "Nature", "Religion", "Deception", "Intimidation",
                    "Performance", "Persuasion"]
    randomised_proficiencies = random.sample(proficiencies, 4)
    
    stats = {
        "Strength": random.randint(1, 20),
        "Dexterity": random.randint(1, 20),
        "Constitution": random.randint(1, 20),
        "Intelligence": random.randint(1, 20),
        "Wisdom": random.randint(1, 20),
        "Charisma": random.randint(1, 20)
    }

    while True:
        character_name = input("Enter character name: ")
        """Code to validate that user has entered a name"""
        if len(character_name) == 0:
            print("Character name must contain at least one character, please try again.")
            continue
        """Code to validate that user has entered text and not numbers or special characters"""
        if not character_name.isalpha():
            print("Character name must contain only letters, please try again.")
            continue
        break

    randomised_character = {
        "Name": character_name,
        "Race/Species": random.choice(races),
        "Class": random.choice(classes),
        "Stats": stats,
        "Proficiencies": randomised_proficiencies,
        "Alignment": random.choice(alignments),
    }
    
    return randomised_character



def launch():
    """
    Function to launch The Compendium, allowing users to select options. 
    To exit the compendium the player should type 0
    """
    while True:
        print(
        "Welcome to the Compendium! \n" \
        "Your one stop shop for all your Dungeon's and Dragon's character needs! \n" \
        "Please select an option: \n" \
        "[1.] View all characters \n" \
        "[2.] Create a new character using The Compendium \n" \
        "[3.] Add your own existing character \n" \
        "[0.] Exit")
        
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                  print("Viewing all characters logged to The Compendium...")

                  """Code to view all characters loaded to The Compendium"""
                  get_stored_characters()
            elif choice == 2:
                  print("Create a new character using The Compendium...")

                  """Code to create a new character using The Compendium as a randomiser"""
                  randomised_character=create_randomised_character()

                  """Code to print new randomised character"""
                  print("\nYour new character:")
                  for key, value in randomised_character.items():
                       if isinstance(value, dict):
                           print(f"{key}:")
                           for stat, stat_value in value.items():
                               print(f"  {stat}: {stat_value}")
                       elif isinstance(value, list):  
                           print(f"{key}: {', '.join(value)}")
                       else:
                           print(f"{key}: {value}")
            elif choice == 3:
                  print("Loading choices to add an existing character to The Compendium...")
                  # Code to add an existing character will go here
            elif choice == 0:
                  print("Exiting the Compendium. Come back soon!")
                  break
            else:
                 print("Invalid choice, please only enter a number between 0 and 3.")
        except ValueError:
            print("Please enter a valid number.")


launch()
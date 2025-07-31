"""Dependencies imports"""
import gspread
from google.oauth2.service_account import Credentials 

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

def get_saved_characters():
    """Function to get saved characters from the Google Sheet"""
    try:
        sheet = SHEET.worksheet('Saved Characters')
        data = sheet.get_all_records()
        return data
    except Exception as e:
        print(f"An error occurred while fetching characters: {e}")
        return []

def launch():
    """Function to launch The Compendium, allowing users to select options. To exit the compendium the player should type 0
    """
    while True:
        print(
        "Welcome to the Compendium! \n" \
        "Your one stop shop for all your Dungeon's and Dragon's character needs! \n" \
        "Please select an option: \n" \
        "1. View all characters \n" \
        "2. Create a new character \n" \
        "0. Exit")
        
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                  print("Viewing all characters...")
            # Code to view all characters would go here
            elif choice == 2:
                  print("Creating a new character...")
            # Code to create a new character would go here
            elif choice == 0:
                  print("Exiting the Compendium. Come back soon!")
                  break
            else:
                 print("Invalid choice, please try again.")
        except ValueError:
            print("Please enter a valid number.")

launch()
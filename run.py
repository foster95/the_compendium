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

stored_characters = SHEET.worksheet('Stored Characters')

characters = stored_characters.get_all_values()

for character in characters:
    print(character)

print("All characters have been printed successfully.")
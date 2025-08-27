Project 03 by Alice Foster

[View live project](https://the-compendium-af-7957ce214c86.herokuapp.com/)

# The Compendium
The Compendium is a Python built project which is built around the concept of character creation for Dungeons and Dragon's (known colloquially as DnD). The project is connected to a Google Sheet and allows users to do the following: See all the characters already logged to the Google Sheet, Create a character using randomised features provided by the Compendium terminal and upload the details of a pre-made DnD character the user already has. Any characters created using The Compendium are automatically uploaded to the Google Sheet. Users can choose if they want to upload the pre-made character to the Google Sheet. 

# Table of Contents
1. Audience
2. Project Logic
3. Current Features
    * Opening Menu
    * View Characters Logged to The Compendium
    * Modifiers
    * Global Variables
    * Amend a Character Logged to The Compendium
        * Amend Classes
        * Amend Statistics
        * Amend Proficiencies
        * Amend Alignments
    * Create a New Character using The Compendium
    * Log a Pre-Made Character
    * Upload a Pre-Made Character to The Compendium
4. Future Features
5. Testing
    * Manual Testing
    * PEP8 CI Python Linter
6. Bugs
7. Deployment
8. Local Deployment
9. Tools and Technologies Used
10. Credits
11. Acknowledgements

Audience
The Compendium is designed for the following audience:
* People who play Dungeons and Dragons (specifically Dungeon Masters) who need to create characters fast, particularly for NPC roles which don't require a huge amount of character detail
* People who play Dungeons and Dragons characters who would like a simple digital record of their own personal characters outside of platforms like DnD Beyond

Project Logic
In order to follow best practise, I created a flowchart using Lucidchart, which maps out the logic of the processes throughout the project

General Project Logic
Ammend Characters Logic

Existing Features
Opening menu
Upon launching the program, users are immediately greeted with a welcome message and the home screen. The welcome message tells the user exactly what the program does and provides them with a short list of options to progress the program. To exit and return to the previous point (or at this point, to leave the program), the user must type 0.

View characters logged to The Compendium
If the uses chooses option 1 they are immediately taken to the list of currently logged characters. This is information that is pulled directly from The_Compendium google sheet and is a real time snapshot of that information shown in the terminal. The information is laid out in the clearest way possible, with breaks between each character to ensure that the user can understand the information shown. 

Modifiers
Within DnD, modifiers play a huge part of character creation. They affect dice rolls and can change reguarly. 

 As such it was really important to me that along with statistics being updated, modifiers were also calculated at the same time, in the clearest possible fashion. When playing DnD, most users will instantly look to their modifier, not their stat. To work out the modifier for each stat, I built the function calculate modifiers. This function is based entirely on the logic behind the DnD modifier system, seen below:

 Taken directly from DnD Beyond:
 | Ability Score | Modifier |
 --- | ---
 1-2 | -4
 3-4 | -3
 5-6 | -2
 7-8 | -1
 9-10 | +0
 11-12 | +1
 13-14 | +2
 15-16 | +3
 17-18 | +4
 19-20 | +5
 
 Using the above logic I created the calculate_modifiers function, which takes the stat, works out its value - 10 and then divides the figure by two

        def calculate_modifiers(stats):
        """
        Function to calculate ability score modifiers
        """
        modifiers = {}
        for stat, value in stats.items():
            modifiers[stat] = (value - 10) // 2
        return modifiers

Global Variables
In order to ensure that the user can only provide information that the program will accept, I create a few global variables. These variables are used in multiple functions across the program, adhering to the DRY principle. 

        ALLOWED_RACES = [
            "Human", "Elf", "Dwarf", "Halfling", "Dragonborn", "Tiefling",
            "Gnome", "Half-Elf", "Half-Orc"
        ]

        ALLOWED_CLASSES = [
            "Fighter", "Wizard", "Rogue", "Cleric", "Paladin", "Druid" "Barbarian","Bard", "Monk", "Ranger", "Sorcerer", "Warlock"
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

By requiring the user to meet these restrictions, the program is immediately not suitable for anyone with HomeBrew characters. HomeBrew characters are charaqcter that don't follow standard Dungeons & Dragons rules. This is particularly relevant with the allowed races option. As of the D5 version of the players handbook, there are currently over 80 races registered in the universe, and this continues to grow. As there are over 80 races in the Dungeons and Dragons universe and I was aware of time, I chose to only include the races that are considered the standard/basic races. However, a further development of the program would include an import of a wider range of races. This would still not allow for HomeBrew characters, but would go a way to making it accessible for players that want to use more unique races.

Ammend a character logged to The Compendium
After the user has trigged the view characters function, they are given the option to either return to the main menu (by typing 0), or alternatively to ammend an individual character. The user is then asked which character they would like to choose, and they are required to type the entire name, with no spelling issues or added special characters, otherwise they will trigger the validation and will not be able to move further into the program. However upon typing the correct name, they will then be greeted with a further sub menu. The sub menu is made up of all of the features that can be adjusted - Class, Statistics, Proficiencies and Alignment. They also have the option to break out of the program and return directly to the main menu.

If a character chooses to change any of their classes, statistics, proficiencies or alignments they must meet the following global variable requirements (these variables are also used for the character randomiser program and for logging a pre-made character)

Once a user has chosen which feature they want to ammend, they can type the number to launch the approporiate program. At all times if the user enters information that is always registered to the character, they should recieve a prompt to state that the character already has that relevant class/alignment/proficiency and ask them to provide something different. The Program is also broken down into further functions. Details of these are below:

Ammend Classes
If the user chooses to launch the Class ammendment option they are told the following information - the current Class associated to the logged character and the allowed classes that the program requires.

A feature of Dungeons & Dragons is that the user can create a character that has multiple classes. This isn't a standardised process, a player has to level up in order to unlock the ability to have multiple classes, and the program currently operates on the assumption that for randomised characters, they should be starting at a L1 with only one class. However, for users that have chosen to multi-class, then they can choose to specifically add a second class. They cannot add the same class already associated to the character, and the second class must be from the allowed classes list.

If the user does not want to add a further class, they can type 0 to return to the character ammendment options. 

Ammend Statistics
If the user chooses to ammend their statistics, they are shown a list of all of their current statistics in the terminal and are prompted to type the name of the statistic that they want to update and hit enter. They are then asked what they want to update their new statistic to. Typically players are unlikely to update more than three statistics at any one time, and provided that the new statistic is accepted by the program, the user is prompted and asked if they want to add any more statistics. 

As with all of the ammendments, the user is required to type the statistic name they wish to ammend exactly, without special characters otherwise this will trigger the validation. If the user tries to update the statistic number to one that is already logged to the character they are told that the character already has this number and asked to try again.

Though it is not seen in the terminal, if the user chooses to update a statistic, the update_modifier function also runs, to ensure that the modifier is updated in line with the statistic number. 

If the user does not want to ammend a statistic, they can type 0 to return to the character ammendment options. 

Ammend Proficiencies
If the user chooses to launch the Proficiencies ammendment option they are told the following information - the current Proficiencies associated to the logged character and the allowed Proficiencies the program requires.

Currently the program restricts users to just four proficencies, and therefore the user is prompted with a submenu for proficiency ammendment. If a user would like to add a proficiency they can choose that option, however if the program already registers four proficiencies are associated to the character, the user will be told that they need to remove an proficiency to add an proficiency. Users are able to bulk add and remove proficiencies, provided they are seperated by a comma but again are limited by no more than four proficiencies. 

If they want to remove they are shown again the current associated proficiencies with the character, and the proficiency removed must match a current proficiency. If it does not, the user will trigger validation and will be asked to remove a proficiency associated with the character. 

If there are less than four proficiencies associated with a character, and the user wants to add a proficiency, they are also shown the current proficinecies associated the character, and are shown the available proficiencies as well. Any proficiency added, must not already be in the current proficiencies, and must also be part of the allowed proficiencies global variable. If either of these things are not true, validation is triggered and the user will be told either that they cannot add a profiency already associated, or that the proficiency they are trying to add, does not meet the allowed proficinecy requirements. 

If the user does not want to ammend a proficiency, they can type 0 to return to the character ammendment options. 

Amend Allignments
If the user chooses to launch the Alignment amendment option they are told the following information - the current Alignment associated to the logged character and the allowed Allignments that the program requires.

If the user wishes to update their Allignment, they must type the new Allignment exactly as listed in the program otherwise they will trigger the validation. A user cannot add the same Alignment already associated to the character.

At the end of any character ammendments, these amendments will be logged and changed on the Google sheet immediately. The user will be brought back to the character ammendment menu and then can choose to amend further fields or return to the main Compendium menu.

Create a new, randomised character using The Compendium
If a user chooses to create a new character they are prompted to provide the following: a first name, which is a required field and a surname, which is an optional field. The program then automatically generates the following using Python's random dependency from the global allowed variables: Race/Species, Class, Statistics, Proficiencies, Alignment.

        randomised_character = {
            "Name": character_name,
            "Race/Species": random.choice(ALLOWED_RACES),
            "Class": random.choice(ALLOWED_CLASSES),
            "Statistics": stats,
            "Proficiencies": randomised_proficiencies,
            "Alignment": random.choice(ALLOWED_ALIGNMENTS),
        }
        return randomised_character

The character is automatically logged to The Compendium, and is added as a new row on the Google sheet, which a user can then go in and ammend, as detailed above. Once the program has finished running, the user is automatically returned to the main menu of The Compendium. 

Log a pre-made Character
If a user chooses to log a pre-made character outside of the randomiser, they are first prompted to enter a required first name and an optional surname. They are then prompted to provide the character's race/species, Class, Alignment, up to four proficiencies and their statistics. All of the information entered must match the allowed variables otherwise they will recieve a prompt informing them that the information is not valid. As with the character amendment options, multiple proficiencies can be typed at once to save the user time. At the end of this process, the terminal will display all of this information to the user and they will be asked if they wish to add the character to the Compendium. If they answer yes, the character is logged to The Compendium and added immediately to the Google sheet. If they answer no, they are taken back to the main menu.

Upload pre-made Character to The Compendium
If a user chooses to upload their pre-made character to the Compendium, the add_character_to_compendium function will run with the paratmeters of the randomised character. This function takes all of the information provided in the terminal and formats it into a string so it can be added to the Google sheet. Once the below function has run, the character is added and the user is taken back to the main menu


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


![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **May 26, 2025**

## Reminders

- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

---

Happy coding!

Bugs to fix
Adding proficiencies for a pre-made character

    """Validation for pre-made character race"""
    while True:
        pre_made_race = input(f"Enter race/species ({', '.join(allowed_races)}): ").strip().title()
        if pre_made_race not in allowed_races:
            print("Invalid race. Please choose one from the list.")
        else:
            break

    """Validation for pre-made character class"""
    while True:
        pre_made_character_class = input(f"Enter class ({', '.join(allowed_classes)}): ").strip().title()
        if pre_made_character_class not in allowed_classes:
            print("Invalid class. Please choose one from the list.")
        else:
            break

    """Validation for pre-made character alignment"""
    while True:
        pre_made_alignment = input(f"Enter alignment ({', '.join(allowed_alignments)}): ").strip().title()
        if pre_made_alignment not in allowed_alignments:
            print("Invalid alignment. Please choose one from the list.")
        else:
            break

while len(pre_made_proficiencies) < 4:
        proficiency = input("Enter proficiency: ").strip().title()
        if proficiency in allowed_proficiencies:
            if proficiency not in pre_made_proficiencies:
                pre_made_proficiencies.append(proficiency)
                print(f"Added proficiency: {proficiency}")
            else:
                print("Proficiency already added, please enter a different one.")
        elif proficiency == "":
            if len(pre_made_proficiencies) < 4:
                print("You must enter at least one proficiency.")
            break
        else:
            print("Invalid proficiency, please choose from the list.")
            print(", ".join(allowed_proficiencies))
    if not pre_made_proficiencies:
        print("No proficiencies added, defaulting to 'None'.")
        pre_made_proficiencies = ["None"]

    The code had been written to only allow one proficiency added at a time. Whilst this worked, it was laborious and required more work from the user when this could be simplified.

    To simplify this process for the user I changed the code so that the user could provide those proficiencies as a string which had to match up to the required proficiencies dictionary above the function

    pre_made_proficiencies = []
    print("\nEnter up to 4 proficiencies from the following list:")
    print(", ".join(allowed_proficiencies))
    print("Press Enter on an empty line when you're done.")

    while len(pre_made_proficiencies) < 4:
        raw_input = input("Enter proficiencies (comma-separated): ").strip()

        if raw_input == "":
            if not pre_made_proficiencies:
                print("You must add four proficiencies.")
                continue
            break

        entries = [item.strip().title() for item in raw_input.split(',')]

        for proficiency in entries:
            if len(pre_made_proficiencies) >= 4:
                break
            if proficiency in allowed_proficiencies:
                if proficiency not in pre_made_proficiencies:
                    pre_made_proficiencies.append(proficiency)
                    print(f"Added: {proficiency} to proficiencies.")
                else:
                    print(f"{proficiency} is already added.")
            else:
                print(f"{proficiency} is not a valid proficiency.")


    Sleight of Hand bug 

    allowed_proficiencies = [
        "Athletics", "Acrobatics", "Stealth", "Perception",
        "Arcana", "History", "Insight", "Medicine",
        "Nature", "Religion", "Deception", "Intimidation",
        "Performance", "Persuasion", "Sleight of Hand", "Investigation",
        "Animal Handling", "Survival"
    ]

    Due to the codee using the strip() process and converting all of the first letters to uppercase, Sleight of Hand was returning as an incorrect option. By changing this to "Sleight Of Hand" in both the allowed_proficiencies and the proficiencies dictionary this fixed the problem. 
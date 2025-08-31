Project 03 by Alice Foster

[View live project](https://the-compendium-af-7957ce214c86.herokuapp.com/)

# The Compendium
The Compendium is a Python built project which is built around the concept of character creation for Dungeons and Dragon's (known colloquially as DnD). The project is connected to a Google Sheet and allows users to do the following: See all the characters already logged to the Google Sheet, Create a character using randomised features provided by the Compendium terminal and upload the details of a pre-made DnD character the user already has. Any characters created using The Compendium are automatically uploaded to the Google Sheet. Users can choose if they want to upload the pre-made character to the Google Sheet. 

# Table of Contents
1. [Audience](#audience)
2. [Project Logic](#project-logic)
3. [Existing Features](#existing-features)
    * [Opening Menu](#opening-menu)
    * [View Characters Logged to The Compendium](#view-characters-logged-to-the-compendium)
    * [Modifiers](#modifiers)
    * [Global Variables](#global-variables)
    * [Amend a Character Logged to The Compendium](#amend-a-character-logged-to-the-compendium)
        * [Amend Classes](#amend-classes)
        * [Amend Statistics](#amend-statistics)
        * [Amend Proficiencies](#amend-proficiencies)
        * [Amend Alignments](#amend-alignments)
    * [Create a New Character using The Compendium](#create-a-new-randomised-character-using-the-compendium)
    * [Log a Pre-Made Character](#log-a-pre-made-character)
    * [Upload a Character to The Compendium](#upload-a-character-to-the-compendium)
4. [Future Features](#future-features)
5. [Testing](#testing)
    * [Manual Testing](#manual-testing)
    * PEP8 CI Python Linter
6. Bugs
7. Deployment
8. Local Deployment
9. Tools and Technologies Used
10. [Credits and acknowledgements](#credits-and-acknowledgements) 
11. [Final note from the Developer](#final-note-from-the-developer)

## Audience
The Compendium is designed for the following audience:
* People who play Dungeons and Dragons (specifically Dungeon Masters) who need to create characters fast, particularly for NPC roles which don't require a huge amount of character detail
* People who play Dungeons and Dragons characters who would like a simple digital record of their own personal characters outside of platforms like DnD Beyond

## Project Logic
In order to follow best practise, I created a flowchart using Lucidchart, which maps out the logic of the processes throughout the project

General Project Logic
![General Project Logic](https://github.com/foster95/the_compendium/blob/main/assets/images/The%20Compendium%20-%20General%20Logic.png)

Character Amendment Logic
![Character Amendment Logic](https://github.com/foster95/the_compendium/blob/main/assets/images/The%20Compendium%20-%20Character%20Amendment.png)

## Existing Features
### Opening menu
Upon launching the program, users are immediately greeted with a welcome message and the home screen. The welcome message tells the user exactly what the program does and provides them with a short list of options to progress the program. To exit and return to the previous point (or at this point, to leave the program), the user must type 0.

### View characters logged to The Compendium
If the uses chooses option 1 they are immediately taken to the list of currently logged characters. This is information that is pulled directly from The_Compendium google sheet and is a real time snapshot of that information shown in the terminal. The information is laid out in the clearest way possible, with breaks between each character to ensure that the user can understand the information shown. 

### Modifiers
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

### Global Variables
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

### Amend a character logged to The Compendium
After the user has trigged the view characters function, they are given the option to either return to the main menu (by typing 0), or alternatively to amend an individual character. The user is then asked which character they would like to choose, and they are required to type the entire name, with no spelling issues or added special characters, otherwise they will trigger the validation and will not be able to move further into the program. However upon typing the correct name, they will then be greeted with a further sub menu. The sub menu is made up of all of the features that can be adjusted - Class, Statistics, Proficiencies and Alignment. They also have the option to break out of the program and return directly to the main menu.

If a character chooses to change any of their classes, statistics, proficiencies or alignments they must meet the following global variable requirements (these variables are also used for the character randomiser program and for logging a pre-made character)

Once a user has chosen which feature they want to amend, they can type the number to launch the approporiate program. At all times if the user enters information that is always registered to the character, they should recieve a prompt to state that the character already has that relevant class/alignment/proficiency and ask them to provide something different. The Program is also broken down into further functions. Details of these are below:

#### Amend Classes
If the user chooses to launch the Class amendment option they are told the following information - the current Class associated to the logged character and the allowed classes that the program requires.

A feature of Dungeons & Dragons is that the user can create a character that has multiple classes. This isn't a standardised process, a player has to level up in order to unlock the ability to have multiple classes, and the program currently operates on the assumption that for randomised characters, they should be starting at a L1 with only one class. However, for users that have chosen to multi-class, then they can choose to specifically add a second class. They cannot add the same class already associated to the character, and the second class must be from the allowed classes list.

If the user does not want to add a further class, they can type 0 to return to the character amendment options. 

#### Amend Statistics
If the user chooses to amend their statistics, they are shown a list of all of their current statistics in the terminal and are prompted to type the name of the statistic that they want to update and hit enter. They are then asked what they want to update their new statistic to. Typically players are unlikely to update more than three statistics at any one time, and provided that the new statistic is accepted by the program, the user is prompted and asked if they want to add any more statistics. 

As with all of the amendments, the user is required to type the statistic name they wish to amend exactly, without special characters otherwise this will trigger the validation. If the user tries to update the statistic number to one that is already logged to the character they are told that the character already has this number and asked to try again.

Though it is not seen in the terminal, if the user chooses to update a statistic, the update_modifier function also runs, to ensure that the modifier is updated in line with the statistic number. 

If the user does not want to amend a statistic, they can type 0 to return to the character amendment options. 

#### Amend Proficiencies
If the user chooses to launch the Proficiencies amendment option they are told the following information - the current Proficiencies associated to the logged character and the allowed Proficiencies the program requires.

Currently the program restricts users to just four proficencies, and therefore the user is prompted with a submenu for proficiency amendment. If a user would like to add a proficiency they can choose that option, however if the program already registers four proficiencies are associated to the character, the user will be told that they need to remove an proficiency to add an proficiency. Users are able to bulk add and remove proficiencies, provided they are seperated by a comma but again are limited by no more than four proficiencies. 

If they want to remove they are shown again the current associated proficiencies with the character, and the proficiency removed must match a current proficiency. If it does not, the user will trigger validation and will be asked to remove a proficiency associated with the character. 

If there are less than four proficiencies associated with a character, and the user wants to add a proficiency, they are also shown the current proficinecies associated the character, and are shown the available proficiencies as well. Any proficiency added, must not already be in the current proficiencies, and must also be part of the allowed proficiencies global variable. If either of these things are not true, validation is triggered and the user will be told either that they cannot add a profiency already associated, or that the proficiency they are trying to add, does not meet the allowed proficinecy requirements. 

If the user does not want to amend a proficiency, they can type 0 to return to the character amendment options. 

#### Amend Alignments
If the user chooses to launch the Alignment amendment option they are told the following information - the current Alignment associated to the logged character and the allowed Alignments that the program requires.

If the user wishes to update their Alignment, they must type the new Alignment exactly as listed in the program otherwise they will trigger the validation. A user cannot add the same Alignment already associated to the character.

At the end of any character amendments, these amendments will be logged and changed on the Google sheet immediately. The user will be brought back to the character amendment menu and then can choose to amend further fields or return to the main Compendium menu.

### Create a New Character using The Compendium
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

The character is automatically logged to The Compendium, and is added as a new row on the Google sheet, which a user can then go in and amend, as detailed above. Once the program has finished running, the user is automatically returned to the main menu of The Compendium. 

### Log a pre-made Character
If a user chooses to log a pre-made character outside of the randomiser, they are first prompted to enter a required first name and an optional surname. They are then prompted to provide the character's race/species, Class, Alignment, up to four proficiencies and their statistics. All of the information entered must match the allowed variables otherwise they will recieve a prompt informing them that the information is not valid. As with the character amendment options, multiple proficiencies can be typed at once to save the user time. At the end of this process, the terminal will display all of this information to the user and they will be asked if they wish to add the character to the Compendium. If they answer yes, the character is logged to The Compendium and added immediately to the Google sheet. If they answer no, they are taken back to the main menu.

### Upload a Character to The Compendium
If a user chooses to upload their pre-made character to the Compendium, the add_character_to_compendium function will run with the paratmeters of the randomised character. This function takes all of the information provided in the terminal and formats it into a string so it can be added to the Google sheet. Once the below function has run, the character is added and the user is taken back to the main menu. This process also automatically runs when a user creates a character through The Compendium's random character generator. 


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

### Future Features
* Additional races - as detailed in the features above, the program is currently limited to a series of common races. A future version of this program would allow for a wider pool of races to be used, with rarer, and more uncommon races available.
* Removal of characters from The Compendium - this is a feature I really wanted to encorporate but could not get to at this stage. Currently the only way to remove characters from The Compendium is to manually delete the row from the google sheet. A future version of this program would have an option underneath character amendments where the character could simply be removed straight away.
* Immediate amendment of randomised characters before they get added to The Compendium - a future version of this program would give users the opportunity to make immediate amendments before the character was added to The Compendium rather than as it currently is, where the character is uploaded and then the user must go to and make character amendments after. 

## Testing
### Manual Testing
Section | Expected Result | Actual Result | Notes
--- | --- | --- | ---
Compendium Launch Page | Program launches. The user is immediately met with the welcome message, and after this offers a series of options that the user can choose to further, or exit the program. On typing 1 and hitting Enter, the get_stored_characters function runs. On typing 2 and hitting Enter, the create_randomised_character function runs. On typing 3 and hitting Enter the add_premade_character function runs. On typing 0 and hitting Enter, the program displays a leaving message and exits out of the program | The user is shown the welcome message and a series of options. Option 1 does launch the get_stored_characters function. Option 2 does launch the create_randomised_character function. Option 3 does launch the add_premade_character function. Typing 0 does display a leaving message and exits out of the program | Compendium Launch Page working as expected
Compendium Launch Page > Option 1 - View all characters | The user is informed that they have launched the get_stored_characters function with the following message: "Viewing all characters logged to The Compendium". The program then prints a formatted block of strings of all the information that is taken from the Google Sheet. The information should be the following: Name, Race/Species, Class, Statistics (with modifiers in brackets), Proficiencies and Alignment. There should be a break between each character to make the program as readable as possible. At the bottom of the terminal, the user should be shown two options - typing option 1 and hitting Enter will launch the amend_stored_character function. Typing option 0 and hitting Enter will take the user back to the main Compendium menu along with the message "returning to main menu" | The user is shown the following message: Viewing all characters logged to The Compendium. The program then prints a formatted block of strings of all the information which is taken directly from the Google Sheet. The information shown is the following: Race/Species, Class, Statistics (with modifiers in brackets), Proficiencies and Alignment. There is a break between each character to make the information as readable as possible. At the bottom of the terminal the user is given two options - typing option 1 and hitting Enter does launch the ammend_stored_characters function. Typing option 0 and hitting Enter takes the user back to the main menu along with the message "returning to main menu..." | Compendium Launch Page > Option 1 - View all characters working as expected
Option 1 - View all characters > Option 1 - Amend a character | The program should immediately request the name of the character that the user wants to amend. The character name should be typed exactly as listed, any deviation from this will trigger validation. If validation is triggered the program will return the user back to the character amendment options. If the user types an accepted name, the program prints a list of character amendment options. If the user wants to update the character Class (for Multi-Classing), they should type 1 and hit Enter. If they want to update Statistics they should type 2 and hit Enter. If they want to update Proficiencies they should type 3 and hit Enter. If they want to update character Alignment they should type 4 and hit Enter. To break out of character amendment and return to the main menu, the user should type 0 and hit Enter. Again if they choose this option they should see the message "returning to main menu..." and be taken to the main Compendium menu. | The program immediately requests the name of the character the user wants to amend. The character name must be typed exactly as listed, as any deviation from this triggers validation. When validation is triggeered, the program returns the user back to the character amendment options. If the user types an accepted name, the program prints a list of character amendmenent options. If the user wants to updated character Class (for Multi-Classing), they type 1 and hit Enter. If the user wants to update character Statistics they type 2 and hit Enter. If the user wants to update character Proficiencies they type 3 and hit Enter. If the user wants to update character Alignment they type 4 and hit Enter. If the user wants to return to the main menu, they type 0. On typing this they are shown: "returning to main menu..." and are taken back to the main menu | Compendium Launch Page > Option 1 - View all characters > Option 1 - Amend a character working as expected
Compendium Launch Page > Option 1 - View all characters > Option 1 - Amend a character > Option 1 > Amend Class | The user should be shown their current class, and then a string of all the ALLOWED_CLASSES global variable. The user should then be given shown a prompt asking if the user would like to add a Class. If they type 01 and hit Enter, the amend_class function will trigger. The amend_class function should ask the user to enter a new Class, or type 0 to return to the character amendment choices. Any new Class added must be from the ALLOWED_CLASSES variable otherwise it will trigger validation and will take the user back to ask if they would like to add a Class. If the new Class is accepted by the program, then the Class will update on the Google sheet. The user should then automatically be asked if they would like to add a further class. The process repeats. If the user types type 0 and hits Enter when they are asked if they want to add a Class they should return to the character amendment choices, with the message "returning to character amendment choices". | The user is shown their current class and a string of the ALLOWED_CLASSES global variable. They are then asked if they would like to add a Class. If the type 01 and hit Enter, the ammend_class function triggers. The amend_class function asks the user to enter a new Class or to type 0 to return to the character amendment options. The new class must match the requirements of the ALLOWED_CLASSES variable. If it does, the Class is updated and the Google sheet updates in real time. If it does not, the user is told that the Class is. not an allowed Class and is asked again if they would like to add a Class. This process continues until the user chooses to return to character amendment choices, which they do by typing 0. | Option 1 - Amend a character > Option 1 > Amend Class working as expected 
Option 1 - Amend a character > Option 2 > Amend Statistics | The user should be shown a full list of all the Statistics available for updating, along with the current number associated with each Statistic in brackets. This information should be pulled directly from the Google sheet and should be a live snapshot. The user should then be asked to type the statistic type. If they type in a statistic that doens't exist or has a spelling error, they will trigger validation. If validation is triggered the user will be asked again which statistic they want to ammend. If the statistic type is accepted the user should be asked what the new value they would like to enter. If they enter the value already associated they will trigger an error validation which will tell the user that the character Statistic already has that number. If the statistic type is accepted but the user tries to update the statistic number to 0, they should be taken back to the Statistic change screen. If the statistic type is accepted and the user updates to a number the program deems valid the program should update the Statistic to the new number and this will also happen on the Google sheet in real time. The user should then be asked if they want to amend another Statistic and must type yes or no. If they type anything other than yes or no, then they will trigger validation and the program will prompt them again to type yes or no. If the user types yes, they should be shown the list of Statistics again, along with the associated number. If the user types 0 then they should be returned to the character amendment options | The user is shown a full list of the statistic types associated with the character, along with their individual statistic number in a bracket. The information they see is pulled live from the Google sheet. The user is asked what statistic the would like to update, and is asked to type the statistic name in the terminal. If the Statistic is spelt incorrectly or the user tries to add something that is not an accepted statistic they trigger validation and will be asked to try again and enter an accepted statistic. On typing an accepted Statistic the user is asked to type the new number they would like to amend the Statistic to. If the user tries to update the statistic number to 0, they are taken back to the Statistic change screen. If the user tries to update the statistic with a number already associated they are informed the character already has the statistic and asked to type the statistic again. If the user types a unique number, the program informs the user the Statistic that has been updated and asks the user if they would like to amend another statistic. The user must respond yes or no, if they type anything other than this the program asks them again to respond yes or no. If they respond yes, they are do the entire process again, if they respond no they are taken back to the character amendment options. | Option 1 - Amend a character > Option 2 > Amend Statistics working as expected
Option 1 - Amend a character > Option 3 > Amend Proficiencies | The user should be shown a full list of their current proficiencies and underneath that a string of the ALLOWED_PROFICIENCIES printed to the terminal. The user should then be given a series of options, to add a proficiency the user should type 1 and hit Enter, to remove a proficiency they user should type 2 and hit Enter and to return to the character ammendment options, the user should type 0 and hit Enter. If the user chooses to add a Proficiency, the program should check for how many Proficiencies are already associated with the character. If the character already has four Profiencies, they should recieve a prompt saying they cannot add any more Proficiencies and should remove one instead. If the user has less than four proficiencies associated with the character they should see a string of their current Proficiencies and a string of the ALLOWED_PROFICIENCIES and will be asked to enter the Proficiency (or Profiencies is they are adding multiple) they want to add. The user can then add a proficiency which must match one of those listed in the ALLOWED_PROFICIENCIES variable. If they try to enter a Proficiency that is not from that list they will trigger validation and will be told the Proficiency is not allowed and to try again. This should continue until the user enters an accepted Proficiency, or they type 0 to take a step back to the Proficiency amendment options. If the Proficiency is accepted, the Google sheet should be updated and the user should be returned to the Proficiency amendment options. If the user chooses to remove a Proficiency, the program should check that there is at least one Proficiency associated to the character on the Google sheet. If there are no Proficiencies associated with the character, the user should be told that there are no Proficiencies to remove and is prompted to add a Proficiency instead. If there is at least one Proficiency associated with the character then the user should see all of the current Proficiencies associated to the characer and a string of the ALLOWED_PROFICIENCIES and should be asked to enter the Proficiency (or Proficiencies if they are removing multiple) they would like to remove from the character. If they try to enter a Proficiency that is not from that list they will trigger validation and will be told the Proficiency is not allowed and to try again.This should continue until the user enters an accepted Proficiency, or they type 0 to take a step back to the Proficiency amendment options. If the Proficiency is accepted, the Google sheet should be updated and the user should be returned to the Proficiency amendment options. | The user is shown a string of the characters current proficiencies which are taken from the Google sheet. Under this they are shown the string of the ALLOWED_PROFICIENCIES global variable. Under this they are asked if they would like to add or remove a proficiency. Typing 1 and hitting Enter triggers the add profiency option. Typing 2 and hitting Enter triggers the remove proficiency option. Typing 0 takes the user back to the character amendment options with the message "Returning to character amendment choices...". When the user types 1 and hits Enter to trigger the add Profiency option, the program checks how many Proficiencies are already associated with the character the user is trying to amend. If there are already four Proficiecies associated with the character validation triggers and the user is informed they cannot add any Proficiencies and must remove one first, they are then taken back to the Proficiency amenment submenu. If there are less than four Proficiencies associated with the character, the user is shown a string of their current proficiencies and a string of the ALLOWED_PROFICIENCIES variable and are asked to type the Proficiency (or Proficiencies if they are adding multiple Proficiencies) into the terminal. The Proficiency the user is trying to add must be one from the ALLOWED_PROFICIENCIES variable otherwise the terminal informs them the variable they have tried to add is not valid and they must try again. If the Proficiency is accepted, the Google sheet is updated in real time and the user is informed that the Proficiency/Proficiencies have been added. The user is then automatically taken back to the Proficiency amendment submenu. If the user chooses to remove a Proficiency the program checks how many Proficiencies are already associated to the character. If no Proficiencies are associated, the program informs the user that there are no Proficiencies to be removed and that they must add a Proficiency first. If there is at least one Proficiency associated with the character, the user is shown a string of their current proficiencies and a string of the ALLOWED_PROFICIENCIES variable and are asked to type the Proficiency (or Proficiencies if they are adding multiple Proficiencies) they would like to remove into the terminal. The Proficiency the user is trying to remove must be one from the ALLOWED_PROFICIENCIES variable otherwise the terminal informs them the variable they have tried to remove is not valid and they must try again. If the Proficiency is accepted, the Google sheet is updated in real time and the user is informed that the Proficiency/Proficiencies has been removed. The user is then automatically taken back to the Proficiency amendment submenu. | Option 1 - Amend a character > Option 3 > Amend Proficiencies working as expected
Option 1 - Amend a character > Option 4 > Amend Alignment | The user should be shown their current Alignment associated to the charaqcter, and a string of the ALLOWED_ALIGNMENTS global variable. They should then be prompted to enter the new Alignment they would like to associate to the character. The Alignment they enter must be a match to one of the allowed alignments. If the user tries to enter an alignment that is not from the allowed list, they program should prompt them that the Alignment they entered is not valid and to try again. If the user enters an alignment that matches one of the allowed list the program should tell the user that their Alignment has been updated and the Google sheet should update in real time. The user should then be taken back to the character amendment options. If the user types 0 on as their updated Alignment, it should take them back to the character amendment options. | The user is shown their current Alignment associated to the character, and a string of the ALLOWED_ALIGNMENTS global variable. They are then prompted to enter the new Alignment they would like to associate to the character.  The Alignment they enter must be a match to one of the allowed alignments. If the user tries to enter an alignment that is not from the allowed list, they program prompts them that the Alignment they entered is not valid and to try again. If the user enters an alignment that matches one of the allowed list the program tells the user that their Alignment has been updated and the Google sheet updates in real time. The user is then be taken back to the character amendment options. If the user types 0 on as their updated Alignment, it takes them back to the character amendment options. | Option 1 - Amend a character > Option 4 > Amend Alignment working as expected
Option 2 - Create a new character using The Compendium's character generator | The user should be prompted to enter a first name and a surname for the character they would like to create. The first name is a required field and must be completed. If the user tries to enter nothing they should be told that they must enter at least one letter and to try again. The user can only enter letters and no special characters. If they try to enter special characters or numbers they should be told that the character name can only be made up of letters. Once the user has typed a first name that is accepted, they should be asked an optional second name. If the user wishes to skip this they should hit enter, otherwise the same rules apply. The program should then use the random function to create a character, using all of the ALLOWED global variables at the top of the code. To work out Statistics the program should produce a random number between one and twenty for each Statistic. To work out the modifier, the code should take the random number that the program produced, minus that number by 10 and then divide that number by 2. The user should be shown the entirety of this random character and the information produced by The Compendium and this character should then automatically be uploaded to the Google sheet so that the information is added when the user tries to run Option 1 to view all characters. The user should then be returned to The Compendium main menu. | The user is prompted to enter a first name and a surname. The first name is a required field and must be completed. If the user tries to enter nothing they are be told that they must enter at least one letter and to try again. The user can only enter letters and no special characters. If they try to enter special characters or numbers they are be told that the character name can only be made up of letters. Once the user has typed a first name that is accepted, they are asked for an optional second name. If the user wishes to skip this they should hit enter, otherwise the same rules apply. The program then creates a random character, using the random function on Python using all the ALLOWED global variables. To work out Statistics the program produces a random number between one and twenty for each Statistic. To work out the modifier, the code takes the random number that the program produced, minuses that number by 10 and then divides that number by 2. The user is then shown the entirety of this random character and the information produced by The Compendium. The character is then automatically be uploaded to the Google sheet so that the information is added when the user tries to run Option 1 to view all characters. The user is then be returned to The Compendium main menu. | Option 2 - Create a new character using The Compendium's character generator working as expected
Option 3 - Add your own existing character to The Compendium | The user should be prompted to enter the character's first name and surname for their pre-existing character. The first name is a required field and must be completed. If the user tries to enter nothing they should be told that they must enter at least one letter and to try again. The user can only enter letters and no special characters. If they try to enter special characters or numbers they should be told that the character name can only be made up of letters. Once the user has typed a first name that is accepted, they should be asked an optional second name. If the user wishes to skip this they should hit enter, otherwise the same rules apply. Provided the user has given information that is accepted by the computer the user should then be asked to enter the characters Race/Species followed by a a string of the ALLOWED_RACES global variable. If the user tries to enter a Race/Species that is not from that list, they should be told that the Race/Species is invalid and to try again. This process will continue until the user provides an accepted Race/Species. The program should then prompt the user to enter the Class of their pre-existing character, followed by a string of the ALLOWED_CLASSES global variable. If the user tries to enter a Class that is not from that list, they should be told that the Class is invalid and to try again. This process will continue until the user provides an accepted Class. The program should then prompt the user to enter the Alignment of their pre-existing character, followed by a string of the ALLOWED_ALIGNMENTS global variable. If the user tries to enter a Alignment that is not from that list, they should be told that the Alignment is invalid and to try again. This process will continue until the user provides as accepted Alignment. The program should then prompt the user to provide four Proficiencies associated with the pre-existing character, followed by a string of the ALLOWED_PROFICIENCIES global varaible. If the user tries to enter a Proficiency that is not from that list, they should be told that the Proficiency is not valid and to try again. To speed up the process of entering Proficiencies, a user should be able to enter up to four Proficiencies in one go, seperated by a comma each time. If they try to add four Proficiencies without a comma the program should inform the user that the Proficiency is invalid and to try again. If the user adds four Proficiencies, seperated by a comma and the program accepts the Proficiency the user should be shown that the proficiency has been added. At the end of this process, the program should then prompt the user to enter their Statistics, starting with Strength and moving on in the following order: Strength, Dexterity, Constitution, Intelligence, Wisdom and Charisma. If the user tries to provide a number greater than 21 they should be prompted that the value must be between 1 and 20 and to try again. The program should at the same time work out the modifiers, using the same function as it did to create the random character (taking the random number produced, minusing 10 and dividing that number by 2) and the terminal should display the full character information provided by the user. At any time in the process up to the user being shown the character in its completion, the user should be able to type 0 to exit back to The Compendium main menu. Once the user has been shown their complete pre-existing character, they should be asked if they would like to add their character to The Compendium. They must type yes or no, if they do not type yes or no, the computer should prompt them that they have entered an invalid option and to try again. If the user chooses not to add the character to The Compendium they should be taken back to the main menu. If the user chooses to add the character to The Compendium, they should be be told the character has been added to The Compendium and then returned to the main menu and the Google sheet should add a row with the character information so it can be called when the user chooses option 1 - view all characters logged to The Compendium. | The user is prompted to enter the first name and surname for their pre-existing character. The first name is a required field and must be completed. If the user tries to enter nothing they are be told that they must enter at least one letter and to try again. The user can only enter letters and no special characters. If they try to enter special characters or numbers they are  told that the character name can only be made up of letters. Once the user has typed a first name that is accepted, they are asked an optional second name. If the user wishes to skip this they should hit enter, otherwise the same rules apply. Provided the user has given information that is accepted by the computer the user is then asked to enter the characters Race/Species followed by a a string of the ALLOWED_RACES global variable. If the user tries to enter a Race/Species that is not from that list, they are told that the Race/Species is invalid and to try again. This process will continue until the user provides an accepted Race/Species. The program then prompts the user to enter the Class of their pre-existing character, followed by a string of the ALLOWED_CLASSES global variable. If the user tries to enter a Class that is not from that list, they are told that the Class is invalid and to try again. This process will continue until the user provides an accepted Class. The program then prompts the user to enter the Alignment of their pre-existing character, followed by a string of the ALLOWED_ALIGNMENTS global variable. If the user tries to enter a Alignment that is not from that list, they are told that the Alignment is invalid and to try again. This process will continue until the user provides an accepted Alignment. The program then prompts the user to provide four Proficiencies associated with the pre-existing character, followed by a string of the ALLOWED_PROFICIENCIES global varaible. If the user tries to enter a Proficiency that is not from that list, they are told that the Proficiency is not valid and to try again. To speed up the process of entering Proficiencies, a user can enter up to four Proficiencies in one go, seperated by a comma each time. If they try to add four Proficiencies without a comma the program should inform the user that the Proficiency is invalid and to try again. If the user adds four Proficiencies, seperated by a comma and the program accepts the Proficiency the user is shown that the proficiency has been added with a message. At the end of this process, the program then prompts the user to enter their Statistics, starting with Strength and moving on in the following order: Strength, Dexterity, Constitution, Intelligence, Wisdom and Charisma. If the user tries to provide a number greater than 21 they are prompted that the value must be between 1 and 20 and to try again. The program should at the same time work out the modifiers, using the same function as it did to create the random character (taking the number provided by the user, minusing 10 and dividing that number by 2). The terminal then displays the full character information provided by the user. At any time in the process up to the user being shown the character in its completion, the user can type 0 to exit back to The Compendium main menu. Once the user has been shown their complete pre-existing character, they are asked if they would like to add their character to The Compendium. They must type yes or no, if they do not type yes or no, the computer prompts them that they have entered an invalid option and to try again. If the user chooses not to add the character to The Compendium they should be taken back to the main menu. If the user chooses to add the character to The Compendium, they are told the character has been added to The Compendium and then returned to the main menu, the character will also be added to the Google sheet, so it can be called when the user selects Option 1 - view all characters logged to The Compendium. | Option 3 - Add your own existing character to The Compendium working as expected

## Credits and acknowledgements
Dungeons & Dragons was unfortunately not created by me, nor do I pretend it was. The credit for the creation of the bonkers and brilliant world of D&D is solely down to Gary Gygax and Dave Arneson though credit must also be given to the brilliant Matt Mercer and Brennan Lee Mulligan who have becoming the modern day magicians of D&D.
There is a small portion of code that was taken directly from the Love Sandwiches module and which was used for deploying to Heroku and for wiring APIs
The three characters that already exist within the program - Hubble Bubble, Marianne Ellingberry and Lucretia Pebble are my own D&D characters, who have stood me strong through multiple campaigns
Credit also to Spencer Barribal who offered invaluable support and assistance in the def parse_stats_string, format_stats_string and format_modifiers_string as well as general support and help throughout this project as he always does.
I would once again like to thank my partner Jon, for his endless support, and boundless enthusiasm when I decided I wanted to try and create something D&D based. Similarly shout out to our DM Connor, who when I showed him the original project, was full of endless praise and also helped me work out which bits of the project would be really useful and if there were any elements I could trim off. 

### Final Note from the Developer
As with all of the Code Institute projects, I find each step to be a major learning curve from the last one and this was as per usual fiendishly difficult at times. The amount of times where I found myself stepping back, scribling notes, going back into the code, tweaking and changing small lines of code to try and make it as user friendly as possible and as polished as possible. As with all of my projects, it is not perfect, and there are certainly bits that I would love to develop and improve with time, but I am very proud of it, and have used it in real time to help create some NPCs for campigns. I continue to be endlessly appreciative of my mentor Spencer Barribal who makes every Slack call genuinely so enjoyable even if we do have to remind ourselves often to stay on track and not stray off down another fun conversation topic.

A year ago I was very new to D&D and already a year down the line I feel immersed in this world that gives me so much genuine joy and happiness that I did not always know was possible. I hope that a year down the line, I will feel that way about coding - I know it has already changed my trajectory in ways that the me from a year ago could not begin to imagine.

As a final disclaimer, this project is for education purposes, and not for public use. It was created for Code Institute's Full Stack Diploma course and is not affiliated with Gary Gygax, Dave Arneson, Brennan Lee Mulligan, Matt Mercer, Dungeons & Dragons, Critial Role or Dimension Twenty and the many other D&D related media that has sprung about in revent years.

All trademarked and/or copyrighted content are the property of their respective owners.

Developed by Alice Foster, 2025.





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
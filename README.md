Project 03 by Alice Foster

View live project

The Compendium
The Compendium is a Python built project which is built around the concept of character creation for Dungeons and Dragon's (known colloquially as DnD). The project is connected to a Google Sheet and allows users to do the following: See all the characters already logged to the Google Sheet, Create a character using randomised features provided by the Compendium terminal and upload the details of a pre-made DnD character the user already has. Any characters created using The Compendium are automatically uploaded to the Google Sheet. Users can choose if they want to upload the pre-made character to the Google Sheet. 

The Compendium is designed for the following audience:
* People who play Dungeons and Dragons (specifically Dungeon Masters) who need to create characters fast, particularly for NPC roles which don't require a huge amount of character detail
* People who play Dungeons and Dragons characters who would like a simple digital record of their own personal characters outside of platforms like DnD Beyond

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

Ammend a character logged to The Compendium
Create a randomised character using The Compendium
Log a pre-made Character
Upload pre-made Character to The Compendium

Project Logic
In order to follow best practise, I created a flowchart using Lucidchart, which maps out the logic of the processes throughout the project

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
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
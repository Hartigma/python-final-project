#Michael Hartig
#Final Python Project

#importing argparse allows us to parse future arguments, important pandas allows us to use pandas library, and importing re, allows us to use regex coinciding with pandas library
import argparse
import pandas as pd
import re

#ABOUT MENU
# This function will be called on to give an overview of all the restaurants, the list positioning, and giving a rundown of the purpose
# using -a will prompt all of these print statements at once
def aboutmenu():
    print("This app will post 4 different lists, the first list being food items you can get at all 3 of the restaurants")
    print("The second list will show the foods only you can get at Cincy Chicken")
    print("The second list will show the foods only you can get at Queen City Burger")
    print("The third list will show the foods only you can get at UC Burrito")
    print("The purpose of this is to help you compare what food you want to get while giving you the option to choose what place works for not only you but possibly multiple people.")

#RUN
# The heart of the app the run function uses a try function in order to assign a variable to to each csv and prompts an error if one of the csvs doesnt exist or is named incorrectly
def runapp():
    try:
        CincyChicken = pd.read_csv('CincyChicken.csv')
        QueenCityBurger = pd.read_csv('QueenCityBurger.csv')
        UCBurrito = pd.read_csv('UCBurrito.csv')
    except FileNotFoundError as e:
        print(f"Error: {e} please make sure these csv files are legitimate.")
        return

# each index is named food item which pandas is pulling from to get these lists each menu variable is grabbing these lists, dropna is not including false entries, and str.lower makes everything lowercase to avoid case sensitive issues and better formatting
    CCmenu = CincyChicken['food_item'].dropna().str.lower()
    QCBmenu = QueenCityBurger['food_item'].dropna().str.lower()
    UCBmenu = UCBurrito['food_item'].dropna().str.lower()

#This portion is setting the variable to defind unique items and also the common items, by using "is in" and "&" you can see each item is being compared through each list and both lists to get accurate results
    commonFood = CCmenu[CCmenu.isin(QCBmenu) & CCmenu.isin(UCBmenu)]
    CCunique = CCmenu[~CCmenu.isin(QCBmenu) & ~CCmenu.isin(UCBmenu)]
    QCBunique = QCBmenu[~QCBmenu.isin(CCmenu) & ~QCBmenu.isin(UCBmenu)]
    UCBunique = UCBmenu[~UCBmenu.isin(QCBmenu) & ~UCBmenu.isin(CCmenu)]

# Foodfinaldf will be made into a dataframe laying out the information of both the uique and common lists. by displaying them this will be shown visually. the printed sections are at the top of the columsn to with a "|" to make it easier to point out where the section is pointing to.
    Foodfinaldf = pd.DataFrame({
        'Food Items that can be had at all restaurants | ': commonFood,
        'Food items only at Cincy Chicken | ': CCunique,
        'Food items only at Queen City Burger | ': QCBunique,
        'Food items only at UC Burrito | ': UCBunique,
    })

# Here we are taking the data and pushing it to a new csv (if it doesnt already exist), (which running for the first time will create this csv and still run the script (even if deleted everytime after running)) from there it is taking the csv content and printing it to the terminal.
#index false means its not being included in the output
    Foodfinaldf.to_csv('ComparedResults.csv', index=False)
    print(pd.read_csv('ComparedResults.csv'))

#EXIT
#This function simply is used for the exit portion, I added to prints for aesthetic purposes, this in itself isnt exiting yet all its doing right now is printing when called on, the break is at a later section which tied together accurately exits
def exitapp():
    print("App closing...")
    print("App exited")

#CONTACTS
# Here is the regex portion, this function sets a variable to attach to the contact.csv, the email regex functino is setting the regex filtering in order to pull real emails from the existing listlist
def regexcontact():
    datacontact = pd.read_csv('contact.csv')
    emailRegex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    #variable acceptedemail is finding the email index, data contact allows us to return the rows where legitimate emails are applied, re.math() is using x as the email address and comparing it to the filter of regex we have established
    acceptedEmail = datacontact[datacontact['email'].apply(lambda x: bool(re.match(emailRegex, str(x))))]
    #prints the list from the index all that apply with the regex filter
    print(" Contacts found for all 3 restaurants include: ")
    print(acceptedEmail['email'])

#LOOP PARSER
# this function allows for the use of the argument parser, this sets up the HMenu and adds prief descriptions for each - option
def loopit():
    parser = argparse.ArgumentParser(description="Hello, this app shows unique menu items at 3 different restaurants along with showing what menu items you can get at all 3 places. We recommend starting with -a to learn about the locations being compared!")
    parser.add_argument('-r', '--run', action='store_true', help="Runs the application")
    parser.add_argument('-a', '--about', action='store_true', help="Find out about the locations of each restaurant")
    parser.add_argument('-c', '--contacts', action='store_true', help="Find legitimate contact emails to reach out to all 3 options")
    parser.add_argument('-e', '--exit', action='store_true', help="Exits out of the application")

# acts as a set up for the arguments being parsed
    args = parser.parse_args()

# vars returns dictionary values, so if not any of the vars involved by defined args, in short this is checking the values are valid and expected upon what has already been defined if not, it pushes the help statement and gives the error message.
    if not any(vars(args).values()): 
        print("Error: this script requires the choice of only -h, for help, -a to learn about the choices, -r to run the script, -c for contacts, or -e to exit")
        parser.print_help()
        return

# Parsing the arguments and calls on each function once selected from the HMENU
    if args.run:
        runapp()
    elif args.about:
        aboutmenu()
    elif args.contacts:
        regexcontact()
    elif args.exit:
        exitapp()

# __name__ == __main__ makes sure that the loop of the loopit() functino is run only if the script is ran, since loopit contains the contents to complete the h menu its important its looped whenever run.
if __name__ == "__main__":
    loopit()
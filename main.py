# %%

import numpy as np
import settings
from exact_functions import *
from help_functions import *

# set global variable system and N
settings.init()

# Define menu items
# Define used variables
menuItems = np.array(["Choose type of Lindenmayer system and number of iterations", "Generate plots", "Change number of iterations", "Quit"])
LindenSystems = np.array(["Koch curve","Sierpinski triangle","User defined system"])



# Start
while True:
# Display menu options and ask user to choose a menu item
    choice = displayMenu(menuItems, "\nPlease choose a menu item: ")
# Menu item chosen
# ------------------------------------------------------------------
# 1. Load data
    if choice == 1:
# Ask user which type of Lindenmayer system to use
        Systemnumber = int(displayMenu(LindenSystems, "\nplease enter the Lindenmayer system you would like to work with: "))
        settings.System = settings.SystemsList[Systemnumber-1]
        while True:
            settings.N = inputInt("\nPlease choose the amount of iterations (recommended 0-9): ")
            if settings.N < 0:
                print("Iterations cannot be less than 0")
            elif settings.N >13:
                print("\nLarge amount of iterations, will have a long computing time")
                svar = input('Do you still wish to continue (y/n): ')
                if svar.lower() == "y":
                    break
                else:
                    pass
            else:
                break
        if settings.System == 'User defined':
            selfDefinedSystem() # asks for user input for the self defined system. Saves input globally.

# ------------------------------------------------------------------
# 2. Generate plot
    elif choice == 2:
# Is there choosen system and iteration?
        if settings.System == "":
# Display error message
            print("\nError: No system and iteration chosen, please choose those")
        else:
            LindenmayerString = LindIter(settings.System,settings.N)
            turtleCommands = turtleGraph(LindenmayerString)
            turtlePlot(turtleCommands)
# ------------------------------------------------------------------
# 3. Change number of iterations
    elif choice == 3:
# Is there choosen system and iteration?
        if settings.System == "":
# Display error message
            print("\nError: No system and iteration chosen, please choose those")
        else:
            settings.N = inputInt("\nPlease choose the amount of iterations (recommended 0-9): ")
# ------------------------------------------------------------------
# 4. Quit
    elif choice == 4:
# End
        break



# %%

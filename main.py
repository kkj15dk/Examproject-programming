import numpy as np
import settings
import pickle
from exact_functions import *
from help_functions import *
from datastorage import *

# set global variable system and N
settings.init()

# Define menu items
# Define used variables
menuItems = np.array(["Choose type of Lindenmayer system and number of iterations", "Generate plots", "Change number of iterations", "Save current L-system", "Factory reset of loaded L-systems", "Quit"])

# Start
while True:
# Display menu options and ask user to choose a menu item
    choice = displayMenu(menuItems, "\nPlease choose a menu item: ")
# Menu item chosen
# ------------------------------------------------------------------
# 1. Load data
    if choice == 1:
        settings.SystemsList = np.array(["Koch curve","Sierpinski triangle"])
        
        # load previously saved systems
        loaded_systems = list(loadall('systems.dat'))

        # load all systems, update the settings list and add user defined option
        for sys in loaded_systems:
            settings.SystemsList = np.append(settings.SystemsList, sys.name)
        settings.SystemsList = np.append(settings.SystemsList, "User defined")
# Ask user which type of Lindenmayer system to use
        Systemnumber = int(displayMenu(settings.SystemsList, "\nplease enter the Lindenmayer system you would like to work with: "))
        settings.System = settings.SystemsList[Systemnumber-1]
        # Have to rename the systems, since this is the input they need in LindIter()
        if settings.System == "Koch curve":
            settings.System = "Koch"
        elif settings.System == "Sierpinski triangle":
            settings.System = "Sierpinski"
        
        # To ask the user of the amount of iterations, and to tell them if they choose a lot of iterations if they're certain they want to continue
        while True:
            settings.N = inputInt("\nPlease choose the amount of iterations (recommended 0-9): ")
            if settings.N < 0:
                print("Iterations cannot be less than 0")
            elif settings.N >13:
                while True: 
                    print("\nLarge amount of iterations, will have a long computing time")   
                    svar = input('Do you still wish to continue (y/n): ')
                    if svar.lower() == "y" or svar.lower() == "n":
                        break
                    else:
                        pass
                if svar.lower == "n":
                    pass
                else:
                    break
            else:
                break

        if settings.System == 'User defined':
            selfDefinedSystem() # asks for user input for the self defined system. Saves input globally.

# ------------------------------------------------------------------
# 2. Generate plot
    elif choice == 2:
# Is there chosen system and iteration?
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
# Is there chosen system and iteration?
        if settings.System == "":
# Display error message
            print("\nError: No system and iteration chosen, please choose those")
        else:
            settings.N = inputInt("\nPlease choose the amount of iterations (recommended 0-9): ")
# ------------------------------------------------------------------
# 4. Save current system
    elif choice == 4:
# Is there chosen system and iteration?
        if settings.System == "":
# Display error message
            print("\nError: No system and iteration chosen, please choose those")
        elif settings.System == 'Sierpinski' or settings.System == 'Koch':
            print('\nSierpinski and Koch are already defined, these cannot be saved')
        else:
            while True:
                answer = input("Do you wish to rename the current L-system from " + settings.name + ' (y/n)? ')
                if answer == 'y':
                    settings.name = input('What do you want to save it as?\n')
                    break
                elif answer == 'n':
                    break
            # dump the new system along with all preexisting ones
            current_system = system(settings.name, settings.lettermapping, settings.selfdefined_start, settings.iteration_scaling) # create system based on system class
            
            previous_systems = loadall('systems.dat')

            list_of_loaded_systems = []
            for sys in loaded_systems:
                list_of_loaded_systems = list_of_loaded_systems + [sys]

            with open('systems.dat', 'wb') as systemsfile:
                for s in list_of_loaded_systems:
                    pickle.dump(s, systemsfile)
                pickle.dump(current_system, systemsfile) # dump new system to pickle

            # Update the list of loaded systems
            loaded_systems = list(loadall('systems.dat'))

# ------------------------------------------------------------------
# 5. Factory reset of loaded L-systems
    elif choice == 5:
        factoryReset()
# ------------------------------------------------------------------
# 6. Quit
    elif choice == 6:
# End
        break

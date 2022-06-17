from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
import settings

def inputInt(prompt):
    # Ask the user to input an integer
    while True:
        try:
            num = int(input(prompt))
            break
        except ValueError:
            pass
    return num

def inputStr(prompt):
    # Ask the user to input an integer
    while True:
        try:
            num = str(input(prompt))
            break
        except ValueError:
            pass
    return num

def inputFloat(prompt):
    # Ask the user to input a float
    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            pass
    return num

def inputFraction(prompt):
    # Ask the user to input an fraction or float
    while True:
        try:
            userinput = input(prompt)
            num = float(Fraction(userinput))
            break
        except:
            try:
                num = float(userinput)
                break
            except ValueError:
                pass
    return num

def displayMenu(options, message):
    # makes a menu of items that can be selected for
    # Input: the options of a menu, as well as the message to be displayed afterwards.
    # Output: the menu

    print('\n') # for prettier format

    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    
    choice = 0
    
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputInt(message)
    
    return choice

def displayMenuStr(options, message):
    # makes a menu of items that can be selected for
    # Input: the options of a menu, as well as the message to be displayed afterwards.
    # Output: the menu, the choice

    print('\n') # for prettier format

    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    
    choice = 0
    
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputInt(message)
    
    return choice


def selfDefinedSystem():
    # User input to define their own system. Changes settings file
    # Input: user input for the self defined L-system
    # Output:
    letteroptions = np.array(['A length', 'An angle', 'Do nothing'])
    while True:
        alphabet = input('\nInput the alphabet of the system(without spaces), make sure you have no duplicates, and only uppercase letters (or [ or ] for saving/loading position): ')
        allowed_chars = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', ']'])
    
        if np.all([char in allowed_chars for char in alphabet]) != True:
            print('\nOnly uppercase letters and [ or ] are allowed')
        elif np.any([alphabet[i] in alphabet[:i] + alphabet[i+1:] for i in range(len(alphabet))]):
            print('\nDuplicates are not allowed')
        else:
            break
    
    settings.iteration_scaling = inputFraction('\nInput what value you want the length of segments in the system to be scaled by after each iteration: ')
    settings.lettermapping = np.zeros((4,len(alphabet)), dtype = object) # for storing the alphabet(0) along with replacement rules(1), turtle grahping rules(2), and turtle grahping action(3) (length or angle)
    
    while True:
        settings.selfdefined_start = input('\nInput the startcondition of the system: ')
        # startconditions need to be a part of the alphabet
        if all(letters in alphabet for letters in settings.selfdefined_start):
            break
        else:
            print('\nYour startcondition needs to be a part of the alphabet')
    
    for i in range(len(alphabet)):
        settings.lettermapping[0,i] = alphabet[i]
        # To be able to use [ and ]
        if alphabet[i] == '[':
            settings.lettermapping[1,i] = '['
            settings.lettermapping[2,i] = 'save'
            settings.lettermapping[3,i] = 'save'
            continue
        elif alphabet[i] == ']':
            settings.lettermapping[1,i] = ']'
            settings.lettermapping[2,i] = 'load'
            settings.lettermapping[3,i] = 'load'
            continue
            

        while True:
            replacement = inputStr('\nWhat should ' + alphabet[i] + ' be replaced with, after each iteration?\n')
            if all(letters in alphabet for letters in replacement):
                settings.lettermapping[1,i] = replacement
                break
            else:
                print('\nAll letters of the replacement need to be part of your alphabet')
        
        option = displayMenu(letteroptions, 'What should ' + alphabet[i] + ' represent? ')
        if option == 1: # A length
            settings.lettermapping[2,i] = 'l' # placeholder
            settings.lettermapping[3,i] = 'length'
        elif option == 2: # An angle
            settings.lettermapping[2,i] = np.pi * inputFraction('\nWrite what value you want x to be, for an angle x*Pi. Positive values denote positive rotation. ')
            settings.lettermapping[3,i] = 'angle'
        elif option == 3: # do nothing
            settings.lettermapping[2,i] = 'nothing'
            settings.lettermapping[3,i] = 'nothing'

    while True:
        settings.name = input('\nWhat do you want to name your system?\n')
        if np.any(settings.name == settings.SystemsList):
            print('\nName cannot be the same as a predefined system (Sierpinski, Koch or User defined)')
        else:
            break
    return

def complexTurtlePlot(turtleCommands):
    # Input: turtleCommands: A row vector consisting of alternating length and angle specifications
    
    saved_positions = []
    saved_angles = []

    x = np.array([[0,0]])
    d = np.array([1,0])

    plt.subplots(1, 1, figsize = (15,15))

    for i in range(np.size(turtleCommands)):
        if settings.turtleAction[i] == 'length':
            x = np.vstack((x, x[-1] + turtleCommands[i] * d))
        elif turtleCommands[i] == 'save':
            # save position
            saved_positions.append(x[-1])
            saved_angles.append(d)
        elif turtleCommands[i] == 'load':
            # load position
            plt.plot(x[:,0],x[:,1], linewidth = 0.5)
            x = np.array([saved_positions[-1]])
            d = saved_angles[-1]
            saved_angles = saved_angles[:-1]
            saved_positions = saved_positions[:-1]
        elif turtleCommands[i] == 'nothing':
            pass
        else:
            darray = np.array([[np.cos(turtleCommands[i]), -np.sin(turtleCommands[i])], [np.sin(turtleCommands[i]), np.cos(turtleCommands[i])]])
            d = darray.dot(d)

    plt.plot(x[:,0],x[:,1], linewidth = 0.5)
    plt.axis('equal')
    if settings.System == 'User defined':
        plt.title(settings.name + ' system with ' + str(settings.N) + ' iterations')
    else:
        plt.title(settings.System + ' system with ' + str(settings.N) + ' iterations')
    plt.show()

def loadUserdefined(turtleCommands, LindenMayerstring):
    # load the user defined system
    l = settings.iteration_scaling**settings.N

    settings.turtleAction = np.zeros(np.size(turtleCommands), dtype = object)

    for i in range(len(LindenMayerstring)):
        command = settings.lettermapping[2][LindenMayerstring[i] == settings.lettermapping[0]] # vectorization is cool
        if command == 'l':
            turtleCommands[i] = l # i have to have this here, i cannot move it to turtlePlot because of the project specifications
            settings.turtleAction[i] = 'length'
        elif command == 'save':
            turtleCommands[i] = 'save'
            settings.turtleAction[i] = 'save'
        elif command == 'load':
            turtleCommands[i] = 'load'
            settings.turtleAction[i] = 'load'
        elif  command == 'nothing':
            turtleCommands[i] = 'nothing'
            settings.turtleAction[i] = 'nothing'
        else:
            turtleCommands[i] = float(command[0])
            settings.turtleAction[i] = 'other'
    return turtleCommands
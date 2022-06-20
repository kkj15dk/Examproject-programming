from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
import settings

def inputInt(prompt):
    """
    Ask the user to input an integer
    """
    while True:
        try:
            num = int(input(prompt))
            break
        except ValueError:
            print('Error: Please input a valid number')
    return num

def inputStr(prompt):
    """
    Ask the user to input an integer
    """
    while True:
        try:
            num = str(input(prompt))
            break
        except ValueError:
            print('Error: Please input a string')
    return num

def inputFloat(prompt):
    """ 
    Ask the user to input a float
    """
    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            print('Error: Please input a valid number')
    return num

def inputFraction(prompt):
    """
    Ask the user to input an fraction or float
    """
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
                print('Error: Please input a valid number (a simple fraction or float)')
    return num

def displayMenu(options, message):
    """
    makes a menu of items that can be selected for
    Input: the options of a menu, as well as the message to be displayed afterwards.
    Output: the menu, the choice
    """
    print('\n') # for prettier format

    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    
    choice = 0
    
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputInt(message)
    
    return choice

def selfDefinedSystem():
    """
    User input to define their own system. Changes settings file.

    The user is first asked to input the alphabet of their system.
    Then the value they want the line segments to be scaled by after each iteration.
    Then the startcondition of the system (axiom).
    For each letter of their alphabet, they must then specify the function of that letter, unless it is [ or ], where the function is assumed to be save position and load position respectively.
    Also, the specific angle to turn must be specified, if the letter is chosen to represent an angle.

    Input: user input for the self defined L-system
    
    Output: none
    """
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
    """
    A function to plot the fractal using a turtle, more complex than the standard turtlePlot function to accompany user defined systems.

    This function is implemented to be able to produce complex plots based on turtlecommands that don't neccesarily alternate between angle and length.

    Input: turtleCommands: A row vector consisting of alternating length and angle specifications

    Output: Screen output of the plot
    """

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
    """
    Loads the user defined system.

    Based on the variables in settings, 
    """
    l = settings.iteration_scaling**settings.N

    settings.turtleAction = np.zeros(np.size(turtleCommands), dtype = object)

    for i in range(len(LindenMayerstring)):
        command = settings.lettermapping[2][LindenMayerstring[i] == settings.lettermapping[0]] # vectorization is cool
        if command == 'l':
            turtleCommands[i] = l # We have to have this here, we cannot move it to turtlePlot because of the project specifications
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

def factoryReset():
    """
    For loading predefined systems into systems.dat using pickle, instead of loading each manually using the interface.
    """
    
    import pickle
    from datastorage import system

    # Create empty array
    predefined_systems = []

    # Koch Snowflake
    settings.System = 'User defined'
    settings.N = 2
    settings.name = 'Koch snowflake'
    settings.selfdefined_start = 'FLLFLLF'
    settings.iteration_scaling = 1/3
    settings.lettermapping = np.array([['F','L','R'],['FRFLLFRF','L', 'R'],['l', 1/3*np.pi, -1/3*np.pi],['length','other','other']])
    current_system = system(settings.name, settings.lettermapping, settings.selfdefined_start, settings.iteration_scaling) # create system based on system class
    predefined_systems.append(current_system)

    # Right angled Koch curve
    settings.System = 'User defined'
    settings.N = 2
    settings.name = 'Right angled Koch curve'
    settings.selfdefined_start = 'F'
    settings.iteration_scaling = 1/3
    settings.lettermapping = np.array([['F','L','R'],['FLFRFRFLF','L', 'R'],['l', 1/2*np.pi, -1/2*np.pi],['length','other','other']])
    current_system = system(settings.name, settings.lettermapping, settings.selfdefined_start, settings.iteration_scaling) # create system based on system class
    predefined_systems.append(current_system)

    # Dragon curve
    settings.System = 'User defined'
    settings.N = 2
    settings.name = 'Dragon curve'
    settings.selfdefined_start = 'F'
    settings.iteration_scaling = 1/2
    settings.lettermapping = np.array([['F', 'G', 'L','R'],['FLG','FRG','L', 'R'],['l', 'l', 1/2*np.pi, -1/2*np.pi],['length','length','other','other']])
    current_system = system(settings.name, settings.lettermapping, settings.selfdefined_start, settings.iteration_scaling) # create system based on system class
    predefined_systems.append(current_system)

    # Levy curve
    settings.System = 'User defined'
    settings.N = 2
    settings.name = 'Levy curve'
    settings.selfdefined_start = 'F'
    settings.iteration_scaling = 1/2
    settings.lettermapping = np.array([['F','L','R'],['LFRRFL','L', 'R'],['l', 1/4*np.pi, -1/4*np.pi],['length','other','other']])
    current_system = system(settings.name, settings.lettermapping, settings.selfdefined_start, settings.iteration_scaling) # create system based on system class
    predefined_systems.append(current_system)

    # Fractal tree
    settings.System = 'User defined'
    settings.N = 2
    settings.name = 'Fractal tree'
    settings.selfdefined_start = 'X'
    settings.iteration_scaling = 1/2
    settings.lettermapping = np.array([['X', 'F', 'L', 'R', '[', ']'],['FL[[X]RX]RF[RFX]LX','FF','L', 'R', '[', ']'],['nothing', 'l', 25/180*np.pi, -25/180*np.pi, 'save', 'load'],['other','length','other','other', 'save', 'load']])
    current_system = system(settings.name, settings.lettermapping, settings.selfdefined_start, settings.iteration_scaling) # create system based on system class
    predefined_systems.append(current_system)

    # Fractal bush
    settings.System = 'User defined'
    settings.N = 2
    settings.name = 'Fractal bush'
    settings.selfdefined_start = 'F'
    settings.iteration_scaling = 1
    settings.lettermapping = np.array([[ 'F', 'L', 'R', '[', ']'],['FFl[LFRFRF]R[RFLFLF]','L', 'R', '[', ']'],['l', 45/360*np.pi, -45/360*np.pi, 'save', 'load'],['length','other','other', 'save', 'load']])
    current_system = system(settings.name, settings.lettermapping, settings.selfdefined_start, settings.iteration_scaling) # create system based on system class
    predefined_systems.append(current_system)

    with open('systems.dat', 'wb') as systemsfile:
        for s in predefined_systems:
            pickle.dump(s, systemsfile)
import numpy as np
import matplotlib.pyplot as plt
import settings
from datastorage import *
from help_functions import *

def LindIter(System,N):
    # Input: string of the current system and integer of number of iteraions
    # Output: the lindenmayer string after that number of iterations in the L-system
    
    # for following the code
    print('\nStarted making the Lindenmayer string')

    if System == "Koch":
        LindenmayerString = 'S'
        for i in range(N):
            LindenmayerString = LindenmayerString.replace("S","SLSRSLS")
    elif System == "Sierpinski":
        LindenmayerString = 'A'
        for i in range(N):
            LindenmayerString = LindenmayerString.replace("A","bRARb")
            LindenmayerString = LindenmayerString.replace("B","ALBLA")
            LindenmayerString = LindenmayerString.replace("b","B")
    
    # The rest is for loading user defined systems
    elif System == "User defined":
        LindenmayerString = settings.selfdefined_start
        for i in range(N):
            for i in range(np.size(settings.lettermapping, axis = 1)):
                LindenmayerString = LindenmayerString.replace(settings.lettermapping[0,i], settings.lettermapping[1,i].lower())
            LindenmayerString = LindenmayerString.upper()
    else: # To be able to load user defined L-systems from previous instances of the application. For instance, this is where 'Dragon curve' comes from
        loaded_systems = loadall('systems.dat')
        for sys in loaded_systems:
            if System == sys.name:
                settings.name = sys.name
                settings.lettermapping = sys.lettermap
                settings.selfdefined_start = sys.start
                settings.iteration_scaling = sys.scaling
                LindenmayerString = settings.selfdefined_start
                for i in range(N):
                    for i in range(np.size(settings.lettermapping, axis = 1)):
                        LindenmayerString = LindenmayerString.replace(settings.lettermapping[0,i], settings.lettermapping[1,i].lower())
                    LindenmayerString = LindenmayerString.upper()
                break
    
    # for following the code
    print('Done making the Lindemayer string')
    
    return LindenmayerString

def turtleGraph(LindenMayerstring):
    """
    Based on the lindenmayerstring, construct turtlecommands for the turtle

    Input: LindenmayerString: A string of symbols representing the state of the system after the Lindemayer iteration.
    
    Output: turtleCommands: A row vector containing the turtle graphics commands consisting of alternating length and angle specifications
    """    
    # for following the code
    print('\nStarted making the turtle commands')

    # setup a vector of zeros
    turtleCommands = np.zeros(len(LindenMayerstring), dtype = object)

    if settings.System == 'Koch':
        # the length for Koch system
        l = (1/3)**settings.N
        
        for i in range(len(LindenMayerstring)):
            if LindenMayerstring[i] == 'S':
                turtleCommands[i] = l
            if LindenMayerstring[i] == 'L':
                turtleCommands[i] = 1/3 * np.pi
            if LindenMayerstring[i] == 'R':
                turtleCommands[i] = - 2/3 * np.pi
    elif settings.System == 'Sierpinski':
        # the length for Sierpinsky system
        l = (1/2)**settings.N
        
        for i in range(len(LindenMayerstring)):
            if LindenMayerstring[i] == 'A' or LindenMayerstring[i] == 'B':
                turtleCommands[i] = l
            if LindenMayerstring[i] == 'L':
                turtleCommands[i] = 1/3 * np.pi
            if LindenMayerstring[i] == 'R':
                turtleCommands[i] = - 1/3 * np.pi
    elif settings.System == 'User defined':
        # load the user defined system
        turtleCommands = loadUserdefined(turtleCommands, LindenMayerstring)
    else:
        # Assume there is a system loaded in settings, make turtlecommands based on this
        turtleCommands = loadUserdefined(turtleCommands, LindenMayerstring)

    # for following the code
    print('Done making the turtle commands')

    return turtleCommands

def turtlePlot(turtleCommands):
    """
    Based on the turtlecommands, plot the fractal.
    
    Input: turtleCommands: A row vector consisting of alternating length and angle specifications
    
    Output: screen output of the fractal plot
    """
    # for following the code
    print('\nStarted drawing the fractal')

    # We need to reroute to another turtleplotting function (complexTurtlePlot(turtleCommands)) if we use a complex L-system, different from Sierpinski and Koch
    if settings.System != 'Sierpinski' and settings.System != 'Koch':
        complexTurtlePlot(turtleCommands)
        return
    
    # Set up vector of zeros for position and direction vectors
    x = np.zeros((int((len(turtleCommands) + 3) / 2), 2))
    d = np.zeros((int((len(turtleCommands) + 1) / 2), 2))

    # Set the first position and direction
    x[0] = np.array([0,0])
    d[0] = np.array([1,0])

    # Calculate all values of d
    for i in range(np.size(d, axis = 0) - 1):
        darray = np.array([[np.cos(turtleCommands[2*i + 1]), -np.sin(turtleCommands[2*i + 1])], [np.sin(turtleCommands[2*i + 1]), np.cos(turtleCommands[2*i + 1])]])
        d[i + 1] = darray.dot(d[i])

    # Calculate all values of x
    # Mistake in the description of the project. It said d[i + 1], meant d[i] (to our knowledge)
    for i in range(np.size(x, axis = 0) - 1):
        x[i + 1] = x[i] + turtleCommands[2 * i] * d[i]

    plt.subplots(1, 1, figsize = (15,15))
    plt.plot(x[:,0],x[:,1], linewidth = 0.5)
    plt.axis('equal')
    if settings.System == 'User defined':
        plt.title(settings.name + ' system with ' + str(settings.N) + ' iterations')
    else:
        plt.title(settings.System + ' system with ' + str(settings.N) + ' iterations')
    
    # for following the code
    print('Done drawing the fractal')

    plt.show()


# NB: This is not a function from the project description, and is situated in this document, simply because all teh needed imports are here
def factoryReset():
    """
    For loading predefined systems into systems.dat using pickle, instead of loading each manually using the interface.
    """
    
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
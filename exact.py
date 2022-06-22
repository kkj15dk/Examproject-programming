import numpy as np
import matplotlib.pyplot as plt
import settings
import datastorage
import help

def LindIter(System,N):
    """
    Based on a given system and number of iterations, make a lindenmayer string.

    Input: string of the current system and integer of number of iteraions.
    
    Output: the lindenmayer string after that number of iterations in the L-system.
    """
    
    # for following the code
    print('\nStarted making the Lindenmayer string')

    # For koch or sierpinski system
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
        loaded_systems = datastorage.loadall('systems.dat')
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
    Based on the lindenmayerstring, construct turtlecommands for the turtle.

    Input: LindenmayerString: A string of symbols representing the state of the system after the Lindemayer iteration.
    
    Output: turtleCommands: A row vector containing the turtle graphics commands consisting of alternating length and angle specifications
    """    
    # for following the code
    print('\nStarted making the turtle commands')

    # setup a vector of zeros
    turtleCommands = np.zeros(len(LindenMayerstring), dtype = object)

    # A global variable, settings.System, is used to differentiate between different L-systems
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
        turtleCommands = help.loadUserdefined(turtleCommands, LindenMayerstring)
    else:
        # Assume there is a system loaded in settings, make turtlecommands based on this
        turtleCommands = help.loadUserdefined(turtleCommands, LindenMayerstring)

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
        help.complexTurtlePlot(turtleCommands)
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

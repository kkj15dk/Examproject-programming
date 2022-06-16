import numpy as np
import matplotlib.pyplot as plt

# # The given system will be declared globally so it is easier to create new systems
# System = 'Sierpinski'
# N = 8

def LindIter(System,N):
    if System == "Koch":
        LindenmayerString = 'S'
        for i in range(N):
            LindenmayerString = LindenmayerString.replace("S","SLSRSLS")
    if System == "Sierpinski":
        LindenmayerString = 'A'
        for i in range(N):
            LindenmayerString = LindenmayerString.replace("A","bRARb")
            LindenmayerString = LindenmayerString.replace("B","ALBLA")
            LindenmayerString = LindenmayerString.replace("b","B")
    return LindenmayerString

def turtleGraph(LindenMayerstring):
    # Input: LindenmayerString: A string of symbols representing the state of the system after the Lindemayer iteration.
    # Output: turtleCommands: A row vector containing the turtle graphics commands consisting of alternating length and angle specifications
    
    # setup a vector of zeroes
    turtleCommands = np.zeros(len(LindenMayerstring))

    if System == 'Koch':
        # the length for Koch system
        l = (1/3)**N
        
        for i in range(len(LindenMayerstring)):
            if LindenMayerstring[i] == 'S':
                turtleCommands[i] = l
            if LindenMayerstring[i] == 'L':
                turtleCommands[i] = 1/3 * np.pi
            if LindenMayerstring[i] == 'R':
                turtleCommands[i] = - 2/3 * np.pi
            
    if System == 'Sierpinski':
        # the length for Sierpinsky system
        l = (1/2)**N
        
        for i in range(len(LindenMayerstring)):
            if LindenMayerstring[i] == 'A' or LindenMayerstring[i] == 'B':
                turtleCommands[i] = l
            if LindenMayerstring[i] == 'L':
                turtleCommands[i] = 1/3 * np.pi
            if LindenMayerstring[i] == 'R':
                turtleCommands[i] = - 1/3 * np.pi

    return turtleCommands

def turtlePlot(turtleCommands):
    # Insert your code here
    # Input: turtleCommands: A row vector consisting of alternating length and angle specifications
    
    
    x = np.zeros((int((len(turtleCommands) + 3) / 2), 2))
    d = np.zeros((int((len(turtleCommands) + 1) / 2), 2))

    x[0] = np.array([0,0])
    d[0] = np.array([1,0])

    for i in range(np.size(d, axis = 0) - 1):
        darray = np.array([[np.cos(turtleCommands[2*i + 1]), -np.sin(turtleCommands[2*i + 1])], [np.sin(turtleCommands[2*i + 1]), np.cos(turtleCommands[2*i + 1])]])
        d[i + 1] = darray.dot(d[i])

    # Mistake in the description of the project. It said d[i + 1], meant d[i]
    for i in range(np.size(x, axis = 0) - 1):
        x[i + 1] = x[i] + turtleCommands[2 * i] * d[i]

    plt.subplots(1, 1, figsize = (15,15))
    plt.plot(x[:,0],x[:,1], linewidth = 0.5)
    plt.axis('equal')
    plt.title(System + ' system with ' + str(N) + ' iterations')
    plt.show()

# # Test
# String = LindIter(System,N)
# print(String)
# commands = turtleGraph(String)
# print(commands)
# turtlePlot(commands)
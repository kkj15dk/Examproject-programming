import pickle

class system():
    """ 
    A class for saving the current system using pickle.

    The class has the following:

    name: string of the name of the system
    lettermap: numpy array object with alphabet of the L-system, along with replacement rules turtleCommands and turtleActions
    start: the start condition of the system
    scaling: what the lengths should be scaled by after each iteration
    """
    def __init__(self, name, lettermap, start, scaling):
        self.name = name
        self.lettermap = lettermap
        self.start = start
        self.scaling = scaling

def loadall(filename):
    """
    A function for loading all systems saved in the systems.dat.
    
    It is a generator, going through all dumps in the file systems.dat
    """
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
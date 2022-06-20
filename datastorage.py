import pickle

class system():
    # A class for saving the cyrrent system using pickle
    def __init__(self, name, lettermap, start, scaling):
        self.name = name
        self.lettermap = lettermap
        self.start = start
        self.scaling = scaling

def loadall(filename):
    # A function for loading all systems saved in the systems.dat.
    # A generator
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break
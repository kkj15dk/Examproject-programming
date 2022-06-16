import pickle

class system():
    def __init__(self, name, lettermap, start, scaling):
        self.name = name
        self.lettermap = lettermap
        self.start = start
        self.scaling = scaling

def loadall(filename):
    with open(filename, "rb") as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break

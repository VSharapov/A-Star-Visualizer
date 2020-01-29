#Class that defines the single square in the grid that we are searching
#This will hold the f,g,h scores, the parent and the position of the node

class Node():

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

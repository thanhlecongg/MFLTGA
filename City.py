import math


class City:

    '''
    Present point in Oxy (x, y)
    '''
    def __init__(self,x ,y):
        self.x = x
        self.y = y

    def __str__(self):
        print(str(self.x) + ", " + str(self.y))

    def euclidDistance(self,other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

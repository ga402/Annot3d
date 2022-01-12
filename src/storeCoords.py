import itertools


class storeCoords:
    newid = itertools.count().__next__

    def __init__(self):
        self.id = storeCoords.newid()
        self.x = None
        self.y = None
        self.h = None
        self.w = None
        self.z0 = None
        self.z1 = None

    def __str__(self):
        return(
            f"id ={self.id}, x={self.x}, y={self.y}, w={self.w}, h={self.h}, z0={self.z0}, z1={self.z1}"
        )

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y

    def setH(self, h):
        self.h = h

    def setW(self, w):
        self.w = w

    def setZ0(self, z):
        self.z0 = z

    def setZ1(self, z):
        self.z1 = z

    def getCoords(self):
        return {
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "h": self.h,
            "w": self.w,
            "z0": self.z0,
            "z1": self.z1,
        }

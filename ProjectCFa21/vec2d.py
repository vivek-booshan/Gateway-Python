import math
from math import cos, sin
class Point():
    def __init__(self, x=0, y=0):
        """generate point (x, y)

        Args:
            x (int, optional): x coordinate. Defaults to 0.
            y (int, optional): y coordinate. Defaults to 0.
        """        
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """string representation

        Returns:
            str: representation of point as x: {} y: {}
        """        
        return "x: %s y: %s" % (self.x, self.y)
    
    def __add__(self, other) -> "Point":
        """element by element addition of two objects of class 'Point'

        Returns:
            Point: object of class Point
        """        
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other) -> "Point":
        """element by element subtraction of two objects of class 'Point'

        Returns:
            Point: object of class Point
        """        
        return Point(self.x - other.x, self.y - other.y)

    def __iadd__(self, other) -> "Point":
        """updates Point with element by element addition of other object of class Point

        Returns:
            Point: object of class Point
        """        
        return self.__add__(other)
    
    def __isub__(self, other) -> "Point":
        """updates Point with element by element subtraction of other object of class Point

        Returns:
            Point: object of class Point
        """        
        return self.__sub__(other)

    def rotate_pt(self, pivot, angle) -> "Point":
        """rotate a point around a pivot by arbitrary angle

        Args:
            pivot (Point): point around which to pivot point
            angle (int / float): angle at which to rotate point

        Returns:
            Point: object of class Point
        """
        #set pivx and pivy as x and y components of Point pivot        
        pivx, pivy = pivot.x, pivot.y
        #set px and py as x and y components of Point self
        px, py = self.x, self.y
        #implement rotation matrix (not really a matrix) to generate new point (x, y)
        new_x = pivx + cos(angle)*(px - pivx) - sin(angle)*(py - pivy)
        new_y = pivy + sin(angle)*(px - pivx) + cos(angle)*(py - pivy)
        return Point(new_x, new_y)

class Vec2D(Point):
    def __init__(self, x=0, y=0):
        """Generate vector <x, y>

        Args:
            x (int or Point, optional): x component of vector. Defaults to 0.
            y (int or Point or NoneType, optional): y component of vector. Defaults to 0.
        """        
        # handles input of type Vec2D(Point(), Point())
        if type(x) == Point and type(y) == Point:
            self.x = y.x - x.x
            self.y = y.y - x.y
        #handles input of type Vec2D(Point())
        elif type(x) == Point:
            self.x = x.x
            self.y = x.y
        #handles input of type Vec2D(num1, num2)
        else:
            super().__init__(x, y)

    def __add__(self, other) -> "Point":
        """element by element addition of two objects of class Vec2D

        Returns:
            Vec2D: object of class Vec2D
        """        
        return Vec2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other) -> "Point":
        """element by element subtraction of two objects of class Vec2D

        Returns:
            Vec2D: object of class Vec2D
        """        
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, a):
        """multiply by scalar and return class Vec2D or return dot product of two vectors 

        Args:
            a (int / float): scale factor
            a (Vec2D / Point): multiply by object of class Vec2D or class Point

        Returns:
            dot_prod (int / float): returns int or float value of dot product of two vectors
            Vec2D: object of class Vec2D
        """        
        #handles input of class Vec2D or Point and returns dot product
        if type(a) == (Vec2D or Point):
            # sum of element by element multiplication of self with a
            dot_prod = self.x*a.x + self.y*a.y
            return dot_prod
        #handles input of type int or float and returns a scaled vector
        elif type(a) == (int or float):
            #define scale_factor as unit scalar by dividing "a" with magnitude of self
            scale_factor = a/self.norm()
            x = self.x * scale_factor
            y = self.y * scale_factor
            return Vec2D(x, y)
    
    def norm(self) -> "Vec2D":
        """return magnitude of a vector

        Returns:
            float: returns magnitude of a vector using the pythagorean formula
        """        
        return math.sqrt(self.x**2 + self.y**2)

if __name__ == '__main__':
    u = Vec2D(3, 4)
    v = Vec2D(1, 1)
    scaled_vec = v * 2
    print(v, scaled_vec)
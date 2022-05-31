from vec2d import Point as P
from vec2d import Vec2D as V
from math import pi

class ConvexPolygon:
    def __init__(self, verts) -> None:
        """generate object of class ConvexPolygon

        Args:
            verts (list): list of points of class Point
        """        
        #assertion check to make sure list is of class Point
        assert [type(i) == P for i in verts] == [True]*len(verts), "vertices are not object 'Point'"
        #method object for vertices in polygon
        self.verts = verts
        #generate method object for number of vertices in polgyon
        self.nverts = len(verts)
        #generate a vector for each side of the polygon as method object
        #self.verts[(i + 1) % self.nverts] orders as [1, 2, 3, 0] without an if/else statement
        self.edges = [V(self.verts[i], self.verts[(i+1) % self.nverts]) for i in range(self.nverts)]

    def __repr__(self) -> str:
        """string representation of object of class ConvexPolygon

        Returns:
            str: Displays No. of Vertices, Vertices, and Edges in separate lines
        """        
        return f"""No. of Vertices: {self.nverts}\nVertices: {self.verts}\nEdges: {self.edges}""" 
    
    def array(self):
        """convert list into array for use of matrix operations in function rotate.
        Primarily used in for test_convexpolygon file to compare with np.linalg version of the rotation function

        Returns:
            array: converts list to array
        """ 
        #empty array       
        array = []
        #using enumerate to get index and values separate and reader friendly
        for vert, _ in enumerate(self.verts):
            #parse through each point in polygon and append list [x, y] into array
            array.append([self.verts[vert].x, self.verts[vert].y])
        return array

    def translate(self, vector: V) -> "ConvexPolygon":
        """translates self (of class ConvexPolygon) across euclidean space by vector V

        Args:
            vector (Vec2D): object of class Vec2D
        """
        for vert, _ in enumerate(self.verts):
            #update each Point by iadd-ing vector
            self.verts[vert] += vector
        #define new polygon and set to updated values of self
        #reason to do this is for debugging issues and clarity
        ngon = ConvexPolygon(self.verts)
        #update self with ngon
        self.verts = ngon.verts
        self.edges = ngon.edges
    
    def centroid(self):
        """find center of a convex polygon

        Returns:
            Point: returns the center of a convex polygon as an object of class Point
        """ 
        #set center @ origin       
        center = P()
        #set n as number of vertices
        n = self.nverts
        #set Area to zero
        Area = 0
        #implementation of the shoelace method; area = 1/2 * sum(determinants)
        for vert, _ in enumerate(self.verts):
            x0, y0 = self.verts[vert].x, self.verts[vert].y
            x1, y1 = self.verts[(vert + 1) % n].x, self.verts[(vert + 1) % n].y
            det = (x0 * y1) - (x1 * y0)
            #update area with value of determinant (area of linear transformation by two vectors)
            Area += det
            #update centroid center based on each iteration of determinant
            center.x += (x0 + x1) * det
            center.y += (y0  + y1) * det
        #multiply area by half to get actual area
        Area *= 0.5
        #divide center values by the area sixfold 
        center.x /= 6*Area
        center.y /= 6*Area
        #return center as point
        return center

    def rotate(self, angle, pivot=0):
        """rotates self (of class polygon) by angle around a pivot point

        Args:
            angle (int / float): angle at which to rotate the polygon
            pivot (Point, optional): point at which to pivot polygon. Defaults to 0.
        """  
        #handles no input for pivot by calling centroid     
        if pivot == 0:
            center = self.centroid()
        #else handles Point argument by setting center as pivot
        else:
            center = pivot
        #generate new point list of vertices by calling rotate_pt for each vertex in polygon
        new_pt_list = [vert.rotate_pt(center, angle) for vert in self.verts]
        #set new polygon as points of new_pt_list for testing and readability issues
        ngon = ConvexPolygon(new_pt_list)
        #update self with ngon
        self.verts = ngon.verts
        self.edges = ngon.edges

    
    def scale(self, n1: float, n2: float) -> "ConvexPolygon":
        """performs linear transformation on ConvexPolygon
        """
        #assertion check to make sure n1 and n2 are type(int) or type(float)
        assert type(n1) == float or int, "Not float or integer object"
        assert type(n2) == float or int, 'Not float or integer object'
        #scales x and y component of each vertex in self
        for vert, _ in enumerate(self.verts):
            self.verts[vert].x *= n1
            self.verts[vert].y *= n2
        #generate Convex Polygon of updated values of self
        ngon = ConvexPolygon(self.verts)
        #define self with ngon
        self.verts = ngon.verts
        self.edges = ngon.edges

if __name__ == "__main__":
    a = ConvexPolygon([P(1,0), P(0,1), P(-1,0), P(0,-1)])
    b = ConvexPolygon([P(0,0), P(1,0), P(1,1), P(0,1)])
    c = ConvexPolygon([P(0,0), P(1,0), P(1,1), P(0,1)])
    print(a)
    #A = a.centroid()
    a.rotate(pi/4, P())
    #A = a.centroid()
    #a.scale(2, 2)
    print(a)

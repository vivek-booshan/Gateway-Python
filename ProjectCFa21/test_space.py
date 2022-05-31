from vec2d import Point as P
from vec2d import Vec2D as V
from math import pi, cos, sin
from numpy import dot, array

class ConvexPolygon:
    def __init__(self, verts) -> None:
        """generate object of class ConvexPolygon

        Args:
            verts (list): list of points of class Point
        """        
        #assertion check to make sure list is of class Point
        assert [type(i) == P for i in verts] == [True]*len(verts), "vertices are not object 'Point'"
        self.verts = verts
        self.nverts = len(verts)
        self.edges = [verts[i] - verts[i-1] for i, _ in enumerate(verts)]

    def __repr__(self) -> str:
        return f"""No. of Vertices: {self.nverts}\nVertices: {self.verts}\nEdges: {self.edges}""" 
    
    def array(self):
        """convert list into array for use of matrix operations in function rotate.

        Returns:
            array: converts list to array
        """        
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
        center = [0, 0]
        n = self.nverts
        Area = 0
        #pts = self.array
        for vert, _ in enumerate(self.verts):
            x0, y0 = self.verts[vert].x, self.verts[vert].y
            x1, y1 = self.verts[(vert + 1) % n].x, self.verts[(vert + 1) % n].y
            A = (x0 * y1) - (x1 * y0)
            Area += A

            center[0] += (x0 + x1) * A
            center[1] += (y0  + y1) * A
        Area *= 0.5
        center[0] = (center[0]) / (6 * Area)
        center[1] = (center[1]) / (6 * Area)
        print(center)
        return P(center[0], center[1])

    def rotate(self, angle, pivot=0):
        if pivot == 0:
            center = self.centroid()
            #center = [[centroid.x, centroid.y]]
        else:
            center = pivot
            #center = [[pivot.x, pivot.y]]
        pts = [vert for vert in self.verts]
        print(pts)
        for pt in pts:
            pt.rotate_pt(center, angle)
            print(pt)
        print(pts)
        ngon = ConvexPolygon(pts)
        self = ngon
        pass

    '''
    def rotate(self, angle: float, pivot=None) -> "ConvexPolygon":
        """rotates self by radian angle around pivot P. If pivot is not defined, defaults to centroid of the polygon.

        Args:
            angle (int / float): int or float value in radians
            pivot (Point): object of class Point around which to pivot. Defaults to centroid of polygon.
        """
        #define point pivot center
        # if type(pivot) == 0:
        #     center = self.centroid()
        #     center = array([center.x, center.y])       
        try:
            center = array([pivot.x, pivot.y])
        except:
            centroid_pt = self.centroid()
            center = array([centroid_pt.x, centroid_pt.y])
        #convert self to array
        pts = self.array()
        #generate new set of x and y components as array
        new_set = array([[cos(angle), sin(angle)], [-sin(angle), cos(angle)]])
        #generate new points by doing matrix multiplication of diagonals (pts - center) of polygon with new_set moved to center
        new_pts = dot(pts - center, new_set + center).tolist()
        #empty list of new points for updating self
        new_pts_list = []
        for new_pt in new_pts:
            #add new point to new_pts_list
           new_pts_list.append(P(new_pt[0], new_pt[1]))
        #generate Convex Polygon of vertices new_pts_list
        ngon = ConvexPolygon(new_pts_list)
        #update self values with ngon values
        self.verts = ngon.verts
        self.nverts = ngon.nverts
        self.edges = ngon.edges
    '''
    
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
    a = ConvexPolygon([P(0,0), P(1,0), P(1,1), P(0,1)])
    b = ConvexPolygon([P(0,0), P(1,0), P(1,1), P(0,1)])
    c = ConvexPolygon([P(0,0), P(1,0), P(1,1), P(0,1)])

    #A = a.centroid()
    a.rotate(pi/4, P())
    #A = a.centroid()
    #a.scale(3, 6/4)
    print(a)

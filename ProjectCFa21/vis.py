from vec2d import Point as P
from vec2d import Vec2D as V
from convexpolygon import ConvexPolygon
from math import pi
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as vis_ngon
import seaborn as sns

######################################################################################
sns.set_style("white", {'xtick.direction': u'in','ytick.direction': u'in'})
sns.set_context("poster")
######################################################################################

def create_vis_polygon(pgon):
    """
        Package vertices of polygon into a Polygon patch object.
        
        Parameters
        ----------
        pgon : ConvexPolygon object

        Returns
        -------
        Polygon patch object that is used by matplotlib
    """  
    vts = []        
    for pt in pgon.verts:
        vts.append([pt.x, pt.y])
    
    return vis_ngon(np.array(vts), color=np.random.rand(3), alpha=0.6)
    
def vis_polygons ( pgons ):
    """
        Visualize polygons
        
        Parameters
        ----------
        pgons : List of ConvexPolygon objects

        Returns
        -------
        None.

    """

    #Create a plot
    fig,ax = plt.subplots()

    for igon in pgons:

        # Add polygon to plot
        p = create_vis_polygon(igon)  
        ax.add_patch(p)

    # Show plot
    ax.autoscale()
    ax.set_aspect('equal')
    plt.show()

    return
        
if __name__=='__main__':

    # cnvx_ngon is an alias for ConvexPolygon
        
    a = ConvexPolygon([P(1,0), P(0,1), P(-1,0), P(0,-1)])
    b = ConvexPolygon([P(1,0), P(0,1), P(-1,0), P(0,-1)])
    c = ConvexPolygon([P(0,0), P(1,0), P(1,1), P(0, 1)]) 

    #c = ConvexPolygon([P(3,0), P(-1,2), P(-1,0)])  
    a.rotate(pi/3)
    # b.rotate(2*pi/3, P())
    # c.rotate(pi, P())
    #c.rotate(pi/2, P())
    #c.translate(V(3, 0))
    b.scale(2, 2)
    vis_polygons([a, b, c])
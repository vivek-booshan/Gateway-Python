#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 11:54:59 2020

@author: vivekbooshan
"""
import math

import numpy as np
from misc import include_atoms_gr, include_atoms_nt, grid_pq

class CarbonFiller():
    def __init__(self, n=0, m=0, l=0) -> None:
        """
        Attributes of CarbonFiller

        Args:
            n (int, optional): The number of hops in the a1 direction. Defaults to 0.
            m (int, optional): The number of hops in the a2 direction. Defaults to 0.
            l (int, optional): The length of the carbon nanotube. Defaults to 0.
            name (str): CarbonFiller
        """        
        self.n = n
        self.m = m
        self.l = l
        self.name = 'Carbon Filler'
        pass

    def vector(self) -> list:
        """
        Instance method for finding the coordinates for the vector Ch,
        by making n hops in the a1 direction and m hops in the a2 direction.

        Returns:
            Ch (list of floats): list of x and y coordinates for Ch
        """ 
        #a1 lies on the (x, 0) line. Scale to cartesian coordinates               
        ch10, ch11 = self.n*math.sqrt(3), 0
        #a2 shears the xy plane @ -45 degrees. Scale to cartesian coordinates
        ch20, ch21 = self.m*math.sqrt(3)/2, self.m*-3/2
        #add x & y components of a1 & a2 to find Ch coordinates
        vector = [ch10 + ch20, ch11 + ch21]
        #round up to 3 decimal places
        Ch = [round(component, 3) for component in vector]
        return Ch

    @staticmethod
    def normVector(vec) -> tuple([list, list]):
        """
        Static method for normalizing vector Ch. 
        Returns the vector c_hat and the magnitude.

        Args:
            vec (list of floats, len(vec)=2): list of x and y coordinates for Ch

        Returns:
            norm_vec (list of floats): Coordinates of the normalized vector c_hat
            norm (float): Length of vector Ch
        """
        #Find magnitude of vector
        norm = math.sqrt(sum(index**2 for index in vec))
        norm = round(norm, 3)
        #Find x, y components of the magnitude
        norm_vec = [round(index/norm, 3) for index in vec]
        return norm_vec, norm

    @staticmethod
    def normTvector(c_hat) -> list:
        """
        Static method to find the coordinates of an orthogonal vector to Ch.
        Takes a list input and returns a list output of equal dimensions.

        Args:
            c_hat (list of floats): normalized vector of Ch

        Returns:
            t_hat (list of floats): normalized vector orthogonal to c_hat
        """        
        #assign c_hat(x, y) -> t_hat(-y, x)
        t_hat = [-c_hat[1], c_hat[0]]
        return t_hat

    def TVector(self, Ch) -> list:
        """
        Instance method for finding coordinates of vector T orthogonal to Ch.
        Utilizes normVector() and normTvector().

        Args:
            Ch (list of floats): Coordinates of vector Ch

        Returns:
            T (list of floats): Coordinates of vector T
        """        
        #extract norm_vec from normVector as c_hat
        c_hat = self.normVector(Ch)[0]
        #convert c_hat to t_Hat using normTvector
        t_hat = self.normTvector(c_hat)
        #scale t_hat by the length of the nanotube
        T = [th * self.l for th in t_hat]
        return T

    @staticmethod
    def pq(Ch, T) -> tuple([list, list]):
        """Find the smallest rectangle with integer components encasing all atoms within the grid formed by Ch and T

        Args:
            Ch (list): Ch vector
            T (list): T vector

        Returns:
            p (list): returns integer domain of x
            q (list): returns integer range of y
        """        
        #values by which x and y are scaled
        xiter = math.sqrt(3)/2
        yiter = 3/2
        #convert back to n and m and sort by float 
        p = sorted([Ch[0]/ xiter, T[0] / xiter], key=float)
        #set p as integer values of domain
        p[0], p[1] = math.floor(p[0]), math.ceil(p[0] + p[1])
        #convert back to n and m and sort by float 
        q = sorted([Ch[1] / yiter, T[1] / yiter], key=float)
        #set p as integer values of range
        q[0], q[1] = math.floor(q[0]), math.ceil(q[1])
        return p, q

    @staticmethod
    def coordinates(pg, qg) -> tuple([list, list]):
        """
        Static method for identifying the coordinates of atoms within the (p, q) grid.
        Returns 2 nested lists holding the x and y coordinates of each atom.

        Args:
            pg (nested list): nested list holding the integers used to identify each atom 
                along the  x-direction
            qg (nested list): nested list holding the integers used to identify each atom 
                along the y-direction

        Returns:
            x (nested list): nested list of an atoms' x coordinates
            y (nested list): nested list of an atoms' y coordinates
        """
        #for each x component in pg, scale by sqrt(3)/2 and round up to 3rd decimal        
        x = [[round(coord * math.sqrt(3)/2, 3) for coord in coordinates] for coordinates in pg]
        #y scale factor
        yscale = 1.5
        #set y as empty list
        y = []
        #zip pg and qg together and parse through the x and y coordinate list
        for coordinatesx, coordinatesy in zip(pg, qg):
            #zip coordinatesx and coordinatesy and parse through every p and q value
            #for each q, scale y and subtract by 0.5 or 1.5 given (pval+qval)%2
            y.append([yscale*qval - ((pval+qval)%2 * 0.5) for pval, qval in zip(coordinatesx, coordinatesy)])
        return x, y
    
    @staticmethod
    def distance(x, y, c_hat) -> tuple([list, list]):
        """
        Function for computing distance of any atom along the mouth and length direction.
        Takes dot product of two coordinate vectors and returns atom position.

        Args:
            x (nested list): nested list of an atoms' x coordinates
            y (nested list): nested list of an atoms' y coordinates
            c_hat (list): x and y components of c_hat

        Returns:
            s (nested list): nested list of an atoms' distance along the mouth direction
            t (nested list): nested list of an atoms' distance along the length direction
        """               
        #set t_hat
        t_hat = CarbonFiller.normTvector(c_hat)
        #zip x and y to align lists; zip each list and extract the x value and yvalue
        #then compute the dot product with c_hat for s and with t_hat for t and append to nested list 
        s = [[round(c_hat[0]*xval + c_hat[1]*yval, 3) for xval, yval in zip(xList, yList)] for xList, yList in zip(x, y)]
        t = [[round(t_hat[0]*xval + t_hat[1]*yval, 3) for xval, yval in zip(xList, yList)] for xList, yList in zip(x, y)]
        return s, t

def Graphene(n=0, m=0, l=0) -> tuple([np.ndarray, np.ndarray]):
    """
    Utilize class CarbonFiller to return a numpy array for plotting a 
    2d display of the graphene sheet or 3d display of the carbon nanotube

    Args:
            n (int, optional): The number of hops in the a1 direction. Defaults to 0.
            m (int, optional): The number of hops in the a2 direction. Defaults to 0.
            l (int, optional): The length of the carbon nanotube. Defaults to 0.
    Returns:
        pos_gr (ndarray): A numpy array containing the coordinates of the atoms 
            included in the graphene sheet.
        pos_nt (ndarray): A numpy array containing the coordinates of the atoms
            included in the carbon nanotube
    """ 
    #create object of class CarbonFiller   
    Cf = CarbonFiller(n, m, l)
    #set Ch vector
    Ch = Cf.vector()
    #set T vector
    T = Cf.TVector(Ch)
    #find integer domain and range encapsulating Ch and T
    p, q = Cf.pq(Ch, T)
    #mesh grid of p and q
    Pgrid, Qgrid = grid_pq(p, q)
    #find x and y components of each atom
    x, y = Cf.coordinates(Pgrid, Qgrid)
    #set the normal vector and magnitude as c_hat and arclen
    c_hat, arclen = Cf.normVector(Ch)
    #find s and t components of each atom
    s, t = Cf.distance(x, y, c_hat)
    #set pos_gr array
    pos_gr = include_atoms_gr(x, y, s, t, arclen, l)
    #divide arclen by 2pi to find radius of tube
    tubrad = arclen / (2*math.pi)
    #set pos_nt array
    pos_nt = include_atoms_nt(pos_gr, c_hat, arclen, tubrad)

    return pos_gr, pos_nt

if __name__ == "__main__": 
    from atomplot import plot
    #define drug radius and solve for drug diameter
    drugrad = 4
    drugdia = drugrad*2
    drugdia /= 1.42
    #set while loop conditions to zero
    tubdia, minzigzag, minarmchair = 0, 0, 0
    #while tube diameter less than or equal to drug diameter,
    #performs the following
    while tubdia <= drugdia:
        #increment minzigzag
        minzigzag += 1
        #define object Czig using minzigzag
        Czig = CarbonFiller(minzigzag, 0, 0)
        #set Ch as Ch vector of Czig
        Ch = Czig.vector()
        #set arclen to the magnitude of Ch
        _, arclen = CarbonFiller.normVector(Ch)
        #solve for tube diameter
        tubdia = arclen/(math.pi)
    #reset tube diameter
    tubdia = 0
    #while tube diameter less than or equal to drug diameter,
    #performs the following
    while tubdia <= drugdia:
        #increment minarmchair
        minarmchair += 1
        #define object Carm using minarmchair
        Carm = CarbonFiller(minarmchair, minarmchair, 0)
        #set Ch as Ch vector of Carm
        Ch = Carm.vector()
        #set arclen to the magnitude of Ch
        _, arclen = CarbonFiller.normVector(Ch)
        #solve for tube diameter
        tubdia = arclen / (math.pi)
    #set numpy arrays for zigzag and armchair to get graphene and nanotube plots
    pos_gr_zig, pos_nt_zig = Graphene(minzigzag, 0, 2)
    pos_gr_arm, pos_nt_arm = Graphene(minarmchair, minarmchair, 2)
    print(f'zigzag = {minzigzag}\narmchair = {minarmchair}')

    # plot(pos_gr_zig)
    # plot(pos_nt_zig)
    # plot(pos_gr_arm)
    # plot(pos_nt_arm)

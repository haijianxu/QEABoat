'''
Quantitative Engineering Analysis course Spring 2016
Boat Design calculation code
'''

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.optimize import fsolve
import math

def righting_arm(n,theta):
    '''
        Returns a coordinate and magitude of righting moment of the boat
    '''
    
    d = .5 #compare() will replace this

    y = np.linspace(-1,1,1000)
    f1 = np.absolute(y)**n - 1 #Hull function without lambda    
    f2 = -np.tan(theta)*y - d

    hull_function = lambda y: np.absolute(y)**n - 1
    water_line = lambda y: -np.tan(theta)*y - d
    
    #displacement(hull_function, water_line,n,theta,d) 
    varying_theta_calc_displacement(n,d)
  #  plot_graph(f1, f2,hull_function,water_line,intersection(hull_function,water_line,n,theta,d))
   
def intersection(hull_func,water_func,n,theta,d):
    '''
        Takes in function representation of hull and water line and then returns the roots
    '''
    func_difference = lambda y: (-np.tan(theta)*y - d) - (np.absolute(y)**n - 1)
    root = fsolve(func_difference,[-10,10])

    if np.absolute(root[0]) > 1:
        root[0] = fsolve(water_func,0)
    elif np.absolute(root[1]) >1:
        root[1] = fsolve(water_func,0)
    print 'this is root', root
    return root

def displacement(hull_func, water_func,n,theta,d):
    '''
        Finds a volume under water
        args: limits - a list with 2 elements (roots)
    '''
    limits = intersection(hull_func, water_func,n,theta,d)
    func_difference_down = lambda y: (-np.tan(theta)*y - d)- (np.absolute(y)**n - 1)
    func_difference_up = lambda y: (-np.tan(theta)*y - d)
    
    print "root value: ", abs(water_func(limits[0]))
    if abs(water_func(limits[0]))<0.01:
        area1 = np.absolute(integrate.quad(hull_func,-1,limits[0])[0])
        print 'area1: ',area1
        area2 = integrate.quad(func_difference_down,limits[0],limits[1])[0]
        print 'area2: ',area2
        displacement = area1 + area2
        print 'displacement: ',displacement
    elif abs(water_func(limits[1]))<0.01:
        area1 = np.absolute(integrate.quad(hull_func,-1,limits[0])[0])
        print 'area1: ',area1
        area2 = np.absolute(integrate.quad(func_difference_up,limits[0],limits[1])[0])
        print 'area2: ',area2
        displacement = area1 + area2
        print 'displacement: ',displacement
    else:     
        displacement = integrate.quad(func_difference_down,limits[0],limits[1])[0]
        print "displacement volume: ", displacement
    return displacement
    

 
def plot_graph(hull,waterline,lambda_hull,lambda_waterline,intersection_points):
    '''
        plots the graph of the hull and water line
        args: intersection_points - a list of x coord of intersection of boat and waterline
    '''
    
    #Reset axes
    axes = plt.gca()
    axes.set_xlim([-1.7,1.7])
    axes.set_ylim([-2,2]) 

    root1 = intersection_points[0]
    root2 = intersection_points[1]

    y = np.linspace(-1,1,1000)
    plt.plot(y,hull)
    plt.plot(y,waterline)
    plt.plot([-2,2],[0,0])

    if np.absolute(lambda_waterline(root1)) < 0.01 or np.absolute(lambda_waterline(root2)) < 0.01:
        plt.plot([root1,root2],[lambda_waterline(root1),lambda_waterline(root2)], 'ro')
    else:
        plt.plot([root1,root2],[lambda_hull(root1),lambda_hull(root2)], 'ro')
    
    plt.show()

def varying_theta_calc_displacement(n,d):
    thetas = np.linspace(0,np.pi/2-0.1,50)
    displacements = []
    for angle in thetas:
        print 'angle: ',angle
        displacements.append(displacement(lambda y: np.absolute(y)**n - 1,
            lambda y: -np.tan(angle)*y - d,n,angle,d))
    print displacements
    plt.plot(thetas,displacements)
    plt.show()



righting_arm(2, 0.4)
righting_arm(2, 0.6)
righting_arm(2,0.8)
righting_arm(2,1.8)

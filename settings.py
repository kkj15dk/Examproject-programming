# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:27:51 2022

@author: Kasper Krunderup Jakobsen and Sofus Boisen
"""

import numpy as np

# global variables for use in multiple files

def init():
    """
    To run on startup of main to set global variables
    """
    global SystemsList
    global System
    global N
    global lettermapping
    global selfdefined_start
    global name
    global iteration_scaling
    global turtleAction
    SystemsList = np.array(["Koch curve","Sierpinski triangle"])
    System = ''
    N = 0
    lettermapping = np.array([], dtype = object)
    selfdefined_start = ''
    name =''
    iteration_scaling = 1
    turtleAction = np.zeros([], dtype = object)
    


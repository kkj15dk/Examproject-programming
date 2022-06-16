# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:27:51 2022

@author: Sofus Boisen
"""

import numpy as np

# global variables for use in multiple files

def init():
    global SystemsList
    global System
    global N
    global lettermapping
    global selfdefined_start
    global name
    global iteration_scaling
    SystemsList = np.array(["Koch", "Sierpinski"])
    System = ''
    N = 0
    lettermapping = np.array([], dtype = object)
    selfdefined_start = ''
    name =''
    iteration_scaling = 1
    


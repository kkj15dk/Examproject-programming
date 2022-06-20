# Examproject-programming

We have chosen project 2D - Lindemayer systems

exact.py is for the functions described in the exam pdf. These have to be precise.
help.py are other functions, which are used throughout the project
datastorage.p is for a function and a class for used to be able to store user defined L systems
settings.py is for global storage of the current L system. This had to be done, since the input variables of the exact_functions.py could not be altereed, since that wouldn't comply with project specification, so settings.py is a way to circumvent this problem.
We know using global variables like this is bad practice, but it was the solution we chose, since we couldn't pass these arguments as input for the functions.

It is possible to define ones own system!
Here, you can only use capital letters for denoting the turtle to either draw a line, rotate some angle, or do nothing at all
You can also use [ for saving a position, and ] for returning to the most recently saved position, deleting that position so it cannot be returned to again

The system can then be saved for later!!!

# Predefined systems

There are som predefined systems which have been loaded at an earlier point.
Some cannot handle as many iterations, for instance fractal tree, which shouldnt be run at more than 6 iterations unless you have a powerhouse of a computer, but looks really cool (rainbow colors are on purpose) :D

# NB

There are some global variables defined in settings.py. These are used to define user defined systems, and are used to 
Also, we know some project files have become rather lengthy, but this is only because of the implementation of predefiend and user defined systems.

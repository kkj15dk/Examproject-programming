from fractions import Fraction
import numpy as np
import settings

def inputInt(prompt):
    # Ask the user to input an integer
    while True:
        try:
            num = int(input(prompt))
            break
        except ValueError:
            pass
    return num

def inputFloat(prompt):
    # Ask the user to input a float
    while True:
        try:
            num = float(input(prompt))
            break
        except ValueError:
            pass
    return num

def inputFraction(prompt):
    # Ask the user to input an fraction or float
    while True:
        try:
            userinput = input(prompt)
            num = float(Fraction(userinput))
            break
        except:
            try:
                num = float(userinput)
                break
            except ValueError:
                pass
    return num

def displayMenu(options, message):
    # makes a menu of items that can be selected for
    # Input: the options of a menu, as well as the message to be displayed afterwards.
    # Output: the menu

    print('\n') # for prettier format

    for i in range(len(options)):
        print("{:d}. {:s}".format(i+1, options[i]))
    
    choice = 0
    
    while not(np.any(choice == np.arange(len(options))+1)):
        choice = inputInt(message)
    
    return choice


def selfDefinedSystem():
    # User input to define their own system. Changes settings file
    # Input: user input for the self defined L-system
    # Output:
    letteroptions = np.array(['A length', 'An angle'])
    while True:
        alphabet = input('\nInput the alphabet of the system(without spaces), make sure you have no duplicates, and only uppercase letters: ')
        if alphabet.isupper() != True or alphabet.isalpha() != True:
            print('\nOnly uppercase letters are allowed')
        else:
            break
    
    settings.iteration_scaling = inputFraction('\nInput what value you want the length of segments in the system to be scaled by after each iteration: ')
    settings.lettermapping = np.zeros((3,len(alphabet)), dtype = object) # for astoring the alphabet(0) along with replacement rules(1) and and turtle grahping rules(2)
    
    while True:
        settings.selfdefined_start = input('\nInput the startcondition of the system: ')
        # startconditions need to be a part of the alphabet
        if all(letters in alphabet for letters in settings.selfdefined_start):
            break
        else:
            print('\nYour startcondition needs to be a part of the alphabet')
    
    for i in range(len(alphabet)):
        settings.lettermapping[0,i] = alphabet[i]

        while True:
            replacement = input('\nWhat should ' + alphabet[i] + ' be replaced with, after each iteration?\n')
            if all(letters in alphabet for letters in replacement):
                settings.lettermapping[1,i] = replacement
                break
            else:
                print('\nAll letters of the replacement need to be part of your alphabet')
        
        option = displayMenu(letteroptions, 'What should ' + alphabet[i] + ' represent? ')
        if option == 1: # A length
            settings.lettermapping[2,i] = 'l' # placeholder
        if option == 2: # An angle
            settings.lettermapping[2,i] = np.pi * inputFraction('\nWrite what value you want x to be, for an angle x*Pi. Positive values denote positive rotation. ')
    
    while True:
        settings.name = input('\nWhat do you want to name your system?\n')
        if np.any(settings.name == settings.SystemsList):
            print('\nName cannot be the same as a predefined system (Sierpinski, Koch or User defined)')
        else:
            break
    return
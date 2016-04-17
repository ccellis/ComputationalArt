""" TODO: Put your header comment here """

import random
from PIL import Image
from math import pi
# from math import sin
# from math import cos
from math import sqrt 
from math import e
import math
import numpy as np

def build_random_function(min_depth, max_depth, depth = 0):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        
        Returns a function that takes in three variables between -1 and 1 
        and returns a single value between -1 and 1.

        No doctests here because the output is random.
    """

    #These lists of functions gave me the best looking results
    three_parameters = []
    two_parameters = ["prod","avg","circle","diff"]
    one_parameter  = ["cos_pi_3","cos_pi","sin_pi_3","sin_pi","intensify"]
    no_parameters  = ["x","y","t","t"]
    random_functions = no_parameters+one_parameter+two_parameters+three_parameters

    if max_depth == 1:
        #If you can only go down one more level, return ["x"] or ["y"]
        random_index = random.randint(0,len(no_parameters)-1)
    elif min_depth > 1:
        #Don't return ["x"] or ["y"] if you haven't hit minimum depth
        random_index = random.randint(4,len(random_functions)-1)
    else:
        #Else return whatever
        random_index = random.randint(0,len(random_functions)-1)

    random_function = random_functions[random_index]
    #print " "*4*depth,random_function

    #Generate new functions so my lambda functions don't generate new functions
    #Every time they're called
    if random_function not in "xyt":
        new_function = build_random_function(min_depth-1,max_depth-1,depth+1)
    if random_function in two_parameters or random_function in three_parameters:
        new_function_2 = build_random_function(min_depth-1,max_depth-1,depth+1)
    if random_function in three_parameters:
        new_function_3 = build_random_function(min_depth-1,max_depth-1,depth+1)

    #Use lambda functions now!
    #All of these work, but not all of them are pretty
    if random_function == "x":
        return lambda x,y,t: x
    elif random_function == "y":
        return lambda x,y,t: y
    elif random_function == "t":
        return lambda x,y,t: t

    elif random_function == "e":
        return lambda x,y,t: e**(new_function(x,y,t)-1)
    elif random_function == "cos_pi":
        return lambda x,y,t: np.cos(pi*new_function(x,y,t))
    elif random_function == "sin_pi":
        return lambda x,y,t: np.sin(pi*new_function(x,y,t))
    elif random_function == "cos_pi_3":
        return lambda x,y,t: np.cos(3*new_function(x,y,t))
    elif random_function == "sin_pi_3":
        return lambda x,y,t: np.sin(3*new_function(x,y,t))
    elif random_function == "square":
        return lambda x,y,t: new_function(x,y,t)**2
    elif random_function == "cube":
        return lambda x,y,t: new_function(x,y,t)**3
    elif random_function == "mone":
        return lambda x,y,t: 1 - np.abs(new_function(x,y,t))
    elif random_function == "mhalf":
        return lambda x,y,t: 0.5 - np.abs(new_function(x,y,t))
    elif random_function == "mrand":
        random_number = float(random.randrange(0,1000,1))
        random_number /= 1000
        return lambda x,y,t: random_number - np.abs(new_function(x,y,t))
    elif random_function == "abs":
        return lambda x,y,t: np.abs(new_function(x,y,t))
    elif random_function == "ceil":
        return lambda x,y,t: np.ceil(new_function(x,y,t))
    elif random_function == "floor":
        return lambda x,y,t: np.floor(new_function(x,y,t))
    elif random_function == "intensify":
        return lambda x,y,t: new_function(x,y,t)+(1-new_function(x,y,t))/2

    elif random_function == "prod":
        return lambda x,y,t: new_function(x,y,t)*new_function_2(x,y,t)
    elif random_function == "avg":
        return lambda x,y,t: (new_function(x,y,t)+new_function_2(x,y,t))/2
    elif random_function == "circle":
        return lambda x,y,t: np.sqrt((new_function(x,y,t)**2)/2+(new_function_2(x,y,t)**2)/2)
    elif random_function == "diff":
        return lambda x,y,t: (new_function(x,y,t)-new_function_2(x,y,t))/2

    #These really weren't worth it, they increase runtime so much
    #And they don't produce interesting art
    elif random_function == "3circle":
        return lambda x,y,t: np.sqrt((new_function(x,y,t)**2)/3+(new_function_2(x,y,t)**2)/3 + (new_function_3(x,y,t)**2)/3)
    elif random_function == "3avg":
        return lambda x,y,t: (new_function(x,y,t)+new_function_2(x,y,t)+new_function_3(x,y,t))/3
    elif random_function == "3prod":
        return lambda x,y,t: new_function(x,y,t)*new_function_2(x,y,t)*new_function_3(x,y,t)

def remap_interval(val,
                   input_min,
                   input_max,
                   output_min,
                   output_max):
    """ Given an input value in the interval [input_min,
        input_max], return an output value scaled to fall within
        the output interval [output_min, output_max].

        val: the value to remap
        input_min: the start of the interval that contains all
                              possible values for val
        input_max: the end of the interval that contains all possible
                            values for val
        output_min: the start of the interval that contains all
                               possible output values
        output_max: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        ALL of the values must be floats. I'd cast them as floats in the
        function, but numpy doesn't like that (plus numpy fills its matrices
        with floats by default). If all the values are floats, it works just fine.

        >>> remap_interval(0.5, 0.0, 1.0, 0.0, 10.0)
        5.0
        >>> remap_interval(5.0, 4.0, 6.0, 0.0, 2.0)
        1.0
        >>> remap_interval(5.0, 4.0, 6.0, 1.0, 2.0)
        1.5
    """

    #Find how big the value is compared to its possible range
    ratio = ((val-input_min)/(input_max - input_min))

    #Apply that ratio to the range of output values
    #Add the minimum output value
    output = ratio*(output_max - output_min) + output_min
    return output


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: float in the interval [0,255]

        >>> color_map(-1.0)
        0.0
        >>> color_map(1.0)
        255.0
        >>> color_map(0.0)
        127.5
        >>> color_map(0.5)
        191.25

        This returns a float now because of numpy. I recast the values
        to integers later on, but there's no nice way to make it so
        numpy matrices and individual numbers return as integers.
    """
    color_code = remap_interval(val, -1, 1, 0, 255)
    return color_code

def generate_art(filename, x_size=1920, y_size=1080,timespan=150):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        The filename should include a flag for numbers somewhere, the save
        statement assumes there will be one.

        x_size, y_size: optional args to set image dimensions (default: 1920,1080)
        timespan: optional arg to set number of frames in movie (default: 150)

        To generate a single frame, set timespan to 1

        This function saves two copies of every frame, so when they're all
        compiled into a single video file it plays forward then loops back
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(10,12)
    green_function = build_random_function(10,12)
    blue_function = build_random_function(10,12)

    #Creates matrices for x and y.
    #  |-1 0 1|   |-1 -1 -1|
    #x=|-1 0 1| y=| 0  0  0|
    #  |-1 0 1|   | 1  1  1|
    #Theyre formatted as such, so every pixel can access
    #its x value and its y value.
    x = np.tile(np.linspace(-1, 1, x_size), (y_size, 1))
    y = np.tile(np.linspace(-1, 1, y_size), (x_size, 1)).T

    #This keeps track of the number of frames generated
    t_index = 0

    #t is linearly spaced from -1 to 1
    for t in np.linspace(-1,1,timespan):

        red = color_map(red_function(x,y,t))
        green = color_map(green_function(x,y,t))
        blue = color_map(blue_function(x,y,t))

        #This transforms the three 1920x1080 matrices into one 1920x1080x3 matrix
        #The transposes are necessary to get the dimensions right
        #Without them you get a 3x1920x1080 matrix
        pixels = np.vstack(([red.T],[green.T],[blue.T])).T


        #Cast the array to integers, Image.fromarray requires it
        im = Image.fromarray(pixels.astype(np.uint8))
        im.save(filename%t_index)
        t_index += 1


if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    
    # i = 1
    # while i:
    #    generate_art(str(i) + "frame%03d.png",1920,1080,150)
    #    print "{} done".format(i)
    #    i += 1

    generate_art("myframe%03d.png",1920,1080,150)
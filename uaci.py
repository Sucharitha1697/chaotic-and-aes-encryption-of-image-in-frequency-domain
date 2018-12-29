import numpy as np
from scipy import misc
from PIL import Image
import sys
import copy
import math

def uaci(pixel1,pixel2):
    width,height=np.shape(pixel1)
    value=0
    for y in range(0,height):
        for x in range(0,width):
             value=(abs(int(pixel1[x,y])-int(pixel2[x,y]))/255)+value
            

    value=(value*100)/(width*height)
    return value

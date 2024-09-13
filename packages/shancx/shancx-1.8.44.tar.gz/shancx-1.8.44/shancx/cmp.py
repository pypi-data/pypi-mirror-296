
import numpy as np
from matplotlib.colors import ListedColormap
 

cmp = {}

newcolorsAU = np.array([
    [245,245,255,255],
    [180,180,255,255],
    [120,120,255,255],
    [20,20,255, 255],
    [0,216,195, 255],
    [0,150,144, 255],
    [0,102,102,255],
    [255,255,0,255],
    [255,200,0,255],
    [255,150,0,255],
    [255,100,0,255],
    [255,0,0,255],
    [200,0,0,255],
    [120,0,0,255],
    [40,0,0,255],
    
    [175,145,237, 255]])/255
cmp["radar_AU"] = ListedColormap(newcolorsAU)
 

from shancx.radar_nmc
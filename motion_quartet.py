import numpy as np
import pandas as pd
from psychopy import visual, core, event
from dot_patterns import *

window_size = [1400, 800]
quartet_mat = [20, 10] # automatic
quartet_mat_orig = np.full(quartet_mat, 1)
ratio_mat = [20, 10] # automatic
ratio_mat_orig = np.full(quartet_mat, 1)

# comment both of the following out if automatic is used 
# quartet_mat_orig = np.array([[0, 0, 1, 0, 0],  # manual
#                              [0, 1, 2, 1, 0],
#                              [0, 0, 1, 0, 0]]).T

# ratio_mat_orig =   np.array([[0, 0, 1, 0, 0],  # determines which ratios are allowed to change 
#                              [0, 1, 0, 1, 0],
#                              [0, 0, 1, 0, 0]]).T

num_cycles = 200  # Number of cycles to show the motion quartet
frame_duration = 0.3  # Time each frame is shown (in seconds)
dot_size = 10
distance = 30 #vertical distance of dots at 1/1 ratio in pixels
aspect_ratio = [1, 1.3]
aspect_ratio_gradient = False

# Import the motion configuration: Available patterns: "diagonal", "horizontal", "vertical", "circular_clockwise_4"
n_visible, dot_arrangement = configuration["diagonal"]

win = visual.Window(
    size=window_size,
    units="pix",
    fullscr=False, 
    color=[-1, -1, -1])

quartet_mat = np.flip(quartet_mat_orig, 1)
ratio_mat = np.flip(ratio_mat_orig, 1)
q_mat_dim = quartet_mat.shape

q_w = np.linspace(-0.5*window_size[0], 0.5*window_size[0], q_mat_dim[0]+2)[1:-1] # calculate center points along width
q_h = np.linspace(-0.5*window_size[1], 0.5*window_size[1], q_mat_dim[1]+2)[1:-1] # calculate center points along height
center_points = np.meshgrid(q_h, q_w) # matrix of center points coordinates 
coordinates_center = np.stack((center_points[1], center_points[0]), 2) # give matrix convenient shape -- old
shift = np.sqrt((distance/2)**2 / 2) # calculate horizontal/ vertical shift distances based on given dot separation

mat_3d = np.zeros((q_mat_dim[0], q_mat_dim[1], 2)) # template matrix of the right dimensions 
scalar_range_3d = mat_3d.copy() # template matrix to scale aspect ratios 

shift_3d = np.tile(shift, (q_mat_dim[0], q_mat_dim[1], 2)) * np.stack((quartet_mat, quartet_mat), 2) # matrix to set width and height

def calculate_position():

    scalar_width = (2 * aspect_ratio[0]) / (aspect_ratio[0] + aspect_ratio[1]) # calculate aspect ratio scalars
    scalar_height = (2 * aspect_ratio[1]) / (aspect_ratio[1] + aspect_ratio[0])

    scalar_range_width = np.repeat(scalar_width, np.prod(q_mat_dim))
    scalar_range_height = np.repeat(scalar_height, np.prod(q_mat_dim))

    if aspect_ratio_gradient:
        scalar_range_height = np.linspace(scalar_height, scalar_width, num=np.prod(q_mat_dim)) 
        scalar_range_width = np.flip(scalar_range_height)

    scalar_range_height = np.c_[scalar_range_height, scalar_range_height] # Adjust dimensions
    scalar_range_width = np.c_[scalar_range_width, scalar_range_width] # Adjust dimensions
    
    scalar_range_3d[:, :, 0] = scalar_range_width[:, 1].reshape(q_mat_dim) 
    scalar_range_3d[:, :, 1] = scalar_range_height[:, 1].reshape(q_mat_dim) 

    scalar_range_3d[ratio_mat == 0] = 1 # make sure selected quartets are keeping aspekt ratio 

    dot_positions = [np.concatenate(coordinates_center + np.tile(dot_arr, (q_mat_dim[1], 1)) * scalar_range_3d*shift_3d) for dot_arr in dot_arrangement]

    coordinates = coordinates = [np.concatenate([dot_positions[vis][np.concatenate(quartet_mat) != 0] for vis in slide]) for slide in n_visible]
    return coordinates 

stims = [visual.ElementArrayStim(win=win, 
                                 units="pix", 
                                 nElements=np.sum(quartet_mat != 0) * len(n_visible[idx]), 
                                 elementTex=None, elementMask="circle", 
                                 xys=calculate_position()[idx], 
                                 sizes=dot_size * np.tile(quartet_mat[quartet_mat != 0], len(n_visible[idx]))
                                 ) for idx in range(len(n_visible))]

fixation = visual.TextStim(win, text='+', pos=(0, 0), units="pix", height = 30)

direction = 1

data = pd.DataFrame([])
clock = core.Clock()

try: 
    for cycle in range(num_cycles):
        stims[cycle%len(stims)].draw()
        fixation.draw()
        win.flip()
        if cycle%4 == 0:
            aspect_ratio[0] += direction * 0.1
            [stims[pos].setXYs(calculate_position()[pos]) for pos in np.arange(len(stims))]
        core.wait(frame_duration)
        if event.getKeys(keyList=['space']): 
                direction = -direction # switch aspect ratio change whenever space is pressed
        if event.getKeys(keyList=['escape']):
            data.to_csv("data")
            win.close()
            core.quit()
            
except: 
    data.to_csv("data")

data.to_csv("data")
win.close()
core.quit()

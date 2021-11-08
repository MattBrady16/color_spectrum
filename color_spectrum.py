from tkinter import *
from Color import Color
import math


import time

# importing the choosecolor package
from tkinter import colorchooser
from types import SimpleNamespace

def make_averaged_row_from_endpoints(color_1, color_2, num_segments):
    return [get_proportion_for_2_colors(color_1, color_2, i, num_segments-1) for i in range(num_segments)]

def get_proportion_for_2_colors(color_1, color_2, numerator, denominator):
    subtracted_color = color_1.sub_with_negative(color_2)
    divided_color =  subtracted_color/(denominator)
    proportional_color = divided_color * numerator
    linear_proportion = color_1 - proportional_color
    return linear_proportion

# algo for calculating a 2d colorspace, from the 4 points outlining the boundary
# input: inputs 1-4 are each a Color, 5 is matrix width, 6 is the height
# output: list of lists in row-major order, so inputListOfLists[row][column]
def calculate_2d_colorspace_from_corners(topLeftColor, topRightColor, btmLeftColor, btmRightColor, dimX, dimY):
    lookAtLast=False
    inputListOfLists = [ [Color() for x in range(dimX)] for y in range(dimY)]
    # for every row in the matrix, calculate the proportional left&right side, then fill it in
    for row_num in range(dimY):
        left_proportion = get_proportion_for_2_colors(topLeftColor, btmLeftColor, row_num, dimY)
        right_proportion = get_proportion_for_2_colors(topRightColor, btmRightColor, row_num, dimY)
        inputListOfLists[row_num] = make_averaged_row_from_endpoints(left_proportion, right_proportion, dimX)
    return inputListOfLists

def map_window_ns_to_new_colorspace(window_ns):
    size_y = len(window_ns)
    size_x = len(window_ns[0])
    top_left = window_ns[0][0].color
    top_right =window_ns[0][size_x-1].color
    bottom_left = window_ns[size_y-1][0].color
    bottom_right =window_ns[size_y-1][size_x-1].color
    colorspace = calculate_2d_colorspace_from_corners(top_left, top_right, bottom_left, bottom_right, size_x, size_y)
    for i in range(size_y):
        print("Row " + str(i+1) + "\n")
        for j in range(size_x):
            window_ns[i][j].color = colorspace[i][j]
            print("Row " + str(i+1) +" Column " + str(j+1) + " color: " + str(colorspace[i][j]))
        print("\n")


def is_corner(x,y,dimX,dimY):
    return ((x == 0 or x == dimX-1) and (y == 0 or y == dimY-1))

def change_color(window_ns, ind_Y, ind_X, dimX, dimY):
    colors = colorchooser.askcolor(title="Tkinter Color Chooser")
    window_ns[ind_Y][ind_X].color = Color.init_from_tkinter_hex(colors[1])
    map_window_ns_to_new_colorspace(window_ns)

def make_window(window_ns, ind_Y, ind_X, dimY, dimX):
    new_window = Tk(className=window_ns[ind_Y][ind_X].name)
    new_window.geometry(window_ns[ind_Y][ind_X].geometry)
    if window_ns[ind_Y][ind_X].is_chooser:
        Button(new_window, text='Select a Color',
            command=lambda: change_color(window_ns, ind_Y, ind_X, dimX, dimY)).pack(expand=True)
    return new_window

def get_window_name(x,y,dimX,dimY):
    if is_corner(x,y,dimX,dimY):
        to_return = "input"
        if x == 0:
            to_return = "left " + to_return
        else:
            to_return = "right " + to_return
        if y == 0:
            return "Top " + to_return
        else:
            return "Bottom " + to_return
    else:
        return "Spectrum Row " + str(x) + " Column " + str(y)

def make_window_geometry(screen_width, screen_height, dimX, dimY, x, y):
    window_width = math.floor(screen_width/dimX)
    # minus 40 accounts for the bar at the top of the window
    window_height = math.floor(screen_height/dimY)-40
    # example geometry:'300x200+640+250'
    window_size = "" + str(window_width) + "x" + str(window_height) + "+"
    geometry = window_size + str(window_width * x) + "+" + str(window_height * y)
    return geometry


def _main():

    # number of windows on the screen in each dimension
    dimX = 16
    dimY = 8
    screen_width = 1440
    screen_height = 1080

    # array of namespaces, will be populated with the following attrs
    window_ns = [ [SimpleNamespace() for x in range(dimX)] for y in range(dimY)]
    window_names= [ [get_window_name(x,y,dimX,dimY) for x in range(dimX)] for y in range(dimY)]
    window_is_input=[ [is_corner(x, y,dimX,dimY) for x in range(dimX)] for y in range(dimY)]

    window_geometries = [ [make_window_geometry(screen_width, screen_height, dimX, dimY, x, y) for x in range(dimX)] for y in range(dimY)]

    for i in range(0,dimY):
        for j in range(0,dimX):
            window_ns[i][j].name=window_names[i][j]
            window_ns[i][j].geometry=window_geometries[i][j]
            window_ns[i][j].color=Color()
            window_ns[i][j].is_chooser=window_is_input[i][j]
            window_ns[i][j].window = make_window(window_ns, i, j, dimY, dimX)

    while True:
        for i in range(0,dimY):
            for j in range(0,dimX):
                window_ns[i][j].window.configure(bg=window_ns[i][j].color)
                window_ns[i][j].window.update_idletasks()
                window_ns[i][j].window.update()

_main()

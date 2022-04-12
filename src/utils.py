import os
import sys
import numpy as np
import argparse
from config import CONF
import shapely
import matplotlib.pyplot as plt

DATA_DIR = CONF.DATA_DIR

def polygon_generator(n_corners=4):
    corners = np.random.randint(0, 10, (n_corners, 2))
    return corners

def calculate_center(corners):
    center = np.mean(corners, axis=0)
    return center

def load_section_geometry(section_file):
    """
    Loads the section geometry from a file.
    """
    section_addr = os.path.join(DATA_DIR, section_file)
    corners = np.loadtxt(section_addr, dtype=np.float32, delimiter=',')
    return corners

def project_center_to_side(corners, center):
    corner_1 = corners[0]
    corner_2 = corners[1]
    side = corner_2 - corner_1
    side_norm = np.linalg.norm(side)
    projection_line = center - corner_1
    projection = (np.dot(side, projection_line)/side_norm**2) * side + corner_1
    return projection

def compute_aspect_ratio(projection, centeroid, edge):
    y_dist = centeroid.distance(projection)
    x_dist_left = projection.distance(edge.boundary[0])
    x_dist_right = projection.distance(edge.boundary[1])
    AR_left = y_dist/x_dist_left
    AR_right = y_dist/x_dist_right
    return AR_left, AR_right

def line_angle_calc(line):
    """
    Returns the type of the triangle.
    """
    horizon_line = [1, 0]
    line_origin = np.array(line)[1]-np.array(line)[0]
    dot_product = np.dot(horizon_line, line_origin)
    line_norm = np.linalg.norm(np.array(line)[1]-np.array(line)[0])
    angle = np.arccos(dot_product/line_norm)
    return angle

def plot_line(line):
    """
    Plots the line.
    """
    plt.plot(*line.xy)
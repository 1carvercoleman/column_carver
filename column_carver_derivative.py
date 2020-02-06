# -*- coding: utf-8 -*-
"""
Column Carver Derivative
Cuts columns based on large changes between mean verticle pixel values
Created on Wed Oct 25 2019
@author: Carver Coleman
"""

import os
import skimage
import numpy as np
import cv2
from glob import glob
import matplotlib.pyplot as plt
import pandas as pd

DEBUG = True
os.chdir("PATH_TO_IMAGES")
path = ("PATH_TO_OUTPUT_FOLDER")
SENSITIVITY = 15 # The minimum derivative to cut column

# Calculates mean pixel changes and cuts image where changes are the largest 
def column_cropper(img, missing_beginning_lines, missing_ending_lines, sensitivity):
    IMG_WIDTH = img.shape[:2][1]
    IMG_HEIGHT = img.shape[:2][0]
    col_mean = []
    crops = []
    final_crops = []
    cut_begin = 'y'
    for i in range(IMG_WIDTH):
        intermediate_sum = 0
        for j in range(IMG_HEIGHT):
            intermediate_sum = intermediate_sum + img[j,i][0]
        col_mean.append(intermediate_sum / IMG_HEIGHT)
        if i > 0 and cut_begin == 'y' and (col_mean[i] - col_mean[i-1] < (-1)*sensitivity) and missing_beginning_lines > 0:
            # Find last complete white line
            intermediate = col_mean[:-200]
            try:
                index1 = len(intermediate) - 1 - intermediate[::-1].index(255.0)
            except ValueError:
                index1 = 6
            crops.append(index1 - 5)
            crops.append(i - 5)
            final_crops.append(crops)
            crops = []
            missing_beginning_lines -= 1
        if i > 0 and cut_begin == 'y' and col_mean[i] - col_mean[i-1] > sensitivity:
            crops.append(i + 5)
            cut_begin = 'n'
        if i > 0 and cut_begin == 'n' and (col_mean[i] - col_mean[i-1] < (-1)*sensitivity) and i - crops[0] > 100:
            crops.append(i - 5)
            cut_begin = 'y'
            final_crops.append(crops)
            crops = []
    if missing_ending_lines > 0:
        desired_mean = 230.0
        for i in range(len(col_mean)):
            if i > 0 and col_mean[-i] < desired_mean:
                crops.append(len(col_mean) - i + 5)
                final_crops.append(crops)
                break
    return (final_crops, col_mean)

# Plots time series of panda data frame
def plot_df(df, x, y, title="", xlabel='Pixel Index', ylabel='Pixel Value', dpi=100):
    plt.figure(figsize=(16,5), dpi=dpi)
    plt.plot(x, y, color='tab:red')
    plt.gca().set(title=title, xlabel=xlabel, ylabel=ylabel)
    plt.show()

# __main__
for image_file in glob(f'*.jpg'):  
    print(image_file)
    gray = cv2.imread(image_file)
    thresh, gray2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) # was 127, 255; 105, 255 worked alright
    
    try:
        final_crops, col_mean = column_cropper(gray2, 1, 1, SENSITIVITY)
        final_crops = np.asarray(final_crops)
        if len(final_crops[-1]) == 1:
            final_crops = final_crops[:-1]
        if len(final_crops) == 0:
            skimage.io.imsave(path + image_file[:-4] + '_col_' + str(1) + '.jpg', gray)
        for i in range(len(final_crops)):
            if i == (len(final_crops) - 1):
                buffer_right = -5
            else:
                buffer_right = 7
            cropped = gray2[:,final_crops[i][0]:final_crops[i][1] - buffer_right]
            skimage.io.imsave(path + image_file[:-4] + '_col_' + str(i + 1) + '.jpg', cropped)
    except IndexError:
        final_crops, col_mean = column_cropper(gray2, 1, 1, SENSITIVITY)
        final_crops = np.asarray(final_crops)
        if len(final_crops[-1]) == 1:
            final_crops = final_crops[:-1]
        if len(final_crops) == 0:
            skimage.io.imsave(path + image_file[:-4] + '_col_' + str(1) + '.jpg', gray)
        for i in range(len(final_crops)):
            if i == (len(final_crops) - 1):
                buffer_right = -5
            else:
                buffer_right = 7
            cropped = gray2[:,final_crops[i][0]:final_crops[i][1] - buffer_right]
            skimage.io.imsave(path + image_file[:-4] + '_col_' + str(i + 1) + '.jpg', cropped)
    
    
    if DEBUG:
        col_mean_deriv = []
        intermediate = col_mean[1:]
        for i in range(len(intermediate)):
            col_mean_deriv.append(intermediate[i] - col_mean[i])   
        #Plots pixels across image
        df = pd.DataFrame(col_mean_deriv)
        df.index.name = 'Pixel Index'
        df.reset_index(inplace=True)
        df.columns = ['Pixel Index', 'Pixel Value']
        plot_df(df, df['Pixel Index'], df['Pixel Value'])
        

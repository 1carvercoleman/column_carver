# -*- coding: utf-8 -*-
"""
Column Carver Pixeler
Maps image pixels to detect verticle lines
Created on Wed Oct 15 09:46:01 2019
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

# Calculates mean pixels on each verticle
def column_cropper(img):
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
        if i > 3 and col_mean[i - 5] > 250.0 and max(col_mean[-4:]) < 250 and cut_begin == 'y':
            crops.append(i - 5)
            cut_begin = 'n'
        if i > 3 and col_mean[i] - col_mean[i - 3] > 20 and cut_begin == 'n' and col_mean[i] > 250.0:
            crops.append(i)
            cut_begin = 'y'
            final_crops.append(crops)
            crops = []
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
    thresh, gray2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    final_crops, col_mean = column_cropper(gray2)
    final_crops = np.asarray(final_crops)
    
    for i in range(len(final_crops)):
        if i == (len(final_crops) - 1):
            buffer_right = -5
        else:
            buffer_right = 7
        cropped = gray2[:,final_crops[i][0]:final_crops[i][1] - buffer_right]
        skimage.io.imsave(path + image_file[:-4] + '_col_' + str(i + 1) + '.jpg', cropped)
    
    if DEBUG:
        #Plots pixels across image
        df = pd.DataFrame(col_mean)
        df.index.name = 'Pixel Index'
        df.reset_index(inplace=True)
        df.columns = ['Pixel Index', 'Pixel Value']
        plot_df(df, df['Pixel Index'], df['Pixel Value'])

# -*- coding: utf-8 -*-
"""
Column Carver Thresh
Uses Skimage line detection to cut columns
Created on Wed Sep 25 09:46:01 2019
@author: Carver Coleman
"""

import os
import skimage
import numpy as np
import cv2
import copy
from glob import glob

TARGET_COLS = 3
DEBUG = True
os.chdir("INSERT_PATH_TO_FOLDER_WITH_IMAGES')

# Finds lines for thresh, minline, and maxlinegap variables
def cutter(x, g, l):
    
    edges = cv2.Canny(th3,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(image=edges, rho=vrho, theta=np.pi/45, threshold=x, lines=np.array([]), minLineLength=l, maxLineGap=g)         
    a,b,c = lines.shape
    for i in range(a):
        cv2.line(gray2, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
    
    final_lines = []        
    for z in range(len(lines)):
        final_lines.append(lines[z][0][0])           
    
    final_lines.sort()
    return final_lines

# Saves column cuts to folder 'split_cols' in original folder
def image_printer (index, col_begin, filename, DEBUG):
    final_vthresh = BEGINNING_THRESHOLD + (index * INCREMENT_VALUE)
    final_lines = cutter(x = final_vthresh, g = vmaxLG, l = vminLL)
    path = (os.getwd() + 'split_cols\\{}\\'.format(filename[:-4]))
    k = col_begin
    
    for i in range((len(final_lines) - 1)):
        if abs(final_lines[i] - final_lines[i+1]) > 200:
            cropped = gray2[:,final_lines[i] + buffer_left:final_lines[i + 1]-buffer_right]
            try:
                skimage.io.imsave(path + '{}_col'.format(filename[:-4]) + str(k) + '.jpg', cropped)
                print('saved')
            except FileNotFoundError:
                os.mkdir(path)
                skimage.io.imsave(path + '{}_col'.format(filename[:-4]) + str(k) + '.jpg', cropped)
                print('saved')
            k += 1
            firstLine = i + 1
            if DEBUG:
                skimage.io.imshow(cropped)
                skimage.io.show()
    
    cropped = gray2[:,final_lines[firstLine] + buffer_left:gray2.shape[:2][1]]
    skimage.io.imsave(path + '{}_col'.format(filename[:-4]) + str(k) + '.jpg', cropped)
    if DEBUG:
        skimage.io.imshow(cropped)
        skimage.io.show()
    print('saved')

# __main__
for image_file in glob(f'*.jpg'):
    try:
        filename = image_file
        print(filename)
        gray2 = cv2.imread(filename)
        
        
        # Convert to grayscale
        """
        gray2 = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
        """
        
        # Median Blur to remove noise
        """
        gray2 = cv2.medianBlur(gray2, 3)
        """

        # Convert to black and white
        """
        thresh, th3 = cv2.threshold(gray2, 127, 255, cv2.THRESH_BINARY) # was 127, 255; 105, 255 worked alright
        """
        # To invert the text to white
        th3 = 255*(gray2 < 128).astype(np.uint8) 
        
        BEGINNING_THRESHOLD = 400
        MAX_THRESHOLD = 800
        INCREMENT_VALUE = 50 # By how much should threshold increase every time
        
        #min line length (higher means less lines)
        vminLL = 400
        #rho value, or sensitivity value *Important for making more lines
        vrho = 1.5
        #What level of pixel to detect (higher means less lines)
        vthresh = copy.copy(BEGINNING_THRESHOLD)
        #How many pixels can break inbetween a line
        vmaxLG = 4
        #Cropped buffer on each side of the column
        buffer_left = 0
        buffer_right = -3
        
        total_num_columns = []
        num_columns = 0
        
        while vthresh <= MAX_THRESHOLD:
            try:
                final_lines = cutter(x = vthresh, g = vmaxLG, l = vminLL)
                num_columns = 0
                lines = []
                for i in range((len(final_lines) - 1)):
                    if abs(final_lines[i] - final_lines[i+1]) > 100:
                        lines.append(final_lines[i])
                        num_columns += 1
                vthresh += INCREMENT_VALUE
                total_num_columns.append(num_columns)
                if num_columns == TARGET_COLS:
                    target_lines = lines
            except AttributeError:
                break
        
        vthresh = 0        
        if TARGET_COLS - 1 in total_num_columns:
            index = len(total_num_columns) - 1 - total_num_columns[::-1].index(TARGET_COLS - 1)
            image_printer(index, col_begin = 1, filename, DEBUG)
        else:
            print("Target columns not found")
        
        print('END END END')
        
        
    except ValueError:
        print("Value Error: Skipped")
        

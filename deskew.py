# -*- coding: utf-8 -*-
"""
Deskew Carver Method
Slightly rotates image until largest horizontal line is straight
Created on Thu Oct 24 09:49:25 2019
@author: Carver Coleman
"""
import os
import skimage
import numpy as np
import cv2
from glob import glob

os.chdir("INSERT_PATH_TO_IMAGES")
path = ("INSERT_DESIRED_OUTPUT_PATH")

# Calculates mean pixels in each row
def calculate_pixels (img):
    row_mean = []
    for i in range(IMG_HEIGHT):
        intermediate_sum = 0
        for j in range(IMG_WIDTH):
            intermediate_sum = intermediate_sum + img[i,j][0]
        row_mean.append(intermediate_sum / IMG_WIDTH)
    return row_mean

# Rotates image without filling in black border
def rotate_image(mat, angle):

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

# Rotates image from MIN_ROTATION to MAX_ROTATION by ROTATION_STEP and calculates the longest line
def find_ideal_rotation (img, pixel_list, MIN_ROTATION, MAX_ROTATION, ROTATION_STEP):
    min_index = pixel_list.index(min(pixel_list))
    min_pixel_total = []
    for i in np.arange(MIN_ROTATION, MAX_ROTATION, ROTATION_STEP):
        new_img = rotate_image(img, i)
        min_pixel = 255.0
        for j in range(min_index - 10, min_index + 10):
            intermediate_sum = 0
            for k in range(50, IMG_WIDTH - 50):
                intermediate_sum = intermediate_sum + new_img[j,k][0]
            if (intermediate_sum / (IMG_WIDTH - 100)) < min_pixel:
                min_pixel = intermediate_sum / (IMG_WIDTH - 100)
        min_pixel_total.append(min_pixel)
    rotation_final = MIN_ROTATION + (min_pixel_total.index(min(min_pixel_total)) * ROTATION_STEP)
    return rotation_final

for image_file in glob(f'*.jpg'):
    print(image_file)
    gray = cv2.imread(image_file)
    
    # Convert to black and white
    thresh, gray2 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY) # was 127, 255; 105, 255 worked alright
    
    # Horizontal lines
    IMG_WIDTH = gray2.shape[:2][1]
    IMG_HEIGHT = gray2.shape[:2][0]
    row_mean = calculate_pixels(gray2)
    rotation_final = find_ideal_rotation(gray2, row_mean, -1.0, 1.0, 0.01)
    horizontal_img = rotate_image(gray2,90)
    print("Image was rotated " + str(rotation_final * (-1)) + " degrees clockwise.")
    
    # Rotate image
    gray = rotate_image(gray, rotation_final)
    
    # Display image
    #skimage.io.imshow(gray)
    
    # Crop blackspace
    crop = int(100 * abs(rotation_final))
    gray = gray[crop:gray2.shape[:2][0] - crop,crop:gray.shape[:2][1] - crop]
    
    # Save image
    skimage.io.imsave(path + image_file, gray)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
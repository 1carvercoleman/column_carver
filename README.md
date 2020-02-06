# column_carver
Different methods to crop images by columns in Python. They are all highly dependent on deskewed images, so my own deskewing method is also included (deskew.py).

## Method 1: column_carver_thresh.py
Uses the skimage package to detect lines. The target number of columns is specified and different values of the thresh variable are attempted until the target columns is reached. Good if you have many similar images.

## Method 2: column_carver_pixeler.py
Sums the pixel values across the height of the image to detect the darkest (lowest mean pixel) columns.

## Method 3: column_carver_derivative.py
Similar to Method 2, but looks as changes in mean pixels between columns. Will also work if columns are separated by whitespace instead of dark lines. 

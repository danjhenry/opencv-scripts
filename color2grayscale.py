import cv2
import os, sys
import numpy as np

def main():
    images = os.listdir('images')
    images.remove('desktop.ini')
    for image in images:
        path = 'images/' + image
        img = cv2.imread(path, 0)
        newPath = 'Gray/' + image
        cv2.imwrite(newPath, img)
    print('done')
        
main()

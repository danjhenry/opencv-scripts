import cv2
import os, sys
import numpy as np

def main():
    images = os.listdir('image path')
    for image in images:
        path = 'image path' + image
        img = cv2.imread(path, 3)
        image = image[:-3]
        newPath = 'png/' + image + 'png'
        cv2.imwrite(newPath, img)
    print('done') 
main()

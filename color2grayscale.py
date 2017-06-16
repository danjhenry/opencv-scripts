import cv2
import os

def main():
    images = os.listdir('dirName')
    for image in images:
        path = 'dirName/' + image
        img = cv2.imread(path, 0)
        newPath = 'gray/' + image
        cv2.imwrite(newPath, img)
    print('done')      
main()

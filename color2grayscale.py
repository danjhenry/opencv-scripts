import cv2
import os

def main():
    images = os.listdir('dir name')
    for image in images:
        path = 'images/' + image
        img = cv2.imread(path, 0)
        newPath = 'gray/' + image
        cv2.imwrite(newPath, img)
    print('done')      
main()

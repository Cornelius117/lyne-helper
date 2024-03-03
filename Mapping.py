import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm

def main():
    img = cv2.imread('Pictures/t1.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plt.imshow(img)
    #plt.imshow(gray, cmap='gray')

    sift = cv2.xfeatures2d.SIFT_create()
    keypoints, descriptors = sift.detectAndCompute(img, None)
    #plt.show()

    clf = svm.SVC()

if __name__ == '__main__':
    main()
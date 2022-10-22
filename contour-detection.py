import cv2
import numpy as np

raw_img = cv2.imread(r'car15crop.png')
# Converts image to grayscale
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

ret, threshold = cv2.threshold(
    gray_img,
    150,  # Any grayscale value above this becomes white, the rest becomes black TODO: find best metriic for binarization
    255, cv2.THRESH_BINARY)  # Creates binarized image

contours:list
contours, hierarchy = cv2.findContours(
    image=threshold,
    mode=cv2.RETR_TREE,  # mode is the type of contours that will be retrieved
    method=cv2.CHAIN_APPROX_SIMPLE  # method is which points within a contour are stored
)

contours = list(contours)

contours.sort(key=cv2.contourArea,reverse=True) #Sorts contours from biggest to smallest by area


largest_contour = contours[0]


def normalizeLP(contour):

    # Gets the smallest possible rectangle that's angle agnostic around the given contour
    bounding_rect_info = cv2.minAreaRect(contour)
    contour_corners = cv2.boxPoints(bounding_rect_info)

    # Gets the smallest possible straight rectangle around the given contour
    x,y,w,h = cv2.boundingRect(contour)
    dst_points = np.array([
        # [x,y],
        # [x+w,y],
        # [x,y+h],
        # [x+w,y+h]
    ],dtype=np.float32)
    

    mat = cv2.getPerspectiveTransform(contour_corners,dst_points)


    return cv2.warpPerspective(raw_img,mat,raw_img.shape[:2])



cv2.imshow('cool',normalizeLP(largest_contour))
cv2.waitKey(0)
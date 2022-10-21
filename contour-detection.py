import cv2


raw_img = cv2.imread(r'car15crop.png')
# Converts image to grayscale
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

ret, threshold = cv2.threshold(
    gray_img,
    150,  # Any grayscale value above this becomes white, the rest becomes black
    255, cv2.THRESH_BINARY)  # Creates binarized image

contours, hierarchy = cv2.findContours()

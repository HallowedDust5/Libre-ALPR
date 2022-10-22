import cv2
import numpy as np

raw_img = cv2.imread(r'car15crop.png')
# Converts image to grayscale
gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)

ret, threshold = cv2.threshold(
    gray_img,
    100,  #TODO: find best metriic for binarization
    255, cv2.THRESH_BINARY)  # Creates binarized image

contours: list
contours, hierarchy = cv2.findContours(
    image=threshold,
    mode=cv2.RETR_TREE,  # mode is the type of contours that will be retrieved
    method=cv2.CHAIN_APPROX_SIMPLE  # method is which points within a contour are stored
)

contours = list(contours)

# Sorts contours from biggest to smallest by area
contours.sort(key=cv2.contourArea, reverse=True)

largest_contour = contours[0]
cv2.drawContours(raw_img,[largest_contour],-1,(0,255,0),3)


def normalizeLP(contour):

    # Gets the smallest possible rectangle that's angle agnostic around the given contour
    bounding_rect_info = cv2.minAreaRect(contour)
    contour_corners = np.array(cv2.boxPoints(bounding_rect_info))

    # Calculates rectangle width and height
    width = int(bounding_rect_info[1][0])
    height = int(bounding_rect_info[1][1])
    # Gets the smallest possible straight rectangle around the given contour
    x, y, w, h = cv2.boundingRect(contour)
    dst_points = np.float32([ #TODO: Figure out how to not have to rotate 90 degrees
        (0,height-1),
        (0,0),
        (width-1,0),
        (width-1,height-1),

    ])

    mat = cv2.getPerspectiveTransform(contour_corners, dst_points)
    warped = cv2.warpPerspective(raw_img, mat, raw_img.shape[:2], flags=cv2.INTER_LINEAR)

    return *cv2.boundingRect(contour), cv2.rotate(warped,cv2.ROTATE_90_CLOCKWISE)

x,y,h,w, warped_lp = normalizeLP(largest_contour)
cv2.imshow('src', np.array(raw_img))
cv2.waitKey(0)
cv2.imshow('warped', warped_lp)
cv2.waitKey(0)
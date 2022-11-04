import cv2
import numpy as np
import os


def main():

    for im_obj in os.scandir('/home/main/Desktop/License-Plates/lp-images'):
        im = cv2.imread(im_obj.path)
        finished_img = perspectiveCorrection(im)

        im = cv2.resize(im,(500,500))
        finished_img = cv2.resize(finished_img,(500,500))

        cv2.imshow('unwarped',im)
        cv2.imshow('warped',finished_img)
        cv2.waitKey(0)

def findLargestContour(img: np.ndarray):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, binarized_img = cv2.threshold(
        gray_img,
        # TODO: find best metriic for binarization
        # 100, #Some sort of constant
        # np.median(gray_img),
        np.average(gray_img),

        255, cv2.THRESH_BINARY)  # Creates binarized image TODO: Test different binarization methods

    contours, _ = cv2.findContours(
        image=binarized_img,
        mode=cv2.RETR_TREE,  # mode is the type of contours that will be retrieved
        method=cv2.CHAIN_APPROX_SIMPLE  # method is which points within a contour are stored
    )

    contours = list(contours)
    # Sorts contours from biggest to smallest by area
    contours.sort(key=cv2.contourArea, reverse=True)

    return contours[0] # The largest contour is chosen because that's what most likely going to be a LP in the given image


def perspectiveCorrection(og_img: np.ndarray):
    img = np.copy(og_img)

    largest_contour = findLargestContour(img)

    # Gets the smallest possible rectangle that's angle agnostic around the given contour
    bounding_rect_info = cv2.minAreaRect(largest_contour)
    contour_corners = np.array(cv2.boxPoints(bounding_rect_info))

    # Calculates rectangle width and height
    height = int(bounding_rect_info[1][1])
    width = height*2  # Multiplied by 2 because US license plates are 2:1
    dst_points = np.float32([
        (0, 0),
        (width, 0),
        (width, height),
        (0, height),
    ])

    warp_mat = cv2.getPerspectiveTransform(contour_corners, dst_points)
    warped = cv2.warpPerspective(
        img, warp_mat, (width, height), flags=cv2.INTER_LINEAR)

    return warped





if __name__ == '__main__':
    main()
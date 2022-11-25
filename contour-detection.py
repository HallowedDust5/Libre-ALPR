import os
from random import randint

import cv2
import numpy as np


ALPHA_RANGE = (0,5)
BETA_RANGE = (-100,300)
ALPHA_BETA_PAIRS = {}


def main():
    """
    1: First image is better than the second
    2: Second image is better than first
    3: Neither are good
    4: Original image is better
    """

    for im_obj in os.scandir('lp-images'):
        im = cv2.imread(im_obj.path)

        alpha_1,beta_1 = generateAlphaBeta()
        alpha_2,beta_2 = generateAlphaBeta()


        im_1, im_1_bin, im_1_gray = perspectiveCorrectionwContrast(im)
        im_2, im_2_bin, im_2_gray = perspectiveCorrectionwContrast(im)
        resize_shape = (500,500)


        im = cv2.resize(im,resize_shape)

        im_1 = cv2.resize(im_1,resize_shape)
        im_1_bin = cv2.resize(im_1_bin,resize_shape)
        im_1_gray = cv2.resize(im_1_gray,resize_shape)

        im_2 = cv2.resize(im_2,resize_shape)
        im_2_bin = cv2.resize(im_2_bin,resize_shape)
        im_2_gray = cv2.resize(im_2_gray,resize_shape)
    




  

        cv2.waitKey(0)

def generateAlphaBeta():
    alpha,beta = randint(*ALPHA_RANGE),randint(*BETA_RANGE)
    
    return 




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

    # The largest contour is chosen because that's what most likely going to be a LP in the given image
    return contours[0], binarized_img, gray_img


def perspectiveCorrection(og_img: np.ndarray):
    img = np.copy(og_img)

    largest_contour, binarized_img, gray_img = findLargestContour(img)

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

    return warped, binarized_img, gray_img


def perspectiveCorrectionwContrast(og_img: np.ndarray, alpha, beta):
    img = np.copy(og_img)

    largest_contour, binarized_img, gray_img = findLargestContourwContrast(
        img, alpha, beta)

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

    return warped, binarized_img, gray_img


def findLargestContourwContrast(img: np.ndarray, alpha, beta):
    constrast_image = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    gray_img = cv2.cvtColor(constrast_image, cv2.COLOR_BGR2GRAY)

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

    # The largest contour is chosen because that's what most likely going to be a LP in the given image
    return contours[0], binarized_img, gray_img


if __name__ == '__main__':
    main()
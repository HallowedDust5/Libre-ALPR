import cv2
import numpy as np


def findLargestContour(img: np.ndarray):
    """Returns largest contour in an image given a to be determined binarization. 
    Currently operates using Otsu's binarization.

    Args:
        img (np.ndarray): License plate image

    Returns:
       contour : Largest contour in the image. Collection of points that represent the contour's shape.
    """
    img_copy = np.copy(img)
    gray_img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

    _, binarized_img = cv2.threshold(
        gray_img,
        # TODO: find best metriic for binarization
        # 100, #Some sort of constant
        # np.median(gray_img),
        # np.average(gray_img),
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # Creates binarized image TODO: Test different binarization methods

    contours, _ = cv2.findContours(
        image=binarized_img,
        mode=cv2.RETR_TREE,  # mode is the type of contours that will be retrieved
        method=cv2.CHAIN_APPROX_SIMPLE  # method is which points within a contour are stored
    )

    contours = list(contours)
    # Sorts contours from biggest to smallest by area
    contours.sort(key=cv2.contourArea, reverse=True)

    # The largest contour is chosen because that's what most likely going to be a LP in the given image
    return contours[0]


def perspectiveCorrection(img: np.ndarray):
    """Corrects perspective distortion on a license plate image 
    by detecting the corners of a given license plate and then reverse warping it.

    Args:
        img (np.ndarray): License plate iamge

    Returns:
        np.ndarray: Corrected image
    """
    img_copy = np.copy(img)

    largest_contour = findLargestContour(img_copy)

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
        img_copy, warp_mat, (width, height), flags=cv2.INTER_LINEAR)

    return warped

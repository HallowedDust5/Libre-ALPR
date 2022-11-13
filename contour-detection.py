import cv2
import numpy as np
import os


def main():

    for im_obj in os.scandir('lp-images'):
        im = cv2.imread(im_obj.path)
        contrast_warped_img,bin_contrast,gray_contrast = perspectiveCorrectionwContrast(im)
        no_contrast_warped_img,bin_no,gray_no = perspectiveCorrection(im)

        im = cv2.resize(im,(500,500))
        contrast_warped_img = cv2.resize(contrast_warped_img,(500,500))
        no_contrast_warped_img = cv2.resize(no_contrast_warped_img,(500,500))

        bin_contrast = cv2.resize(bin_contrast,(500,500))
        gray_contrast = cv2.resize(gray_contrast,(500,500))
        bin_no = cv2.resize(bin_no,(500,500))
        gray_no = cv2.resize(gray_no,(500,500))



        cv2.imshow('unwarped',im)
        cv2.imshow('warped w/o contrast',no_contrast_warped_img)
        cv2.imshow('warped w contrast',contrast_warped_img)

        cv2.imshow('contrasted binarization',bin_contrast)
        cv2.imshow('constrated grayscale',gray_contrast)
        cv2.imshow('no contrast binar',bin_no)
        cv2.imshow('no contrast grayscale',gray_no)





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

    return contours[0], binarized_img,gray_img # The largest contour is chosen because that's what most likely going to be a LP in the given image


def perspectiveCorrection(og_img: np.ndarray):
    img = np.copy(og_img)

    largest_contour, binarized_img,gray_img = findLargestContour(img)

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

    return warped, binarized_img,gray_img


def perspectiveCorrectionwContrast(og_img: np.ndarray):
    img = np.copy(og_img)

    largest_contour, binarized_img,gray_img = findLargestContourwContrast(img)

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

    return warped, binarized_img,gray_img


def findLargestContourwContrast(img: np.ndarray):
    constrast_image = cv2.convertScaleAbs(img, alpha=3, beta=-100)

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

    return contours[0], binarized_img,gray_img # The largest contour is chosen because that's what most likely going to be a LP in the given image



if __name__ == '__main__':
    main()
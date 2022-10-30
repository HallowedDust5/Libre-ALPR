import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr
import os

directory = 'dataset/'
failed = 0
past_result = None
result = None

run_all = False
runall = input("type y to run through all images")
if runall == 'y':
    run_all = True
show = False
show_plots = input("type y to show images")
if show_plots == 'y':
    show = True
print_failures = True
fails = input("type y to remove failure print statements")
if fails == 'y':
    print_failures = False
for i in os.listdir(directory):
    if os.path.isfile(os.path.join(directory, i)):
        img = cv2.imread(directory + i)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if show:
            plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
            plt.show()

        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
        edged = cv2.Canny(bfilter, 200, 300) #Edge detection
        if show:
            plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
            plt.show()

        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        location = None

        for contour in contours:
            approx = cv2.approxPolyDP(contour, 18, True)
            if len(approx) == 4:
                location = approx
                break

        try:    
            mask = np.zeros(gray.shape, np.uint8)
            new_image = cv2.drawContours(mask, [location], 0,255, -1)
            new_image = cv2.bitwise_and(img, img, mask=mask)
            if show:
                plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
                plt.show()
        except:
            if print_failures:
                print("mask failed")

        try:
            (x,y) = np.where(mask==255)
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))
            cropped_image = gray[x1:x2+1, y1:y2+1]
            if show:
                plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
                plt.show()
        except:
            if print_failures:
                print("crop failed")

        try:
            reader = easyocr.Reader(['en'])
            result = reader.readtext(cropped_image)
            text = result[0][-2]
            font = cv2.FONT_HERSHEY_SIMPLEX
            res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
            res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
            if show:
                plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
                plt.show()
        except:
            if print_failures:
                print("result failed")
            failed += 1


        if not result == past_result:
            if show:
                print(result)
                for i in result:
                    print(i[-2])
        past_result = result

        if not run_all:
            quit = input("q to quit, enter for next")
            if quit == 'q':
                break

print("failed " + str(failed) + "/" + str(len(os.listdir(directory))))
print('finished')

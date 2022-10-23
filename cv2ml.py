import cv2
from matplotlib import pyplot as plt
import numpy as np
import imutils
import easyocr

failed = 0
past_result = None
result = None

run_all = False
runall = input("type y to run through all images")
if runall == 'y':
    run_all = True
show_plots = False
show = input("type y to show images")
if show == 'y':
    show_plots = True
for i in range(104):
    curNumber = i+1
    image = r'carswithlicense\images - 2022-10-23T001656.992 (' +  str(curNumber) + ').jpg'
    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if show_plots:
        plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        plt.show()

    bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Noise reduction
    edged = cv2.Canny(bfilter, 230, 300) #Edge detection
    if show_plots:
        plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
        plt.show()

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 30, True)
        if len(approx) == 4:
            location = approx
            break

    mask = np.zeros(gray.shape, np.uint8)
    try:
        new_image = cv2.drawContours(mask, [location], 0,255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
        if show_plots:
            plt.imshow(cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB))
            plt.show()

        (x,y) = np.where(mask==255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        if show_plots:
            plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
            plt.show()
    except:
        print("contours failed")

    try:
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        text = result[0][-2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        res = cv2.putText(img, text=text, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)            
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0,255,0),3)
        if show_plots:
            plt.imshow(cv2.cvtColor(res, cv2.COLOR_BGR2RGB))
            plt.show()
        print(result[0][1])
    except:
        print("Text not detected")

    if not result == past_result:
        print(result)
    past_result = result

    if not run_all:
        quit = input("q to quit, enter for next")
        if quit == 'q':
            break

print("failed " + failed + "/104 ")
print('finished')

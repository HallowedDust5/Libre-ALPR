from PIL import Image

file_loc = r'custom_dataset' + r'\ '
file_loc = file_loc[0:-1]
file_loc2 = r'custom_dataset2' + r'\ '
file_loc2 = file_loc2[0:-1]
for i in range(104):
    curNumber = i+1
    im1 = Image.open(file_loc + "images - 2022-10-23T001656.992 (" + str(curNumber) + ").jpg")
    im1.save(file_loc2 + str(curNumber) + ".png")
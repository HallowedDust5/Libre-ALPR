import os
from PIL import Image #pip install pillow

directory = r'dataset/'
new_csv_name = 'dataset.csv'
new_csv = open(new_csv_name, 'w')
new_csv.write('filename,width,height,class,xmin,ymin,xmax,ymax,image_id\n')
new_csv.close()
col = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'image_id']
to_append = ['filename', 'width', 'height', 'License', 'xmin', 'ymin', 'xmax', 'ymax', 'image_id']
row = 0
counter = 0
print(len(os.listdir(directory)))
for image in os.listdir(directory):
    counter += 1
    if counter == 350:
        break
    to_append[0] = image
    if os.path.isfile(os.path.join(directory, image)):
        img = Image.open(directory + image)
        to_append[1] = img.width
        to_append[2] = img.height
        txt = open(directory + 'Label/' + image[0:-4] + '.txt', 'r')
        box = []
        for line in txt:
            number = False
            rec = ''
            for i in line:
                try:
                   int(i)
                   number = True
                   rec += i
                except ValueError:
                    if not(i == '.') and number:
                        number = False
                        box.append(float(rec))
                        rec = ''
                    elif number:
                        rec += i
            to_append[8] = row
            row += 1
            new_row = ''
            for i in range(4):
                to_append[4] = box[0]
                to_append[5] = box[1]
                to_append[6] = box[2]
                to_append[7] = box[3]
            for i in range(9):
                new_row += str(to_append[i]) + ','
            csv_open = open(new_csv_name, 'a')
            csv_open.write(new_row[0:-1] + '\n')
            csv_open.close()
        txt.close()
        # inpu = input("next\n")

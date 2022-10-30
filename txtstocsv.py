import pandas as pd
import os
from PIL import Image

directory = r'dataset/'
new_csv_name = 'dataset.csv'
new_csv = open(new_csv_name, 'w')
new_csv.write('filename, width, height, class, xmin, ymin, xmax, ymax, image_id\n')
new_csv.close()
csv = pd.read_csv(new_csv_name)
col = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax', 'image_id']
to_append = ['filename', 'width', 'height', 'License', 'xmin', 'ymin', 'xmax', 'ymax', 'image_id']
row = 0
for image in os.listdir(directory):
    to_append[0] = image
    if os.path.isfile(os.path.join(directory, image)):
        img = Image.open(directory + image)
        to_append[1] = img.width
        to_append[2] = img.height
        txt = open(directory + 'Label/' + image[0:-4] + '.txt', 'r')
        for line in txt:
            cur = 4
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
                        to_append[cur] = float(rec)
                        cur += 1
                        rec = ''
                    elif number:
                        rec += i
            to_append[8] = row
            row += 1
            new_row = ''
            for i in range(9):
                new_row += str(to_append[i]) + ','
            csv_open = open(new_csv_name, 'a')
            csv_open.write(new_row[0:-1] + '\n')
            csv_open.close()
        txt.close()
        inpu = input("next\n")


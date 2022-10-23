import numpy as np
# import matplotlib.pyplot as plt
# import os
# import cv2
# import random
# import pickle

# datadir = 'custom_dataset2/'
# categories = ["car", "carswithlicense"]
# img_size = 250
# # for category in categories:
# #     path = os.path.join(datadir, category)
# #     for img in os.listdir(path):
# #         img_array = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE)
# #         new_array = cv2.resize(img_array,(img_size,img_size))
# #         plt.imshow(new_array,cmap = "gray")
# #         plt.show()
# #         break

# training_data = []
# def create_training_data():
#     for category in categories:
#         path = os.path.join(datadir, category)
#         class_num = categories.index(category)
#         for img in os.listdir(path):
#             try:
#                 img_array = cv2.imread(os.path.join(path,img),cv2.IMREAD_GRAYSCALE)
#                 new_array = cv2.resize(img_array,(img_size,img_size))
#                 training_data.append([new_array,class_num])
#             except Exception as e:
#                 pass

# create_training_data()
# print(len(training_data))
# random.shuffle(training_data)
# for sample in training_data[:10]:
#     print(sample[1])

# X = []
# y = []
# for features, label in training_data:
#     X.append(features)
#     y.append(label)

# X = np.array(X).reshape(-1, img_size, img_size, 1)

# pickle_out = open("X.pickle","wb")
# pickle.dump(X, pickle_out)
# pickle_out.close()

# pickle_out = open("y.pickle","wb")
# pickle.dump(y, pickle_out)
# pickle_out.close()

# # pickle_in = open("X.pickle","rb")
# # X = pickle.load(pickle_in)
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
import pickle

X = pickle.load(open("X.pickle", "rb"))
y = pickle.load(open("y.pickle", "rb"))

X = X/255.0

model = Sequential()
model.add(Conv2D(64, (3,3), input_shaoe = X.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Conv2D(64, (3,3), input_shaoe = X.shape[1:]))
model.add(Activation("relu"))
model.add(MaxPooling2D(pool_size = (2,2)))

model.add(Flatten())
model.add(Dense(64))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss = "binary_crossentropy", optimizer = "adam", metrics = ['accuracy'])

model.fit(X,y, batch_size = 32, validation_split=0.1)
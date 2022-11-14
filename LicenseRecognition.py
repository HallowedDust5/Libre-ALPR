# from detecto.core import Model, Dataset
# from detecto import utils, visualize

# dataset = Dataset('dataset.csv', 'dataset/')
# model = Model(['License'])
# model.fit(dataset)

# image = utils.read_image('dataset/0c756c9366a8cb10.jpg')
# labels, boxes, scores = model.predict(image)
# predictions = model.predict_top(image)
# print(labels, boxes, scores)
# print(predictions)
# visualize.show_labeled_image(image, boxes, labels)
# visualize.detect_live(model)


from detecto import utils, visualize
from detecto.core import Model, Dataset
from PIL import Image
import os


def load_model(filepath):
    #USE filepath for model as parameter
    #returns the working model. Set equal to a variable
    labels = ["License"]
    #Loads the Model
    try:
        model = Model.load(filepath, labels)
        return model
    except:
        print("no such file name")


def predict_image(model, image_name, box_only = False): #Possible change to only return boxes
    #image name as parameter string and boolean box_only to just return the box
    #returns the labels, boxes, and scores of image. SET equal to three variables
    #Eg labels, boxes, scores = predict_image(image_name)
    try:
        image = utils.read_image(image_name)
    except:
        print("no such file name or error opening image")
        return
    #Predicts the image
    if box_only:
        a, boxes, c = model.predict(image)
        return boxes
    #Coordinates given as an array [xmin, ymin, xmax, ymax]
    print(model.predict(image))
    return model.predict(image)


def crop_image(image_name, dimensions):
    #Returns the cropped image using the Pillow module
    #Takes in parameters, image_name and array of coordinates for box
    if len(dimensions) == 0:
        print("dimensions has no coordinates")
        return
    try:
        im = Image.open(image_name) #Opens image using Pillow to be cropped depending on dimensions established by boxes
    except:
        print("no such file name or error opening image")
        return
    #TODO change index depending on how the boxes variable is formatted to determine dimensions of license location
    print(im.height, im.width)
    left = dimensions[0]
    top = dimensions[1]
    right = dimensions[2]
    bottom = dimensions[3]
    return im.crop((left,top,right,bottom))


def showPillowImage(image):
    if image == None:
        return
    image.show()


model_path = r'C:\Users\eizak\Documents\GitHub\Libre-ALPR\LibreALPR_1.0.pth'
model = load_model(model_path)
for image_name in os.listdir('dataset/'):
    image_name = 'dataset/' + image_name
    image = utils.read_image(image_name)
    # labels, boxes, scores = model.predict(image)
    labels, boxes, scores = predict_image(model, image_name)
    new_image = crop_image(image_name, boxes)
    showPillowImage(Image.open(image_name))
    showPillowImage(new_image)
    inpu = input("enter for next")

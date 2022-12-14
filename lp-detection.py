from detecto import utils, visualize
from detecto.core import Model, Dataset
from PIL import Image


def load_model(filepath):
    #USE filepath for model as parameter
    #returns the working model. Set equal to a variable
    labels = ["License"]
    #Loads the Model
    return Model.load(filepath, labels)


def predict_image(image_name, box_only): #Possible change to only return boxes
    #image name as parameter string and boolean box_only to just return the box
    #returns the labels, boxes, and scores of image. SET equal to three variables
    #Eg labels, boxes, scores = predict_image(image_name)
    image = utils.read_image(image_name)
    #Predicts the image
    if box_only:
        a, boxes, c = model.predict(image)
        return boxes
    #Coordinates given as an array [xmin, ymin, xmax, ymax]
    return model.predict(image)


def crop_image(image_name, dimensions):
    #Returns the cropped image using the Pillow module
    #Takes in parameters, image_name and array of coordinates for box
    im = Image.open(image_name) #Opens image using Pillow to be cropped depending on dimensions established by boxes
    #TODO change index depending on how the boxes variable is formatted to determine dimensions of license location
    left = dimensions[0]
    top = dimensions[1]
    right = dimensions[2]
    bottom = dimensions[3]
    return im.crop((left,top,right,bottom))


def showPillowImage(image):
    image.show()

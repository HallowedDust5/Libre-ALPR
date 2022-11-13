from detecto import utils, visualize
from detecto.core import Model, Dataset
from PIL import Image


def load_model(filepath):
    #USE filepath for model as parameter
    #returns the working model. Set equal to a variable
    labels = ["License"]
    #Loads the Model
    return Model.load(model_name, labels)


def predict_image(image_name):
    #image name as parameter string
    #returns the labels, boxes, and scores of image. SET equal to three variables
    #Eg labels, boxes, scores = predict_image(image_name)
    image = utils.read_image(image_name)
    #Predicts the image
    return model.predict(image)


def crop_image(image_name, coordinates):
    #Returns the cropped image using the Pillow module
    #Takes in parameters, image_name and array of coordinates for box
    im = Image.open(image_name) #Opens image using Pillow to be cropped depending on dimensions established by boxes
    #TODO change index depending on how the boxes variable is formatted to determine dimensions of license location
    left = dimensions[0]
    top = dimensions[1]
    right = dimensions[2]
    bottom = dimensions[3]
    return im.crop((left,top,right,bottom))


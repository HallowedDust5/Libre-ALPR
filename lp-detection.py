from detecto import utils, visualize
from detecto.core import Model, Dataset
from PIL import Image

#TODO put file name and path here for the model
model_name = r""
labels = ["License"]
#Loads the Model
model = Model.load(model_name, labels)

#TODO determine file path to new images and how to iterate through new images
image_name = r""
image = utils.read_image(image_name)
image_data = [image_name] #Temporary array holding the images attributes
#Predicts the image
labels, boxes, scores = model.predict(image)
Licenses = [] 
#Uses Licenses Array and creates new cropped images for each 
im = Image.open(image_name) #Opens image using Pillow to be cropped depending on dimensions established by boxes
for i in range(len(boxes)): #Assumes that boxes in an array of arrays with each inner array housing coordinates for each box
    width, height = im.size
    #TODO change index depending on how the boxes variable is formatted to determine dimensions of license location
    left = boxes[0]
    top = boxes[1]
    right = boxes[2]
    bottom = boxes[3]
    cropped_image = im.crop((left,top,right,bottom))
    Licenses.append(cropped_image)

image_data.append(Licenses)

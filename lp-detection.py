from detecto import utils, visualize
from detecto.core import Model, Dataset
from PIL import Image

image_name = r""
image = utils.read_image(image_name)

model_name = r""
labels = ["License"]

model = Model.load(model_name, labels)

labels, boxes, scores = model.predict(image)

Licenses = [] 

for i in range(len(boxes)):
    im = Image.open(image_name)
    width, height = im.size
    left = boxes[0]
    top = boxes[1]
    right = boxes[2]
    bottom = boxes[3]
    cropped_image = im.crop((left,top,right,bottom))
    Licenses.append(cropped_image)


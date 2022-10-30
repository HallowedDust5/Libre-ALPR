from detecto.core import Model, Dataset
from detecto import utils, visualize
from detecto.utils import xml_to_csv

xml_to_csv('your_labels/', 'validation-annotations-box.csv')
dataset = Dataset('validation-annotations-bbox.csv', 'Vehicleregistrationplate/')
model = Model(['license'])
model.fit(dataset)

image = utils.read_image('Vehicleregistrationplate/0c756c9366a8cb10.jpg')
license = model.predict(image)
print(cars)
visualize.show_labed_image(image, license)
visualize.detect_live(model)



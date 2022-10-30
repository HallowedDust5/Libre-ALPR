from detecto.core import Model, Dataset
from detecto import utils, visualize

dataset = Dataset('dataset.csv', 'dataset/')
model = Model(['License'])
model.fit(dataset)

image = utils.read_image('dataset/0c756c9366a8cb10.jpg')
license = model.predict(image)
print(license)
visualize.show_labeled_image(image, license)
visualize.detect_live(model)



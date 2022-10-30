from detecto.core import Model, Dataset
from detecto import utils, visualize

dataset = Dataset('dataset.csv', 'dataset/')
model = Model(['License'])
model.fit(dataset)

image = utils.read_image('dataset/0c756c9366a8cb10.jpg')
labels, boxes, scores = model.predict(image)
predictions = model.predict_top(image)
print(labels, boxes, scores)
print(predictions)
visualize.show_labeled_image(image, boxes, labels)
visualize.detect_live(model)



import argparse
import os
import numpy as np
from tensorflow import keras


IMAGE_TARGET_SIZE = (224, 224)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='File with image ids', required=True)

    args = parser.parse_args()

    folder = os.path.basename(args.input)
    folder = os.path.splitext(folder)[0]

    with open(args.input) as file:
        ids = file.read().splitlines()

    model = initialize_model()
    arr = np.empty([len(ids), 2048])
    for index, id in enumerate(ids):
        filename = os.path.join(folder, id + '.png')
        image = keras.preprocessing.image.load_img(filename, target_size=IMAGE_TARGET_SIZE)
        vector = image_to_vector(image, model)
        arr[index] = vector

    arr = np.array(arr)

    np.save(folder, arr)


def initialize_model():
    resnet = keras.applications.resnet50.ResNet50(weights='imagenet')
    model = keras.models.Model(inputs=resnet.input, outputs=resnet.get_layer('avg_pool').output)
    return model


def image_to_vector(image, model):
    x = keras.preprocessing.image.img_to_array(image)
    x = np.expand_dims(x, axis=0)
    x = keras.applications.resnet50.preprocess_input(x)
    intermediate_layer = model.predict(x)

    return intermediate_layer[0]


if __name__ == '__main__':
    main()

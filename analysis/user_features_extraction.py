# imports

import os
import numpy as np
from keras.applications.imagenet_utils import preprocess_input
from keras.preprocessing.image import load_img, img_to_array


def features_extraction_user(feat_extractor):
    # parameters setup
    path_img_user = "./data/img_users/"
    imgs_model_width, imgs_model_height = 224, 224
    # 1. load the VGG pre-trained model from Keras
    # load the model
    # vgg_model = vgg16.VGG16(weights='imagenet')
    # remove the last layers in order to get features instead of predictions
    # feat_extractor = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer("fc2").output)
    # 2. get the user image path
    files_users = [path_img_user + x for x in os.listdir(path_img_user) if ("jpg" in x) or ("jpeg" in x) or ("JPG" in x)]
    # 3. feed one image into the CNN
    # load an image in PIL format
    print(f"{files_users} try.....!")
    original_user = load_img(files_users[0], target_size=(imgs_model_width, imgs_model_height))
    # convert the PIL image to a numpy array
    # in PIL - image is in (width, height, channel)
    # in Numpy - image is in (height, width, channel)
    numpy_image_user = img_to_array(original_user)
    # convert the image / images into batch format
    # expand_dims will add an extra dimension to the data at a particular axis
    # we want the input matrix to the network to be of the form (batchsize, height, width, channels)
    # thus we add the extra dimension to the axis 0.
    image_batch_user = np.expand_dims(numpy_image_user, axis=0)
    # prepare the image for the VGG model
    processed_image_user = preprocess_input(image_batch_user.copy())
    # get the extracted features
    img_features_user = feat_extractor.predict(processed_image_user)
    print("features successfully extracted!")
    print("number of image features:", img_features_user.size)
    return img_features_user

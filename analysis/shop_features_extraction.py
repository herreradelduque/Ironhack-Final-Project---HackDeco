# imports
from keras.applications import vgg16
from keras.preprocessing.image import load_img,img_to_array
from keras.models import Model
from keras.applications.imagenet_utils import preprocess_input
import os
import numpy as np

def features_extraction():
    # parameters setup
    shop_lst = ['Ikea']
    product_lst = ['Sillas']
    print('Starting features extraction')
    for i, shop in enumerate(shop_lst):
        for j, product in enumerate(product_lst):
            print('Getting path...')
            imgs_path = '../data/' + 'img_' + shop.lower() + '_' + product + '/'
            imgs_model_width, imgs_model_height = 224, 224
            ##  1. load the VGG pre-trained model from Keras
            # load the model
            vgg_model = vgg16.VGG16(weights='imagenet')
            # remove the last layers in order to get features instead of predictions
            feat_extractor = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer("fc2").output)
            # 2. get the images paths
            files = [imgs_path + x for x in os.listdir(imgs_path) if "jpg" in x]
            print("number of images:",len(files))
            # 4. feed all the images into the CNN
            # load all the images and prepare them for feeding into the CNN
            importedImages = []
            for f in files:
                filename = f
                original = load_img(filename, target_size=(imgs_model_width, imgs_model_height))
                numpy_image = img_to_array(original)
                image_batch = np.expand_dims(numpy_image, axis=0)
                importedImages.append(image_batch)
            images = np.vstack(importedImages)
            processed_imgs = preprocess_input(images.copy())
            # extract the images features
            imgs_features = feat_extractor.predict(processed_imgs)
            print("features successfully extracted!")
            np.save(f'../data/features_extraction_products/img_features_{shop_lst[i]}_{product_lst[j]}', imgs_features)
            print(f"img_features_user saved at: '../data/features_extraction_products/img_features_{shop_lst[i]}_{product_lst[j]}'")
features_extraction()
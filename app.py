from flask import Flask, request
import json
from keras.applications import vgg16
from keras.models import Model
import tensorflow as tf
from analysis.user_features_extraction import features_extraction_user
from analysis.visual_recommendations import cos_simil
from tensorflow.python.keras.backend import set_session
from flask import jsonify


app = Flask(__name__)
sess = tf.Session()
# global graph
graph = tf.get_default_graph()

# 1. load the VGG pre-trained model from Keras
# load the model
set_session(sess)
vgg_model = vgg16.VGG16(weights="imagenet")
# remove the last layers in order to get features instead of predictions
feat_extractor = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer("fc2").output)


@app.route("/", methods=["GET"])
def home():
    return "<h1> Deployed to Furnitour!!!</h1>"


# get user search preferences: shop and furniture
@app.route("/furnitour", methods=["POST"])
def features_extract():
    # user_search_preferences = {'shop': request.json['shop'], 'furniture': request.json['furniture']}
    # selections = {'shop': request.form['shop'], 'furniture': request.form['furniture']}
    #print("Resquest received:", request.get_json())
    print("Feature extract...")
    shop = request.json["shop"]
    print("shop", shop)
    product = request.json["furniture"]
    print("product", product)
    # shop = request.form["shop"]
    # furniture = request.form["furniture"]

    global graph
    global sess
    with graph.as_default():
        set_session(sess)
        img_features_user = features_extraction_user(feat_extractor)
        # print(vgg_model.summary())
    cos_simil(shop, product, img_features_user)

    # we're now loading the JSON file's data into file_data
    # every time a request is made to this endpoint
    with open(f"./data/cos_similarities_{shop}_{product}.json", "r") as jsonfile:
        file_data = json.loads(jsonfile.read())
    # We can then find the data for the requested info and send it back as json
    # return json.dumps(file_data)
    return jsonify(file_data)


if __name__ == "__main__":
    app.run(debug=True)

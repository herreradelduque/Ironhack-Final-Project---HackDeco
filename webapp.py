from flask import Flask, redirect, url_for, render_template,request,session,flash
from analysis.cam_capture import capture
import os
from werkzeug.utils import secure_filename
import requests
import json
from requests import get
from flask import jsonify
from flask import Response




app = Flask(__name__)


app.config["IMAGE_UPLOADS"] = "./data/img_users"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
#app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024



def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contacta')
def contata():
    return render_template('contacta.html')

@app.route('/deepdeco')
def deepdeco():
    return render_template('deepdeco.html')

@app.route('/search', methods=["GET","POST"])
def selections():
    if request.method == 'POST':
        print("1-----")
        shop = request.form.get("shop")
        furniture = request.form.get("furniture")
        data = {'shop':shop,'furniture':furniture}
        #user_pref_json = json.dumps(data)
        #user_pref_json = jsonify(data)
        #user_pref_json = (data)
        print(data)
        print('2----')
        r = requests.post('http://127.0.0.1:5000/furnitour', json=data)
        similar = r.json()
        print("3-----")
        print(similar[0])
        print(type(data))
        if r.ok:
            print(r.json()[0]['Buy_url'])
            print('4----')
            return render_template('result.html', similar=similar)
        #r = requests.post('http://127.0.0.1:5000/furnitour')
        #return jsonify(r.json())
        #return redirect(url_for("http://127.0.0.1:3000/result"))
    return render_template('search.html')

@app.route("/upload-image", methods=["GET", "POST"])
def selections_and_upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print("No filename")
                return redirect(request.url)
            if allowed_image(image.filename):
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], 'img.jpg'))
                print("Image saved")
                return redirect(request.url)
            else:
                print("That file extension is not allowed")
                return redirect(request.url)
    return render_template("upload-image.html")



@app.route("/cam-capture", methods=["GET", "POST"])
def cam():
    if request.method == 'POST':
        return capture()
    return render_template("camcapture.html")




@app.route("/result",methods=["GET","POST"])
def result():
    #r = requests.get('http://127.0.0.1:5000/furnitour')
    #return jsonify(r.json())
    return render_template("result.html")






if __name__ == '__main__':
    app.run(debug=True, port=3000)
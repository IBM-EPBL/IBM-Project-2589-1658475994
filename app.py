
import numpy as np
import pickle
import os
from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates")
model = pickle.load(open('fdemand.pkl', 'rb'))


@app. route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app. route('/home', methods=['GET'])
def about():
    return render_template('home.html')

"""
@app. route('/pred', methods=['GET'])
def page():
    return render_template('upload.html')
"""

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print('[INFO] Loading model…')
    input_features = [float(x) for x in request.form.values()]
    
    features_value = [np.array(input_features)]
    print(features_value)

    features_name = ['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine',
                     'city_code', 'region_code', 'category']
    prediction = model.predict(features_value)
    output = prediction[0]
    res=round(output)
    return render_template('home.html', prediction_text=res)

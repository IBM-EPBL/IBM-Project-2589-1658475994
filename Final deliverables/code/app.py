import numpy as np
import pickle
import os
from flask import Flask, request, render_template
import requests
import json

app = Flask(__name__, template_folder="templates")


@app. route('/', methods=['GET'])
def index():
    return render_template('home.html')


@app. route('/home', methods=['GET'])
def about():
    return render_template('home.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    print('[INFO] Loading model…')
    #print(request.form.values())
    input_features = [float(x) for x in request.form.values()]
    print(input_features)
    
    API_KEY = "RSUKnz_dvhPrn3OXEeNdh0hZHTYSaexP0OEFqJgSFU9a"
    token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
                                                                                    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
    mltoken = token_response.json()["access_token"]

    header = {'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + mltoken}

    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ['homepage_featured', 'emailer_for_promotion', 'op_area', 'cuisine',
                                                  'city_code', 'region_code', 'category'], "values": [
        input_features]}]}

    response_scoring = requests.post('https://jp-tok.ml.cloud.ibm.com/ml/v4/deployments/8c4cb961-7490-4977-8763-65929bc9bfb7/predictions?version=2022-11-17', json=payload_scoring,
                                    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    #res_scr=response_scoring.json()
    pred_res = response_scoring.json()['predictions'][0]['values'][0][0]
    prediction=round(pred_res)

    return render_template('home.html', prediction_text = prediction)


if __name__ == "__main__":
    app.run(debug=True)
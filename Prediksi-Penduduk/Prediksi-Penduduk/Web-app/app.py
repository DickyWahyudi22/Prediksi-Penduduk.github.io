from flask import Flask, request, render_template
import requests
from requests.structures import CaseInsensitiveDict
from flask import json
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction_data = False

    if request.method == 'POST':
        print(request.form['propinsi'])
        print(request.form['tahun'])
        print(request.form['kelamin'])
       
        propinsi_value = request.form['propinsi']
        tahun_value = request.form['tahun']
        kelamin_value = request.form['kelamin']
        

        access_token = get_access_token()

        prediction_value = get_prediction(
            access_token,
            propinsi_value, tahun_value, kelamin_value
        )

        prediction_data = prediction_value
    return render_template('index.html', prediction = prediction_data)

def get_access_token():
    url = "https://iam.cloud.ibm.com/oidc/token"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    data = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=ded63fa1-6c3b-4400-8558-d14a5ade6266"
    resp = requests.post(url, headers=headers, data=data)
    if resp.status_code == 200:
        json_resp = resp.json()
        return json_resp.get('access_token')
    else:
        return None

def get_prediction(access_token, *input_values):
    url = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/fe4310cd-86db-4f7e-beca-9e718958847c/predictions?version=2021-05-01"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + access_token

    data = {
        "input_data": [
            {
                "fields": [
                    "propinsi", "tahun", "kelamin"
                ],
                "values": [list(input_values)]
            }
        ]
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 200:
        predictions = resp.json()
        prediction_value = predictions['predictions'][0]['values'][0][0]
        output = json.loads(resp.text)
        print("output >>", output)
        return prediction_value
    else:
        return None
    
#Uncomment code below if you want to host it locally
#if __name__ == '__main__':
#    app.run(debug=False,host='0.0.0.0')



#Made Dicky Wahyudi 
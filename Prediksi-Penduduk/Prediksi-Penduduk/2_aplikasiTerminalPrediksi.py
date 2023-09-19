import requests
from requests.structures import CaseInsensitiveDict

# Get access token
url = "https://iam.cloud.ibm.com/oidc/token"
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/x-www-form-urlencoded"
data = "grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey=ded63fa1-6c3b-4400-8558-d14a5ade6266"
resp = requests.post(url, headers=headers, data=data)
if resp.status_code == 200:
    json_resp = resp.json()
    access_token= json_resp.get('access_token')
else:
    print("Failed to retrieve access token. Status code:", resp.status_code)
 
def prediksi():
    #Get Prediction
    url = "https://us-south.ml.cloud.ibm.com/ml/v4/deployments/fe4310cd-86db-4f7e-beca-9e718958847c/predictions?version=2021-05-01"
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "application/json"
    headers["Authorization"] = "Bearer " + access_token

    data = {
        "input_data": [
            {
                "fields": [
                    "Kelamin", "Tahun", "Propinsi"
                ],
                "values": [
                    [
                        Kelamin_value, Tahun_value, Propinsi_value
                    ]
                ]
            }
        ]
    }

    resp = requests.post(url, headers=headers, json=data)

    if resp.status_code == 200:
        predictions = resp.json()
        prediction_value = predictions['predictions'][0]['values'][0][0]
        print("\n=============================== PREDICTION RESULTS =============================================")
        print("\t\t\t   "+"Adaptivity Level = "+prediction_value+"\t\t\t")
        print("================================================================================================")
    else:
        print("Error:", resp.status_code)

while(True):
    # Input data
    Kelamin_value=str(input("Kelamin= "))
    Tahun_value=str(input("Tahun= "))
    Propinsi_value=str(input("Propinsi= "))
    

    # Call prediksi function
    prediksi()
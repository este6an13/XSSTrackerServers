from flask import Flask, request
from flask import jsonify
import requests
from bs4 import BeautifulSoup
from joblib import load

app = Flask(__name__)
model = load('rf_model.joblib')
headers = {'Content-Type': 'application/json'}

@app.route('/', methods=['POST'])
def result():
    packet = request.get_json(force=True)    
    print(packet)
    vector = []
    for key in list(packet.keys())[1:]:
        vector.append(packet[key])
    print(vector)
    p = model.predict([vector])
    print(p)
    data = {'URL':packet['url'], 'XSSClass':int(p[0])}
    r = requests.post('https://xsstracker20210712213835.azurewebsites.net/api/records', json=data, verify=False, headers=headers)
    print(r)
    dictToReturn = {'Received': 'OK'}
    return jsonify(dictToReturn)
if __name__ == '__main__':
    app.run()

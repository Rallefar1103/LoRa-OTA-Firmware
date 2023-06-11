from flask import Flask, request 
import requests
import urllib
import base64


app = Flask(__name__)

url = 'https://lorala.nam1.cloud.thethings.industries/api/v3/as/applications/my-application/webhooks/test-webhook/devices/eui-70b3d5499a2b29c2/down/push'
headers = {'Authorization': "Bearer NNSXS.36NKRJCT6PUYWDZJR3B26XRA5FAY4BQSN2SMSVI.DB5MRJ2YQBOXNSAGU5LKMG6RDMEBOVD3SEDHXAENTO7V2UKFTHEQ",
       'Content-Type': "application/json",
       'User-Agent': "my-integration/my-integration-version"}
data = {"downlinks":[{
       "f_port":2,
       "frm_payload": "EQ==",
      #"decoded_payload": {
       # "bytes": list(base64.b64encode(b'data to be encoded'))
      #}
    }]
  }

  
@app.route('/')
def hello():
    return "Hello World!"


@app.route('/join-accept', methods=['POST'])
def webhook3():
    print("hello")
    if(request.method == 'POST'):
        print(request.json)
    return 'success', 200

@app.route('/uplinks', methods=['POST'])
def webhook1():
    if(request.method == 'POST'):
        
        res = requests.post(url, json=data, headers=headers)
        print (res.status_code)
        print("sent")
        print (res.raise_for_status())
        return 'success', 200


@app.route('/downlinks', methods=['POST'])
def webhook2():
    if(request.method == 'POST'):
        print(request.json)
        return 'success', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

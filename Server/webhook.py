from flask import Flask, request 
import requests
import json
import base64
import get_blobs


app = Flask(__name__)

# our tenant
url = 'https://lorala.nam1.cloud.thethings.industries/api/v3/as/applications/my-application/webhooks/test-webhook/devices/eui-70b3d5499a2b29c2/down/push'
headers = {'Authorization': "Bearer NNSXS.36NKRJCT6PUYWDZJR3B26XRA5FAY4BQSN2SMSVI.DB5MRJ2YQBOXNSAGU5LKMG6RDMEBOVD3SEDHXAENTO7V2UKFTHEQ",
       'Content-Type': "application/json",
       'User-Agent': "my-integration/my-integration-version"}
data = {
    "downlinks":[{
       "f_port":2,
       "frm_payload": "EQ==",
    }]
  }

# Mike's tenant
# url = 'https://219proj.nam1.cloud.thethings.industries/api/v3/as/applications/my-application/webhooks/test-webhook/devices/eui-70b3d5499a2b29c2/down/push'
# headers = {'Authorization': "Bearer NNSXS.7WS6FXL64X66VEW5MCGPMR5NZ65BYVUDZ7P4NKI.4RFGQD4GRGPOGETGBEXPDX3XTRYUYS4UQAIEGYBDEXALCJTJOY5A",
#        'Content-Type': "application/json",
#        'User-Agent': "my-integration/my-integration-version"}
# data = {"downlinks":[{
#        "f_port":2,
#        "frm_payload": "EQ==",
#     }]
#   }

file_chunks = []

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/join-accept', methods=['POST'])
def webhook3():
    print("join-accept")
    if(request.method == 'POST'):
        print(request.json)
        log("join-accept", request.json)
    return 'success', 200

@app.route('/uplinks', methods=['POST'])
def webhook1():
    global file_chunks

    if(request.method == 'POST'):

        decoded_uplink_data = decode_frm_payload(request.json["uplink_message"]["frm_payload"])

        # if we get the OTA trigger
        if(decoded_uplink_data == '\x01\x02\x03'):
            json, file_chunks = start_ota("thisisatest.txt")
            res = requests.post(url, json=json, headers=headers)
            log("uplinks", request.json)
            return 'success', 200

        if(decoded_uplink_data == '\x03\x02\x01'):
            json = start_ota("thisisatest.txt")
            
            if(len(file_chunks)):
                blob = file_chunks.pop(0)
                json = insert_payload_in_json(blob)

                res = requests.post(url, json=json, headers=headers)
                log("uplinks", request.json)
                return 'success', 200
            else:
                res = requests.post(url, json=insert_payload_in_json('brontasaurus!'), headers=headers)
                log("uplinks", request.json)
                return 'success', 200

        res = requests.post(url, json=insert_payload_in_json(b'\x11'), headers=headers)
        
        log("uplinks", request.json)
        return 'success', 200


@app.route('/downlinks', methods=['POST'])
def webhook2():
    if(request.method == 'POST'):
        print(request.json)
        return 'success', 200

def log(log_name, data):
    try:
        with open(f"logs/{log_name}.log", 'a') as logFile:
            logFile.writelines(json.dumps(data) + "\n")
    except:
        with open(f"logs/{log_name}.log", 'w') as logFile:
            logFile.writelines(json.dumps(data) + "\n")

def insert_payload_in_json(data):
    edata = base64.b64encode(data).decode('utf-8')
    log("encoded_data", f"{data} : {edata}" )

    payload = {
        "downlinks":[{
        "f_port":2,
        "frm_payload": f"{edata}",
        }]
    }
    return payload

def decode_frm_payload(data):
    decoded_data = base64.b64decode(data).decode('utf-8')
    log("decoded_data", f"{data} : {decoded_data}" )
    return decoded_data

def start_ota(filename):
    blobs = get_blobs.get_blobs_from_file(filename)
    messages = len(blobs)
    json = insert_payload_in_json(messages)
    return (json, blobs)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

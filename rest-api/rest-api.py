
import os
import json

import logging 
import logging.handlers as handlers
from flask import Flask, jsonify, request

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)

build_dict = {'build_id':1, 'image_name':'test-ami1', 'provider':'amazon', 'status':'success', 'state':'non-vulnerable', 'cve_id':0, 'date':'na'}

@app.route('/')
def index():
   app.logger.info("reved a blank query - ignore")
   return jsonify({'Hi':'reachable & working'})


@app.route('/apiv1/get-table', methods=['GET'])
def get_table():
   app.logger.info("recvd get table query")
   json_data = json.dumps(build_dict)
   return json_data; 

if __name__ == '__main__':
    print('Calling main')
    app.run(host='0.0.0.0', port=5000, debug=False)


import os
import json

import logging 
import logging.handlers as handlers
from flask import Flask, jsonify, request
import sqlite3

#To read DE and reply using rest-api
DBFILE = "demo1.db"

class dbopen(object):
    def __init__(self, path):
        self.path = path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
    
app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler())
app.logger.setLevel(logging.INFO)


@app.route('/')
def index():
   app.logger.info("reved a blank query - ignore")
   return jsonify({'Hi':'reachable & working'})

# GET TABLE
@app.route('/apiv1/get-table', methods=['GET'])
def get_table():
   app.logger.info("recvd get table query")
   with dbopen(DBFILE) as c:
        c.execute("SELECT * FROM seekmap")
        result = c.fetchall()
        print(result) 
   json_data = json.dumps(result)
   return json_data; 

#POST - TRIGGER CVE detection
@app.route('/apiv1/trigger-cve-detection', methods=['POST'])
def post():
   app.logger.info("recvd post query to trigger cve detection")
   user_input = request.json['input']
   json_data = jsonify({'User request to CVE detection: ': 'Success'})
   return json_data

if __name__ == '__main__':
    print('Calling main')
    app.run(host='0.0.0.0', port=5000, debug=False)

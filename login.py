from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import requests
#import pandas as pd
import json
#from oneclasssvm import getresult
app = Flask(__name__)

#app.config['MONGO_DBNAME'] = 'databasename'
app.config['MONGO_URI'] = 'mongodb://admin:123456@ds139219.mlab.com:39219/smart_irrigation'

mongo = PyMongo(app)
@app.route('/', methods=['GET'])
def get():
    return "Hello"
@app.route('/login', methods=['GET'])
def get_all_frameworks():
    framework = mongo.db.login

    output = []

    for q in framework.find():
        output.append({'user' : q['user'], 'password' : q['password']})
        print(output)
        return jsonify(output)
@app.route('/login/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.login

    q = framework.find_one({'user' : name})

    if q:
        output = {'user' : q['user'], 'password' : q['password'],'crop': q['crop']}
    else:
        output = 'No results found'
    print(output)
    return jsonify(output)
@app.route('/signup', methods=['POST'])
def add_framework():
    framework = mongo.db.framework
    emailid = request.json['user']
    password = request.json['password']
    crop= request.json['crop']
    framework_id = framework.insert({'user' : emailid, 'password' : password, 'crop': crop})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'user' : new_framework['user'], 'password' : new_framework['password'],'crop':new_framework['crop']}

    return jsonify(output)

def getdata(data,name):
    framework = mongo.db.login
    q = framework.find_one({'user' : name})
    framework = mongo.db.crop_details
    crop=framework.find_one({'crop': q['crop']})
    '''
    result=getresult(data,crop)
    count=0
    output={}
    print(len(result))
    for i in range(len(result)):
        #print(type(result[i]))
        if(result[i]==1):
            count=1+count
    if(count>(3*len(result))/4):
        d=json.loads(data)
        d=d['feeds']
        l=0
        for i in d:
            l=int(i['field2'])+l
        l=l/(len(d)) '''
    output={'sensor1':60,'sensor2':20,'sensor3':45, 'threshold':35}
    return jsonify(output)

@app.route('/getinfo/<name>',methods=['GET'])
def get_info(name):
	soil_data=requests.get("https://api.thingspeak.com/channels/452295/feeds.json?api_key=FYZ31ZL74D3RUEML&results=200")
	return getdata(soil_data.text,name)

if __name__ == '__main__':
    app.run()

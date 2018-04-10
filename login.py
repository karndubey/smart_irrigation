from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import requests
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
        output.append({'emailid' : q['emailid'], 'password' : q['password']})
        print(output)
        return jsonify({'result' : output})
@app.route('/login/<name>', methods=['GET'])
def get_one_framework(name):
    framework = mongo.db.login

    q = framework.find_one({'emailid' : name})

    if q:
        output = {'name' : q['emailid'], 'language' : q['password']}
    else:
        output = 'No results found'
    print(output)
    return jsonify({'result' : output})
@app.route('/signup', methods=['POST'])
def add_framework():
    framework = mongo.db.framework
    emailid = request.json['emailid']
    password = request.json['password']

    framework_id = framework.insert({'emailid' : passwordyy, 'password' : password})
    new_framework = framework.find_one({'_id' : framework_id})

    output = {'name' : new_framework['name'], 'language' : new_framework['language']}

    return jsonify({'result' : output})
@app.route('/getinfo',methods=['GET'])
def get_info():
	soil_data=requests.get("https://api.thingspeak.com/channels/452295/feeds.json?api_key=FYZ31ZL74D3RUEML&results=200")
	return soil_data.text
if __name__ == '__main__':
    app.run(debug=True)

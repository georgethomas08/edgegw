# app.py


from flask import Flask
from flask import request, render_template, flash, redirect, url_for, json, jsonify
from random import sample
from flask_sqlalchemy import SQLAlchemy
from config import BaseConfig
from flask_mongoengine import MongoEngine
from datetime import datetime
from datetime import timedelta
from werkzeug import secure_filename
import logging
import json
import requests


app = Flask(__name__)
app.config.from_object(BaseConfig)
app.config['MONGODB_SETTINGS'] = {
    'db': 'edgedb',
    'host': 'mongodb',
    'username': 'edgedbuser',
    'password': 'edgedb',
    'port': 27017
}
app.config['DEBUG'] = True
logging.basicConfig(level=logging.INFO, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
#db = SQLAlchemy(app)

UPLOAD_FOLDER = '/path'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mdb = MongoEngine()
mdb.init_app(app)

from forms import LoginForm
from forms import RegistrationForm
from forms import ManageForm
from forms import DataFreqForm
#from models import *
from nosqlmodels import *

#@app.route('/', methods=['GET', 'POST'])
#def index():
#    if request.method == 'POST':
#        text = request.form['text']
#        post = Post(text)
#        db.session.add(post)
#        db.session.commit()
#    posts = Post.query.order_by(Post.date_posted.desc()).all()
#    return render_template('index.html', posts=posts)

@app.route('/')
def index():
        #return "Welcome to the Edge Gateway Solution!"
        return jsonify({'Welcome to the Edge Gateway Solution': request.remote_addr}), 200

@app.route('/test', methods=['GET', 'POST'])
def test():
        return jsonify({'ip': request.environ.get('HTTP_X_REAL_IP', request.remote_addr)}), 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Login :" + form.username.data + " Password:"+ form.password.data)
        #flash('Login requested by user {}, remember_me={}'.format(
        #form.username.data, form.remember_me.data))
        doc= User.objects(name = form.username.data).to_json()
        print(doc)
        if doc is None:
            flash('Login has Failed!!!')
            return render_template('login.html', title='Sign In', form=form)
        #flash('Login is Successful!!!')
        return redirect(url_for('dboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
        form = RegistrationForm()
        if form.validate_on_submit():
                user = User(name=form.username.data, email=form.email.data)
                user.save()
                print("UserName :" + form.username.data)
                print("Email:    " + form.email.data)
                print("Password: " + form.password.data)
                flash('Congratulations, you are now a registered user!!!')
                return redirect(url_for('login'))
        return render_template('register.html', title='Regsiter', form=form)

@app.route('/manage', methods=['GET', 'POST'])
def manage():
        form = ManageForm()
        if form.validate_on_submit():
                dev = Devinfo(
                        devName=form.devName.data,
                        devId=form.devId.data,
                        devStatus=0,
                        devType=form.devType.data,
                        devVendor=form.devVendor.data
                        )
                dev.save()
                print("devName: " + form.devName.data)
                #print("devId: " + form.devId.data)
                print("devType: " + form.devType.data)
                print("devVendor: " + form.devVendor.data)
                return redirect(url_for('manage'))
        return render_template('manage.html', title='Manage', form=form)

@app.route('/dboard', methods=['GET', 'POST'])
def dboard():
        form = DataFreqForm()
        if form.validate_on_submit():
                dataF = DataFrequency(dataFq=form.freqValue.data, dataUt=str(form.freqUnit.data), eTemp=str(form.tEnable.data), eHumi=str(form.hEnable.data), ePres=str(form.pEnable.data))
                dataF.save()
                print("Data Frequency: " + str(form.freqValue.data))
                print("Data Unit: " + str(form.freqUnit.data))
                if(form.freqUnit.data):
                    flash('Current Data Frequency:' + str(form.freqValue.data) + 'minutes')
                else:
                    flash('Current Data Frequency:' + str(form.freqValue.data) + 'seconds')
                #return redirect(url_for('dboard'))
        return render_template('dboard.html', title='Dashboard', form=form)

@app.route('/config', methods=['GET', 'POST'])
def config():
        return render_template('config.html')

@app.route('/modbus', methods=['GET', 'POST'])
def modbus():
        return render_template('modbus.html')

@app.route('/lora', methods=['GET', 'POST'])
def lora():
        return render_template('lora.html')

@app.route('/modbusupload]', methods=['GET', 'POST'])
def modbusupload():
    print("Inside modbus_upload")
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        data1 = f.read()
        print(data)
        return "File uploaded successfully"

@app.route('/tdata', methods=['GET', 'POST'])
def tdata():
        #for temprec in Tsdata.objects(deviceId=1):
            #print(f'DeviceID:{temprec.deviceId} Temperature:{temprec.temp} Timestamp:{temprec.ts}')
        tslowlimit = datetime.datetime.now()-timedelta(hours=1)
        temprecs = Tsdata.objects(deviceId=1,ts__gte=tslowlimit).only('temp','ts')
        #temprecs = Tsdata.objects(deviceId=1).only('temp','ts')
        return jsonify({'temprecs':temprecs})
        #return jsonify({'results': sample(range(1,10),5)})

@app.route('/hdata', methods=['GET', 'POST'])
def hdata():
        #for humrec in Tsdata.objects(deviceId=1):
            #print(f'DeviceID:{humrec.deviceId} Humidity:{humrec.humidity} Timestamp:{humrec.ts}')
        tslowlimit = datetime.datetime.now()-timedelta(hours=1)
        humrecs = Tsdata.objects(deviceId=1,ts__gte=tslowlimit).only('humidity','ts')
        #humrecs = Tsdata.objects(deviceId=1).only('humidity','ts')
        return jsonify({'humrecs':humrecs})

@app.route('/pdata', methods=['GET', 'POST'])
def pdata():
        #for presrec in Tsdata.objects(deviceId=1):
            #print(f'DeviceID:{presrec.deviceId} Humidity:{presrec.pressure} Timestamp:{presrec.ts}')
        tslowlimit = datetime.datetime.now()-timedelta(hours=1)
        presrecs = Tsdata.objects(deviceId=1,ts__gte=tslowlimit).only('pressure','ts')
        #presrecs = Tsdata.objects(deviceId=1).only('pressure','ts')
        return jsonify({'presrecs':presrecs})

@app.route('/tsdataput', methods=['GET', 'POST'])
def tsdataput():
        temp = 0
        humidity = 0
        pressure = 0

        req_data = request.get_json()

        if(req_data.get('temp')):
            temp = int(req_data['temp'])
        if(req_data.get('humidity')):
            humidity = int(req_data['humidity'])
        if(req_data.get('pressure')):
            pressure = int(req_data['pressure'])

        deviceId = int(req_data['deviceId'])
        ts       = datetime.datetime.strptime(req_data['ts'], '%Y-%m-%d %H:%M:%S.%f')
        tsdata   = Tsdata(temp=temp,humidity=humidity,pressure=pressure,ts=ts,deviceId=deviceId)
        tsdata.save()
        print(f'Data received is Temp:{temp} Humidity:{humidity} pressure:{pressure} ts:{ts}')
        for dataFreq in DataFrequency.objects:
            print(dataFreq.dataFq)

        resp = {
        "DataFreq":dataFreq.dataFq,
        "Unit":dataFreq.dataUt,
        "Temperature":dataFreq.eTemp,
        "Humidity":dataFreq.eHumi,
        "Pressure":dataFreq.ePres
        }

        resp = json.dumps(resp)
        #return '''Temp:{} Humidity:{} Pressure:{} ts:{}'''.format(temp,humidity,pressure,ts)
        return (resp)

def add_user_db():
    print("In add_user_db()")
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    print(username, email, password)
    user1 = EUser(EntUserName=username, EntUserEmail=email)
    user1.set_password(password)
    user1.EntUserID = 1010
    db.session.add(user1)
    db.session.commit()
    return("User added succesfully")

def validate_user():
    print("In validate_user()")
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    user1 = EUser.query.filter_by(EntUserName=username).first()
    if user1 is None or not user1.check_password(password):
        print ('Authentication failed!')
        return Response("Authentication failed!", 401)
    print ('Authentication Success!')
    return Response("Authentication Success!!!", 200)

if __name__ == '__main__':
    app.run(debug=True)

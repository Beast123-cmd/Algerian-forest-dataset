from flask import Flask,request,jsonify,render_template
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

application=Flask(__name__)
app=application

## import the ridge anf scaler models
ridge_model=pickle.load(open('models/ridge.pkl','rb'))
standard_scaler=pickle.load(open('models/scaler.pkl','rb'))


@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/predictdata",methods=['GET','POST'])
def predict_datapoint():
    if request.method=='POST':
        Temperature=float(request.form.get('Temperature'))
        RH=float(request.form.get('RH'))
        Ws=float(request.form.get('Ws'))
        Rain=float(request.form.get('Rain'))
        FFMC=float(request.form.get('FFMC'))
        DMC=float(request.form.get('DMC'))
        ISI=float(request.form.get('ISI'))
        classes = float(request.form.get("Classes"))
        region = float(request.form.get("Region"))

        new_data_scaled=standard_scaler.transform([[Temperature,RH,Ws,Rain,FFMC,DMC,ISI,classes,region]])
        result=ridge_model.predict(new_data_scaled)

        return render_template('home.html',results=result[0])


    else:
        return render_template('home.html')

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
    
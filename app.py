from flask import Flask,render_template,request
import traceback
import os
import numpy as np
import pandas as pd
from mlProject.pipeline.prediction import PredictionPipeline

app=Flask(__name__)

@app.route('/',methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route("/train",methods=['GET'])
def training():
    os.system("python main.py")
    return "training successful"

@app.route("/predict",methods=['POST','GET'])

def index():
    if request.method=='POST':
        try:
            fixed_acidity=float(request.form['fixed_acidity'])
            volatile_acidity=float(request.form['volatile_acidity'])
            citric_acid=float(request.form['citric_acid'])
            residual_sugar=float(request.form['residual_sugar'])
            cholrides=float(request.form['chlorides'])
            free_sulfur_dioxide=float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide=float(request.form['total_sulfur_dioxide'])
            density=float(request.form['density'])
            pH=float(request.form['pH'])
            sulphates=float(request.form['sulphates'])
            alcohol=float(request.form['alcohol'])

            data=[fixed_acidity,volatile_acidity,citric_acid,residual_sugar,cholrides,free_sulfur_dioxide,total_sulfur_dioxide,density,pH,sulphates,alcohol]
            columns=['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar','chlorides','free sulfur dioxide','total sulfur dioxide','density','pH','sulphates','alcohol']
            data=pd.DataFrame([data],columns=columns)

            obj=PredictionPipeline()
            predict=obj.predict(data)
            # Convert prediction to float for template calculations
            predict=float(predict[0])
            
            # Pass all parameters to results page
            return render_template("results.html",
                                 prediction=round(predict, 2))
        except Exception as e:
            print(str(e))
        
if __name__=="__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)
from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
import joblib

app = Flask(__name__)

# Load the model directly
model = joblib.load('artifacts/model_trainer/model.joblib')

@app.route('/', methods=['GET'])
def homePage():
    return render_template("index.html")

@app.route("/train", methods=['GET'])
def training():
    os.system("python main.py")
    return "Training successful!"

@app.route("/predict", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            fixed_acidity = float(request.form['fixed_acidity'])
            volatile_acidity = float(request.form['volatile_acidity'])
            citric_acid = float(request.form['citric_acid'])
            residual_sugar = float(request.form['residual_sugar'])
            chlorides = float(request.form['chlorides'])
            free_sulfur_dioxide = float(request.form['free_sulfur_dioxide'])
            total_sulfur_dioxide = float(request.form['total_sulfur_dioxide'])
            density = float(request.form['density'])
            pH = float(request.form['pH'])
            sulphates = float(request.form['sulphates'])
            alcohol = float(request.form['alcohol'])

            data = [fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
                   free_sulfur_dioxide, total_sulfur_dioxide, density, pH, sulphates, alcohol]
            
            columns = ['fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar',
                      'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density',
                      'pH', 'sulphates', 'alcohol']
            data = pd.DataFrame([data], columns=columns)

            # Use the loaded model to make prediction
            predict = model.predict(data)
            predict = float(predict[0])
            
            return render_template("results.html", prediction=round(predict, 2))
            
        except Exception as e:
            import traceback
            print("=" * 50)
            print("EXCEPTION OCCURRED:")
            print(str(e))
            print("FULL TRACEBACK:")
            traceback.print_exc()
            print("=" * 50)
            return f"Error: {str(e)}"
    
    return render_template("index.html")

if __name__ == "__main__":
    # Use port 8080 for production, 5000 for local development
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)

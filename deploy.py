from flask import Flask, render_template, request, jsonify
import json
import pickle

app = Flask(__name__)
# Load the Model
model = pickle.load(open('insurance_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template()

@app.route('/predict', methods=['POST'])
def predict():

    print(request.get_json())
    # Extracting form data
    age = request.get_json()['age']
    gender = request.get_json()['gender']
    bmi = request.get_json()['bmi']
    children = request.get_json()['children']
    smoker = request.get_json()['smoker']
    region = request.get_json()['region']


    # Convert to appropriate data types
    age = int(age)
    gender = int(gender)
    bmi = float(bmi)
    children = int(children)
    smoker = int(smoker)
    region = int(region)

    # Make prediction
    prediction = model.predict([[age, gender, bmi, children, smoker, region]])

    output= prediction.tolist()

    output2= json.dumps(output)
    return jsonify({
        'data': output2
    })


if __name__ == '__main__':
    app.run(debug=True)

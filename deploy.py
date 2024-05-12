from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
import bcrypt
import json
import pickle
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('indexs.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check if any field is empty
        if not name or not email or not password:
            error_message = 'All fields are required.'
            return render_template('register.html', error=error_message)


         # Check if the email already exists
        existing_user = User.query.filter_by(email=email).first()
           # Check if any field is empty
        if existing_user:
            error_message = 'Email already exists!.'
            return render_template('register.html', error=error_message)
        
          # If email is unique, proceed with registration    
        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    
    

    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        # Check if any field is empty
        if not email or not password:
            error_message = 'All fields are required.'
            return render_template('login.html', error=error_message)


        if not user:
            error_message = 'Incorrect email.  Please try again.!'
            return render_template('login.html', error=error_message)
        
        if user and user.check_password(password):
            session['email'] = user.email
            # return redirect('/dashboard')
            return redirect('/Home')
        else:
            error_message = 'Incorrect password. Please try again.'
            return render_template('login.html',error=error_message)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')


# Load the Model
model = pickle.load(open('insurance_model.pkl', 'rb'))

@app.route('/Home')
def home():
     if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('index.html',user=user)
     return redirect('/login')

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
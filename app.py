from flask import Flask, request, render_template
import pickle
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)

model = pickle.load(open("model_pickle.pkl", 'rb'))

app = Flask(__name__)

scaler=StandardScaler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def prediction():
    gender = request.form['gender']
    age = float(request.form['age'])
    hypertension = int(request.form['hypertension'])
    heartdisease = int(request.form['heartdisease'])
    ever_married = request.form['ever_married']
    work_type = request.form['work_type']
    Residence_type = request.form['Residence_type']
    avg_glucose_level = float(request.form['avg_glucose_level'])
    bmi = float(request.form['bmi'])
    smoking_status = request.form['smoking_status']

    if (gender == "Male"):
            gender_male=1
            gender_other=0
    elif(gender == "Other"):
            gender_male = 0
            gender_other = 1
    else:
            gender_male=0
            gender_other=0
        
        # married
    if(ever_married=="Yes"):
            ever_married_yes = 1
    else:
            ever_married_yes=0

        # work  type
    if(work_type=='Self-employed'):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 1
            work_type_children=0
    elif(work_type == 'Private'):
            work_type_Never_worked = 0
            work_type_Private = 1
            work_type_Self_employed = 0
            work_type_children=0
    elif(work_type=="children"):
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=1
    elif(work_type=="Never_worked"):
            work_type_Never_worked = 1
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0
    else:
            work_type_Never_worked = 0
            work_type_Private = 0
            work_type_Self_employed = 0
            work_type_children=0

        # residence type
    if (Residence_type=="Urban"):
            Residence_type_Urban=1
    else:
            Residence_type_Urban=0

        # smoking sttaus
    if(smoking_status=='formerly smoked'):
            smoking_status_formerly_smoked = 1
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0
    elif(smoking_status == 'smokes'):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 1
    elif(smoking_status =="never smoked"):
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 1
            smoking_status_smokes = 0
    else:
            smoking_status_formerly_smoked = 0
            smoking_status_never_smoked = 0
            smoking_status_smokes = 0

    feature = scaler.fit_transform([[age, hypertension, heartdisease, avg_glucose_level, bmi, gender_male, gender_other, ever_married_yes, work_type_Never_worked, work_type_Private, work_type_Self_employed, work_type_children, Residence_type_Urban,smoking_status_formerly_smoked, smoking_status_never_smoked, smoking_status_smokes]])

    prediction = model.predict(feature)[0]

    if prediction == 1:
       print("Yes, you may be likely to have a stroke. Please see a doctor.")
    elif prediction == 0:
        print("No, you are not likely to have a stroke")
    return render_template("index.html", prediction_text="Chance of Stroke Prediction is --> {}".format(prediction))

if __name__ == '__main__':
    # you can run init / fiting here
    app.run(debug=True)
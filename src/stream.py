from model_call import gen as gen
import streamlit as st
import pickle
import pandas as pd

valid = False
called = False
model = pickle.load(open('model.pkl', 'rb'))
# hide_streamlit_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
st.title("Women's Diabetes Diagnosis Assessment")
st.caption("Enter the following fields")
preg = st.text_input('Number of pregnancies', )

age = st.text_input('Age')

gluc = st.text_input('Plasma Glucose Concentration (mg/DL)')

bp = st.text_input('Blood Pressure (mm Hg)')

skin = st.text_input('Tricep Skin Fold Thickness (mm)')

ins = st.text_input('Insulin Level (mu U/ml)')

bmi = st.text_input('Body Mass Index')

dpf = st.text_input('Diabetes Pedigree Function')


def get_outcome(preg2, age2, gluc2, bp2, skin2, ins2, bmi2, dpf2):
    result = gen(preg2, gluc2, bp2, skin2, ins2, bmi2, dpf2, age2)
    return result


def getProbability(preg2, age2, gluc2, bp2, skin2, ins2, bmi2, dpf2):
    df = pd.DataFrame()
    preg1 = [float(preg2)]
    gluc1 = [float(gluc2)]
    bp1 = [float(bp2)]
    st1 = [float(skin2)]
    ins1 = [float(ins2)]
    bmi1 = [float(bmi2)]
    dpf1 = [float(dpf2)]
    age1 = [float(age2)]
    df['Pregnancies'] = preg1
    df['Glucose'] = gluc1
    df['BloodPressure'] = bp1
    df['SkinThickness'] = st1
    df['Insulin'] = ins1
    df['BMI'] = bmi1
    df['DiabetesPedigreeFunction'] = dpf1
    df['Age'] = age1
    outcome = (model.predict_proba(df))
    return outcome[0][0]


def check_float(string):
    try:
        float_value = float(string)
        if float_value >= 0 and string.strip() != "":
            return True
        else:
            return False
    except ValueError:
        return False


def check(pr, ag, gl, b, sk, i, bm, dp):
    if (check_float(pr) and check_float(ag) and check_float(gl) and check_float(b) and check_float(sk) and check_float(
            i) and check_float(bm) and check_float(dp)):
        out = get_outcome(pr, ag, gl, b, sk, i, bm, dp)
        if(out == 0):
            result = "negative"
        else:
            result = "positive"

        prob = getProbability(pr, ag, gl, b, sk, i, bm, dp)
        if out==0:
            real_prob = prob
        else:
            real_prob = 1-prob
        print_prob = round(real_prob.item()*100, 2)
        st.header("The patient is most likely diabetes " + result)
        st.write("It is " + str(print_prob) + "% probable that the patient is " + result + "")
    else:
        st.write("One or more fields are empty or invalid.")


check(preg, age, gluc, bp, skin, ins, bmi, dpf)

import Relative
import time
from model_call import gen as gen
import streamlit as st
import pickle
import pandas as pd
from random import *
from dpf import dpf_calculate as dpf
import Relative
model = pickle.load(open('model.pkl', 'rb'))
keys = []
fh_filled = True
def newKey():
    int_key = (randint(1, 100))
    while int_key in keys:
        int_key = (randint(1, 100))
    keys.append(int_key)
    return int_key
def add_row():
    # Add an empty row to the session state
    rows = st.session_state.get("rows", [])
    rows.append({"dropdown1": "","dropdown2": "","textbox1": "", "textbox2": ""})
    st.session_state.rows = rows
def delete_row(row_index):
    # Delete the row with the given index from the session state
    rows = st.session_state.get("rows", [])
    del rows[row_index]
    st.session_state.rows = rows
def replace_values(lst):
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            if lst[i][j] == '':
                lst[i][j] = 0
            elif lst[i][j].isdigit():
                lst[i][j] = int(lst[i][j])
    return lst
def calculate():
    # Calculate and display the result based on the user input

    data = []
    relative_set = []
    for row in st.session_state.get("rows", []):
        data.append([row["dropdown"], row["textbox1"], row["textbox2"], row["dropdown2"]])
    fixed_data = replace_values(data)
    # st.write(fixed_data)
    object_dict = {}

    for x in fixed_data: # for every array in fixed data
        # "Parent", "Sibling", "Half-Sibling", "Grandparent",
        # "Uncle/Aunt", "Half-Uncle/Aunt", "First Cousin"
        rel_type = "p"
        if x[0] == "Parent" or x[0] == "Sibling":
            rel_type = "p"
        elif x[0] == "Half-Sibling" or x[0] == "Grandparent" or x[0] == "Uncle/Aunt":
            rel_type == "half_sibling"
        else:
            rel_type = "first_cousin"
        adm = x[1]
        acl = x[2]
        if x[3] == "Positive":
            dia = True
        else:
            dia = False
        object_dict[f"relative_{newKey()}"] = Relative.Relative(rel_type, adm, acl, dia)
    listed = list(object_dict.values())
    if not listed:
        global fh_filled
        fh_filled = False

    return dpf(listed)


def kill_all_rows():
    rows = st.session_state.get("rows", [])

def main():
    hide_streamlit_style = """
                    <style>
                    div[data-testid="stToolbar"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stDecoration"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    div[data-testid="stStatusWidget"] {
                    visibility: hidden;
                    height: 0%;
                    position: fixed;
                    }
                    #MainMenu {
                    visibility: hidden;
                    height: 0%;
                    }
                    header {
                    visibility: hidden;
                    height: 0%;
                    }
                    footer {
                    visibility: hidden;
                    height: 0%;
                    }
                    </style>
                    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Pregnancies,Glucose,BloodPressure,SkinThickness,Insulin,BMI,DiabetesPedigreeFunction,Age,Outcome
    st.title("Predict the Onset of Diabetes")

    st.caption("Enter the following fields")
    preg = st.text_input('Number of pregnancies')

    age = st.text_input('Age')

    gluc = st.text_input('Plasma Glucose Concentration (mg/DL)')

    bp = st.text_input('Diastolic blood pressure (mm Hg)')

    skin = st.text_input('Tricep Skin Fold Thickness (mm)')

    ins = st.text_input('2-Hour Serum Insulin (mu U/ml) ')
    weight = st.text_input('Weight (in lbs)')
    height = st.text_input("Height (in in)")
    # bmi = st.text_input('Body Mass Index')
    st.header("Family History")
    st.caption("Add all of the individual's parents, grandparents, siblings, aunts/uncles, and first cousin. "
               "If the diagnosis is negative, ignore the diagnosis age field. Double-Click delete to remove a row")
    col1, col2, col3 = st.columns(3)
    if col1.button("New Relative"):
        add_row()
    if col2.button("Calculate"):
        dpf = str(calculate())

        check(preg, age, gluc, bp, skin, ins, weight, height, dpf)

    # Add the rows
    for i, row in enumerate(st.session_state.get("rows", [])):
        # st.write(f"Row {i + 1}")
        col1, col2, col3, col4, col5 = st.columns(5)
        row["dropdown"] = col1.selectbox("Relative Type", ["Parent", "Sibling", "Half-Sibling", "Grandparent",
                                                           "Uncle/Aunt", "Half-Uncle/Aunt", "First Cousin"],
                                         key=f"dropdown_{i}")
        row["dropdown2"] = col2.selectbox("Diagnosis", ["Positive", "Negative"], key=f"dropdown2_{i}")
        row["textbox1"] = col3.text_input("Age at Last Physical", value=row["textbox1"], key=f"textbox1_{i}")
        row["textbox2"] = col4.text_input("Age At Diagnosis", value=row["textbox2"], key=f"textbox2_{i}")
        if col5.button("Delete", key=f"delete_{i}"):
            delete_row(i)

    if col3.button("Clear All"):
        rows = st.session_state.get("rows", [])
        del rows
        rows = []
        st.session_state.rows = rows


# outcome
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

def check_b(w, h):
    if int(w)*int(h) > 0:
        return True
    return False
def check(pr, ag, gl, b, sk, i, w, h, dp):
    if (check_float(pr) and check_float(ag) and check_float(gl) and check_float(b) and check_float(sk) and check_float(
            i) and check_float(w) and check_float(h) and check_float(dp) and check_b(w, h) and fh_filled):
        kg = float(w)/2.205
        m = 0.0254 * float(h)
        bm = kg / (m * m)
        out = get_outcome(pr, ag, gl, b, sk, i, bm, dp)
        if (out == 0):
            result = "not develop"
        else:
            result = "develop"
        prob = getProbability(pr, ag, gl, b, sk, i, bm, dp)

        if out == 0:
            real_prob = prob
        else:
            real_prob = 1 - prob
        print_prob = round(real_prob.item() * 100, 2)
        if int(gl) > 200 or int(i) > 300:
            print_prob = 99
            result = "develop"
        if print_prob >= 90:
            amt = "extremely"
        elif 80 <= print_prob < 90:
            amt = "very"
        elif 70 <= print_prob < 80:
            amt = "moderately"
        else:
            amt = "somewhat"
        with st.spinner('Analyzing Data...'):
            time.sleep(1.5)
        with st.spinner('Body Mass Index is ' + str(float(int(bm*100))/100)):
            time.sleep(1)
        with st.spinner('Making Prediction...'):
            time.sleep(1.5)
        st.header("It is " + amt + " likely that the patient will " + result + " diabetes within the next 5 years.")
        st.write("It is " + str(print_prob) + "% probable that the patient will " + result + " diabetes within the next 5 years.")
        if int(gl) > 200 or int(i) > 300:
            st.caption("Note: The information you provided indicates you may already have diabetes. Learn More")
    else:
        st.error("One or more fields are empty or invalid.")


if __name__ == "__main__":
    main()

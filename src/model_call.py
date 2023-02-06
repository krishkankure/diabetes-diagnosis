import pickle
def gen(preg, gluc, bp, skin, insu, bmi, dpf, age):
    model = pickle.load(open('model.pkl', 'rb'))
    output = model.predict([[preg, gluc, bp, skin, insu, bmi, dpf, age]])
    return output[0]
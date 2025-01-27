import streamlit as st
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib

st.set_page_config(layout="wide")

scaler = joblib.load("Scaler.pkl")

st.title("Restorent Rating prediction app")



st.caption("this app helps you predict a restorent rewviw class")

st.divider()

averagecost = st.number_input("please enter the estimated average cost for two")
tablebooking = st.selectbox("resturent has table booking?",["yes","no"])
onlinedelivary = st.selectbox("Restyrent has online booking?",["yes","no"])
pricerange = st.selectbox("what is price range (1 chepest, 4 mosteexpensive)",[1,2,3,4])

predictbutton = st.button("predict the review")

st.divider()

model = joblib.load("mlmodel.pkl")

bookingstatus = 1 if tablebooking == "yes" else 0

delivarystatus = 1 if onlinedelivary == "yes" else 0

values = [[averagecost, bookingstatus, delivarystatus, pricerange]]
my_x_values = np.array(values)

X = scaler.transform(my_x_values)

if predictbutton:
    st.snow()

    prediction = model.predict(X)

    # st.write(prediction)

    if prediction <2.5:
        st.write("poor")
    elif prediction < 3.5:
        st.write("average")
    elif prediction <4.0:
        st.write("good")
    elif prediction <4.5:
        st.write("very good")
    else:
        st.write("excellent")


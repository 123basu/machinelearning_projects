import streamlit as st
import pandas as pd
import numpy as np
import joblib

@st.cache_data
def load_model_and_data():
    model = joblib.load("model3.pkl")
    scaler = joblib.load("t3scaler.pkl")
    data = pd.read_csv("Dataset .csv", encoding="utf-8")
    return model, scaler, data

model, scaler, data = load_model_and_data()

st.title("Cuisine-Based Restaurant Predictor")
st.write("Enter a cuisine to find matching restaurants.")

cuisine_input = st.text_input("Enter Cuisine:", "")

if cuisine_input:
    # Filter matching cuisines
    matched_restaurants = data[data["Cuisines"].str.contains(cuisine_input, case=False, na=False)]

    if not matched_restaurants.empty:
        # Preprocess the data
        X = matched_restaurants[["Restaurant Name", "Average Cost for two"]]
        
        # Use LabelEncoder with consistent mappings
        from sklearn.preprocessing import LabelEncoder
        label_encoder = LabelEncoder()
        data["Restaurant Name"] = label_encoder.fit_transform(data["Restaurant Name"])
        X["Restaurant Name"] = label_encoder.transform(X["Restaurant Name"])  # Use same mapping
        
        # Apply scaling
        X_scaled = scaler.transform(X)
        
        # Ensure dimensions match
        if X_scaled.shape[1] != model.n_features_in_:
            st.error("Feature mismatch: Check if preprocessing matches training.")
        else:
            # Predict scores
            scores = model.predict(X_scaled)
            matched_restaurants["Score"] = scores
            
            # Display results
            st.write("### Matching Restaurants:")
            st.dataframe(matched_restaurants[["Restaurant Name", "Average Cost for two", "Score"]])
    else:
        st.write("No matching restaurants found for the given cuisine.")


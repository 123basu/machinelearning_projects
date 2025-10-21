import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os


@st.cache_data
def load_model_and_data():
    # Use paths relative to this script so the app works no matter where streamlit is started from
    base_dir = os.path.dirname(__file__)
    model_path = os.path.join(base_dir, "model3.pkl")
    scaler_path = os.path.join(base_dir, "t3scaler.pkl")
    data_path = os.path.join(base_dir, "Dataset .csv")

    # Helpful error messages if files are missing or inaccessible
    missing = []
    for p in (model_path, scaler_path, data_path):
        if not os.path.exists(p):
            missing.append(p)
    if missing:
        # Raise to show a traceback in the Streamlit logs and also show a friendly message
        msg = "Required files not found:\n" + "\n".join(missing)
        st.error(msg)
        raise FileNotFoundError(msg)

    try:
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        data = pd.read_csv(data_path, encoding="utf-8")
    except Exception as e:
        st.error(f"Error loading model/scaler/data: {e}")
        raise

    return model, scaler, data


model, scaler, data = load_model_and_data()

st.title("Cuisine-Based Restaurant Predictor")
st.write("Enter a cuisine to find matching restaurants.")

cuisine_input = st.text_input("Enter Cuisine:", "")

if cuisine_input:
    # Filter matching cuisines
    matched_restaurants = data[data["Cuisines"].str.contains(cuisine_input, case=False, na=False)]

    if not matched_restaurants.empty:
        # Try two modes:
        # 1) model is a scikit-learn estimator with predict()
        # 2) model is a numpy array of precomputed scores (align by index or by matched rows)
        import numpy as _np
        from sklearn.preprocessing import LabelEncoder

        # Defensive copy so we don't get SettingWithCopyWarning
        matched_restaurants = matched_restaurants.copy()

        if hasattr(model, "predict"):
            # Preprocess the data expected by the trained model
            X = matched_restaurants[["Restaurant Name", "Average Cost for two"]].copy()

            # Use LabelEncoder with consistent mappings across full data
            label_encoder = LabelEncoder()
            # Fit on full dataset (original names) and transform both
            label_encoder.fit(data["Restaurant Name"])
            X["Restaurant Name"] = label_encoder.transform(X["Restaurant Name"])  # Use same mapping

            # Apply scaling
            try:
                X_scaled = scaler.transform(X)
            except Exception as e:
                st.error(f"Error applying scaler: {e}")
                raise

            # Ensure dimensions match if model exposes n_features_in_
            if hasattr(model, "n_features_in_") and X_scaled.shape[1] != model.n_features_in_:
                st.error("Feature mismatch: Check if preprocessing matches training.")
            else:
                # Predict scores
                try:
                    scores = model.predict(X_scaled)
                except Exception as e:
                    st.error(f"Error during model prediction: {e}")
                    raise

                matched_restaurants["Score"] = scores

                # Display results
                st.write("### Matching Restaurants:")
                st.dataframe(matched_restaurants[["Restaurant Name", "Average Cost for two", "Score"]])

        else:
            # model is not an estimator — treat it as array-like of precomputed scores
            model_arr = _np.asarray(model)
            # Try to align by full data index
            if model_arr.ndim == 1:
                if model_arr.shape[0] == data.shape[0]:
                    # Assume model_arr aligns with `data` row-for-row
                    scores_series = pd.Series(model_arr, index=data.index, name="Score")
                    matched_restaurants["Score"] = scores_series.loc[matched_restaurants.index].values
                    st.write("### Matching Restaurants (using precomputed scores):")
                    st.dataframe(matched_restaurants[["Restaurant Name", "Average Cost for two", "Score"]])
                elif model_arr.shape[0] == matched_restaurants.shape[0]:
                    # Scores correspond exactly to the matched subset (same order)
                    matched_restaurants["Score"] = model_arr
                    st.write("### Matching Restaurants (using precomputed scores):")
                    st.dataframe(matched_restaurants[["Restaurant Name", "Average Cost for two", "Score"]])
                else:
                    # Attempt to interpret the array as a list of Restaurant IDs (or keys)
                    # and use frequency/count as a score. This is useful when the pickle
                    # contains recommended restaurant IDs rather than numeric scores.
                    import pandas as _pd

                    counts = _pd.Series(model_arr).astype(str).value_counts()
                    mapping = counts.to_dict()  # keys are str(ids), values are counts

                    if 'Restaurant ID' in data.columns:
                        # Map using Restaurant ID (cast to str for robust matching)
                        matched_restaurants['Score'] = (
                            matched_restaurants['Restaurant ID'].astype(str).map(mapping).fillna(0).astype(int)
                        )

                        if matched_restaurants['Score'].sum() == 0:
                            st.error(
                                "Precomputed ID list was found but could not be matched to the dataset's Restaurant ID column."
                            )
                            raise ValueError("Cannot align precomputed ID array with data Restaurant ID column")
                        else:
                            st.write("### Matching Restaurants (using precomputed ID frequencies as score):")
                            st.dataframe(matched_restaurants[["Restaurant Name", "Average Cost for two", "Score"]])
                    else:
                        st.error(
                            f"Loaded model is a 1-D array of length {model_arr.shape[0]} which cannot be aligned with the dataset ({data.shape[0]}) or the matched subset ({matched_restaurants.shape[0]})."
                        )
                        raise ValueError("Cannot align precomputed score array with data")
            else:
                st.error(f"Loaded model has unexpected shape: {model_arr.shape}")
                raise ValueError("Unexpected model array shape")
    else:
        st.write("No matching restaurants found for the given cuisine.")


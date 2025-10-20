1. Cuisine Classification
Objective: Recommend restaurants to users based on the cuisine they enter using a trained Random Forest classifier.
Key Features:
Preprocessing and encoding of restaurant dataset
Model training and evaluation (Accuracy, Precision, Recall, F1-score)
Streamlit-based web deployment (app.py)
Model persistence using joblib (model3.pkl, t3scaler.pkl)
Tech Stack:
Python, pandas, numpy, scikit-learn, Streamlit, joblib

2. Predict Restaurant Rating
Objective: Predict restaurant ratings and average cost using regression models and analyze business insights.
Key Features:
Comprehensive EDA and feature engineering
Regression models: SVR, DecisionTree, RandomForest, KNN, AdaBoost
Model tuning with GridSearchCV
Evaluation using MAE and RMSE
Visual insights with matplotlib
Tech Stack:
Python, pandas, numpy, scikit-learn, matplotlib

3. Restaurant Recommendation System
Objective: Suggest top restaurants based on user’s preferred cuisine, price range, and rating using NLP and cosine similarity.
Key Features:
Feature vectorization using CountVectorizer
Similarity computation via cosine_similarity
Dynamic user input handling with Streamlit UI
Error handling for missing/no match cases
Tech Stack:
Python, pandas, scikit-learn, Streamlit, NLP (CountVectorizer)

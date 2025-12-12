from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import pickle
import xgboost as xgb

app = Flask(__name__)
CORS(app)  # allow frontend access

# Load your XGBoost model
model = pickle.load(open("model/xgb_model_updated.pkl", "rb"))

@app.route("/")
def home():
    return "Backend is running successfully!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # -----------------------------
    # ENGINEERED FEATURES
    # -----------------------------
    Risk_Score = data["PaymentDelay"] * data["SupportCalls"]
    Spend_per_month = data["Total_spend"] / data["Contract_Length"]
    Engagement_Score = (
        data["Usage_Frequency"] - data["PaymentDelay"] - data["SupportCalls"]
    )

    # -----------------------------
    # FINAL FEATURE ORDER — 15 FEATURES
    # MUST MATCH TRAINING EXACTLY
    # -----------------------------
    features = np.array([
        data["Age"],              # 1
        data["Gender_Label"],     # 2
        data["Usage_Frequency"],  # 3
        data["SupportCalls"],     # 4
        data["PaymentDelay"],     # 5
        data["Total_spend"],      # 6
        data["Last_Interaction"], # 7
        data["Churn"],            # 8  ⭐ Churn added
        Engagement_Score,         # 9
        Risk_Score,               # 10
        data["Contract_Length"],  # 11
        Spend_per_month,          # 12
        data["Sub_Basic"],        # 13
        data["Sub_Premium"],      # 14
        data["Sub_Standard"],     # 15
    ]).reshape(1, -1)

    # Predict using model
    prediction = model.predict(features)[0]

    # Return integer month
    response = jsonify({"tenure_prediction": int(round(prediction))})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == "__main__":
    app.run(debug=True)

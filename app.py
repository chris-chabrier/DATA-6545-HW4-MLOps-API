from flask import Flask, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load model
try:
    model = joblib.load("model.pkl")
    model_loaded = True
except:
    model_loaded = False

# Define expected schema (adjust if needed)
REQUIRED_FIELDS = {
    "delivery_days": (int, float),
    "delivery_vs_estimated": (int, float),
    "price": (int, float),
    "freight_ratio": (int, float),
    "product_category": str,
    "customer_state": str,
    "seller_state": str,
    "payment_type": str,
    "distance_miles": (int, float),
    "product_volume_cm^3": (int, float),
    "total_order_value": (int, float)
}

# ---------------------------
# 1. HEALTH CHECK
# ---------------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model": "loaded" if model_loaded else "not loaded"
    })

# ---------------------------
# INPUT VALIDATION FUNCTION
# ---------------------------
def validate_input(data):
    errors = {}

    # Missing fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors[field] = "missing"

    # Type + value checks
    for field, expected_type in REQUIRED_FIELDS.items():
        if field in data:
            if not isinstance(data[field], expected_type):
                errors[field] = "must be a number" if expected_type != str else "must be a string"
            else:
            # Only run numeric checks if type is valid
                if field in ["price", "freight_value"] and data[field] < 0:
                    errors[field] = "must be positive"

    return errors

# ---------------------------
# 2. SINGLE PREDICTION
# ---------------------------
@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input", "details": "No JSON provided"}), 400

    errors = validate_input(data)
    if errors:
        return jsonify({"error": "Invalid input", "details": errors}), 400

    df = pd.DataFrame([data])

    try:
        pred = model.predict(df)[0]
        prob = model.predict_proba(df)[0][1]
    except Exception as e:
        return jsonify({
            "error": "Model prediction failed",
            "details": str(e)
        }), 400

    return jsonify({
        "prediction": int(pred),
        "probability": round(float(prob), 4),
        "label": "positive" if pred == 1 else "negative"
    })

# ---------------------------
# 3. BATCH PREDICTION
# ---------------------------
@app.route("/predict/batch", methods=["POST"])
def predict_batch():

    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input", "details": "No JSON provided"}), 400

    if not isinstance(data, list):
        return jsonify({"error": "Input must be a list"}), 400

    if len(data) > 100:
        return jsonify({"error": "Max 100 records allowed"}), 400

    results = []

    for record in data:
        errors = validate_input(record)
        if errors:
            return jsonify({"error": "Invalid input", "details": errors}), 400

        df = pd.DataFrame([record])
        try:
            pred = model.predict(df)[0]
            prob = model.predict_proba(df)[0][1]
        except Exception as e:
            return jsonify({
                "error": "Model prediction failed",
                "details": str(e)
            }), 400

        results.append({
            "prediction": int(pred),
            "probability": round(float(prob), 4),
            "label": "positive" if pred == 1 else "negative"
        })

    return jsonify(results)

# ---------------------------
# RUN APP
# ---------------------------
if __name__ == "__main__":
    # Port was originally 5001 during testing
    app.run(host="0.0.0.0", port=5000, debug=True)
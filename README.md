**Description:** This project deploys a machine learning model trained on the Olist e-commerce dataset to predict customer satisfaction (positive vs. negative reviews). 
The trained model (Random Forest classifier) is served via a Flask REST API that allows real-time and batch predictions.
The API is designed for production-style deployment using Docker and is hosted on a cloud platform for public access.

**Live URL:** https://data-6545-hw4-mlops-api.onrender.com/

**API Endpoints:**

  Health Check:
  
    Endpoint: GET /health
    
    Response:
    {
      "status": "healthy",
      "model": "loaded"
    }

  Single Prediction

    Endpoint: POST /predict

    Request Body:
    {
      "delivery_days": 12.0,
      "delivery_vs_estimated": 3.0,
      "price": 149.99,
      "freight_ratio": 0.29,
      "product_category": "electronics",
      "customer_state": "BA",
      "seller_state": "SP",
      "payment_type": "credit_card",
      "distance_miles": 11.5,
      "product_volume_cm^3": 1975.0,
      "total_order_value": 89.97
    }

    Response:
    {
      "label": "negative", 
      "prediction": 0, 
      "probability": 0.4746
    }

  Batch Prediction

    Endpoint: POST /predict/batch

    Request Body:
    [
      { "delivery_days": 10, ... },
      { "delivery_days": 5, ... }
    ]

    Response:
    {
      "predictions": [
        {"label": "negative", "prediction": 1, "probability": 0.73},
        {"label": "negative", "prediction": 0, "probability": 0.41}
      ]
    }

**Expected Model Schema:**

    "delivery_days": (int, float), [0 : 209]
    "delivery_vs_estimated": (int, float), [-147 : 188]
    "price": (int, float), [0.85 : 6735]
    "freight_ratio": (int, float), [0 : 26.24]
    "product_category": str, [e.g. agro_industry_and_commerce, watches_gifts]
    "customer_state": str, [e.g. AC, TO]
    "seller_state": str, [e.g. AM, SP]
    "payment_type": str, [e.g. boleto, voucher]
    "distance_miles": (int, float), [0 : 5377]
    "product_volume_cm^3": (int, float), [168 : 296208]
    "total_order_value": (int, float), [0.85 : 13440]

**Local Setup Instructions:**

  Without Docker:
    1. Install dependencies (pip install -r requirements.txt)
    2. Run Flask API (python app.py)
    3. Test API locally (python test_api.py)

  With Docker:
    1. Build image (docker build -t hw4-api)
    2. Run container (docker run -p 5000:5000 hw4.api)

**Model Information:**

  Model type: Random Forest Classifier (balanced version trained in HW2 assignment)

  Key features:
    - Delivery time features
    - Price/freight values
    - Product categories
    - Payment methods
    - Customer/seller locations and distances

  Key performance metrics: 
    - Accuracy: 0.853
    - Precision: 0.85
    - Recall: 0.981
    - F1 score: 0.911
    - ROC-AUC score: 0.802

import joblib
import os
import pandas as pd
import sys
from app.preprocess import ColumnSelector, NewFeatureHousePricing, TypeImputer, AutoScalerEncoder


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

MODELS_PATH = os.path.join(PROJECT_ROOT, "outputs")

model = None
preprocess_pipeline = None

def load_models():
    """
    Model loading function that ensures the model and preprocess pipeline are loaded only once and reused across predictions.
    """
    global model, preprocess_pipeline
    
    if model is None or preprocess_pipeline is None:
        model = joblib.load(os.path.join(MODELS_PATH, "best_model.pkl"))
        preprocess_pipeline = joblib.load(os.path.join(MODELS_PATH, "preprocess_pipeline.pkl"))
        print("Models loaded successfully.")
    
    return model, preprocess_pipeline


def predict_price(df: pd.DataFrame):
    """
    Predict the price of a house based on the input DataFrame. This function loads the pre-trained model and preprocess pipeline, applies the necessary transformations, and returns the predicted price.
    
    Args:
        df: DataFrame containing the features of the house to predict.
        
    Returns:
        A numpy array with the predicted price.
    """

    model, preprocess_pipeline = load_models()
    
    processed = preprocess_pipeline.transform(df)
    
    prediction = model.predict(processed)
    
    return prediction
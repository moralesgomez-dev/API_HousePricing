from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from app.schemas import HouseFeatures
from app.model import predict_price, load_models
import pandas as pd
import numpy as np


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loading models at startup to improve response times."""
    load_models()
    yield


app = FastAPI(
    title="House Pricing API",
    description="API for predicting house prices based on various features. Built with FastAPI and a machine learning model.",
    version="1.0.0",
    lifespan=lifespan
)


DEFAULT_VALUES = {
    'Id': 0,
    'MSSubClass': 60,
    'MSZoning': 'RL',
    'LotFrontage': 0,
    'LotArea': 8000,
    'Street': 'Pave',
    'Alley': np.nan,
    'LotShape': 'Reg',
    'LandContour': 'Lvl',
    'Utilities': 'AllPub',
    'LotConfig': 'Inside',
    'LandSlope': 'Gtl',
    'Neighborhood': 'NAmes',
    'Condition1': 'Norm',
    'Condition2': 'Norm',
    'BldgType': '1Fam',
    'HouseStyle': '1Story',
    'OverallQual': 5,
    'OverallCond': 5,
    'YearBuilt': 1970,
    'YearRemodAdd': 1970,
    'RoofStyle': 'Gable',
    'RoofMatl': 'CompShg',
    'Exterior1st': 'VinylSd',
    'Exterior2nd': 'VinylSd',
    'MasVnrType': 'None',
    'MasVnrArea': 0,
    'ExterQual': 'TA',
    'ExterCond': 'TA',
    'Foundation': 'PConc',
    'BsmtQual': 'TA',
    'BsmtCond': 'TA',
    'BsmtExposure': 'No',
    'BsmtFinType1': 'Unf',
    'BsmtFinSF1': 0,
    'BsmtFinType2': 'Unf',
    'BsmtFinSF2': 0,
    'BsmtUnfSF': 0,
    'TotalBsmtSF': 0,
    'Heating': 'GasA',
    'HeatingQC': 'Ex',
    'CentralAir': 'Y',
    'Electrical': 'SBrkr',
    '1stFlrSF': 0,
    '2ndFlrSF': 0,
    'LowQualFinSF': 0,
    'GrLivArea': 1000,
    'BsmtFullBath': 0,
    'BsmtHalfBath': 0,
    'FullBath': 1,
    'HalfBath': 0,
    'BedroomAbvGr': 2,
    'KitchenAbvGr': 1,
    'KitchenQual': 'TA',
    'TotRmsAbvGrd': 5,
    'Functional': 'Typ',
    'Fireplaces': 0,
    'FireplaceQu': np.nan,
    'GarageType': 'Attchd',
    'GarageYrBlt': 1970,
    'GarageFinish': 'Unf',
    'GarageCars': 0,
    'GarageArea': 0,
    'GarageQual': 'TA',
    'GarageCond': 'TA',
    'PavedDrive': 'Y',
    'WoodDeckSF': 0,
    'OpenPorchSF': 0,
    'EnclosedPorch': 0,
    '3SsnPorch': 0,
    'ScreenPorch': 0,
    'PoolArea': 0,
    'PoolQC': np.nan,
    'Fence': np.nan,
    'MiscFeature': np.nan,
    'MiscVal': 0,
    'MoSold': 6,
    'YrSold': 2010,
    'SaleType': 'WD',
    'SaleCondition': 'Normal'
}


@app.get("/")
def root():
    """Root endpoint with basic info about the API."""
    return {
        "message": "House Pricing API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "predict": "/v1/predict",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Check if the API is running."""
    return {
        "status": "OK",
        "message": "API is running correctly"
    }


@app.post("/v1/predict")
def predict(features: HouseFeatures):
    """
    Predict the price of a house based on its features.

    Args:
        features: house features (OverallQual, GrLivArea, etc.)

    Returns:
        Predicted price and model version.
    """
    try:
        input_data = DEFAULT_VALUES.copy()

        user_features = features.model_dump()
        input_data.update(user_features)

        input_df = pd.DataFrame([input_data])

        prediction = predict_price(input_df)

        return {
            "predicted_price": float(prediction[0]),
            "currency": "USD",
            "model_version": "v1.0",
            "input_features": user_features
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error in prediction: {str(e)}"
        )

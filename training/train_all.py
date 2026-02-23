"""
Script to RE-TRAIN both the pipeline and the model.
This is necessary so that the .pkl files have the correct references to the modules.
"""
import os
import sys
import pandas as pd
import joblib

# Add the app directory to the path for importing
sys.path.insert(0, os.path.join(os.getcwd(), 'app'))

# Import from app.preprocess (IMPORTANT: must be this way for pickle to work correctly)
from app.preprocess import create_pipeline

# Path configuration
PROJECT_ROOT = os.path.abspath(os.getcwd())
MODELS_PATH = os.path.join(PROJECT_ROOT, "outputs")
DATA_PATH = os.path.join(PROJECT_ROOT, "DATA")


def retrain_pipeline():
    """
    Re-trains the pipeline with the correct module references.
    """
    print("=" * 70)
    print("PIPELINE AND MODEL RE-TRAINING")
    print("=" * 70)

    # Load training data
    train_file = os.path.join(DATA_PATH, "train.csv")
    print(f"\n📂 Loading data from: {train_file}")
    train_data = pd.read_csv(train_file)

    # Split features and target
    X_train = train_data.drop(columns=["SalePrice"])
    y_train = train_data["SalePrice"]

    print(f"✅ Data loaded: {X_train.shape[0]} rows, {X_train.shape[1]} columns")

    # Create and train pipeline
    print("\n🔧 Creating and training pipeline...")
    pipeline = create_pipeline()
    pipeline.fit(X_train)
    print("✅ Pipeline trained successfully")

    # Transform training data
    print("\n🔄 Transforming training data...")
    X_train_processed = pipeline.transform(X_train)
    print(f"✅ Data transformed: shape = {X_train_processed.shape}")

    # Save pipeline
    os.makedirs(MODELS_PATH, exist_ok=True)
    preprocess_file = os.path.join(MODELS_PATH, "preprocess_pipeline.pkl")

    print(f"\n💾 Saving pipeline to: {preprocess_file}")
    joblib.dump(pipeline, preprocess_file)
    print("✅ Pipeline saved")

    # Verify it can be loaded
    print("\n🔍 Verifying pipeline load...")
    loaded_pipeline = joblib.load(preprocess_file)
    test_transform = loaded_pipeline.transform(X_train.iloc[[0]])
    print(f"✅ Pipeline loaded correctly (test shape: {test_transform.shape})")

    return X_train_processed, y_train


def retrain_model(X_train_processed, y_train):
    """
    Re-trains the model (if necessary).
    If you already have a trained model, you can use the same algorithm.
    """
    print("\n" + "=" * 70)
    print("MODEL TRAINING")
    print("=" * 70)

    # Use your real model here
    # Using a simple RandomForest as default
    from sklearn.ensemble import RandomForestRegressor

    print("\n🤖 Training RandomForest model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train_processed, y_train)
    print("✅ Model trained")

    # Save model
    model_file = os.path.join(MODELS_PATH, "best_model.pkl")
    print(f"\n💾 Saving model to: {model_file}")
    joblib.dump(model, model_file)
    print("✅ Model saved")

    # Verify load
    print("\n🔍 Verifying model load...")
    loaded_model = joblib.load(model_file)
    test_pred = loaded_model.predict(X_train_processed[:1])
    print(f"✅ Model loaded correctly (test prediction: ${test_pred[0]:,.2f})")

    return model


if __name__ == "__main__":
    try:
        # Re-train pipeline
        X_train_processed, y_train = retrain_pipeline()

        # Re-train model
        model = retrain_model(X_train_processed, y_train)

        print("\n" + "=" * 70)
        print("✅ RE-TRAINING COMPLETED")
        print("=" * 70)
        print("\n📝 Generated files:")
        print(f"   - {os.path.join(MODELS_PATH, 'preprocess_pipeline.pkl')}")
        print(f"   - {os.path.join(MODELS_PATH, 'best_model.pkl')}")
        print("\n🚀 You can now start the API with:")
        print("   uvicorn app.main:app --reload")

    except Exception as e:
        print("\n" + "=" * 70)
        print("❌ RE-TRAINING ERROR")
        print("=" * 70)
        print(f"\n{str(e)}")
        import traceback
        traceback.print_exc()

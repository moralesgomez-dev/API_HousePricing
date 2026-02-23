import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder


class ColumnSelector(BaseEstimator, TransformerMixin):
    def __init__(self, important_columns=None, exclude_columns=None):
        self.important_columns = important_columns or []
        self.exclude_columns = exclude_columns or []

    def fit(self, X, y=None):
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        X = X.copy()
        X = X.drop(columns=[c for c in self.exclude_columns if c in X.columns])
        return X


class NewFeatureHousePricing(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        X = X.copy()
        X["TotalArea"] = X["GrLivArea"] + X["TotalBsmtSF"] + X["GarageArea"]
        return X


class TypeImputer(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.num_cols = None
        self.cat_cols = None
        self.num_imp = None
        self.cat_imp = None
    
    def fit(self, X, y=None):
        self.num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
        self.cat_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
        
        # Create and initialize imputers
        if len(self.num_cols) > 0:
            self.num_imp = SimpleImputer(strategy="median")
            self.num_imp.fit(X[self.num_cols])
        
        if len(self.cat_cols) > 0:
            self.cat_imp = SimpleImputer(strategy="most_frequent")
            self.cat_imp.fit(X[self.cat_cols])
        
        # IMPORTANT: Mark as fitted
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        X = X.copy()
        if self.num_cols and len(self.num_cols) > 0:
            X[self.num_cols] = self.num_imp.transform(X[self.num_cols])
        if self.cat_cols and len(self.cat_cols) > 0:
            X[self.cat_cols] = self.cat_imp.transform(X[self.cat_cols])
        return X


class AutoScalerEncoder(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.num_cols = None
        self.cat_cols = None
        self.scaler = None
        self.encoder = None
    
    def fit(self, X, y=None):
        self.num_cols = X.select_dtypes(include=["int64", "float64"]).columns.tolist()
        self.cat_cols = X.select_dtypes(include=["object", "string"]).columns.tolist()
        
        # Create and fit scaler and encoder
        if len(self.num_cols) > 0:
            self.scaler = StandardScaler()
            self.scaler.fit(X[self.num_cols])
        
        if len(self.cat_cols) > 0:
            self.encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
            self.encoder.fit(X[self.cat_cols])
        
        # IMPORTANT: Mark as fitted
        self.n_features_in_ = X.shape[1]
        return self

    def transform(self, X):
        X = X.copy()
        
        num = pd.DataFrame(
            self.scaler.transform(X[self.num_cols]),
            columns=self.num_cols,
            index=X.index
        ) if self.num_cols and len(self.num_cols) > 0 else pd.DataFrame(index=X.index)
        
        cat = pd.DataFrame(
            self.encoder.transform(X[self.cat_cols]),
            columns=self.encoder.get_feature_names_out(self.cat_cols),
            index=X.index
        ) if self.cat_cols and len(self.cat_cols) > 0 else pd.DataFrame(index=X.index)
        
        return pd.concat([num, cat], axis=1)


def create_pipeline():
    """
    Creates and returns the preprocessing pipeline for house pricing.
    """
    important_cols = ["OverallQual", "GrLivArea", "GarageCars", "GarageArea", "TotalBsmtSF"]
    exclude_cols = ["LotFrontage", "Fence", "Alley", "PoolQC"]

    pipeline = Pipeline([
        ("selector", ColumnSelector(important_columns=important_cols, exclude_columns=exclude_cols)),
        ("new_features", NewFeatureHousePricing()),
        ("imputer", TypeImputer()),
        ("scaler_encoder", AutoScalerEncoder())
    ])

    return pipeline
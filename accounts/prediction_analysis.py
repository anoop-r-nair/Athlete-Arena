import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib
matplotlib.use('Agg')  # Set the backend to non-interactive Agg
import matplotlib.pyplot as plt

class PerformancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = [
            'Position', 'Club', 'Age', 'Matches', 
            'Goals', 'Assists', 'Pass Accuracy', 'Tackles'
        ]
        self.is_trained = False
        
    def preprocess_data(self, df):
        """Preprocess the input data"""
        processed_df = df.copy()
        
        # Handle Pass Accuracy
        if 'Pass Accuracy' in processed_df.columns:
            if not pd.api.types.is_numeric_dtype(processed_df['Pass Accuracy']):
                processed_df['Pass Accuracy'] = processed_df['Pass Accuracy'].apply(
                    lambda x: float(str(x).rstrip('%')) if isinstance(x, str) else float(x)
                )
        
        # Handle numeric columns
        numeric_columns = processed_df.select_dtypes(include=['int64', 'float64']).columns
        for col in numeric_columns:
            processed_df[col] = processed_df[col].fillna(processed_df[col].mean())
        
        # Handle categorical columns
        categorical_columns = ['Position', 'Club']
        for col in categorical_columns:
            if col in processed_df.columns:
                processed_df[col] = processed_df[col].fillna(processed_df[col].mode().iloc[0])
                if col not in self.label_encoders:
                    self.label_encoders[col] = LabelEncoder()
                    self.label_encoders[col].fit(processed_df[col].unique())
                try:
                    processed_df[col] = self.label_encoders[col].transform(processed_df[col])
                except ValueError:
                    # Handle new categories
                    new_categories = np.setdiff1d(processed_df[col].unique(), 
                                                self.label_encoders[col].classes_)
                    if len(new_categories) > 0:
                        # Retrain encoder with new categories
                        all_categories = np.concatenate([
                            self.label_encoders[col].classes_, new_categories
                        ])
                        self.label_encoders[col].fit(all_categories)
                        processed_df[col] = self.label_encoders[col].transform(processed_df[col])
        
        return processed_df
    
    def train(self, df):
        """Train the model with input data"""
        if len(df) < 2:
            raise ValueError("Training data must contain at least 2 samples")
            
        processed_df = self.preprocess_data(df)
        
        # Prepare features and target
        X = processed_df[self.feature_columns]
        y = processed_df['Performance_Rating']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            min_samples_split=2,
            min_samples_leaf=1
        )
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Calculate metrics
        y_pred = self.model.predict(X_scaled)
        metrics = {
            'mae': mean_absolute_error(y, y_pred),
            'mse': mean_squared_error(y, y_pred),
            'r2': r2_score(y, y_pred)
        }
        
        return metrics
    
    def predict(self, df):
        """Make predictions for new data"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        processed_df = self.preprocess_data(df)
        
        # Ensure all required features are present
        missing_cols = set(self.feature_columns) - set(processed_df.columns)
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        X = processed_df[self.feature_columns]
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        return predictions
    
    def plot_feature_importance(self):
        """Plot feature importance graph"""
        if not self.is_trained:
            raise ValueError("Model must be trained before plotting feature importance")
        
        feature_importance = pd.Series(
            self.model.feature_importances_,
            index=self.feature_columns
        ).sort_values(ascending=False)
        
        plt.figure(figsize=(10, 5))
        feature_importance.plot(kind='bar', color='teal')
        plt.title("Feature Importance")
        plt.tight_layout()
        return plt.gcf() 
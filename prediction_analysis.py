import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

class PerformancePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        
    def preprocess_data(self, df):
        # Create a copy to avoid modifying the original dataframe
        processed_df = df.copy()
        
        # Handle numeric columns
        numeric_columns = processed_df.select_dtypes(include=['int64', 'float64']).columns
        processed_df[numeric_columns] = processed_df[numeric_columns].fillna(processed_df[numeric_columns].mean())
        
        # Handle non-numeric columns
        non_numeric_columns = processed_df.select_dtypes(exclude=['int64', 'float64']).columns
        processed_df[non_numeric_columns] = processed_df[non_numeric_columns].fillna(processed_df[non_numeric_columns].mode().iloc[0])
        
        # Handle Pass Accuracy if present
        if 'Pass Accuracy' in processed_df.columns:
            processed_df['Pass Accuracy'] = processed_df['Pass Accuracy'].str.rstrip('%').astype(float)
            processed_df['Pass Accuracy'] = processed_df['Pass Accuracy'].fillna(processed_df['Pass Accuracy'].mean())
        
        # Encode categorical variables
        columns_to_encode = ['Position', 'Club']  # Add other categorical columns as needed
        for col in columns_to_encode:
            if col in processed_df.columns:
                le = LabelEncoder()
                processed_df[col] = le.fit_transform(processed_df[col])
                self.label_encoders[col] = le
        
        return processed_df
    
    def train(self, df):
        """Train the model with the provided dataset"""
        processed_df = self.preprocess_data(df)
        
        # Define features and target
        X = processed_df.drop(columns=['Performance_Rating', 'Player'])
        self.feature_columns = X.columns
        y = processed_df['Performance_Rating']
        
        # Split dataset
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = self.model.predict(X_test_scaled)
        
        # Calculate metrics
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'r2': r2_score(y_test, y_pred)
        }
        
        return metrics
    
    def predict(self, df):
        """Make predictions for new data"""
        processed_df = self.preprocess_data(df)
        X = processed_df.drop(columns=['Player'])
        X = X[self.feature_columns]  # Ensure columns match training data
        
        X_scaled = self.scaler.transform(X)
        predictions = self.model.predict(X_scaled)
        
        return predictions
    
    def plot_feature_importance(self):
        """Plot feature importance graph"""
        if self.model is None:
            raise ValueError("Model has not been trained yet")
            
        feature_importance = pd.Series(
            self.model.feature_importances_,
            index=self.feature_columns
        ).sort_values(ascending=False)
        
        plt.figure(figsize=(10, 5))
        feature_importance.plot(kind='bar', color='teal')
        plt.title("Feature Importance")
        plt.tight_layout()
        return plt.gcf() 
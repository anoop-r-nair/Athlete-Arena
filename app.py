import streamlit as st
import pandas as pd
from prediction_analysis import PerformancePredictor

def main():
    st.title("Football Player Performance Predictor")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
    
    if uploaded_file is not None:
        # Load data
        df = pd.read_csv(uploaded_file)
        st.write("Dataset Preview:", df.head())
        
        # Initialize and train model
        predictor = PerformancePredictor()
        
        with st.spinner('Training model...'):
            metrics = predictor.train(df)
        
        # Display metrics
        st.write("Model Performance Metrics:")
        st.write(f"Mean Absolute Error (MAE): {metrics['mae']:.4f}")
        st.write(f"Mean Squared Error (MSE): {metrics['mse']:.4f}")
        st.write(f"R² Score: {metrics['r2']:.4f}")
        
        # Make predictions
        predictions = predictor.predict(df)
        df['Predicted_Performance'] = predictions
        
        # Display predictions
        st.write("Player Performance Predictions:")
        st.write(df[['Player', 'Performance_Rating', 'Predicted_Performance']])
        
        # Plot feature importance
        st.write("Feature Importance:")
        fig = predictor.plot_feature_importance()
        st.pyplot(fig)

if __name__ == "__main__":
    main() 
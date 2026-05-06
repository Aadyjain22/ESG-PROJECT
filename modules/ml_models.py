"""
ML Models for ESG Data Analysis

This module contains machine learning functions for anomaly detection and forecasting.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Optional
import warnings

# Suppress sklearn warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')


def anomaly_detection(df: pd.DataFrame, col: str, contamination: float = 0.1) -> pd.DataFrame:
    """
    Detect anomalies in a numeric column using Isolation Forest algorithm.
    
    Args:
        df: DataFrame containing the data
        col: Column name to analyze for anomalies
        contamination: Expected proportion of anomalies (default: 0.1 = 10%)
        
    Returns:
        DataFrame with additional 'anomaly_flag' column indicating anomalies
    """
    if col not in df.columns:
        raise ValueError(f"Column '{col}' not found in DataFrame")
    
    # Create a copy to avoid modifying original
    result_df = df.copy()
    
    # Check if column has enough data
    if len(df) < 3:
        result_df['anomaly_flag'] = False
        return result_df
    
    # Get numeric values, handling missing values
    values = pd.to_numeric(df[col], errors='coerce').dropna()
    
    if len(values) < 3:
        result_df['anomaly_flag'] = False
        return result_df
    
    # Reshape for sklearn (needs 2D array)
    X = values.values.reshape(-1, 1)
    
    # Apply standardization for better anomaly detection
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Initialize and fit Isolation Forest
    iso_forest = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )
    
    # Fit the model and predict anomalies
    anomaly_predictions = iso_forest.fit_predict(X_scaled)
    
    # Create anomaly flags (1 = normal, -1 = anomaly)
    anomaly_flags = anomaly_predictions == -1
    
    # Map back to original DataFrame indices
    result_df['anomaly_flag'] = False
    result_df.loc[values.index, 'anomaly_flag'] = anomaly_flags
    
    return result_df


def simple_forecast(df: pd.DataFrame, date_col: str, value_col: str, 
                   forecast_days: int = 7, window_size: int = 5) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Generate simple rolling average forecast for the next N days.
    
    Args:
        df: DataFrame with time series data
        date_col: Name of the date column
        value_col: Name of the value column to forecast
        forecast_days: Number of days to forecast (default: 7)
        window_size: Rolling window size for average calculation (default: 5)
        
    Returns:
        Tuple of (original_df_with_forecast, forecast_df)
    """
    if date_col not in df.columns or value_col not in df.columns:
        raise ValueError(f"Columns '{date_col}' or '{value_col}' not found in DataFrame")
    
    result_df = df.copy()
    
    # Check if we have enough data for forecasting
    if len(df) < window_size:
        return result_df, pd.DataFrame()
    
    # Ensure date column is datetime
    if not pd.api.types.is_datetime64_any_dtype(df[date_col]):
        result_df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    # Sort by date
    result_df = result_df.sort_values(date_col).reset_index(drop=True)
    
    # Get numeric values
    values = pd.to_numeric(df[value_col], errors='coerce')
    
    if values.isna().all():
        return result_df, pd.DataFrame()
    
    # Calculate rolling average using the last window_size values
    recent_values = values.tail(window_size)
    if recent_values.isna().all():
        return result_df, pd.DataFrame()
    
    # Use mean of recent values (excluding NaN)
    forecast_value = recent_values.mean()
    
    # Generate forecast dates
    last_date = result_df[date_col].iloc[-1]
    forecast_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1),
        periods=forecast_days,
        freq='D'
    )
    
    # Create forecast DataFrame
    forecast_df = pd.DataFrame({
        date_col: forecast_dates,
        value_col: [forecast_value] * forecast_days,
        'is_forecast': [True] * forecast_days
    })
    
    # Add forecast flag to original data
    result_df['is_forecast'] = False
    
    # Combine original and forecast data for visualization
    combined_df = pd.concat([result_df, forecast_df], ignore_index=True)
    
    return combined_df, forecast_df


def detect_trend_anomalies(df: pd.DataFrame, col: str, threshold_std: float = 2.0) -> pd.DataFrame:
    """
    Detect trend anomalies using statistical methods (Z-score based).
    
    Args:
        df: DataFrame containing the data
        col: Column name to analyze
        threshold_std: Number of standard deviations for anomaly threshold
        
    Returns:
        DataFrame with 'trend_anomaly_flag' column
    """
    result_df = df.copy()
    
    if col not in df.columns or len(df) < 3:
        result_df['trend_anomaly_flag'] = False
        return result_df
    
    # Get numeric values
    values = pd.to_numeric(df[col], errors='coerce')
    
    if values.isna().all():
        result_df['trend_anomaly_flag'] = False
        return result_df
    
    # Calculate rolling statistics
    window_size = min(5, len(values) // 2) if len(values) > 4 else len(values)
    
    rolling_mean = values.rolling(window=window_size, min_periods=1).mean()
    rolling_std = values.rolling(window=window_size, min_periods=1).std()
    
    # Calculate Z-scores
    z_scores = np.abs((values - rolling_mean) / rolling_std)
    
    # Flag anomalies
    anomaly_flags = z_scores > threshold_std
    
    result_df['trend_anomaly_flag'] = anomaly_flags.fillna(False)
    
    return result_df


def get_anomaly_summary(df: pd.DataFrame, col: str) -> dict:
    """
    Get summary statistics about anomalies in a column.
    
    Args:
        df: DataFrame with anomaly flags
        col: Column name to summarize
        
    Returns:
        Dictionary with anomaly summary statistics
    """
    if 'anomaly_flag' not in df.columns or col not in df.columns:
        return {'total_points': 0, 'anomalies': 0, 'anomaly_rate': 0}
    
    total_points = len(df)
    anomalies = df['anomaly_flag'].sum()
    anomaly_rate = (anomalies / total_points * 100) if total_points > 0 else 0
    
    # Get anomaly values
    anomaly_values = df[df['anomaly_flag']][col].tolist() if anomalies > 0 else []
    
    return {
        'total_points': total_points,
        'anomalies': int(anomalies),
        'anomaly_rate': round(anomaly_rate, 2),
        'anomaly_values': anomaly_values,
        'mean_value': round(df[col].mean(), 2) if pd.api.types.is_numeric_dtype(df[col]) else None,
        'anomaly_mean': round(np.mean(anomaly_values), 2) if anomaly_values else None
    }


def create_ml_insights(df: pd.DataFrame, col: str) -> str:
    """
    Generate human-readable insights about anomalies and trends.
    
    Args:
        df: DataFrame with anomaly detection results
        col: Column name being analyzed
        
    Returns:
        String with ML insights
    """
    if 'anomaly_flag' not in df.columns:
        return f"No anomaly analysis available for {col}."
    
    summary = get_anomaly_summary(df, col)
    
    if summary['total_points'] == 0:
        return f"Insufficient data for {col} analysis."
    
    insights = []
    
    # Anomaly insights
    if summary['anomalies'] > 0:
        insights.append(f"🔍 **Anomaly Detection**: {summary['anomalies']} anomalies detected ({summary['anomaly_rate']}% of data points)")
        
        if summary['anomaly_mean'] is not None and summary['mean_value'] is not None:
            if summary['anomaly_mean'] > summary['mean_value']:
                insights.append(f"📈 Anomalies tend to be higher than average ({summary['anomaly_mean']} vs {summary['mean_value']})")
            else:
                insights.append(f"📉 Anomalies tend to be lower than average ({summary['anomaly_mean']} vs {summary['mean_value']})")
    else:
        insights.append("✅ **No significant anomalies detected** - data appears consistent")
    
    # Trend insights (if we have enough data)
    if len(df) >= 7:
        recent_values = df[col].tail(7)
        if pd.api.types.is_numeric_dtype(recent_values):
            trend = "increasing" if recent_values.iloc[-1] > recent_values.iloc[0] else "decreasing"
            insights.append(f"📊 **Recent trend**: {trend} over last 7 periods")
    
    return "\n\n".join(insights) if insights else "No insights available."

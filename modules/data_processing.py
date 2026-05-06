"""
ESG Data Processing Module

This module contains functions for validating ESG data and computing ESG scores.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Any


def validate_env(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate environmental data DataFrame.
    
    Args:
        df: DataFrame containing environmental data
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = [
        'carbon_emissions', 'energy_consumption', 'waste_generated', 
        'water_usage', 'renewable_energy_percentage'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for non-numeric values in numeric columns
    for col in required_columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return False, f"Column '{col}' must contain numeric values"
    
    return True, ""


def validate_social(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate social data DataFrame.
    
    Args:
        df: DataFrame containing social data
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = [
        'employee_satisfaction', 'diversity_score', 'community_investment',
        'safety_incidents', 'training_hours_per_employee'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for non-numeric values in numeric columns
    for col in required_columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return False, f"Column '{col}' must contain numeric values"
    
    return True, ""


def validate_gov(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate governance data DataFrame.
    
    Args:
        df: DataFrame containing governance data
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_columns = [
        'board_independence', 'executive_compensation_ratio', 'audit_quality',
        'transparency_score', 'stakeholder_engagement'
    ]
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing required columns: {', '.join(missing_columns)}"
    
    # Check for non-numeric values in numeric columns
    for col in required_columns:
        if not pd.api.types.is_numeric_dtype(df[col]):
            return False, f"Column '{col}' must contain numeric values"
    
    return True, ""


def normalize_data(df: pd.DataFrame, invert_columns: list = None) -> pd.DataFrame:
    """
    Normalize data to 0-100 scale for scoring.
    
    Args:
        df: DataFrame to normalize
        invert_columns: List of columns to invert (lower is better)
        
    Returns:
        Normalized DataFrame
    """
    if invert_columns is None:
        invert_columns = []
    
    df_normalized = df.copy()
    
    for col in df.columns:
        if col in df.select_dtypes(include=[np.number]).columns:
            # Handle missing values
            df_normalized[col] = df_normalized[col].fillna(df_normalized[col].median())
            
            # Normalize to 0-100 scale
            min_val = df_normalized[col].min()
            max_val = df_normalized[col].max()
            
            if max_val != min_val:
                if col in invert_columns:
                    # Invert: higher values become lower scores
                    df_normalized[col] = 100 - ((df_normalized[col] - min_val) / (max_val - min_val) * 100)
                else:
                    # Normal: higher values become higher scores
                    df_normalized[col] = (df_normalized[col] - min_val) / (max_val - min_val) * 100
            else:
                df_normalized[col] = 50  # Neutral score if all values are the same
    
    return df_normalized


def compute_esg_score(env_df: pd.DataFrame, soc_df: pd.DataFrame, 
                     gov_df: pd.DataFrame, weights: Dict[str, int]) -> Dict[str, Any]:
    """
    Compute ESG scores based on provided data and weights using detailed normalization.
    
    Args:
        env_df: Environmental data DataFrame
        soc_df: Social data DataFrame
        gov_df: Governance data DataFrame
        weights: Dictionary with E, S, G weight percentages
        
    Returns:
        Dictionary containing E, S, G sub-scores, overall ESG score, and detailed breakdown
    """
    # Define columns and their normalization type
    env_lower_better = ['carbon_emissions', 'energy_consumption', 'waste_generated', 'water_usage']
    env_higher_better = ['renewable_energy_percentage']
    
    soc_lower_better = ['safety_incidents']
    soc_higher_better = ['employee_satisfaction', 'diversity_score', 'community_investment', 'training_hours_per_employee']
    
    gov_lower_better = ['executive_compensation_ratio']
    gov_higher_better = ['board_independence', 'audit_quality', 'transparency_score', 'stakeholder_engagement']
    
    # Normalize Environmental KPIs
    env_scores = {}
    for col in env_df.columns:
        if col in env_lower_better:
            # Lower is better: score = (max - value) / (max - min) * 100
            max_val = env_df[col].max()
            min_val = env_df[col].min()
            if max_val != min_val:
                env_scores[col] = ((max_val - env_df[col].mean()) / (max_val - min_val) * 100)
            else:
                env_scores[col] = 50
        elif col in env_higher_better:
            # Higher is better: score = (value - min) / (max - min) * 100
            max_val = env_df[col].max()
            min_val = env_df[col].min()
            if max_val != min_val:
                env_scores[col] = ((env_df[col].mean() - min_val) / (max_val - min_val) * 100)
            else:
                env_scores[col] = 50
    
    # Normalize Social KPIs
    soc_scores = {}
    for col in soc_df.columns:
        if col in soc_lower_better:
            max_val = soc_df[col].max()
            min_val = soc_df[col].min()
            if max_val != min_val:
                soc_scores[col] = ((max_val - soc_df[col].mean()) / (max_val - min_val) * 100)
            else:
                soc_scores[col] = 50
        elif col in soc_higher_better:
            max_val = soc_df[col].max()
            min_val = soc_df[col].min()
            if max_val != min_val:
                soc_scores[col] = ((soc_df[col].mean() - min_val) / (max_val - min_val) * 100)
            else:
                soc_scores[col] = 50
    
    # Normalize Governance KPIs
    gov_scores = {}
    for col in gov_df.columns:
        if col in gov_lower_better:
            max_val = gov_df[col].max()
            min_val = gov_df[col].min()
            if max_val != min_val:
                gov_scores[col] = ((max_val - gov_df[col].mean()) / (max_val - min_val) * 100)
            else:
                gov_scores[col] = 50
        elif col in gov_higher_better:
            max_val = gov_df[col].max()
            min_val = gov_df[col].min()
            if max_val != min_val:
                gov_scores[col] = ((gov_df[col].mean() - min_val) / (max_val - min_val) * 100)
            else:
                gov_scores[col] = 50
    
    # Calculate sub-scores (average of normalized KPI scores)
    e_score = sum(env_scores.values()) / len(env_scores) if env_scores else 0
    s_score = sum(soc_scores.values()) / len(soc_scores) if soc_scores else 0
    g_score = sum(gov_scores.values()) / len(gov_scores) if gov_scores else 0
    
    # Calculate weighted overall ESG score
    total_weight = weights['E'] + weights['S'] + weights['G']
    if total_weight > 0:
        e_contribution = e_score * weights['E'] / total_weight
        s_contribution = s_score * weights['S'] / total_weight
        g_contribution = g_score * weights['G'] / total_weight
        overall_score = e_contribution + s_contribution + g_contribution
    else:
        overall_score = (e_score + s_score + g_score) / 3
    
    return {
        'E': round(e_score, 2),
        'S': round(s_score, 2),
        'G': round(g_score, 2),
        'ESG': round(overall_score, 2),
        'weights': weights,
        'detailed_scores': {
            'environmental': env_scores,
            'social': soc_scores,
            'governance': gov_scores
        },
        'contributions': {
            'E_contribution': round(e_contribution, 2),
            'S_contribution': round(s_contribution, 2),
            'G_contribution': round(g_contribution, 2)
        }
    }


def get_esg_grade(score: float) -> str:
    """
    Convert ESG score to letter grade.
    
    Args:
        score: ESG score (0-100)
        
    Returns:
        Letter grade (A+, A, A-, B+, B, B-, C+, C, C-, D, F)
    """
    if score >= 95:
        return "A+"
    elif score >= 90:
        return "A"
    elif score >= 85:
        return "A-"
    elif score >= 80:
        return "B+"
    elif score >= 75:
        return "B"
    elif score >= 70:
        return "B-"
    elif score >= 65:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 55:
        return "C-"
    elif score >= 50:
        return "D"
    else:
        return "F"


def analyze_trends(env_df: pd.DataFrame, soc_df: pd.DataFrame, gov_df: pd.DataFrame) -> list:
    """
    Analyze trends and identify KPIs that have worsened by more than 10%.
    
    Args:
        env_df: Environmental data DataFrame
        soc_df: Social data DataFrame  
        gov_df: Governance data DataFrame
        
    Returns:
        List of trend alerts
    """
    alerts = []
    
    # Analyze Environmental trends
    for col in env_df.columns:
        if len(env_df) >= 2:
            # For lower-is-better metrics, an increase is bad
            if col in ['carbon_emissions', 'energy_consumption', 'waste_generated', 'water_usage']:
                latest = env_df[col].iloc[-1]
                previous = env_df[col].iloc[-2]
                if previous != 0:
                    change_pct = ((latest - previous) / previous) * 100
                    if change_pct > 10:
                        alerts.append(f"⚠️ {col.replace('_', ' ').title()} increased by {change_pct:.1f}%")
            # For higher-is-better metrics, a decrease is bad
            elif col == 'renewable_energy_percentage':
                latest = env_df[col].iloc[-1]
                previous = env_df[col].iloc[-2]
                if previous != 0:
                    change_pct = ((latest - previous) / previous) * 100
                    if change_pct < -10:
                        alerts.append(f"⚠️ {col.replace('_', ' ').title()} decreased by {abs(change_pct):.1f}%")
    
    # Analyze Social trends
    for col in soc_df.columns:
        if len(soc_df) >= 2:
            if col == 'safety_incidents':
                latest = soc_df[col].iloc[-1]
                previous = soc_df[col].iloc[-2]
                if previous != 0:
                    change_pct = ((latest - previous) / previous) * 100
                    if change_pct > 10:
                        alerts.append(f"⚠️ {col.replace('_', ' ').title()} increased by {change_pct:.1f}%")
            else:  # Higher is better
                latest = soc_df[col].iloc[-1]
                previous = soc_df[col].iloc[-2]
                if previous != 0:
                    change_pct = ((latest - previous) / previous) * 100
                    if change_pct < -10:
                        alerts.append(f"⚠️ {col.replace('_', ' ').title()} decreased by {abs(change_pct):.1f}%")
    
    # Analyze Governance trends
    for col in gov_df.columns:
        if len(gov_df) >= 2:
            if col == 'executive_compensation_ratio':
                latest = gov_df[col].iloc[-1]
                previous = gov_df[col].iloc[-2]
                if previous != 0:
                    change_pct = ((latest - previous) / previous) * 100
                    if change_pct > 10:
                        alerts.append(f"⚠️ {col.replace('_', ' ').title()} increased by {change_pct:.1f}%")
            else:  # Higher is better
                latest = gov_df[col].iloc[-1]
                previous = gov_df[col].iloc[-2]
                if previous != 0:
                    change_pct = ((latest - previous) / previous) * 100
                    if change_pct < -10:
                        alerts.append(f"⚠️ {col.replace('_', ' ').title()} decreased by {abs(change_pct):.1f}%")
    
    return alerts


def get_card_color(score: float) -> str:
    """
    Get color for KPI cards based on score.
    
    Args:
        score: ESG score (0-100)
        
    Returns:
        Color string for Streamlit styling
    """
    if score >= 80:
        return "green"
    elif score >= 60:
        return "orange"
    else:
        return "red"

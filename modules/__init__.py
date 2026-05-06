"""
ESG Analysis Modules

This package contains modules for ESG data processing and reporting.
"""

from .data_processing import (
    validate_env, validate_social, validate_gov,
    compute_esg_score, get_esg_grade, analyze_trends, get_card_color
)

from .reports import (
    generate_excel_report, generate_pdf_report, generate_ai_insights
)

from .ml_models import (
    anomaly_detection, simple_forecast, detect_trend_anomalies,
    get_anomaly_summary, create_ml_insights
)

__all__ = [
    # Data processing functions
    'validate_env', 'validate_social', 'validate_gov',
    'compute_esg_score', 'get_esg_grade', 'analyze_trends', 'get_card_color',
    # Report generation functions
    'generate_excel_report', 'generate_pdf_report', 'generate_ai_insights',
    # ML models functions
    'anomaly_detection', 'simple_forecast', 'detect_trend_anomalies',
    'get_anomaly_summary', 'create_ml_insights'
]

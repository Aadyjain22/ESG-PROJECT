"""
AI-Driven ESG Sustainability Platform

A Streamlit application for analyzing Environmental, Social, and Governance (ESG) data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os
from pathlib import Path
import sys
from datetime import datetime

# Add modules directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from modules.data_processing import (
    validate_env, validate_social, validate_gov, 
    compute_esg_score, get_esg_grade, analyze_trends, get_card_color
)
from modules.reports import generate_excel_report, generate_pdf_report, generate_ai_insights, ESGReporter
from modules.ml_models import (
    anomaly_detection, simple_forecast, get_anomaly_summary, create_ml_insights
)


def load_config():
    """Load ESG weights and thresholds configuration from config.json"""
    default_config = {
        "weights": {"E": 45, "S": 30, "G": 25},
        "thresholds": {
            "co2_tonnes": 500,
            "energy_kwh": 200000,
            "accidents_count": 5,
            "waste_generated": 1000,
            "water_usage": 50000,
            "employee_satisfaction": 70,
            "diversity_score": 60,
            "safety_incidents": 10,
            "board_independence": 80,
            "transparency_score": 75
        }
    }
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            
            # Handle legacy config format
            if "weights" not in config:
                config = {
                    "weights": config,
                    "thresholds": default_config["thresholds"]
                }
            
            # Ensure all required keys exist
            if "thresholds" not in config:
                config["thresholds"] = default_config["thresholds"]
                
            return config
    except FileNotFoundError:
        return default_config
    except json.JSONDecodeError:
        return default_config


def save_config(config):
    """Save ESG weights and thresholds configuration to config.json"""
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)


def check_thresholds(df, df_type, thresholds):
    """Check if any values exceed configured thresholds"""
    alerts = []
    
    if df_type == 'environmental':
        # Check environmental thresholds
        if 'carbon_emissions' in df.columns and 'co2_tonnes' in thresholds:
            max_co2 = df['carbon_emissions'].max()
            if max_co2 > thresholds['co2_tonnes']:
                alerts.append(f"🚨 **CO2 emissions exceeded threshold!** Max: {max_co2:.1f} tonnes (limit: {thresholds['co2_tonnes']})")
        
        if 'energy_consumption' in df.columns and 'energy_kwh' in thresholds:
            max_energy = df['energy_consumption'].max()
            if max_energy > thresholds['energy_kwh']:
                alerts.append(f"⚡ **Energy consumption exceeded threshold!** Max: {max_energy:.0f} kWh (limit: {thresholds['energy_kwh']:,})")
        
        if 'waste_generated' in df.columns and 'waste_generated' in thresholds:
            max_waste = df['waste_generated'].max()
            if max_waste > thresholds['waste_generated']:
                alerts.append(f"🗑️ **Waste generation exceeded threshold!** Max: {max_waste:.1f} units (limit: {thresholds['waste_generated']})")
        
        if 'water_usage' in df.columns and 'water_usage' in thresholds:
            max_water = df['water_usage'].max()
            if max_water > thresholds['water_usage']:
                alerts.append(f"💧 **Water usage exceeded threshold!** Max: {max_water:.0f} units (limit: {thresholds['water_usage']:,})")
    
    elif df_type == 'social':
        # Check social thresholds
        if 'employee_satisfaction' in df.columns and 'employee_satisfaction' in thresholds:
            min_satisfaction = df['employee_satisfaction'].min()
            if min_satisfaction < thresholds['employee_satisfaction']:
                alerts.append(f"😞 **Employee satisfaction below threshold!** Min: {min_satisfaction:.1f}% (minimum: {thresholds['employee_satisfaction']}%)")
        
        if 'diversity_score' in df.columns and 'diversity_score' in thresholds:
            min_diversity = df['diversity_score'].min()
            if min_diversity < thresholds['diversity_score']:
                alerts.append(f"👥 **Diversity score below threshold!** Min: {min_diversity:.1f}% (minimum: {thresholds['diversity_score']}%)")
        
        if 'safety_incidents' in df.columns and 'safety_incidents' in thresholds:
            max_incidents = df['safety_incidents'].max()
            if max_incidents > thresholds['safety_incidents']:
                alerts.append(f"⚠️ **Safety incidents exceeded threshold!** Max: {max_incidents:.0f} incidents (limit: {thresholds['safety_incidents']})")
    
    elif df_type == 'governance':
        # Check governance thresholds
        if 'board_independence' in df.columns and 'board_independence' in thresholds:
            min_independence = df['board_independence'].min()
            if min_independence < thresholds['board_independence']:
                alerts.append(f"🏛️ **Board independence below threshold!** Min: {min_independence:.1f}% (minimum: {thresholds['board_independence']}%)")
        
        if 'transparency_score' in df.columns and 'transparency_score' in thresholds:
            min_transparency = df['transparency_score'].min()
            if min_transparency < thresholds['transparency_score']:
                alerts.append(f"📊 **Transparency score below threshold!** Min: {min_transparency:.1f}% (minimum: {thresholds['transparency_score']}%)")
    
    return alerts


def validate_weights(weights):
    """Validate that weights sum to 100"""
    total = sum(weights.values())
    return abs(total - 100) < 0.01, total


def save_uploaded_file(uploaded_file, folder_name):
    """Save uploaded file to the specified folder"""
    folder_path = Path(folder_name)
    folder_path.mkdir(exist_ok=True)
    
    file_path = folder_path / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def create_esg_chart(scores):
    """Create a radar chart for ESG scores"""
    categories = ['Environmental', 'Social', 'Governance', 'Overall']
    values = [scores['E'], scores['S'], scores['G'], scores['ESG']]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='ESG Scores',
        line_color='rgb(32, 201, 151)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="ESG Performance Radar Chart",
        height=500
    )
    
    return fig


def create_gauge_chart(value, title, subtitle):
    """Create a gauge chart for performance metrics"""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': title},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 40], 'color': "lightgray"},
                {'range': [40, 70], 'color': "yellow"},
                {'range': [70, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        title_x=0.5,
        annotations=[
            {
                'text': subtitle,
                'x': 0.5,
                'y': -0.1,
                'xref': 'paper',
                'yref': 'paper',
                'showarrow': False,
                'font': {'size': 12, 'color': 'gray'}
            }
        ]
    )
    
    return fig


def create_trend_chart(df, title):
    """Create trend analysis chart for time series data"""
    if df is None or len(df) == 0:
        return None
    
    fig = go.Figure()
    
    # Create date range for x-axis
    periods = list(range(1, len(df) + 1))
    
    # Plot each column as a line
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            fig.add_trace(go.Scatter(
                x=periods,
                y=df[column],
                mode='lines+markers',
                name=column.replace('_', ' ').title(),
                line=dict(width=3),
                marker=dict(size=6)
            ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time Period",
        yaxis_title="Value",
        hovermode='x unified',
        title_x=0.5,
        height=400
    )
    
    return fig


def create_category_comparison_chart(scores):
    """Create bar chart comparing ESG categories"""
    categories = ['Environmental', 'Social', 'Governance']
    values = [scores['E'], scores['S'], scores['G']]
    
    # Define colors based on performance
    colors = []
    for value in values:
        if value >= 70:
            colors.append('#28a745')  # Green
        elif value >= 40:
            colors.append('#ffc107')  # Yellow
        else:
            colors.append('#dc3545')  # Red
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories,
            y=values,
            marker_color=colors,
            text=[f'{v:.1f}' for v in values],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="ESG Category Performance Comparison",
        xaxis_title="ESG Categories",
        yaxis_title="Score",
        yaxis=dict(range=[0, 100]),
        title_x=0.5,
        height=400
    )
    
    return fig


def create_weight_contribution_chart(scores):
    """Create pie chart showing weight contributions"""
    labels = ['Environmental', 'Social', 'Governance']
    values = [scores['weights']['E'], scores['weights']['S'], scores['weights']['G']]
    colors = ['#28a745', '#007bff', '#6f42c1']
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.3,
        marker_colors=colors,
        textinfo='label+percent',
        textposition='outside'
    )])
    
    fig.update_layout(
        title="ESG Weight Distribution",
        title_x=0.5,
        height=400
    )
    
    return fig


def create_kpi_breakdown_chart(env_df, social_df, gov_df):
    """Create detailed KPI breakdown chart"""
    if env_df is None or social_df is None or gov_df is None:
        return None
    
    # Calculate average values for each KPI
    env_metrics = {}
    social_metrics = {}
    gov_metrics = {}
    
    # Environmental metrics
    for col in env_df.columns:
        if pd.api.types.is_numeric_dtype(env_df[col]):
            env_metrics[col.replace('_', ' ').title()] = env_df[col].mean()
    
    # Social metrics
    for col in social_df.columns:
        if pd.api.types.is_numeric_dtype(social_df[col]):
            social_metrics[col.replace('_', ' ').title()] = social_df[col].mean()
    
    # Governance metrics
    for col in gov_df.columns:
        if pd.api.types.is_numeric_dtype(gov_df[col]):
            gov_metrics[col.replace('_', ' ').title()] = gov_df[col].mean()
    
    # Create subplot
    from plotly.subplots import make_subplots
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Environmental KPIs', 'Social KPIs', 'Governance KPIs'),
        specs=[[{'type': 'bar'}, {'type': 'bar'}, {'type': 'bar'}]]
    )
    
    # Add Environmental bars
    if env_metrics:
        fig.add_trace(
            go.Bar(x=list(env_metrics.keys()), y=list(env_metrics.values()), 
                   name='Environmental', marker_color='#28a745'),
            row=1, col=1
        )
    
    # Add Social bars
    if social_metrics:
        fig.add_trace(
            go.Bar(x=list(social_metrics.keys()), y=list(social_metrics.values()), 
                   name='Social', marker_color='#007bff'),
            row=1, col=2
        )
    
    # Add Governance bars
    if gov_metrics:
        fig.add_trace(
            go.Bar(x=list(gov_metrics.keys()), y=list(gov_metrics.values()), 
                   name='Governance', marker_color='#6f42c1'),
            row=1, col=3
        )
    
    fig.update_layout(
        title="Detailed KPI Breakdown",
        showlegend=False,
        title_x=0.5,
        height=500
    )
    
    return fig


def create_esg_heatmap(env_df, social_df, gov_df):
    """Create ESG performance heatmap"""
    if env_df is None or social_df is None or gov_df is None:
        return None
    
    # Prepare data for heatmap
    all_data = []
    categories = []
    metrics = []
    
    # Environmental data
    for col in env_df.columns:
        if pd.api.types.is_numeric_dtype(env_df[col]):
            avg_value = env_df[col].mean()
            all_data.append(avg_value)
            categories.append('Environmental')
            metrics.append(col.replace('_', ' ').title())
    
    # Social data
    for col in social_df.columns:
        if pd.api.types.is_numeric_dtype(social_df[col]):
            avg_value = social_df[col].mean()
            all_data.append(avg_value)
            categories.append('Social')
            metrics.append(col.replace('_', ' ').title())
    
    # Governance data
    for col in gov_df.columns:
        if pd.api.types.is_numeric_dtype(gov_df[col]):
            avg_value = gov_df[col].mean()
            all_data.append(avg_value)
            categories.append('Governance')
            metrics.append(col.replace('_', ' ').title())
    
    if not all_data:
        return None
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=[all_data],
        x=metrics,
        y=['Performance'],
        colorscale='RdYlGn',
        showscale=True,
        hoverongaps=False,
        text=[[f'{val:.1f}' for val in all_data]],
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title="ESG Performance Heatmap",
        xaxis_title="ESG Metrics",
        yaxis_title="Categories",
        title_x=0.5,
        height=300
    )
    
    return fig


def create_kpi_indicators(df, category):
    """Create KPI indicators for a specific category"""
    if df is None or len(df) == 0:
        return ["No data available"]
    
    indicators = []
    
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            current_value = df[col].iloc[-1] if len(df) > 0 else 0
            previous_value = df[col].iloc[-2] if len(df) > 1 else current_value
            
            # Calculate change
            if previous_value != 0:
                change_pct = ((current_value - previous_value) / previous_value) * 100
                if change_pct > 0:
                    change_icon = "📈"
                    change_color = "🟢"
                elif change_pct < 0:
                    change_icon = "📉"
                    change_color = "🔴"
                else:
                    change_icon = "➡️"
                    change_color = "🟡"
                
                indicators.append(f"{change_color} {col.replace('_', ' ').title()}: {current_value:.1f} ({change_icon} {change_pct:+.1f}%)")
            else:
                indicators.append(f"📊 {col.replace('_', ' ').title()}: {current_value:.1f}")
    
    return indicators if indicators else ["No indicators available"]


def create_co2_chart(env_df):
    """Create line chart for CO2 emissions over time with anomaly detection and forecasting"""
    if 'carbon_emissions' not in env_df.columns or len(env_df) < 2:
        return None
    
    # Detect anomalies
    env_with_anomalies = anomaly_detection(env_df, 'carbon_emissions')
    
    # Generate forecast
    try:
        # Create a simple date column for forecasting if it doesn't exist
        if 'date' not in env_with_anomalies.columns:
            env_with_anomalies['date'] = pd.date_range(start='2023-01-01', periods=len(env_with_anomalies), freq='D')
        
        env_with_forecast, forecast_df = simple_forecast(env_with_anomalies, 'date', 'carbon_emissions')
        
        # Create the main chart
        fig = go.Figure()
        
        # Add main line
        fig.add_trace(go.Scatter(
            x=env_with_anomalies.index,
            y=env_with_anomalies['carbon_emissions'],
            mode='lines+markers',
            name='CO2 Emissions',
            line=dict(color='blue', width=2),
            marker=dict(size=6)
        ))
        
        # Add anomaly points in red
        anomaly_data = env_with_anomalies[env_with_anomalies['anomaly_flag']]
        if not anomaly_data.empty:
            fig.add_trace(go.Scatter(
                x=anomaly_data.index,
                y=anomaly_data['carbon_emissions'],
                mode='markers',
                name='Anomalies',
                marker=dict(color='red', size=10, symbol='x'),
                hovertemplate='<b>Anomaly Detected</b><br>' +
                             'Period: %{x}<br>' +
                             'CO2 Emissions: %{y:.2f} tons<extra></extra>'
            ))
        
        # Add forecast line
        if not forecast_df.empty:
            forecast_start_idx = len(env_with_anomalies)
            fig.add_trace(go.Scatter(
                x=list(range(forecast_start_idx, forecast_start_idx + len(forecast_df))),
                y=forecast_df['carbon_emissions'],
                mode='lines+markers',
                name='Forecast (7 days)',
                line=dict(color='green', width=2, dash='dash'),
                marker=dict(size=6, symbol='triangle-up')
            ))
        
        fig.update_layout(
            title='CO2 Emissions Trend with Anomaly Detection & Forecasting',
            xaxis_title='Time Period',
            yaxis_title='CO2 Emissions (tons)',
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        return fig
        
    except Exception as e:
        # Fallback to simple chart if ML features fail
        fig = px.line(
            env_with_anomalies, 
            y='carbon_emissions',
            title='CO2 Emissions Trend',
            labels={'carbon_emissions': 'CO2 Emissions (tons)', 'index': 'Time Period'}
        )
        
        # Add anomaly points if available
        anomaly_data = env_with_anomalies[env_with_anomalies['anomaly_flag']]
        if not anomaly_data.empty:
            fig.add_scatter(
                x=anomaly_data.index,
                y=anomaly_data['carbon_emissions'],
                mode='markers',
                name='Anomalies',
                marker=dict(color='red', size=10, symbol='x')
            )
        
        fig.update_layout(height=400)
        return fig


def create_energy_chart(env_df):
    """Create line chart for energy consumption over time"""
    if 'energy_consumption' not in env_df.columns or len(env_df) < 2:
        return None
    
    fig = px.line(
        env_df, 
        y='energy_consumption',
        title='Energy Consumption Trend',
        labels={'energy_consumption': 'Energy Consumption (kWh)', 'index': 'Time Period'}
    )
    fig.update_layout(height=300)
    return fig


def create_satisfaction_chart(soc_df):
    """Create bar chart for employee satisfaction"""
    if 'employee_satisfaction' not in soc_df.columns:
        return None
    
    fig = px.bar(
        soc_df, 
        y='employee_satisfaction',
        title='Employee Satisfaction by Period',
        labels={'employee_satisfaction': 'Satisfaction Score', 'index': 'Time Period'}
    )
    fig.update_layout(height=300)
    return fig


def create_compliance_chart(gov_df):
    """Create bar chart for compliance incidents"""
    if 'executive_compensation_ratio' not in gov_df.columns:
        return None
    
    # Use executive compensation ratio as a proxy for compliance issues
    fig = px.bar(
        gov_df, 
        y='executive_compensation_ratio',
        title='Executive Compensation Ratio (Lower is Better)',
        labels={'executive_compensation_ratio': 'Compensation Ratio', 'index': 'Time Period'}
    )
    fig.update_layout(height=300)
    return fig


def create_kpi_card(title, score, color):
    """Create a styled KPI card"""
    if color == "green":
        color_hex = "#28a745"
    elif color == "orange":
        color_hex = "#fd7e14"
    else:
        color_hex = "#dc3545"
    
    return f"""
    <div style="
        background-color: {color_hex};
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    ">
        <h3 style="margin: 0; font-size: 0.9rem;">{title}</h3>
        <h2 style="margin: 0; font-size: 2rem; font-weight: bold;">{score}/100</h2>
    </div>
    """


def get_status_badge(score):
    """Get status badge color based on score"""
    if score >= 70:
        return "🟢", "success"
    elif score >= 40:
        return "🟡", "warning"
    else:
        return "🔴", "error"


def get_status_delta(score):
    """Get delta direction for metrics"""
    if score >= 70:
        return "normal"
    elif score >= 40:
        return "off"
    else:
        return "inverse"


def display_esg_metrics(scores):
    """Display ESG scores using Streamlit metrics with status badges"""
    col1, col2, col3, col4 = st.columns(4)
    
    # Environmental
    with col1:
        e_badge, e_status = get_status_badge(scores['E'])
        st.metric(
            label=f"🌍 Environmental {e_badge}",
            value=f"{scores['E']:.1f}",
            delta=None
        )
        st.caption(f"Weight: {scores['weights']['E']}%")
    
    # Social
    with col2:
        s_badge, s_status = get_status_badge(scores['S'])
        st.metric(
            label=f"👥 Social {s_badge}",
            value=f"{scores['S']:.1f}",
            delta=None
        )
        st.caption(f"Weight: {scores['weights']['S']}%")
    
    # Governance
    with col3:
        g_badge, g_status = get_status_badge(scores['G'])
        st.metric(
            label=f"⚖️ Governance {g_badge}",
            value=f"{scores['G']:.1f}",
            delta=None
        )
        st.caption(f"Weight: {scores['weights']['G']}%")
    
    # Overall ESG
    with col4:
        esg_badge, esg_status = get_status_badge(scores['ESG'])
        grade = get_esg_grade(scores['ESG'])
        st.metric(
            label=f"🎯 Overall ESG {esg_badge}",
            value=f"{scores['ESG']:.1f}",
            delta=f"Grade: {grade}",
            delta_color=get_status_delta(scores['ESG'])
        )
        st.caption("Weighted Average")


def main():
    # Page configuration
    st.set_page_config(
        page_title="AI-Driven ESG Sustainability Platform",
        page_icon="🌱",
        layout="wide"
    )
    
    # Main title
    st.title("🌱 AI-Driven ESG Sustainability Platform")
    st.markdown("---")
    
    # Load configuration
    config = load_config()
    
    # Sidebar
    st.sidebar.header("📊 Analysis Controls")
    
    # File upload section in sidebar
    st.sidebar.markdown("### 📁 Data Upload")
    
    env_file = st.sidebar.file_uploader(
        "🌍 Environmental Data",
        type=['csv'],
        key='env_upload'
    )
    
    if env_file is not None:
        env_df = pd.read_csv(env_file)
        is_valid, error_msg = validate_env(env_df)
        
        if is_valid:
            st.sidebar.success("✅ Environmental data is valid!")
            save_uploaded_file(env_file, "data")
            st.session_state.env_df = env_df
        else:
            st.sidebar.error(f"❌ {error_msg}")
    
    social_file = st.sidebar.file_uploader(
        "👥 Social Data",
        type=['csv'],
        key='social_upload'
    )
    
    if social_file is not None:
        social_df = pd.read_csv(social_file)
        is_valid, error_msg = validate_social(social_df)
        
        if is_valid:
            st.sidebar.success("✅ Social data is valid!")
            save_uploaded_file(social_file, "data")
            st.session_state.social_df = social_df
        else:
            st.sidebar.error(f"❌ {error_msg}")
    
    gov_file = st.sidebar.file_uploader(
        "⚖️ Governance Data",
        type=['csv'],
        key='gov_upload'
    )
    
    if gov_file is not None:
        gov_df = pd.read_csv(gov_file)
        is_valid, error_msg = validate_gov(gov_df)
        
        if is_valid:
            st.sidebar.success("✅ Governance data is valid!")
            save_uploaded_file(gov_file, "data")
            st.session_state.gov_df = gov_df
        else:
            st.sidebar.error(f"❌ {error_msg}")
    
    st.sidebar.markdown("---")
    
    # Run Analysis button
    if st.sidebar.button("🚀 Run Analysis", type="primary", use_container_width=True):
        if all(key in st.session_state for key in ['env_df', 'social_df', 'gov_df']):
            with st.spinner("Computing ESG scores..."):
                # Compute ESG scores
                scores = compute_esg_score(
                    st.session_state.env_df,
                    st.session_state.social_df,
                    st.session_state.gov_df,
                    config['weights']
                )
                
                # Analyze trends
                trend_alerts = analyze_trends(
                    st.session_state.env_df,
                    st.session_state.social_df,
                    st.session_state.gov_df
                )
                
                # Check thresholds
                threshold_alerts = []
                threshold_alerts.extend(check_thresholds(st.session_state.env_df, 'environmental', config['thresholds']))
                threshold_alerts.extend(check_thresholds(st.session_state.social_df, 'social', config['thresholds']))
                threshold_alerts.extend(check_thresholds(st.session_state.gov_df, 'governance', config['thresholds']))
                
                st.session_state.esg_scores = scores
                st.session_state.trend_alerts = trend_alerts
                st.session_state.threshold_alerts = threshold_alerts
                st.sidebar.success("Analysis completed successfully!")
        else:
            st.sidebar.error("Please upload all three ESG data files before running analysis.")
    
    # Main content area with tabs
    if 'esg_scores' in st.session_state:
        # Create tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Overview", 
            "🌍 Environmental", 
            "👥 Social", 
            "⚖️ Governance", 
            "📊 Reports", 
            "⚙️ Admin"
        ])
        
        scores = st.session_state.esg_scores
        
        # Overview Tab
        with tab1:
            st.header("🏠 ESG Overview Dashboard")
            st.markdown("---")
            
            # Display ESG metrics with improved UI
            display_esg_metrics(scores)
            
            st.markdown("---")
            
            # Enhanced Quick Highlights with better visual design
            st.subheader("📊 Key Performance Insights")
            
            # Create a more comprehensive insights section
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                overall_grade = get_esg_grade(scores['ESG'])
                grade_badge, _ = get_status_badge(scores['ESG'])
                st.metric(
                    label=f"Overall Grade {grade_badge}",
                    value=overall_grade,
                    help="Overall ESG performance grade"
                )
            
            with col2:
                best_category = max(['E', 'S', 'G'], key=lambda x: scores[x])
                category_names = {'E': 'Environmental', 'S': 'Social', 'G': 'Governance'}
                best_score = scores[best_category]
                best_badge, _ = get_status_badge(best_score)
                st.metric(
                    label=f"Best Category {best_badge}",
                    value=f"{category_names[best_category]}",
                    delta=f"{best_score:.1f}",
                    help=f"Highest performing ESG category with score {best_score:.1f}"
                )
            
            with col3:
                worst_category = min(['E', 'S', 'G'], key=lambda x: scores[x])
                worst_score = scores[worst_category]
                worst_badge, _ = get_status_badge(worst_score)
                st.metric(
                    label=f"Needs Attention {worst_badge}",
                    value=f"{category_names[worst_category]}",
                    delta=f"{worst_score:.1f}",
                    help=f"Category requiring improvement with score {worst_score:.1f}"
                )
            
            with col4:
                # Calculate improvement opportunity
                max_possible = 100
                current_score = scores['ESG']
                improvement_potential = max_possible - current_score
                st.metric(
                    label="🎯 Improvement Potential",
                    value=f"{improvement_potential:.1f} points",
                    help="Maximum possible improvement from current score"
                )
            
            st.markdown("---")
            
            # Enhanced Alerts Section with better organization
            alerts_col1, alerts_col2 = st.columns(2)
            
            with alerts_col1:
                if 'threshold_alerts' in st.session_state and st.session_state.threshold_alerts:
                    st.subheader("🚨 Critical Threshold Alerts")
                    alert_count = len(st.session_state.threshold_alerts)
                    st.error(f"**{alert_count} Critical Alert{'s' if alert_count != 1 else ''}**")
                    
                    for i, alert in enumerate(st.session_state.threshold_alerts[:3], 1):
                        st.error(f"{i}. {alert}")
                    
                    if len(st.session_state.threshold_alerts) > 3:
                        st.info(f"... and {len(st.session_state.threshold_alerts) - 3} more critical alerts")
                else:
                    st.success("✅ **No Critical Threshold Alerts**")
                    st.caption("All metrics are within acceptable thresholds")
            
            with alerts_col2:
                if 'trend_alerts' in st.session_state and st.session_state.trend_alerts:
                    st.subheader("📈 Trend Monitoring Alerts")
                    trend_count = len(st.session_state.trend_alerts)
                    st.warning(f"**{trend_count} Trend Alert{'s' if trend_count != 1 else ''}**")
                    
                    for i, alert in enumerate(st.session_state.trend_alerts[:3], 1):
                        st.warning(f"{i}. {alert}")
                    
                    if len(st.session_state.trend_alerts) > 3:
                        st.info(f"... and {len(st.session_state.trend_alerts) - 3} more trend alerts")
                else:
                    st.success("✅ **No Trend Alerts**")
                    st.caption("All metrics are trending positively or stable")
            
            st.markdown("---")
            
            # Performance Summary Cards
            st.subheader("📈 Performance Summary")
            
            summary_col1, summary_col2, summary_col3 = st.columns(3)
            
            with summary_col1:
                # Score distribution
                st.markdown("**Score Distribution:**")
                for category, score in [('E', scores['E']), ('S', scores['S']), ('G', scores['G'])]:
                    badge, _ = get_status_badge(score)
                    category_name = {'E': 'Environmental', 'S': 'Social', 'G': 'Governance'}[category]
                    st.caption(f"{badge} {category_name}: {score:.1f}")
            
            with summary_col2:
                # Weight contributions
                st.markdown("**Weight Contributions:**")
                contributions = scores['contributions']
                for category, contrib in [('E', contributions['E_contribution']), 
                                        ('S', contributions['S_contribution']), 
                                        ('G', contributions['G_contribution'])]:
                    category_name = {'E': 'Environmental', 'S': 'Social', 'G': 'Governance'}[category]
                    st.caption(f"📊 {category_name}: {contrib:.1f} pts")
            
            with summary_col3:
                # Quick stats
                st.markdown("**Quick Stats:**")
                avg_score = sum([scores['E'], scores['S'], scores['G']]) / 3
                st.caption(f"📊 Average Score: {avg_score:.1f}")
                st.caption(f"🏆 Best Score: {max([scores['E'], scores['S'], scores['G']]):.1f}")
                st.caption(f"⚠️ Lowest Score: {min([scores['E'], scores['S'], scores['G']]):.1f}")
            
            st.markdown("---")
            
            # Enhanced Charts Section
            st.subheader("📊 Interactive Performance Visualizations")
            
            # Create tabs for different chart types
            chart_tab1, chart_tab2, chart_tab3, chart_tab4 = st.tabs([
                "🎯 Performance Overview", 
                "📈 Trend Analysis", 
                "📊 KPI Comparison", 
                "🔥 Performance Heatmap"
            ])
            
            with chart_tab1:
                # Radar chart with enhanced title
                st.subheader("ESG Performance Radar Chart")
                st.caption("Interactive radar chart showing performance across all ESG dimensions")
                st.plotly_chart(create_esg_chart(scores), use_container_width=True)
                
                # Add gauge charts for key metrics
                st.subheader("🎯 Key Performance Gauges")
                gauge_col1, gauge_col2, gauge_col3 = st.columns(3)
                
                with gauge_col1:
                    # Environmental Gauge
                    fig_env = create_gauge_chart(scores['E'], "Environmental Score", "Environmental Performance")
                    st.plotly_chart(fig_env, use_container_width=True)
                
                with gauge_col2:
                    # Social Gauge
                    fig_social = create_gauge_chart(scores['S'], "Social Score", "Social Performance")
                    st.plotly_chart(fig_social, use_container_width=True)
                
                with gauge_col3:
                    # Governance Gauge
                    fig_gov = create_gauge_chart(scores['G'], "Governance Score", "Governance Performance")
                    st.plotly_chart(fig_gov, use_container_width=True)
            
            with chart_tab2:
                st.subheader("📈 ESG Trends Over Time")
                st.caption("Track how your ESG performance has evolved over time")
                
                # Create trend analysis charts
                trend_col1, trend_col2 = st.columns(2)
                
                with trend_col1:
                    # Environmental trends
                    env_trend_fig = create_trend_chart(st.session_state.env_df, "Environmental Trends")
                    if env_trend_fig:
                        st.plotly_chart(env_trend_fig, use_container_width=True)
                    else:
                        st.info("📊 Environmental trend data not available")
                
                with trend_col2:
                    # Social trends
                    social_trend_fig = create_trend_chart(st.session_state.social_df, "Social Trends")
                    if social_trend_fig:
                        st.plotly_chart(social_trend_fig, use_container_width=True)
                    else:
                        st.info("📊 Social trend data not available")
                
                # Governance trends
                gov_trend_fig = create_trend_chart(st.session_state.gov_df, "Governance Trends")
                if gov_trend_fig:
                    st.plotly_chart(gov_trend_fig, use_container_width=True)
                else:
                    st.info("📊 Governance trend data not available")
            
            with chart_tab3:
                st.subheader("📊 ESG Category Comparison")
                
                # Create comparison charts
                comp_col1, comp_col2 = st.columns(2)
                
                with comp_col1:
                    # Category comparison bar chart
                    category_fig = create_category_comparison_chart(scores)
                    st.plotly_chart(category_fig, use_container_width=True)
                
                with comp_col2:
                    # Weight contribution pie chart
                    weight_fig = create_weight_contribution_chart(scores)
                    st.plotly_chart(weight_fig, use_container_width=True)
                
                # Detailed KPI breakdown
                st.subheader("🔍 Detailed KPI Breakdown")
                kpi_fig = create_kpi_breakdown_chart(st.session_state.env_df, st.session_state.social_df, st.session_state.gov_df)
                if kpi_fig:
                    st.plotly_chart(kpi_fig, use_container_width=True)
                else:
                    st.info("📊 Detailed KPI data not available")
            
            with chart_tab4:
                st.subheader("🔥 ESG Performance Heatmap")
                st.caption("Visual representation of all ESG metrics with color-coded performance levels")
                
                # Create heatmap
                heatmap_fig = create_esg_heatmap(st.session_state.env_df, st.session_state.social_df, st.session_state.gov_df)
                if heatmap_fig:
                    st.plotly_chart(heatmap_fig, use_container_width=True)
                else:
                    st.info("📊 Heatmap data not available")
                
                # Performance indicators
                st.subheader("🎯 Performance Indicators")
                indicator_col1, indicator_col2, indicator_col3 = st.columns(3)
                
                with indicator_col1:
                    # Environmental indicators
                    st.markdown("**🌍 Environmental KPIs**")
                    env_indicators = create_kpi_indicators(st.session_state.env_df, "Environmental")
                    for indicator in env_indicators:
                        st.write(indicator)
                
                with indicator_col2:
                    # Social indicators
                    st.markdown("**👥 Social KPIs**")
                    social_indicators = create_kpi_indicators(st.session_state.social_df, "Social")
                    for indicator in social_indicators:
                        st.write(indicator)
                
                with indicator_col3:
                    # Governance indicators
                    st.markdown("**⚖️ Governance KPIs**")
                    gov_indicators = create_kpi_indicators(st.session_state.gov_df, "Governance")
                    for indicator in gov_indicators:
                        st.write(indicator)
        
        # Environmental Tab
        with tab2:
            st.header("🌍 Environmental Analysis")
            st.markdown("---")
            
            # Enhanced Environmental metrics with colored badges
            env_score = scores['E']
            env_badge, env_status = get_status_badge(env_score)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f"Environmental Score {env_badge}",
                    value=f"{env_score:.1f}",
                    delta=f"Grade: {get_esg_grade(env_score)}",
                    delta_color=get_status_delta(env_score),
                    help="Overall environmental performance score"
                )
            
            with col2:
                st.metric(
                    label="Weight Contribution",
                    value=f"{scores['contributions']['E_contribution']:.1f} points",
                    delta=f"({scores['weights']['E']}% weight)",
                    help="Contribution to overall ESG score based on configured weight"
                )
            
            with col3:
                # Environmental performance status
                if env_score >= 70:
                    status_text = "Excellent"
                    status_color = "🟢"
                elif env_score >= 40:
                    status_text = "Good"
                    status_color = "🟡"
                else:
                    status_text = "Needs Improvement"
                    status_color = "🔴"
                
                st.metric(
                    label=f"Performance Status {status_color}",
                    value=status_text,
                    help="Current environmental performance level"
                )
            
            # Environmental charts
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                co2_chart = create_co2_chart(st.session_state.env_df)
                if co2_chart:
                    st.plotly_chart(co2_chart, use_container_width=True)
                else:
                    st.info("📊 CO2 emissions chart requires at least 2 data points")
            
            with chart_col2:
                energy_chart = create_energy_chart(st.session_state.env_df)
                if energy_chart:
                    st.plotly_chart(energy_chart, use_container_width=True)
                else:
                    st.info("📊 Energy consumption chart requires at least 2 data points")
            
            # Environmental data preview
            if 'env_df' in st.session_state:
                st.subheader("📋 Environmental Data")
                st.dataframe(st.session_state.env_df, use_container_width=True)
        
        # Social Tab
        with tab3:
            st.header("👥 Social Analysis")
            st.markdown("---")
            
            # Enhanced Social metrics with colored badges
            social_score = scores['S']
            social_badge, social_status = get_status_badge(social_score)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f"Social Score {social_badge}",
                    value=f"{social_score:.1f}",
                    delta=f"Grade: {get_esg_grade(social_score)}",
                    delta_color=get_status_delta(social_score),
                    help="Overall social performance score"
                )
            
            with col2:
                st.metric(
                    label="Weight Contribution",
                    value=f"{scores['contributions']['S_contribution']:.1f} points",
                    delta=f"({scores['weights']['S']}% weight)",
                    help="Contribution to overall ESG score based on configured weight"
                )
            
            with col3:
                # Social performance status
                if social_score >= 70:
                    status_text = "Excellent"
                    status_color = "🟢"
                elif social_score >= 40:
                    status_text = "Good"
                    status_color = "🟡"
                else:
                    status_text = "Needs Improvement"
                    status_color = "🔴"
                
                st.metric(
                    label=f"Performance Status {status_color}",
                    value=status_text,
                    help="Current social performance level"
                )
            
            # Social charts
            satisfaction_chart = create_satisfaction_chart(st.session_state.social_df)
            if satisfaction_chart:
                st.plotly_chart(satisfaction_chart, use_container_width=True)
            
            # Social data preview
            if 'social_df' in st.session_state:
                st.subheader("📋 Social Data")
                st.dataframe(st.session_state.social_df, use_container_width=True)
        
        # Governance Tab
        with tab4:
            st.header("⚖️ Governance Analysis")
            st.markdown("---")
            
            # Enhanced Governance metrics with colored badges
            gov_score = scores['G']
            gov_badge, gov_status = get_status_badge(gov_score)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label=f"Governance Score {gov_badge}",
                    value=f"{gov_score:.1f}",
                    delta=f"Grade: {get_esg_grade(gov_score)}",
                    delta_color=get_status_delta(gov_score),
                    help="Overall governance performance score"
                )
            
            with col2:
                st.metric(
                    label="Weight Contribution",
                    value=f"{scores['contributions']['G_contribution']:.1f} points",
                    delta=f"({scores['weights']['G']}% weight)",
                    help="Contribution to overall ESG score based on configured weight"
                )
            
            with col3:
                # Governance performance status
                if gov_score >= 70:
                    status_text = "Excellent"
                    status_color = "🟢"
                elif gov_score >= 40:
                    status_text = "Good"
                    status_color = "🟡"
                else:
                    status_text = "Needs Improvement"
                    status_color = "🔴"
                
                st.metric(
                    label=f"Performance Status {status_color}",
                    value=status_text,
                    help="Current governance performance level"
                )
            
            # Governance charts
            compliance_chart = create_compliance_chart(st.session_state.gov_df)
            if compliance_chart:
                st.plotly_chart(compliance_chart, use_container_width=True)
            
            # Governance data preview
            if 'gov_df' in st.session_state:
                st.subheader("📋 Governance Data")
                st.dataframe(st.session_state.gov_df, use_container_width=True)
        
        # Reports Tab
        with tab5:
            st.header("📊 Reports & Export")
            st.markdown("---")
            
            # Enhanced report section with better presentation
            st.subheader("📋 Report Configuration")
            
            col_config1, col_config2 = st.columns(2)
            
            with col_config1:
                company_name = st.text_input(
                    "Company/Facility Name", 
                    value="Sample Company", 
                    key="company_name",
                    help="Enter the name of your company or facility for the report"
                )
            
            with col_config2:
                report_date = st.date_input(
                    "Report Date",
                    value=datetime.now().date(),
                    help="Select the date for this ESG report"
                )
            
            st.markdown("---")
            
            # Enhanced report generation section
            st.subheader("🚀 Generate Reports")
            
            # Show current ESG summary before generating reports
            col_summary1, col_summary2, col_summary3 = st.columns(3)
            
            with col_summary1:
                st.metric(
                    label="Overall ESG Score",
                    value=f"{scores['ESG']:.1f}",
                    delta=f"Grade: {get_esg_grade(scores['ESG'])}"
                )
            
            with col_summary2:
                st.metric(
                    label="Environmental",
                    value=f"{scores['E']:.1f}",
                    delta=f"Weight: {scores['weights']['E']}%"
                )
            
            with col_summary3:
                st.metric(
                    label="Social",
                    value=f"{scores['S']:.1f}",
                    delta=f"Weight: {scores['weights']['S']}%"
                )
            
            st.markdown("---")
            
            # AI-Powered Report Generation Section
            st.subheader("🤖 AI-Powered ESG Analysis")
            st.caption("Generate comprehensive ESG reports using Google Gemini AI")
            
            # Check API status
            try:
                reporter = ESGReporter()
                if reporter.gemini_model:
                    st.success("✅ Gemini API is configured and ready!")
                elif reporter.openai_client:
                    st.warning("⚠️ Using OpenAI API (Gemini not configured)")
                else:
                    st.error("❌ No AI API configured. Please set up your API keys.")
            except Exception as e:
                st.error(f"❌ Error checking AI configuration: {str(e)}")
            
            col_ai1, col_ai2 = st.columns(2)
            
            with col_ai1:
                if st.button("🧠 Generate AI Insights", use_container_width=True):
                    with st.spinner("🤖 Generating AI insights with Gemini..."):
                        try:
                            reporter = ESGReporter()
                            dfs = {
                                'env': st.session_state.env_df,
                                'social': st.session_state.social_df,
                                'gov': st.session_state.gov_df
                            }
                            
                            ai_insights = reporter.generate_ai_insights(scores, dfs)
                            
                            st.success("✅ AI insights generated successfully!")
                            st.markdown("---")
                            st.markdown("### 🤖 AI-Generated ESG Insights")
                            st.markdown(ai_insights)
                            
                        except Exception as e:
                            st.error(f"❌ Error generating AI insights: {str(e)}")
                            st.info("💡 Make sure your Gemini API key is properly configured in the .env file")
            
            with col_ai2:
                if st.button("📊 Generate Detailed ESG Report", use_container_width=True):
                    with st.spinner("🤖 Generating comprehensive ESG report with Gemini..."):
                        try:
                            reporter = ESGReporter()
                            dfs = {
                                'env': st.session_state.env_df,
                                'social': st.session_state.social_df,
                                'gov': st.session_state.gov_df
                            }
                            
                            detailed_report = reporter.generate_detailed_esg_report(scores, dfs, company_name)
                            
                            st.success("✅ Detailed ESG report generated successfully!")
                            st.markdown("---")
                            st.markdown("### 📊 Comprehensive ESG Report")
                            st.markdown(detailed_report)
                            
                            # Add download option for the AI report
                            report_text = f"ESG Report for {company_name}\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n{detailed_report}"
                            
                            st.download_button(
                                label="💾 Download AI Report (TXT)",
                                data=report_text,
                                file_name=f"AI_ESG_Report_{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                            
                        except Exception as e:
                            st.error(f"❌ Error generating detailed report: {str(e)}")
                            st.info("💡 Make sure your Gemini API key is properly configured in the .env file")
            
            st.markdown("---")
            
            # Traditional Report generation buttons
            st.subheader("📋 Traditional Reports")
            st.caption("Generate Excel and PDF reports with charts and data")
            
            col_report1, col_report2 = st.columns(2)
            
            with col_report1:
                if st.button("📈 Generate Excel Report", use_container_width=True):
                    with st.spinner("Generating Excel report..."):
                        try:
                            dfs = {
                                'env': st.session_state.env_df,
                                'social': st.session_state.social_df,
                                'gov': st.session_state.gov_df
                            }
                            
                            excel_data = generate_excel_report(scores, dfs, company_name)
                            
                            st.download_button(
                                label="💾 Download Excel Report",
                                data=excel_data,
                                file_name=f"ESG_Report_{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                            st.success("Excel report generated successfully!")
                        except Exception as e:
                            st.error(f"Error generating Excel report: {str(e)}")
            
            with col_report2:
                if st.button("📄 Generate PDF Report", use_container_width=True):
                    with st.spinner("Generating PDF report..."):
                        try:
                            dfs = {
                                'env': st.session_state.env_df,
                                'social': st.session_state.social_df,
                                'gov': st.session_state.gov_df
                            }
                            
                            pdf_data = generate_pdf_report(scores, dfs, company_name)
                            
                            st.download_button(
                                label="💾 Download PDF Report",
                                data=pdf_data,
                                file_name=f"ESG_Report_{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
                            st.success("PDF report generated successfully!")
                        except Exception as e:
                            st.error(f"Error generating PDF report: {str(e)}")
            
            # AI Insights preview
            if st.button("🤖 Generate AI Insights", use_container_width=True):
                with st.spinner("Generating AI insights..."):
                    try:
                        dfs = {
                            'env': st.session_state.env_df,
                            'social': st.session_state.social_df,
                            'gov': st.session_state.gov_df
                        }
                        
                        insights = generate_ai_insights(scores, dfs)
                        st.session_state.ai_insights = insights
                        st.success("AI insights generated!")
                    except Exception as e:
                        st.error(f"Error generating insights: {str(e)}")
            
            # Display AI insights if available
            if 'ai_insights' in st.session_state:
                st.subheader("🤖 AI-Generated Insights")
                st.markdown(st.session_state.ai_insights)
        
        # Admin Tab
        with tab6:
            st.header("⚙️ Admin Settings")
            
            # ESG Weights Configuration
            st.subheader("🎯 ESG Weights Configuration")
            col_e, col_s, col_g = st.columns(3)
            
            with col_e:
                new_e = st.number_input("Environmental Weight (%)", min_value=0, max_value=100, value=config['weights']['E'], key="admin_weight_e")
            with col_s:
                new_s = st.number_input("Social Weight (%)", min_value=0, max_value=100, value=config['weights']['S'], key="admin_weight_s")
            with col_g:
                new_g = st.number_input("Governance Weight (%)", min_value=0, max_value=100, value=config['weights']['G'], key="admin_weight_g")
            
            total_weight = new_e + new_s + new_g
            
            if total_weight != 100:
                st.warning(f"⚠️ Total weights must equal 100% (currently {total_weight}%)")
            else:
                if st.button("💾 Save Weights", key="admin_save_weights"):
                    new_config = config.copy()
                    new_config['weights'] = {"E": int(new_e), "S": int(new_s), "G": int(new_g)}
                    save_config(new_config)
                    st.success("✅ Weights saved successfully!")
                    st.rerun()
            
            # Threshold Configuration
            st.subheader("🚨 Threshold Configuration")
            
            # Environmental Thresholds
            st.markdown("**🌍 Environmental Thresholds:**")
            col1, col2 = st.columns(2)
            with col1:
                new_co2 = st.number_input("CO2 Emissions (tonnes)", min_value=0, value=int(config['thresholds']['co2_tonnes']), key="admin_co2")
                new_energy = st.number_input("Energy Consumption (kWh)", min_value=0, value=int(config['thresholds']['energy_kwh']), key="admin_energy")
            with col2:
                new_waste = st.number_input("Waste Generated", min_value=0, value=int(config['thresholds']['waste_generated']), key="admin_waste")
                new_water = st.number_input("Water Usage", min_value=0, value=int(config['thresholds']['water_usage']), key="admin_water")
            
            # Social Thresholds
            st.markdown("**👥 Social Thresholds:**")
            col3, col4 = st.columns(2)
            with col3:
                new_satisfaction = st.number_input("Employee Satisfaction (%)", min_value=0, max_value=100, value=int(config['thresholds']['employee_satisfaction']), key="admin_satisfaction")
                new_diversity = st.number_input("Diversity Score (%)", min_value=0, max_value=100, value=int(config['thresholds']['diversity_score']), key="admin_diversity")
            with col4:
                new_safety = st.number_input("Safety Incidents", min_value=0, value=int(config['thresholds']['safety_incidents']), key="admin_safety")
            
            # Governance Thresholds
            st.markdown("**⚖️ Governance Thresholds:**")
            col5, col6 = st.columns(2)
            with col5:
                new_independence = st.number_input("Board Independence (%)", min_value=0, max_value=100, value=int(config['thresholds']['board_independence']), key="admin_independence")
            with col6:
                new_transparency = st.number_input("Transparency Score (%)", min_value=0, max_value=100, value=int(config['thresholds']['transparency_score']), key="admin_transparency")
            
            # Save thresholds
            if st.button("💾 Save Thresholds", key="admin_save_thresholds"):
                new_config = config.copy()
                new_config['thresholds'] = {
                    'co2_tonnes': int(new_co2),
                    'energy_kwh': int(new_energy),
                    'accidents_count': int(config['thresholds'].get('accidents_count', 5)),
                    'waste_generated': int(new_waste),
                    'water_usage': int(new_water),
                    'employee_satisfaction': int(new_satisfaction),
                    'diversity_score': int(new_diversity),
                    'safety_incidents': int(new_safety),
                    'board_independence': int(new_independence),
                    'transparency_score': int(new_transparency)
                }
                save_config(new_config)
                st.success("✅ Thresholds saved successfully!")
                st.rerun()
            
            # Reset to defaults
            if st.button("🔄 Reset to Defaults", key="admin_reset"):
                default_config = {
                    "weights": {"E": 45, "S": 30, "G": 25},
                    "thresholds": {
                        "co2_tonnes": 500,
                        "energy_kwh": 200000,
                        "accidents_count": 5,
                        "waste_generated": 1000,
                        "water_usage": 50000,
                        "employee_satisfaction": 70,
                        "diversity_score": 60,
                        "safety_incidents": 10,
                        "board_independence": 80,
                        "transparency_score": 75
                    }
                }
                save_config(default_config)
                st.success("✅ Reset to defaults successfully!")
                st.rerun()
            
            # Current settings display
            with st.expander("📋 Current Settings"):
                st.json(config)
        
    
    else:
        # Show welcome message when no analysis has been run
        st.info("👆 Please upload ESG data files and click 'Run Analysis' to view results.")
        
        # Show file format help
        st.subheader("📋 Data Format Requirements")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            **🌍 Environmental CSV Required Columns:**
            - carbon_emissions
            - energy_consumption
            - waste_generated
            - water_usage
            - renewable_energy_percentage
            """)
        
        with col2:
            st.markdown("""
            **👥 Social CSV Required Columns:**
            - employee_satisfaction
            - diversity_score
            - community_investment
            - safety_incidents
            - training_hours_per_employee
            """)
        
        with col3:
            st.markdown("""
            **⚖️ Governance CSV Required Columns:**
            - board_independence
            - executive_compensation_ratio
            - audit_quality
            - transparency_score
            - stakeholder_engagement
            """)


if __name__ == "__main__":
    main()

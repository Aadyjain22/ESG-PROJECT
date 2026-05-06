# AI-Driven ESG Sustainability Platform

A comprehensive Streamlit application for analyzing Environmental, Social, and Governance (ESG) data with AI-driven scoring and visualization.

## 🚀 Features

- **CSV Upload & Validation**: Upload and validate Environmental, Social, and Governance data files
- **Advanced ESG Scoring**: Compute weighted ESG scores with detailed normalization methodology
- **Interactive Analytics Dashboard**: Beautiful visualizations with radar charts, line charts, and bar charts
- **KPI Performance Cards**: Color-coded performance indicators (green/orange/red)
- **Trend Analysis**: Real-time alerts for KPIs that worsen by more than 10%
- **Admin Settings**: Adjustable ESG weight configurations
- **Data Preview**: Preview uploaded data before analysis
- **Grade System**: Convert ESG scores to letter grades (A+ to F)
- **Detailed Breakdown**: Individual KPI scores and weighted contribution analysis
- **Calculation Transparency**: Full methodology explanation for ESG scoring
- **AI-Powered Reports**: Generate Excel and PDF reports with AI insights
- **Export Functionality**: Download comprehensive ESG reports with charts and analysis
- **Flexible AI Integration**: Support for OpenAI GPT and Google Gemini APIs

## 📁 Project Structure

```
project_root/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── config.json              # Default ESG weights configuration
├── modules/
│   ├── data_processing.py   # Data validation and ESG scoring functions
│   └── reports.py          # AI-powered report generation (Excel/PDF)
├── data/                    # Directory for uploaded CSV files
│   ├── sample_environmental.csv
│   ├── sample_social.csv
│   └── sample_governance.csv
└── README.md               # This file
```

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:8501`

5. **Optional: Set up AI API keys** (for enhanced insights):
   - Copy `env_example.txt` to `.env`
   - Add your OpenAI or Gemini API key
   - See "AI API Setup Instructions" in the app for details

## 📊 Data Format Requirements

### Environmental CSV
Required columns:
- `carbon_emissions`
- `energy_consumption`
- `waste_generated`
- `water_usage`
- `renewable_energy_percentage`

### Social CSV
Required columns:
- `employee_satisfaction`
- `diversity_score`
- `community_investment`
- `safety_incidents`
- `training_hours_per_employee`

### Governance CSV
Required columns:
- `board_independence`
- `executive_compensation_ratio`
- `audit_quality`
- `transparency_score`
- `stakeholder_engagement`

## 🎯 Usage

1. **Upload Data**: Upload your three CSV files (Environmental, Social, Governance)
2. **Validate**: The app will automatically validate your data format
3. **Run Analysis**: Click "Run Analysis" in the sidebar
4. **View Results**: See your ESG scores, radar chart, and detailed breakdown
5. **Adjust Weights**: Use admin settings to customize ESG weight percentages

## ⚙️ Configuration

Default ESG weights are stored in `config.json`:
- Environmental: 45%
- Social: 30%
- Governance: 25%

You can adjust these weights through the admin settings in the app sidebar.

## 📈 Sample Data

The `data/` folder contains sample CSV files that you can use to test the application. These files demonstrate the required data format and structure.

## 🔧 Technical Details

- **Framework**: Streamlit
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Validation**: Custom validation functions for each ESG category
- **Scoring**: Weighted average with normalization and inversion for negative indicators

## 🌱 ESG Scoring Logic

The application uses a sophisticated scoring methodology:

### 1. **Data Normalization** (0-100 scale)
- **Lower is better**: `score = (max - value) / (max - min) * 100`
  - Carbon emissions, energy consumption, waste, water usage, safety incidents, executive compensation ratio
- **Higher is better**: `score = (value - min) / (max - min) * 100`
  - Renewable energy %, employee satisfaction, diversity, community investment, training, board independence, audit quality, transparency, stakeholder engagement

### 2. **Sub-score Calculation**
- Environmental: Average of all environmental KPI scores
- Social: Average of all social KPI scores  
- Governance: Average of all governance KPI scores

### 3. **Weighted Overall Score**
```
ESG = (E_score × E_weight + S_score × S_weight + G_score × G_weight) / 100
```

### 4. **Grade Assignment**
- A+ (95+), A (90+), A- (85+), B+ (80+), B (75+), B- (70+), C+ (65+), C (60+), C- (55+), D (50+), F (<50)

### 5. **Trend Analysis**
- Monitors KPI changes over time
- Alerts when any metric worsens by more than 10% from previous period

### 6. **AI-Powered Reporting**
- **Excel Reports**: Comprehensive spreadsheets with multiple sheets, charts, and AI insights
- **PDF Reports**: Professional documents with executive summaries and key metrics
- **AI Integration**: Uses OpenAI GPT or Google Gemini for intelligent analysis and recommendations
- **Fallback Mode**: Built-in insights when AI APIs are not available

## 📝 Notes

- All uploaded files are automatically saved to the `data/` folder
- The application handles missing values by using median imputation
- Scores are calculated as averages across all data points in each category
- The radar chart provides a visual representation of ESG performance across all dimensions
- Reports include timestamp and customizable company/facility names
- AI insights are generated in real-time and can be refreshed on demand
- Both Excel and PDF reports include all KPI data, charts, and AI-generated recommendations

## 🤖 AI Integration

The application supports two AI providers for enhanced insights:

### OpenAI GPT Integration
- Uses GPT-3.5-turbo for intelligent ESG analysis
- Provides actionable recommendations and risk assessments
- Requires OpenAI API key in `.env` file

### Google Gemini Integration  
- Alternative AI provider with similar capabilities
- Requires Gemini API key in `.env` file
- Automatically falls back if OpenAI is unavailable

### Fallback Mode
- Built-in insights when no AI APIs are configured
- Provides basic analysis and recommendations
- Ensures the application works without external dependencies

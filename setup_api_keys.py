#!/usr/bin/env python3
"""
AI API Keys Setup Script
This script helps you set up AI API keys for enhanced ESG insights.
"""

import os
from pathlib import Path

def create_env_file():
    """Create .env file with API key template."""
    
    env_content = """# AI API Keys for ESG Report Generation
# Copy your actual API key below

# Google Gemini API Key (FREE - Recommended)
GEMINI_API_KEY=your_gemini_key_here

# OpenAI API Key (Premium - Optional)
# OPENAI_API_KEY=your_openai_key_here

# Instructions:
# 1. Get Gemini API key from: https://makersuite.google.com/app/apikey
# 2. Replace 'your_gemini_key_here' with your actual key
# 3. Save this file
# 4. Restart the Streamlit app
"""
    
    env_path = Path('.env')
    
    if env_path.exists():
        print("✅ .env file already exists!")
        print("📝 Please edit it with your actual API key.")
    else:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("✅ Created .env file successfully!")
        print("📝 Please edit it with your actual API key.")
    
    print("\n🔑 To get your Gemini API key:")
    print("   1. Visit: https://makersuite.google.com/app/apikey")
    print("   2. Sign in with Google account")
    print("   3. Click 'Create API Key'")
    print("   4. Copy the key and replace 'your_gemini_key_here' in .env file")
    
    return env_path.exists()

def check_api_keys():
    """Check if API keys are configured."""
    
    if not Path('.env').exists():
        print("❌ No .env file found")
        return False
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    has_gemini = bool(os.getenv('GEMINI_API_KEY') and os.getenv('GEMINI_API_KEY') != 'your_gemini_key_here')
    has_openai = bool(os.getenv('OPENAI_API_KEY') and os.getenv('OPENAI_API_KEY') != 'your_openai_key_here')
    
    print("\n🔍 API Key Status:")
    if has_gemini:
        print("   ✅ Gemini API key configured")
    else:
        print("   ❌ Gemini API key not configured")
    
    if has_openai:
        print("   ✅ OpenAI API key configured")
    else:
        print("   ❌ OpenAI API key not configured")
    
    return has_gemini or has_openai

def test_ai_integration():
    """Test AI integration with sample data."""
    
    try:
        import sys
        sys.path.append('modules')
        from modules.reports import ESGReporter
        
        print("\n🤖 Testing AI Integration...")
        
        # Create sample ESG scores
        scores_dict = {
            'E': 75.5,
            'S': 82.3,
            'G': 78.9,
            'ESG': 78.9,
            'weights': {'E': 45, 'S': 30, 'G': 25}
        }
        
        # Create sample dataframes
        import pandas as pd
        dfs = {
            'env': pd.DataFrame({'carbon_emissions': [250, 200, 180]}),
            'social': pd.DataFrame({'employee_satisfaction': [85, 90, 95]}),
            'gov': pd.DataFrame({'board_independence': [80, 85, 90]})
        }
        
        # Test AI insights
        reporter = ESGReporter()
        insights = reporter.generate_ai_insights(scores_dict, dfs)
        
        print("✅ AI integration working!")
        print("📄 Sample insight preview:")
        print("   " + insights[:100] + "...")
        
        return True
        
    except Exception as e:
        print(f"❌ AI integration test failed: {e}")
        return False

def main():
    """Main setup function."""
    
    print("🚀 ESG Platform - AI API Setup")
    print("=" * 40)
    
    # Step 1: Create .env file
    print("\n📝 Step 1: Creating .env file...")
    create_env_file()
    
    # Step 2: Check current status
    print("\n🔍 Step 2: Checking API key status...")
    keys_configured = check_api_keys()
    
    if not keys_configured:
        print("\n⚠️  No API keys configured yet.")
        print("   Please edit the .env file with your actual API key.")
        print("   Then run this script again to test.")
        return
    
    # Step 3: Test integration
    print("\n🧪 Step 3: Testing AI integration...")
    if test_ai_integration():
        print("\n🎉 Setup complete! AI features are ready to use.")
        print("   Run 'streamlit run app.py' to start the enhanced platform.")
    else:
        print("\n❌ Setup incomplete. Please check your API key.")

if __name__ == "__main__":
    main()

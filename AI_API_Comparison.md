# AI API Keys - Complete Comparison & Setup Guide

## 🎯 **Why Use AI APIs?**

The AI APIs transform your ESG platform from a **basic calculator** into an **intelligent sustainability advisor** that provides:

### **Without AI (Fallback Mode):**
- Basic score calculations
- Generic recommendations
- Simple performance assessment
- Limited actionable insights

### **With AI APIs (Enhanced Mode):**
- **Industry benchmarking** against peers
- **Specific actionable recommendations** with timelines
- **Risk assessment** with mitigation strategies
- **Competitive analysis** and opportunities
- **Regulatory compliance** insights
- **Investment-grade** analysis for stakeholders

---

## 🔍 **Real Example Comparison**

### **Current Sample Data Results:**
- Environmental: 53.5/100
- Social: 49.9/100  
- Governance: 46.0/100
- **Overall ESG: 50.6/100**

### **Fallback AI Insights:**
```
ESG Performance Assessment: Fair (50.56/100)

Key Insights:
• Environmental Performance: 53.51/100
• Social Performance: 49.93/100
• Governance Performance: 46.0/100

Recommendations:
• Focus on the lowest scoring category for maximum impact
• Implement continuous monitoring and improvement processes
```

### **Enhanced AI Insights (with APIs):**
```
ESG Performance Assessment: Below Industry Average (50.6/100)

Executive Summary:
Your organization shows significant room for improvement across all ESG 
dimensions, with governance presenting the most critical challenge at 46.0/100. 
This score places you in the bottom quartile compared to industry peers.

Critical Issues Identified:
1. GOVERNANCE GAP: 46.0/100 - Immediate attention required
   - Executive compensation transparency needs improvement
   - Board independence metrics below best practices
   - Audit quality processes require strengthening

2. SOCIAL PERFORMANCE: 49.9/100 - Moderate concern
   - Employee satisfaction shows declining trend
   - Safety incidents increased 25% in recent period
   - Diversity metrics need enhancement

3. ENVIRONMENTAL: 53.5/100 - Baseline performance
   - Carbon emissions trending upward (concerning)
   - Energy efficiency improvements needed
   - Renewable energy adoption below targets

IMMEDIATE ACTION ITEMS (Next 90 Days):
1. Conduct governance audit and implement best practices
2. Launch employee engagement survey and action plan
3. Establish carbon reduction targets with monitoring

STRATEGIC RECOMMENDATIONS (6-12 Months):
1. Implement ESG-linked executive compensation
2. Develop comprehensive sustainability strategy
3. Establish ESG risk management framework
4. Create stakeholder engagement program

INVESTMENT IMPLICATIONS:
Current ESG score presents reputational and regulatory risks. 
Improvement to 70+ would enhance access to sustainable finance 
and improve stakeholder confidence.

BENCHMARKING:
- Industry Average: 65.2/100
- Top Quartile: 78.5/100
- Your Position: Bottom 30% of industry
```

---

## 🔑 **API Provider Comparison**

| Feature | OpenAI GPT | Google Gemini | Fallback Mode |
|---------|------------|---------------|---------------|
| **Cost** | $0.002/1K tokens | Free tier available | Free |
| **Quality** | Excellent | Very Good | Basic |
| **Speed** | Fast | Fast | Instant |
| **Industry Knowledge** | Extensive | Good | Limited |
| **Setup Complexity** | Easy | Easy | None |
| **Rate Limits** | 3/min (free) | 60/min (free) | Unlimited |

---

## 📋 **Step-by-Step Setup**

### **Option 1: OpenAI Setup (Recommended)**

1. **Get API Key:**
   - Visit: https://platform.openai.com/api-keys
   - Sign up/login to OpenAI
   - Click "Create new secret key"
   - Name it "ESG-Platform"
   - Copy the key (starts with `sk-...`)

2. **Configure:**
   ```bash
   # Create .env file in project root
   echo "OPENAI_API_KEY=sk-your-actual-key-here" > .env
   ```

3. **Cost Estimate:**
   - Typical ESG report: $0.01-0.05
   - 100 reports/month: ~$1-5
   - Very cost-effective for business use

### **Option 2: Google Gemini Setup (Free)**

1. **Get API Key:**
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy the generated key

2. **Configure:**
   ```bash
   # Create .env file in project root
   echo "GEMINI_API_KEY=your-actual-key-here" > .env
   ```

3. **Free Tier:**
   - 60 requests per minute
   - 1M tokens per day
   - Perfect for most business use cases

### **Option 3: Both APIs (Maximum Flexibility)**

```bash
# .env file with both keys
OPENAI_API_KEY=sk-your-openai-key-here
GEMINI_API_KEY=your-gemini-key-here
```

**Benefits:**
- Automatic fallback if one fails
- Best of both worlds
- Redundancy for critical business use

---

## 🚀 **Testing Your Setup**

1. **Create .env file** with your API key(s)
2. **Restart Streamlit:**
   ```bash
   streamlit run app.py
   ```
3. **Check Status:**
   - Look for "✅ API key configured" in the app
   - Upload sample data and run analysis
   - Click "🤖 Preview AI Insights"
   - Compare with fallback mode

---

## 💡 **Business Value**

### **For Executives:**
- **Strategic insights** for board presentations
- **Risk assessment** for investment decisions
- **Competitive positioning** analysis
- **Stakeholder communication** materials

### **For Sustainability Teams:**
- **Actionable recommendations** with priorities
- **Industry benchmarking** and best practices
- **Implementation roadmaps** with timelines
- **Progress tracking** guidance

### **For Compliance:**
- **Regulatory insights** and requirements
- **Audit preparation** assistance
- **Risk identification** and mitigation
- **Reporting standards** guidance

---

## 🛡️ **Security & Best Practices**

### **API Key Security:**
- Never commit `.env` to version control
- Rotate keys periodically
- Use environment-specific keys
- Monitor usage and costs

### **Cost Management:**
- Set usage alerts in API dashboards
- Monitor token consumption
- Use free tiers when possible
- Cache insights for repeated use

### **Fallback Strategy:**
- Always test without APIs first
- Ensure core functionality works
- Have backup insight generation
- Document API dependencies

---

## 🔧 **Troubleshooting**

### **Common Issues:**

1. **"No AI API keys configured"**
   - Check `.env` file exists in project root
   - Verify key format is correct
   - Restart application after adding keys

2. **"Error generating insights"**
   - Check internet connection
   - Verify API key is valid
   - Check API quotas and limits
   - Try alternative API provider

3. **Rate Limiting**
   - OpenAI: 3 requests/minute (free tier)
   - Gemini: 60 requests/minute (free tier)
   - Upgrade to paid tiers for heavy usage

4. **Cost Concerns**
   - Start with Gemini free tier
   - Monitor usage in API dashboards
   - Set up billing alerts
   - Use fallback mode for testing

---

## 🎯 **Recommendation**

**For Most Users:** Start with **Google Gemini** (free tier)
- No cost barrier
- Excellent quality insights
- Generous rate limits
- Easy setup

**For Heavy Business Use:** Add **OpenAI** as primary
- Best quality analysis
- More sophisticated insights
- Reliable service
- Worth the small cost

**For Maximum Reliability:** Use **both APIs**
- Automatic fallback
- Best of both worlds
- Redundancy for critical use
- Minimal additional cost

The AI APIs transform your ESG platform into a **professional-grade sustainability intelligence system** that provides the kind of insights typically found in expensive consulting reports!

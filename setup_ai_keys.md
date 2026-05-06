# AI API Keys Setup Instructions

## Step 1: Create .env File

Create a file named `.env` in your project root directory (same level as app.py):

```
# Copy env_example.txt to .env and edit with your actual keys
```

## Step 2: Add Your API Key

### For OpenAI (Recommended):
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
```

### For Google Gemini (Free Alternative):
```
GEMINI_API_KEY=your-actual-gemini-key-here
```

### For Both (Maximum Flexibility):
```
OPENAI_API_KEY=sk-your-actual-openai-key-here
GEMINI_API_KEY=your-actual-gemini-key-here
```

## Step 3: Verify Setup

1. Restart your Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Check the "AI API Setup Instructions" section in the app
3. You should see: "✅ OpenAI API key configured" or "✅ Gemini API key configured"

## Security Notes

- Never commit .env file to version control
- .env is already in .gitignore
- Keep your API keys secure and private
- Rotate keys periodically for security

## Troubleshooting

### "No AI API keys configured"
- Check .env file exists in project root
- Verify key format is correct
- Restart the application after adding keys

### "Error generating insights"
- Check internet connection
- Verify API key is valid and has credits
- Try the other API provider as backup

### Rate Limiting
- OpenAI: 3 requests per minute on free tier
- Gemini: 60 requests per minute on free tier
- Consider upgrading to paid tiers for heavy usage

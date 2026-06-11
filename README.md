# 🚀 KILLCRITIC - AI-Powered Startup Analyzer

An intelligent startup idea analyzer with a modern, enhanced UI that provides comprehensive feedback using AI.

## Features

✨ **AI-Powered Analysis** - Real-time startup idea evaluation using GPT-3.5
🎨 **Modern UI** - Beautiful, responsive dark theme interface
⚡ **Real-time Feedback** - Instant analysis of startup concepts
📊 **Detailed Reports** - Comprehensive breakdown including strengths, weaknesses, risks, and more
💾 **Copy Results** - Easy-to-use copy functionality for sharing analysis
📱 **Mobile Responsive** - Works seamlessly on all devices

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for local dev server)
- OpenAI API Key (optional, but recommended for full AI features)

### Installation

1. **Clone or download the project**
```bash
cd killcritic
```

2. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Set up OpenAI API Key (Optional but Recommended)**

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

**On Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "your-api-key-here"
```

**On Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**On macOS/Linux:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

### Running the Application

1. **Start the backend server**
```bash
cd backend
python app.py
```
You should see:
```
🚀 KILLCRITIC Backend Starting...
📊 AI Mode: ENABLED (OpenAI)
```

2. **Open the frontend in your browser**
- Navigate to `http://localhost:5000` OR
- Open `frontend/index.html` directly in your browser (limited AI features)

## Project Structure

```
killcritic/
├── frontend/
│   ├── index.html      # Main UI
│   ├── script.js       # Frontend logic & API calls
│   └── styles.css      # Modern styling
├── backend/
│   ├── app.py          # Flask backend with AI integration
│   └── requirements.txt # Python dependencies
└── README.md           # This file
```

## How It Works

### Without OpenAI API Key
The system uses intelligent fallback analysis with:
- Keyword detection for contextual feedback
- Smart suggestions based on startup type
- Realistic scoring and risk assessment

### With OpenAI API Key
Full AI-powered analysis using GPT-3.5:
- In-depth market analysis
- Competitive landscape assessment
- Detailed improvement suggestions
- Realistic success probability scoring

## API Endpoints

### POST /analyze
Analyzes a startup idea
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{"idea": "An AI tool that helps developers write better code reviews"}'
```

Response:
```json
{
  "agent": "KILLCRITIC",
  "analysis": {
    "summary": "...",
    "strengths": [...],
    "weaknesses": [...],
    "risks": [...],
    "competitors": [...],
    "improvement_suggestions": [...],
    "mvp_roadmap": [...],
    "score": 7.5,
    "failure_probability": "medium"
  },
  "ai_model": "gpt-3.5-turbo"
}
```

### GET /health
Health check endpoint
```bash
curl http://localhost:5000/health
```

## Features Breakdown

### Analysis Sections

1. **📋 Summary** - Quick overview of the startup concept
2. **✅ Strengths** - Key competitive advantages
3. **⚠️ Weaknesses** - Areas needing improvement
4. **🚨 Risks** - Potential failure points
5. **🎯 Competitors** - Similar solutions in the market
6. **💡 Improvement Suggestions** - Actionable next steps
7. **🛣️ MVP Roadmap** - Development phases
8. **Viability Score** - 0-10 rating of the idea
9. **📊 Failure Risk** - Probability assessment

## Troubleshooting

### "Backend not running" error
- Make sure the Flask server is running on `http://localhost:5000`
- Check if port 5000 is available
- Run: `cd backend && python app.py`

### Analysis not working
- If using OpenAI: Verify your API key is set correctly
- Try the fallback mode (works without API key)
- Check browser console for errors (F12)

### Port already in use
Change the port in `backend/app.py`:
```python
app.run(debug=True, port=5001)  # Change 5000 to 5001
```

## Environment Variables

Create a `.env` file (optional) in the backend folder:
```
OPENAI_API_KEY=your-api-key-here
FLASK_ENV=development
FLASK_DEBUG=1
```

## Performance Tips

- **Reduce API costs**: Use the fallback mode for basic analysis
- **Faster response**: Fallback analysis is instant, AI analysis takes 2-5 seconds
- **Multiple instances**: Run multiple backend processes for load balancing

## Future Enhancements

- [ ] Support for multiple AI models
- [ ] Analysis history and comparison
- [ ] Team collaboration features
- [ ] Export to PDF/CSV
- [ ] Advanced metrics dashboard
- [ ] Custom analysis templates

## License

MIT License - Feel free to use and modify!

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API endpoint documentation
3. Check Flask server logs for errors

---

**Made with ❤️ for startup founders and entrepreneurs**

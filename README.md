# 📊 Pipeline Intelligence

**AI-powered sales pipeline risk analysis tool** — Instantly identify deals at risk, understand why, and get actionable recommendations.

![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

---

## 🚀 Quick Start

### Try the Live Demo
👉 **[Launch Pipeline Intelligence](https://pipeline-intelligence.streamlit.app)**

Upload your CRM CSV → Get instant risk analysis with AI insights

### Run Locally
```bash
git clone https://github.com/YOUR-USERNAME/pipeline-intelligence.git
cd pipeline-intelligence
pip install -r requirements.txt
streamlit run app.py
```

Then visit: **http://localhost:8501**

---

## ✨ Features

### 📊 **Risk Scoring Engine** (Phase 1)
- 6 transparent risk signals:
  - Days in stage (stagnant deals)
  - Days since last activity (engagement)
  - Days until close date (urgency)
  - Proposal sent without response (stuck)
  - Stakeholder count (complexity)
  - Days in proposal stage
  
- **Risk Levels:**
  - 🟢 **Healthy** (<30): On track
  - 🟡 **Watch** (30-59): Needs attention
  - 🔴 **At Risk** (60+): Immediate action required

### 🤖 **AI Analysis** (Phase 2)
- Claude AI integration for contextual deal analysis
- Demo mode included (no API key needed)
- For each deal:
  - ✅ Why it's at risk
  - ✅ Recommended actions
  - ✅ Confidence level

### 📥 **Smart CSV Parsing** (Phase 3)
Auto-detects CRM format and normalizes columns:
- ✅ **HubSpot** — Auto-detected
- ✅ **Salesforce** — Auto-detected  
- ✅ **Pipedrive** — Auto-detected
- ✅ **Generic CSV** — Falls back to fuzzy matching

Supports 12 standard fields with fuzzy matching for column names.

### 🎨 **Web Interface** (Phase 4)
- Streamlit-based production app
- Drag & drop CSV upload
- Real-time analysis with progress tracking
- Interactive report with:
  - 4 key metrics
  - Top 5 highest-risk deals
  - Full deals table
  - Strategic recommendations
  - CSV export

---

## 📁 Project Structure

```
pipeline-intelligence/
├── app.py                     # Phase 4: Streamlit web app
├── pipeline_intelligence.py   # Phase 1: Risk scoring engine
├── ai_analyzer.py             # Phase 2: Claude API integration
├── demo_ai_analyzer.py        # Phase 2: Demo mode (no API key)
├── csv_parser.py              # Phase 3: CSV parsing & normalization
├── column_mappings.py         # Phase 3: CRM field definitions
├── config.py                  # Configuration
├── sample-pipeline-raw.csv    # Test data
├── requirements.txt           # Python dependencies
├── QUICKSTART.md              # Quick start guide
├── DEPLOY_TO_GITHUB.md        # GitHub & Streamlit Cloud setup
└── docs/                      # Documentation
```

---

## 🔧 Configuration

### Environment Variables
Create a `.streamlit/secrets.toml` file for optional Claude API key:

```toml
CLAUDE_API_KEY = "your-key-here"
```

Without it, the app runs in demo mode with mock AI analysis.

---

## 📊 Supported CRM Formats

| CRM | Auto-Detect | Example Columns |
|-----|-------------|-----------------|
| **HubSpot** | ✅ Yes | Deal Name, Company, Amount, Pipeline Stage |
| **Salesforce** | ✅ Yes | Opportunity Name, Account, Amount, Stage |
| **Pipedrive** | ✅ Yes | Title, Org Name, Value, Stage |
| **Generic CSV** | ✅ Yes | Fuzzy matches any column names |

---

## 🚢 Deployment

### Option 1: Streamlit Cloud (Recommended - Free)

1. **Push to GitHub**
```bash
git remote add origin https://github.com/YOUR-USERNAME/pipeline-intelligence.git
git push -u origin main
```

2. **Deploy at https://streamlit.io/cloud**
   - Connect your GitHub repo
   - Set main file to `app.py`
   - Deploy (free tier available!)

3. **Share your live URL**
```
https://pipeline-intelligence.streamlit.app
```

### Option 2: Docker

```bash
docker build -t pipeline-intelligence .
docker run -p 8501:8501 pipeline-intelligence
```

### Option 3: Self-Hosted

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8000
```

---

## 💡 How It Works

```
1. User uploads CSV
   ↓
2. Phase 3: Auto-detect columns + normalize data
   ↓
3. Phase 1: Calculate risk scores (6 signals)
   ↓
4. Phase 2: Generate AI insights for each deal
   ↓
5. Phase 4: Display interactive report in Streamlit
   ↓
6. User downloads results as CSV
```

---

## 📈 Example Analysis

**Input:** 30-deal pipeline CSV

**Output:**
- Total Pipeline: $1.53M
- At Risk: $435K (28.4%)
- Avg Risk Score: 39.4/100
- Top 5 deals analyzed with:
  - Risk assessment
  - Why at risk
  - Recommended actions

---

## 🔮 Roadmap

**Future Improvements:**
- [ ] Charts & visualizations (deal distribution, trends)
- [ ] PDF report export
- [ ] Email delivery of reports
- [ ] Real Claude API integration (production)
- [ ] Database for report history persistence
- [ ] User authentication
- [ ] Deal filtering & search
- [ ] Historical trend analysis
- [ ] Slack integration
- [ ] Custom risk scoring rules

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repo
2. Create a feature branch
3. Submit a pull request

---

## 📝 License

MIT License — see LICENSE file

---

## 🆘 Support

### Common Issues

**Q: "ModuleNotFoundError" when uploading**  
A: Ensure `requirements.txt` dependencies are installed:
```bash
pip install -r requirements.txt
```

**Q: CSV not parsing correctly**  
A: Check CSV format and column names. Most CRM exports work automatically.

**Q: AI Analysis not working**  
A: App runs in demo mode by default. Add Claude API key to `.streamlit/secrets.toml` for real analysis.

### Documentation
- 📖 [Quick Start Guide](QUICKSTART.md)
- 📖 [Deployment Guide](DEPLOY_TO_GITHUB.md)
- 📖 [Architecture Docs](docs/README.md)

---

## 👨‍💻 Built With

- **Streamlit** — Web framework
- **Pandas** — Data processing
- **Claude AI** — Natural language analysis (optional)
- **Python 3.8+** — Runtime

---

## 📧 Contact

Questions? Open an issue or reach out at quantomdigitals@gmail.com

---

**Pipeline Intelligence — Ship your sales pipeline analysis in minutes, not months.** 🚀

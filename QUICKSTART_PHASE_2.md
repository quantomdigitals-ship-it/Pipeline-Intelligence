# Phase 2 Quick Start — Claude AI Integration

**Status:** ✅ COMPLETE  
**Files Created:** 3  
**Lines of Code:** ~330  
**Setup Time:** <1 minute  

---

## What You Have Now

### 1. **ai_analyzer.py** — Claude API Integration
Analyzes individual deals and returns contextual explanations.

```python
from ai_analyzer import analyze_deal_with_claude

deal = {"opportunity_name": "Deal X", "amount": 100000, "risk_score": 75, ...}
analysis = analyze_deal_with_claude(deal)
# Returns: {"explanation": "...", "recommended_action": "...", "confidence_level": "High"}
```

### 2. **pipeline_with_ai.py** — Full Pipeline with AI
Processes entire CSV through scoring + AI analysis.

```python
from pipeline_with_ai import analyze_pipeline_full

summary = analyze_pipeline_full('sample-pipeline-raw.csv')
# Returns: full summary with AI insights on all deals
```

### 3. **demo_ai_analyzer.py** — Demo Mode (No API Required)
See example outputs without making API calls.

```bash
python demo_ai_analyzer.py
```

---

## Quick Start (3 Options)

### Option A: Try Demo (Right Now, No Setup)

```bash
cd C:\pipeline-intelligence
python demo_ai_analyzer.py
```

**Output:** Shows 3 sample deals with AI analysis  
**Time:** <1 second  
**Cost:** $0  

---

### Option B: Use Real Claude API (Requires API Key)

**Step 1:** Get API key from https://console.anthropic.com

**Step 2:** Set environment variable (PowerShell)
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-xxx..."
```

**Step 3:** Run full analysis
```bash
cd C:\pipeline-intelligence
python pipeline_with_ai.py
```

**Output:** Full pipeline with real AI analysis  
**Time:** ~1-2 minutes for 30 deals  
**Cost:** ~$0.01 per run  

---

### Option C: Use in Your Own Code

```python
from pipeline_with_ai import analyze_pipeline_full, print_full_analysis

summary = analyze_pipeline_full('your-file.csv')
print_full_analysis(summary)

# Or get individual deals:
for deal in summary['all_deals']:
    if deal['risk_score'] >= 60:
        print(f"{deal['opportunity_name']}: {deal['ai_analysis']['explanation']}")
```

---

## What It Produces

```
CloudFirst Migration — CloudFirst
Amount: $120,000 | Score: 57/100 (Watch)

📌 WHY AT RISK:
   Deal shows early warning signs with long gaps between activities,
   suggesting buyer deprioritization.

✅ RECOMMENDED ACTION:
   Confirm buyer still engaged; propose trial or pilot to re-energize discussion.

Confidence: High
```

---

## Files Summary

| File | Purpose | Status |
|------|---------|--------|
| `ai_analyzer.py` | Claude API integration | ✅ Ready |
| `pipeline_with_ai.py` | Full pipeline orchestration | ✅ Ready |
| `demo_ai_analyzer.py` | Testing without API | ✅ Ready |
| `docs/PHASE_2_AI_INTEGRATION.md` | Full documentation | ✅ Ready |

---

## What's Next?

### For Testing:
1. Try demo mode first (no setup)
2. Set API key if you want real analysis
3. Integrate into Phase 3 (Streamlit UI)

### For Development:
Phase 3: CSV Handling (Days 6-7)
- Build column auto-detection
- Support multiple CRM formats
- Then integrate with Streamlit

---

## API Key Setup (Permanent)

**Windows Environment Variable:**
1. Press `Win + X` → System
2. Advanced system settings → Environment Variables
3. New → Variable name: `ANTHROPIC_API_KEY`
4. Variable value: `sk-ant-...`
5. Click OK, restart terminal

**PowerShell (Current Session Only):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

---

## Troubleshooting

**"ModuleNotFoundError: No module named 'anthropic'"**
```bash
pip install anthropic
```

**"Invalid API key"**
- Verify key is set: `echo $env:ANTHROPIC_API_KEY`
- Check key is valid at https://console.anthropic.com
- Make sure there are no extra spaces in the key

**"Rate limited"**
- Normal with many sequential calls
- Demo mode has no rate limits

---

## Cost Analysis

| Scenario | Deals | Cost |
|----------|-------|------|
| Demo (unlimited) | 30 | $0.00 |
| 1 pipeline | 30 | $0.01 |
| 10 pipelines | 300 | $0.10 |
| 100 pipelines | 3000 | $1.00 |

---

## Next Steps

**Ready to move to Phase 3?**

Phase 3 (Sept 18-19):
- Build CSV parser
- Auto-detect columns
- Support HubSpot, Salesforce, Pipedrive, etc.
- Then: Streamlit UI

Let's ship! 🚀

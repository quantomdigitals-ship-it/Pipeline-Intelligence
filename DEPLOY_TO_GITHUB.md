# Deploy to GitHub & Streamlit Cloud

Your code is ready! Follow these **3 simple steps** to deploy:

---

## **Step 1: Create GitHub Repository**

1. Go to https://github.com/new
2. **Repository name:** `pipeline-intelligence`
3. **Description:** Pipeline risk analysis tool with AI insights
4. **Visibility:** Public
5. Click **"Create repository"**

---

## **Step 2: Push Code to GitHub**

Copy & paste these commands in PowerShell:

```powershell
cd C:\pipeline-intelligence

# Add remote (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/pipeline-intelligence.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**That's it!** Your code is now on GitHub ✅

---

## **Step 3: Deploy to Streamlit Cloud**

1. Go to https://streamlit.io/cloud
2. Click **"New app"**
3. Select your repo: `YOUR-USERNAME/pipeline-intelligence`
4. Set:
   - **Main file path:** `app.py`
   - **Python version:** 3.11
5. Click **"Deploy"**

**Wait 1-2 minutes...** Your app goes live! 🚀

---

## **Your Live URL Will Be:**

```
https://pipeline-intelligence.streamlit.app
```

---

## **Share with Clients!**

Send them the link → They can:
- Upload their CSV
- Get instant risk analysis
- See AI recommendations
- Download results

---

## **What's Deployed**

✅ **Phase 1:** Risk scoring engine (6 signals)  
✅ **Phase 2:** AI analysis & insights  
✅ **Phase 3:** CSV parsing (auto-detect columns)  
✅ **Phase 4:** Streamlit web interface  

---

## **Troubleshooting**

**Problem:** "requirements.txt not found"  
**Fix:** Create `requirements.txt` in root:
```
streamlit>=1.28.0
pandas>=2.0.0
```

**Problem:** "ModuleNotFoundError: No module named 'csv_parser'"  
**Fix:** Already included! All files are in root directory.

**Problem:** App won't load CSV  
**Fix:** Check browser console (F12) for errors. Usually encoding issue.

---

## **Next Steps**

Once deployed:
1. Test with sample data
2. Test with real CSV
3. Share link with clients
4. Collect feedback
5. Add improvements (charts, email export, etc.)

---

**You're shipping! 🎉**

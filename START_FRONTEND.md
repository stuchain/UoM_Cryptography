# 🚀 Quick Start - Frontend Demo

## Step 1: Install Dependencies

```bash
# Make sure you're in the project root
pip install flask flask-cors

# Or install all requirements at once
pip install -r requirements.txt
```

## Step 2: Start the Server

```bash
# From project root
python frontend/app.py
```

You should see:
```
============================================================
Secure Channel Demo Frontend
============================================================

Starting Flask server...
Open your browser to: http://localhost:5000

Press Ctrl+C to stop the server
============================================================
```

## Step 3: Open in Browser

Navigate to: **http://localhost:5000**

## Step 4: Use the Interface

1. Click any phase button to run that phase
2. Or click "Run All Phases" to execute everything
3. Watch the visualizations update in real-time!

## 🎨 What You Get

- **Interactive UI**: Modern, colorful interface
- **Real-time Charts**: Chart.js visualizations for each phase
- **Status Indicators**: See what's running
- **Detailed Results**: Key comparisons, attack results, encryption metrics

## 📊 Features

### Phase 1: Key Comparison Chart
- Bar chart showing if Alice and Bob's keys match

### Phase 2: MITM Attack Visualization  
- Shows all 4 keys (Alice, Bob, Mallory↔Alice, Mallory↔Bob)
- Visual demonstration of attack success

### Phase 3: Authentication Status
- Doughnut chart showing signature validity, key matching, attack prevention

### Phase 4: Encryption Metrics
- Message size comparison (original vs encrypted)
- Shows encryption overhead

### Phase 5: Blockchain Verification
- Status of key registration and verification on blockchain

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
**Solution**: Run `pip install flask flask-cors`

### Port 5000 already in use
**Solution**: Edit `frontend/app.py` and change `port=5000` to `port=5001`

### Charts not loading
**Solution**: 
- Check internet connection (Chart.js loads from CDN)
- Check browser console (F12) for errors
- Try hard refresh (Ctrl+F5)

### "Cannot find module" errors
**Solution**: Make sure you're running from project root:
```bash
cd secure_channel  # project root
python frontend/app.py
```

## 💡 Tips

- **For Presentation**: Run phases one at a time and explain each visualization
- **For Quick Demo**: Click "Run All Phases" and watch everything happen
- **For Screenshots**: Great visualizations for your report!

---

**Enjoy your interactive demo! 🎉**



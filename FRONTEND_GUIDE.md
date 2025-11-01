# 🎨 Frontend Demo Guide

Quick guide for using the interactive web frontend.

## 🚀 Starting the Frontend

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Run the Flask server
python frontend/app.py
```

Then open: **http://localhost:5000**

## 📱 Using the Interface

### Main Features

1. **Phase Buttons**: Click any phase button to run that specific phase
2. **Run All**: Click "Run All Phases" to execute everything sequentially
3. **Status Indicators**: 
   - Gray = Not run yet
   - Orange = Running
   - Green = Success
   - Red = Error

### What You'll See

Each phase card shows:
- Phase number and title
- Status indicator
- Results with visualizations
- Summary of what happened

### Phase-Specific Visualizations

**Phase 1 (Basic DH)**:
- Comparison of Alice's and Bob's keys
- Shows if keys match (green) or differ (red)

**Phase 2 (MITM Attack)**:
- All 4 keys visualized
- Clearly shows Alice and Bob have different keys
- Demonstrates attack success

**Phase 3 (Authenticated DH)**:
- Authentication status chart
- Shows signatures valid, keys match, attack prevented

**Phase 4 (Secure Channel)**:
- Message size comparison
- Shows encryption overhead
- Security properties status

**Phase 5 (Blockchain)**:
- Blockchain verification status
- Shows which keys are registered and verified

## 🎯 Demo Flow

### For Presentation:

1. **Introduction**: Show the interface
2. **Phase 1**: "Watch - Alice and Bob derive the same key"
3. **Phase 2**: "But look - MITM attack succeeds, keys differ!"
4. **Phase 3**: "Here's the fix - signatures prevent the attack"
5. **Phase 4**: "Now messages are encrypted securely"
6. **Phase 5**: "Blockchain adds decentralized trust"

### Quick Demo:
Just click "Run All Phases" and watch everything happen!

## 💻 Technical Details

- **Backend**: Flask (Python) serving REST API
- **Frontend**: HTML/CSS/JavaScript with Chart.js
- **Charts**: Interactive Chart.js visualizations
- **Real-time**: Updates as phases complete

## 🔧 Troubleshooting

**Server won't start?**
- Check if port 5000 is in use
- Make sure Flask is installed: `pip install flask flask-cors`

**Charts not showing?**
- Check browser console (F12)
- Ensure internet connection (Chart.js loads from CDN)
- Try refreshing the page

**Errors in phase execution?**
- Check that all dependencies are installed
- Verify Python version (3.10+)
- Check terminal for error messages

## 📸 Screenshot Tips

Great for including in your report:
- Phase 1 showing matching keys
- Phase 2 showing different keys (attack success)
- Phase 3 showing attack prevention
- Phase 4 showing encryption
- Phase 5 showing blockchain verification

---

**The frontend makes it easy to demonstrate and visualize all phases! 🎉**



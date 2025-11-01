# 🎨 Secure Channel Demo - Interactive Frontend

Interactive web-based frontend for demonstrating all phases of the secure channel project with real-time visualizations.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# From project root
pip install -r requirements.txt
```

### 2. Run the Frontend Server

```bash
# From project root
cd frontend
python app.py
```

Or from project root:

```bash
python frontend/app.py
```

### 3. Open in Browser

Navigate to: **http://localhost:5000**

## 📋 Features

### Interactive Phase Controls
- **Individual Phase Buttons**: Run each phase independently
- **Run All Phases**: Execute all phases sequentially
- **Real-time Status Indicators**: See which phase is running

### Visualizations
Each phase includes interactive charts and graphs:
- **Phase 1**: Key comparison chart showing if Alice and Bob derived the same key
- **Phase 2**: MITM attack visualization showing key mismatches
- **Phase 3**: Authentication status (signatures, key matching, attack prevention)
- **Phase 4**: Encryption metrics (message sizes, overhead, security properties)
- **Phase 5**: Blockchain verification status

### Results Display
- **Key Comparisons**: Visual comparison of derived keys
- **Attack Results**: Clear indication of attack success/failure
- **Security Properties**: Check marks for confidentiality, integrity, authentication
- **Blockchain Status**: Registration and verification status

## 🎯 Usage

1. **Start the server** (see Quick Start above)
2. **Open browser** to http://localhost:5000
3. **Click any phase button** to run that phase
4. **View results** in the phase card below
5. **Analyze charts** showing cryptographic operations

## 🏗️ Architecture

```
frontend/
├── app.py              # Flask backend API
├── templates/
│   └── index.html      # Main frontend HTML
└── static/
    ├── main.js         # Frontend JavaScript
    └── style.css       # Additional styles
```

### Backend (Flask)
- REST API endpoints for each phase (`/api/phase1`, `/api/phase2`, etc.)
- Runs cryptographic operations and returns JSON results
- Handles errors gracefully

### Frontend (HTML/JS)
- Interactive UI with Chart.js visualizations
- Real-time status updates
- Dynamic result display

## 📊 Visualization Types

### Phase 1: Key Comparison
- Bar chart comparing Alice's and Bob's shared keys
- Green if keys match, red if different

### Phase 2: MITM Attack
- Bar chart showing all 4 keys (Alice, Bob, Mallory↔Alice, Mallory↔Bob)
- Visualizes how MITM attack creates different keys

### Phase 3: Authentication
- Doughnut chart showing:
  - Signature validity
  - Key matching
  - Attack prevention

### Phase 4: Encryption
- Bar chart showing:
  - Original message size
  - Encrypted message size
  - Encryption overhead

### Phase 5: Blockchain
- Bar chart showing verification status for Alice and Bob

## 🐛 Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```python
# Edit frontend/app.py, change:
app.run(debug=True, host='0.0.0.0', port=5000)
# To:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Module Import Errors
Make sure you're running from the project root:
```bash
cd secure_channel
python frontend/app.py
```

### Charts Not Displaying
- Check browser console for JavaScript errors
- Ensure Chart.js is loading (check network tab)
- Try hard refresh (Ctrl+F5)

## 💡 Tips for Presentation

1. **Start with Phase 1**: Show basic key exchange
2. **Run Phase 2**: Demonstrate the vulnerability
3. **Run Phase 3**: Show how authentication fixes it
4. **Run Phase 4**: Show full secure channel
5. **Run Phase 5**: Show blockchain integration
6. **Or use "Run All"**: For a complete demo

The visualizations automatically update with each phase run, making it easy to compare results and explain concepts.

## 🎓 Educational Value

This frontend is perfect for:
- **Classroom demonstrations**: Interactive and visual
- **Recorded presentations**: Easy to follow along
- **Self-study**: Understand each phase visually
- **Report documentation**: Screenshots of visualizations

## 🔧 Customization

### Adding More Visualizations
Edit `frontend/static/main.js` and add new chart functions.

### Changing Colors/Styles
Edit `frontend/templates/index.html` (inline styles) or `frontend/static/style.css`.

### Adding New Phases
1. Add endpoint in `frontend/app.py` (`/api/phase6`)
2. Add button in `frontend/templates/index.html`
3. Add display function in `frontend/static/main.js`

---

**Enjoy the interactive demo! 🚀**



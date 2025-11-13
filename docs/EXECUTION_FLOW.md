# 🔄 Execution Flow - Complete Guide

**Detailed explanation of what happens when you run the application, from clicking `run.bat` to executing phases and displaying results.**

---

## 📋 Table of Contents

1. [Quick Overview](#quick-overview)
2. [Startup Flow](#startup-flow)
3. [Application Runtime](#application-runtime)
4. [Phase Execution Flow](#phase-execution-flow)
5. [Complete Flow Diagram](#complete-flow-diagram)
6. [File Execution Order](#file-execution-order)

---

## 🎯 Quick Overview

When you run the application, here's what happens:

```
1. User clicks run.bat
   ↓
2. run.bat calls scripts/run.bat
   ↓
3. scripts/run.bat checks Python, installs dependencies
   ↓
4. scripts/run.bat starts backend/app.py
   ↓
5. Flask server starts on port 5000
   ↓
6. Browser opens to http://localhost:5000
   ↓
7. User clicks "Phase 1" button
   ↓
8. JavaScript sends POST /api/phase1
   ↓
9. Flask executes phase code
   ↓
10. Results displayed in browser
```

---

## 🚀 Startup Flow

### Step 1: User Initiates Launch

**Action:** User double-clicks `run.bat` (or runs `./run.sh` on macOS/Linux)

**File:** `run.bat` (root directory)

**What it does:**
```batch
@echo off
cd /d "%~dp0"           # Change to script directory
call scripts\run.bat    # Call the main launcher script
```

**Purpose:** Simple wrapper that calls the main launcher in `scripts/` folder

---

### Step 2: Main Launcher Script

**File:** `scripts/run.bat` (Windows) or `scripts/run.sh` (macOS/Linux)

**What it does:**

#### 2.1: Check Python Installation
```batch
python --version
```
- Verifies Python 3.10+ is installed
- Checks if Python is in PATH
- **If fails:** Shows error message and exits

#### 2.2: Check Project Files
```batch
if not exist "requirements.txt" (
    echo ERROR: Project files not found!
    exit
)
```
- Verifies we're in the correct directory
- Checks for `requirements.txt`
- **If fails:** Shows error and exits

#### 2.3: Check/Install Dependencies
```batch
python -c "import flask"
if errorlevel 1 (
    pip install -r requirements.txt
)
```
- Checks if Flask is installed
- If not, installs all dependencies from `requirements.txt`
- Installs: `flask`, `flask-cors`, `cryptography`, etc.

#### 2.4: Check Backend and Frontend
```batch
if not exist "backend\app.py" (
    echo ERROR: Backend not found!
    exit
)
if not exist "frontend\templates\index.html" (
    echo ERROR: Frontend not found!
    exit
)
```
- Verifies `backend/app.py` exists
- Verifies `frontend/templates/index.html` exists
- **If fails:** Shows error and exits

#### 2.5: Start Flask Server
```batch
cd backend
python app.py
```
- Changes to `backend/` directory
- Starts Flask application
- Server runs on `http://localhost:5000`

#### 2.6: Open Browser
```batch
timeout /t 2 /nobreak
start http://localhost:5000
```
- Waits 2 seconds for server to start
- Opens default browser to `http://localhost:5000`

---

### Step 3: Flask Server Initialization

**File:** `backend/app.py`

**What happens:**

#### 3.1: Import Dependencies
```python
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import sys
import os
```

#### 3.2: Setup Flask App
```python
# Flask app with paths pointing to frontend folder
frontend_dir = os.path.join(project_root, 'frontend')
app = Flask(__name__, 
            template_folder=os.path.join(frontend_dir, 'templates'),
            static_folder=os.path.join(frontend_dir, 'static'))
CORS(app)  # Enable CORS for frontend-backend communication
```

#### 3.3: Import Phase Modules
```python
from phases.phase1_dh.dh_exchange import generate_x25519_keypair, ...
from cryptography.hazmat.primitives.asymmetric import ed25519
# ... other imports
```

#### 3.4: Define Routes
```python
@app.route('/')                    # Main page
@app.route('/api/phase1', methods=['POST'])  # Phase 1 endpoint
@app.route('/api/phase2', methods=['POST'])  # Phase 2 endpoint
# ... all phase endpoints
@app.route('/api/run-all', methods=['POST'])  # Run all phases
```

#### 3.5: Start Server
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

**Server is now running and listening for requests!**

---

### Step 4: Browser Loads Frontend

**What happens:**

1. Browser requests `http://localhost:5000/`
2. Flask (from `backend/app.py`) serves `frontend/templates/index.html`
3. HTML loads:
   - CSS styles (`frontend/static/style.css`)
   - JavaScript (`frontend/static/main.js`)
   - Chart.js library (from CDN)
4. JavaScript initializes:
   - Creates phase cards
   - Sets up event listeners
   - Ready for user interaction

---

## 🏃 Application Runtime

### User Interface Ready

The browser now shows:
- Header with project title
- Control buttons (Phase 1-6, Run All)
- Phase cards (one for each phase)
- Each card shows "Click button above to run this phase"

### User Clicks "Phase 1" Button

**What happens:**

#### 1. JavaScript Event Handler
**File:** `frontend/static/main.js`

```javascript
function runPhase(phaseNum) {
    updateStatus(phaseNum, 'running');  // Show loading indicator
    const response = await fetch(`/api/phase${phaseNum}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    });
    const data = await response.json();
    displayPhaseResults(phaseNum, data);  // Update UI with results
}
```

#### 2. HTTP Request Sent
- **Method:** POST
- **URL:** `http://localhost:5000/api/phase1`
- **Headers:** `Content-Type: application/json`
- **Body:** Empty (no data needed)

#### 3. Flask Receives Request
**File:** `backend/app.py`

```python
@app.route('/api/phase1', methods=['POST'])
def run_phase1():
    try:
        # Execute Phase 1 code
        # Return JSON results
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
```

---

## ⚙️ Phase Execution Flow

### Detailed Flow for Phase 1

**File:** `backend/app.py`

#### Step 1: Flask Route Handler
```python
@app.route('/api/phase1', methods=['POST'])
def run_phase1():
```

#### Step 2: Generate Keys
```python
# Alice generates keypair
alice_priv, alice_pub = generate_x25519_keypair()
alice_pub_bytes = public_bytes(alice_pub)

# Bob generates keypair
bob_priv, bob_pub = generate_x25519_keypair()
bob_pub_bytes = public_bytes(bob_pub)
```

#### Step 3: Derive Shared Keys
```python
# Alice derives shared key
alice_key = derive_shared_key(alice_priv, bob_pub_bytes)

# Bob derives shared key
bob_key = derive_shared_key(bob_priv, alice_pub_bytes)
```

#### Step 4: Build Response
```python
return jsonify({
    'success': True,
    'phase': 1,
    'title': 'Basic Diffie-Hellman Key Exchange',
    'steps': [...],  # Step-by-step information
    'data': {
        'alice': {...},
        'bob': {...},
        'keys_match': alice_key == bob_key
    },
    'visualization': {...},
    'summary': '...'
})
```

#### Step 5: JavaScript Receives Response
```javascript
const data = await response.json();
// data contains all the phase results
```

#### Step 6: Update UI
```javascript
displayPhase1Results(contentDiv, data);
// Updates the phase card with:
// - Step-by-step information
// - Key displays
// - Charts
// - Summary
```

---

## 📊 Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    USER ACTION                               │
│              Double-click run.bat                            │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              ROOT: run.bat                                   │
│  - Changes to script directory                               │
│  - Calls scripts/run.bat                                      │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│           SCRIPTS: run.bat / run.sh                          │
│  1. Check Python installation                                │
│  2. Check project files                                      │
│  3. Install dependencies (if needed)                         │
│  4. Check backend/app.py and frontend/templates/              │
│  5. Start Flask server                                       │
│  6. Open browser                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              FRONTEND: app.py                                │
│  - Initialize Flask app                                      │
│  - Import phase modules                                      │
│  - Define API routes                                         │
│  - Start server on port 5000                                 │
│  - Listen for HTTP requests                                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│                    BROWSER                                   │
│  - Loads index.html                                         │
│  - Loads main.js                                            │
│  - Loads style.css                                          │
│  - Initializes phase cards                                   │
│  - Ready for user interaction                                │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│              USER CLICKS "Phase 1"                           │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         JAVASCRIPT: main.js                                   │
│  - runPhase(1) called                                        │
│  - Sends POST /api/phase1                                    │
│  - Shows loading indicator                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ HTTP POST Request
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         FLASK: app.py - /api/phase1                           │
│  - Receives POST request                                     │
│  - Calls run_phase1() function                               │
│  - Executes phase code                                       │
│  - Returns JSON response                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Python Imports
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         PHASES: phase1_dh/dh_exchange.py                      │
│  - generate_x25519_keypair()                                 │
│  - public_bytes()                                            │
│  - derive_shared_key()                                        │
│  - Returns cryptographic results                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ Results
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         FLASK: Formats JSON Response                          │
│  - Adds step-by-step information                             │
│  - Adds visualization data                                   │
│  - Adds summary                                              │
│  - Returns to JavaScript                                     │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ JSON Response
                        ▼
┌─────────────────────────────────────────────────────────────┐
│         JAVASCRIPT: Receives Response                         │
│  - Parses JSON data                                          │
│  - Calls displayPhase1Results()                              │
│  - Updates UI with results                                   │
│  - Creates charts                                            │
│  - Shows success indicator                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 File Execution Order

### Startup Sequence

1. **`run.bat`** (root)
   - Entry point
   - Calls `scripts/run.bat`

2. **`scripts/run.bat`** (or `scripts/run.sh`)
   - Main launcher
   - Checks environment
   - Installs dependencies
   - Starts Flask

3. **`backend/app.py`**
   - Flask server
   - Defines routes
   - Starts HTTP server

4. **`frontend/templates/index.html`**
   - Loaded by browser
   - Defines UI structure

5. **`frontend/static/main.js`**
   - Loaded by browser
   - Handles user interactions
   - Makes API calls
   - Updates UI

### Phase Execution Sequence

When user clicks "Phase 1":

1. **`frontend/static/main.js`**
   - `runPhase(1)` function
   - Sends HTTP request

2. **`backend/app.py`**
   - `@app.route('/api/phase1')`
   - `run_phase1()` function

3. **`phases/phase1_dh/dh_exchange.py`**
   - `generate_x25519_keypair()`
   - `public_bytes()`
   - `derive_shared_key()`

4. **`backend/app.py`**
   - Formats results
   - Returns JSON

5. **`frontend/static/main.js`**
   - `displayPhase1Results()`
   - Updates UI

---

## 🔍 Key Points

### 1. Two Separate Processes

**Backend (Flask):**
- Runs continuously
- Listens for HTTP requests
- Executes phase code
- Returns JSON responses

**Frontend (Browser):**
- Loads once
- Makes HTTP requests
- Displays results
- Updates UI dynamically

### 2. Stateless Design

- Each phase execution is independent
- No state is stored between requests
- Each request generates fresh results
- Phases don't depend on previous executions

### 3. Modular Architecture

- Each phase is a separate Python module
- Can be run standalone or via API
- Functions can be imported and reused
- Clear separation of concerns

### 4. Error Handling

**At Each Level:**
- Launcher: Checks prerequisites
- Flask: Catches exceptions, returns error JSON
- JavaScript: Handles failed requests, shows error messages

---

## 🎓 Understanding the Flow

### Why This Design?

**Educational:**
- Clear separation makes it easy to understand
- Each component has a single responsibility
- Students can trace execution flow

**Flexible:**
- Phases can be run independently
- Can be used via API or command line
- Easy to extend with new phases

**User-Friendly:**
- Simple launcher script
- Automatic dependency installation
- Browser-based interface

---

## 📚 Related Documentation

- **[HOW_TO_RUN.md](HOW_TO_RUN.md)** - How to run the application
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[FRONTEND_DETAILED.md](FRONTEND_DETAILED.md)** - Frontend implementation details
- **[PHASE1_DETAILED.md](PHASE1_DETAILED.md)** - Phase 1 execution details

---

**Last Updated:** December 2024


# 🚀 How to Run - Secure Channel Demo

This guide provides step-by-step instructions to install and run the Secure Channel Demo project.

---

## ⚡ SUPER SIMPLE - Just Run This!

**For Windows users - the easiest way:**

1. **Double-click `run.bat`** (or right-click and select "Run")
   - The script will automatically:
     - Check if Python is installed
     - Install dependencies if needed
     - Start the server
     - Open your browser

2. **That's it!** The app will open at `http://localhost:5000`

**Note:** If `run.bat` doesn't work, you can also use `RUN_ME.bat` which has the same functionality.

**Alternative (PowerShell):**
- Right-click `run.ps1` → "Run with PowerShell"
- If you get an execution policy error, run this first in PowerShell:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

**For macOS/Linux users:**
1. Make the script executable:
   ```bash
   chmod +x run.sh
   ```
2. Run it:
   ```bash
   ./run.sh
   ```
- Or see the [Manual Installation](#-installation) section below

---

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Individual Phases](#running-individual-phases)
- [Running the Interactive Frontend](#running-the-interactive-frontend)
- [Troubleshooting](#troubleshooting)

---

## 🔧 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Python 3.10 or higher**
   - Check your version: `python --version` or `python3 --version`
   - Download from: https://www.python.org/downloads/
   - **Important**: During installation, check "Add Python to PATH"

2. **pip** (Python package manager)
   - Usually comes with Python
   - Check: `pip --version` or `pip3 --version`

### Optional (for Solana/Blockchain Phase)

3. **Rust** (for Solana smart contracts)
   - Only needed for Phase 6 (Blockchain Integration)
   - Install from: https://www.rust-lang.org/tools/install

4. **Solana CLI** (for blockchain deployment)
   - Only needed for Phase 6
   - Install from: https://docs.solana.com/cli/install-solana-cli-tools

5. **Anchor Framework** (for Solana development)
   - Only needed for Phase 6
   - Install from: https://www.anchor-lang.com/docs/installation

---

## 📦 Installation

### Step 1: Clone or Download the Project

If you have the project in a folder, navigate to it:

```bash
cd path/to/secure_channel
```

### Step 2: Create a Virtual Environment (Recommended)

Creating a virtual environment isolates the project dependencies:

**Windows:**
```powershell
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command prompt.

### Step 3: Install Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `cryptography` - For X25519, Ed25519, ChaCha20-Poly1305
- `pynacl` - Additional cryptographic primitives
- `solana` - Solana blockchain integration
- `anchorpy` - Anchor framework Python bindings
- `matplotlib` - For generating diagrams
- `numpy` - Numerical computations
- `flask` - Web framework for frontend
- `flask-cors` - CORS support for Flask

### Step 4: Verify Installation

Test that everything is installed correctly:

```bash
python test_env.py
```

You should see:
```
[SUCCESS] All required packages are installed!
```

If you see any errors, check the [Troubleshooting](#troubleshooting) section.

---

## 🎮 Running Individual Phases

You can run each cryptographic phase independently to understand the progression:

### Phase 1: Basic Diffie-Hellman Key Exchange

Demonstrates the fundamental key exchange protocol:

```bash
python phases/phase1_dh/dh_exchange.py
```

**What you'll see:**
- Alice and Bob generate key pairs
- They exchange public keys
- They derive a shared secret
- The shared keys match (demonstrating successful key exchange)

### Phase 2: MITM Attack Demonstration

Shows how an attacker can intercept and manipulate the key exchange:

```bash
python phases/phase2_mitm/mallory_attack.py
```

**What you'll see:**
- Mallory (the attacker) intercepts messages
- Alice and Bob unknowingly establish keys with Mallory
- Mallory can decrypt and read all messages
- Demonstration of the vulnerability in unauthenticated protocols

### Phase 3: Authenticated Diffie-Hellman

Fixes the MITM vulnerability using digital signatures:

```bash
python phases/phase3_auth/authenticated_dh.py
```

**What you'll see:**
- Alice and Bob sign their public keys with Ed25519
- Signature verification prevents Mallory's attack
- Successful authenticated key exchange

### Phase 4: Secure Channel with AEAD

Complete secure channel with authenticated encryption:

```bash
python phases/phase4_aead/secure_channel.py
```

**What you'll see:**
- Authenticated key exchange
- Message encryption using ChaCha20-Poly1305
- Successful message transmission
- Tampering detection demonstration

### Phase 5: Blockchain Integration (Optional)

Solana-based decentralized key registry:

```bash
python phases/phase5_solana/solana_registry_client.py
```

**Note:** This requires Solana CLI and Anchor to be installed. See [Prerequisites](#prerequisites).

### Run All Phases Sequentially

To see all phases in action:

```bash
python demo_all_phases.py
```

This runs all phases in order and provides a comprehensive overview.

---

## 🌐 Running the Interactive Frontend

The interactive web frontend provides a visual interface to test each phase with graphs and detailed step-by-step information.

### Step 1: Navigate to Backend Directory

```bash
cd backend
```

### Step 2: Start the Flask Server

**Windows:**
```powershell
python app.py
```

**macOS/Linux:**
```bash
python3 app.py
```

You should see output like:
```
============================================================
Secure Channel Demo - Backend Server
============================================================

Starting Flask server...
Open your browser to: http://localhost:5000

Press Ctrl+C to stop the server
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Open your web browser and navigate to:

```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

### Step 4: Use the Interface

1. Click on any phase button (Phase 1, Phase 2, etc.)
2. Wait for the phase to execute (you'll see a loading indicator)
3. View the results:
   - Detailed step-by-step information
   - Visual graphs and charts
   - Cryptographic data (keys, signatures, ciphertexts)
   - Security analysis

### Step 5: Stop the Server

Press `Ctrl+C` in the terminal to stop the Flask server.

---

## 🔍 Troubleshooting

### Problem: `python: command not found`

**Solution:**
- Use `python3` instead of `python` on macOS/Linux
- On Windows, ensure Python is added to PATH during installation
- Reinstall Python and check "Add Python to PATH"

### Problem: `pip: command not found`

**Solution:**
- Use `pip3` instead of `pip` on macOS/Linux
- On Windows, try `python -m pip` instead of `pip`

### Problem: `ModuleNotFoundError: No module named 'flask'`

**Solution:**
- Ensure you're in the virtual environment (see `(venv)` in prompt)
- Reinstall dependencies: `pip install -r requirements.txt`
- Check that you're using the correct Python interpreter

### Problem: `UnicodeEncodeError` or encoding errors

**Solution:**
- This is already fixed in the code (ASCII-safe output)
- If you still see errors, ensure your terminal supports UTF-8
- On Windows, try using PowerShell or Windows Terminal instead of Command Prompt

### Problem: Port 5000 is already in use

**Solution:**
- Find the process using port 5000:
  - **Windows:** `netstat -ano | findstr :5000`
  - **macOS/Linux:** `lsof -i :5000`
- Kill the process or use a different port
- To use a different port, edit `backend/app.py` and change `port=5000` to another number (e.g., `port=5001`)

### Problem: `localhost refused to connect`

**Solution:**
- Ensure the Flask server is running (check terminal output)
- Try `http://127.0.0.1:5000` instead of `http://localhost:5000`
- Check Windows Firewall settings
- Ensure no antivirus is blocking the connection

### Problem: Frontend shows errors when running phases

**Solution:**
- Check the terminal running Flask for error messages
- Ensure all Python dependencies are installed
- Verify you're in the project root directory structure
- Check that all phase files exist in their respective directories

### Problem: Solana/Blockchain phase doesn't work

**Solution:**
- Phase 6 is optional - you can skip it if you don't need blockchain features
- Ensure Rust, Solana CLI, and Anchor are installed
- Configure Solana: `solana config set --url devnet`
- Check that you have a Solana wallet configured

### Problem: Virtual environment not activating

**Windows:**
- If you get an execution policy error, run:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
- Then try activating again: `venv\Scripts\activate`

**macOS/Linux:**
- Ensure you're using `source venv/bin/activate` (not just `venv/bin/activate`)

---

## 📝 Quick Start Summary

For a quick start without reading everything:

1. **Install Python 3.10+**
2. **Navigate to project folder**
3. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Run frontend:**
   ```bash
cd backend
python app.py
   ```
6. **Open browser:** `http://localhost:5000`

---

## 🎓 Next Steps

After successfully running the project:

1. **Explore each phase** using the interactive frontend
2. **Read the README.md** to understand what's happening in each phase
3. **Review the code** - all files have detailed comments
4. **Experiment** - try modifying parameters and see what happens
5. **Check DEMO_GUIDE.md** for detailed explanations of each phase

---

## 💡 Tips

- **Use the frontend** for the best experience - it provides visualizations and detailed explanations
- **Read the code comments** - every file has extensive documentation
- **Start with Phase 1** and progress sequentially to understand the evolution
- **The frontend shows step-by-step details** - perfect for learning and presentations

---

## 📞 Need Help?

If you encounter issues not covered here:

1. Check the terminal output for specific error messages
2. Verify all prerequisites are installed correctly
3. Ensure you're using the correct Python version (3.10+)
4. Try running individual phases from the command line to isolate issues

---

**Last Updated:** December 2024



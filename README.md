# 🔐 Secure Channel Demo

**Cryptography Course Assignment - University of Macedonia**

A comprehensive demonstration of building a secure communication channel, from basic key exchange to blockchain-integrated authentication.

---

## ⚡ Quick Start

### Windows
**Just double-click `run.bat`** - that's it!

### macOS / Linux
**Just run `./run.sh`** - that's it!

Or if you prefer:
```bash
bash run.sh
```

The app will open automatically at `http://localhost:5000`

---

## 📁 Project Structure

```
secure_channel/
├── run.bat                 # Quick launcher (Windows)
├── run.sh                  # Quick launcher (macOS/Linux)
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
├── phases/                # All implementation phases
│   ├── phase1_dh/         # Basic Diffie-Hellman
│   ├── phase2_mitm/        # MITM attack demo
│   ├── phase3_auth/        # Authenticated DH
│   ├── phase4_aead/        # Secure channel with AEAD
│   ├── phase5_solana/      # Blockchain integration
│   ├── phase6_blockchain_attack/  # Blockchain attack prevention
│   └── visualizations/     # Diagram generators
│
├── frontend/               # Web interface
│   ├── app.py             # Flask backend
│   ├── templates/         # HTML templates
│   └── static/            # CSS & JavaScript
│
├── scripts/                # Utility scripts
│   ├── run.bat            # Windows launcher
│   ├── run.ps1             # PowerShell version
│   ├── run.sh              # macOS/Linux launcher
│   ├── demo_all_phases.py  # Run all phases
│   └── test_env.py         # Environment checker
│
└── docs/                   # Additional documentation
```

---

## 🎯 What This Demonstrates

1. **Phase 1: Basic Diffie-Hellman** - X25519 key exchange
2. **Phase 2: MITM Attack** - Vulnerability demonstration
3. **Phase 3: Authenticated DH** - Ed25519 signatures prevent attacks
4. **Phase 4: Secure Channel** - ChaCha20-Poly1305 AEAD encryption
5. **Phase 5: Blockchain** - Solana-based key registry
6. **Phase 6: Blockchain Attack Prevention** - Mallory's attacks on blockchain, all prevented

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- Internet connection (for first-time setup)

### Automatic Setup
The launcher script (`run.bat` or `scripts/run.sh`) will automatically:
- ✅ Check Python installation
- ✅ Install all dependencies
- ✅ Start the server
- ✅ Open your browser

### Manual Setup
```bash
pip install -r requirements.txt
cd frontend
python app.py
```

---

## 🚀 Usage

### Interactive Web Interface (Recommended)
1. Run `run.bat` (or `scripts/run.sh`)
2. Browser opens automatically
3. Click phase buttons to test each cryptographic protocol
4. View step-by-step details, visualizations, and results

### Command Line
Run individual phases:
```bash
python phases/phase1_dh/dh_exchange.py
python phases/phase2_mitm/mallory_attack.py
python phases/phase3_auth/authenticated_dh.py
python phases/phase4_aead/secure_channel.py
python phases/phase5_solana/solana_registry_client.py
python phases/phase6_blockchain_attack/blockchain_mitm_attack.py
```

Run all phases:
```bash
python scripts/demo_all_phases.py
```

---

## 🔧 Technology Stack

- **Cryptography**: `cryptography` library (X25519, Ed25519, ChaCha20-Poly1305)
- **Web Framework**: Flask
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Blockchain**: Solana (optional, Phase 5)

---

## 📚 Documentation

- **README.md** (this file) - Overview and quick start
- **docs/EXECUTION_FLOW.md** - What happens when you run the app (run.bat → app.py → phases)
- **docs/** - Additional detailed documentation

---

## 🎓 Learning Objectives

By exploring this project, you will understand:
- How secure channels are constructed from cryptographic primitives
- The critical importance of authentication in key exchange
- How AEAD schemes provide confidentiality and integrity
- Blockchain as a decentralized trust layer for PKI
- Real-world attacks (MITM) and their mitigations
- How blockchain prevents impersonation attacks through wallet ownership

---

## ⚠️ Troubleshooting

**Python not found:**
- Install Python 3.10+ from python.org
- Check "Add Python to PATH" during installation
- Restart your computer after installation

**Port 5000 in use:**
- Close other applications using port 5000
- Or edit `frontend/app.py` and change the port number

**Dependencies not installing:**
- Check internet connection
- Try: `pip install -r requirements.txt` manually

For more help, see `docs/TROUBLESHOOTING.txt`

---

## 📝 License

Educational project for Cryptography course at University of Macedonia.

---

**Last Updated:** December 2024

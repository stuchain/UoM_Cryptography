# 🔐 Mini Secure Channel (Solana Edition)

**Cryptography Course Assignment - AUEB MSc**  
**Due: January 5, 2026 | Presentation: January 9, 2026**

A comprehensive implementation demonstrating the construction, analysis, and hardening of a secure communication channel, integrated with Solana blockchain for decentralized key verification.

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Implementation Phases](#implementation-phases)
- [Installation](#installation)
- [Usage](#usage)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Deliverables](#deliverables)

---

## 🎯 Project Overview

This project demonstrates the step-by-step construction of a secure communication channel:

1. **Basic Diffie-Hellman Key Exchange** (X25519)
2. **MITM Attack Demonstration** - Shows vulnerabilities in unauthenticated protocols
3. **Authentication** - Adds Ed25519 signatures to prevent MITM attacks
4. **AEAD Encryption** - Implements ChaCha20-Poly1305 for secure messaging
5. **Blockchain Integration** - Solana-based decentralized key registry

### Learning Objectives

By completing this project, students will:
- Understand secure channel construction from cryptographic primitives
- Recognize the critical importance of authentication in key exchange
- Implement and use AEAD schemes correctly
- Explore blockchain as a decentralized trust layer for PKI
- Connect classical cryptography with modern Web3 infrastructure

---

## 📁 Project Structure

```
secure_channel/
├── phase2_dh/
│   └── dh_exchange.py              # Phase 1: Basic DH key exchange
├── phase3_mitm/
│   └── mallory_attack.py           # Phase 2: MITM attack demonstration
├── phase4_auth/
│   └── authenticated_dh.py         # Phase 3: Authenticated DH exchange
├── phase5_aead/
│   └── secure_channel.py           # Phase 4: Complete secure channel with AEAD
├── phase6_solana/
│   ├── solana_registry/            # Solana smart contract (Anchor)
│   │   ├── Cargo.toml
│   │   ├── Anchor.toml
│   │   └── src/
│   │       └── lib.rs              # Key Registry program
│   └── solana_registry_client.py   # Python client for Solana integration
├── visualizations/
│   └── diagram_generator.py        # Diagram generation utilities
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## 🚀 Implementation Phases

### Phase 1: Basic Diffie-Hellman Key Exchange

**File**: `phase2_dh/dh_exchange.py`

Demonstrates a minimal Diffie-Hellman key exchange using X25519 (Curve25519):
- Key pair generation (X25519)
- Public key exchange
- Shared secret derivation via HKDF-SHA256

**Run**:
```bash
python phase2_dh/dh_exchange.py
```

---

### Phase 2: MITM Attack Demonstration

**File**: `phase3_mitm/mallory_attack.py`

Simulates a Man-in-the-Middle attack on the unauthenticated DH exchange:
- Mallory intercepts and replaces public keys
- Demonstrates how both Alice and Bob unknowingly share keys with Mallory
- Shows the vulnerability of unauthenticated key exchange

**Run**:
```bash
python phase3_mitm/mallory_attack.py
```

---

### Phase 3: Authenticated Diffie-Hellman

**File**: `phase4_auth/authenticated_dh.py`

Fixes the MITM vulnerability by adding Ed25519 digital signatures:
- Each participant signs their DH public key with Ed25519
- Receivers verify signatures before accepting keys
- Mallory cannot forge signatures without private keys

**Run**:
```bash
python phase4_auth/authenticated_dh.py
```

---

### Phase 4: Secure Channel with AEAD

**File**: `phase5_aead/secure_channel.py`

Complete secure channel implementation:
- Authenticated DH key exchange
- ChaCha20-Poly1305 AEAD encryption
- Message confidentiality, integrity, and authentication
- Tampering detection

**Run**:
```bash
python phase5_aead/secure_channel.py
```

---

### Phase 5: Blockchain Integration

**File**: `phase6_solana/solana_registry_client.py`

Solana blockchain integration for decentralized key verification:
- Smart contract (Anchor) for on-chain key registry
- Python client to register and verify public keys
- Decentralized PKI model

**Run**:
```bash
python phase6_solana/solana_registry_client.py
```

**Smart Contract** (Rust/Anchor):
```bash
cd phase6_solana/solana_registry
anchor build
anchor deploy
```

---

## 💻 Installation

### Prerequisites

- Python 3.10+
- Rust (for Solana smart contracts)
- Solana CLI tools
- Anchor Framework (for Solana development)

### Python Dependencies

```bash
pip install -r requirements.txt
```

### Solana Setup

1. Install Solana CLI: https://docs.solana.com/cli/install-solana-cli-tools
2. Install Anchor: https://www.anchor-lang.com/docs/installation
3. Configure Solana CLI:
   ```bash
   solana config set --url devnet
   ```

---

## 📖 Usage

### Running Individual Phases

```bash
# Phase 1: Basic DH
python phase2_dh/dh_exchange.py

# Phase 2: MITM Attack
python phase3_mitm/mallory_attack.py

# Phase 3: Authenticated DH
python phase4_auth/authenticated_dh.py

# Phase 4: Secure Channel
python phase5_aead/secure_channel.py

# Phase 5: Blockchain Integration
python phase6_solana/solana_registry_client.py
```

### Generating Visualizations

```bash
python visualizations/diagram_generator.py
```

This generates diagrams in `visualizations/`:
- `dh_exchange.png` - Basic DH flow
- `mitm_attack.png` - MITM attack scenario
- `authenticated_flow.png` - Authenticated protocol
- `secure_channel.png` - Complete secure channel
- `blockchain_integration.png` - Blockchain verification

---

## 🔐 Key Features

### Security Properties

1. **Confidentiality**: Messages encrypted with ChaCha20-Poly1305
2. **Integrity**: MAC verification detects tampering
3. **Authentication**: Ed25519 signatures verify key ownership
4. **Replay Protection**: Unique nonces per message
5. **Forward Secrecy**: Ephemeral DH keys
6. **Decentralized Trust**: Solana blockchain for key verification

### Cryptographic Primitives

- **X25519**: Elliptic curve Diffie-Hellman key exchange
- **Ed25519**: Digital signatures for authentication
- **ChaCha20-Poly1305**: Authenticated encryption (AEAD)
- **HKDF-SHA256**: Key derivation function
- **Solana**: Blockchain-based key registry

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Protocol simulation & encryption |
| Cryptography | `cryptography`, `pynacl` | DH, Ed25519, AEAD |
| Blockchain | Solana (Anchor) | Decentralized key registry |
| Smart Contract | Rust / Anchor | On-chain key storage |
| Visualization | matplotlib | Message flow diagrams |

---

## 📄 Deliverables

### Technical Report (~25 pages)

- Introduction to secure communication
- Theoretical background (DH, MITM, AEAD, signatures)
- Implementation details and code explanation
- MITM attack demonstration results
- Blockchain integration analysis
- Discussion, evaluation, and future improvements
- References (Google Scholar, proper citation)

### Presentation (15 minutes)

- Concept overview with visual diagrams
- Live demo or recorded execution
- Key takeaways & comparison with real-world protocols

### Project Files

- Implementation code (all phases)
- Solana smart contract
- Visualization diagrams
- Documentation (README, comments)

---

## 🔬 Security Analysis

### Attack Scenarios Tested

1. ✅ **MITM Attack**: Demonstrated and prevented
2. ✅ **Tampering Detection**: AEAD MAC verification
3. ✅ **Signature Forgery**: Prevented by Ed25519
4. ✅ **Replay Attacks**: Mitigated by nonces

### Blockchain Benefits

- **Decentralized Trust**: No single point of failure
- **Immutable Registry**: Keys cannot be retrospectively modified
- **Transparent Verification**: Anyone can verify keys on-chain
- **No Certificate Authorities**: Trustless PKI model

---

## 📚 References

### Academic Sources

- Diffie, W., & Hellman, M. (1976). New directions in cryptography.
- Bernstein, D. J. (2006). Curve25519: new Diffie-Hellman speed records.
- Bernstein, D. J., et al. (2005). The Poly1305-AES message-authentication code.
- Josefsson, S., & Liusvaara, I. (2017). EdDSA and Ed25519.

### Technical Documentation

- [Cryptography Library](https://cryptography.io/)
- [Solana Documentation](https://docs.solana.com/)
- [Anchor Framework](https://www.anchor-lang.com/)
- [ChaCha20-Poly1305 RFC 8439](https://tools.ietf.org/html/rfc8439)

---

## 🚧 Extension Ideas (Optional)

- Add replay-attack protection via timestamps
- Compare AEAD algorithms (AES-GCM vs ChaCha20-Poly1305)
- Integrate post-quantum key exchange (liboqs)
- Formal verification using Tamarin Prover
- Deploy to Solana Devnet with real transactions
- Add performance benchmarking and metrics

---

## 👥 Author

**Cryptography Course Assignment - AUEB MSc**  
**Academic Year 2025-2026**

---

## 📝 License

This project is created for educational purposes as part of the Cryptography course assignment at AUEB.

---

## ⚠️ Security Notice

**This is a demonstration project for educational purposes.** The code should not be used in production environments without thorough security audits and additional hardening.

---

## 🤝 Contributing

This is an academic assignment. For questions or clarifications, please refer to the course materials and instructor.

---

**Last Updated**: December 2024


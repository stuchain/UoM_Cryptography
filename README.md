# 🔐 Mini Secure Channel (Solana Edition)

**Cryptography Course Assignment - University of Macedonia**  
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

This project demonstrates the step-by-step construction of a secure communication channel, showing both the vulnerabilities and the solutions in modern cryptography. The project is structured as a progressive learning experience, where each phase builds upon the previous one, revealing the evolution from a basic key exchange to a fully secure communication channel.

### What This Project Demonstrates

1. **Basic Diffie-Hellman Key Exchange** (X25519) - The foundation of secure key establishment
2. **MITM Attack Demonstration** - Shows how unauthenticated protocols can be compromised
3. **Authentication** - Adds Ed25519 signatures to prevent MITM attacks
4. **AEAD Encryption** - Implements ChaCha20-Poly1305 for secure messaging with integrity
5. **Blockchain Integration** - Solana-based decentralized key registry for trustless PKI

### Learning Objectives

By completing this project, students will:
- Understand secure channel construction from cryptographic primitives
- Recognize the critical importance of authentication in key exchange
- Implement and use AEAD schemes correctly
- Explore blockchain as a decentralized trust layer for PKI
- Connect classical cryptography with modern Web3 infrastructure
- See real-world attacks and their mitigations in action

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

#### What Happens in This Phase

This phase demonstrates the fundamental problem of secure key exchange: how can two parties (Alice and Bob) establish a shared secret key over an insecure channel without ever meeting?

**Step-by-Step Process:**

1. **Key Generation**: 
   - Alice generates a private key `a` (random 32 bytes) and computes her public key `A = a * G` (where G is the generator point on Curve25519)
   - Bob generates a private key `b` (random 32 bytes) and computes his public key `B = b * G`
   - These are X25519 key pairs, using the elliptic curve Curve25519

2. **Public Key Exchange**:
   - Alice sends her public key `A` to Bob (this can be intercepted by attackers)
   - Bob sends his public key `B` to Alice (this can also be intercepted)

3. **Shared Secret Derivation**:
   - Alice computes: `shared_secret = a * B = a * (b * G) = ab * G`
   - Bob computes: `shared_secret = b * A = b * (a * G) = ab * G`
   - Both arrive at the same value due to the commutative property of elliptic curve scalar multiplication

4. **Key Derivation (HKDF)**:
   - The raw shared secret is passed through HKDF-SHA256 (HMAC-based Key Derivation Function)
   - This ensures the final key is uniformly random and cryptographically strong
   - HKDF uses SHA-256 as the underlying hash function

**Why This Matters:**
- Demonstrates the mathematical beauty of Diffie-Hellman: two parties can agree on a secret without ever transmitting it
- Shows that public keys can be safely transmitted (they don't reveal the private keys)
- However, this phase is **vulnerable** - there's no authentication, so an attacker can intercept and replace keys

**Cryptographic Concepts:**
- **X25519**: Elliptic curve Diffie-Hellman on Curve25519, providing 128-bit security
- **HKDF**: Key derivation function that transforms a shared secret into a usable symmetric key
- **Forward Secrecy**: Each key exchange uses new ephemeral keys, so compromise of long-term keys doesn't affect past sessions

**Run**:
```bash
python phase2_dh/dh_exchange.py
```

---

### Phase 2: MITM Attack Demonstration

**File**: `phase3_mitm/mallory_attack.py`

#### What Happens in This Phase

This phase demonstrates a **Man-in-the-Middle (MITM) attack**, showing how an attacker (Mallory) can completely compromise the key exchange from Phase 1. This is the critical vulnerability that motivates all subsequent security improvements.

**The Attack Scenario:**

1. **Mallory's Setup**:
   - Mallory generates two key pairs: one to impersonate Bob to Alice, and one to impersonate Alice to Bob
   - Mallory positions herself between Alice and Bob in the network

2. **Interception and Replacement**:
   - When Alice sends her public key `A` to Bob, Mallory intercepts it
   - Mallory replaces it with her own public key `M_B` (pretending to be Bob)
   - When Bob sends his public key `B` to Alice, Mallory intercepts it
   - Mallory replaces it with her own public key `M_A` (pretending to be Alice)

3. **The Compromise**:
   - Alice thinks she's establishing a key with Bob, but actually establishes a key with Mallory: `K_Alice = a * M_B`
   - Bob thinks he's establishing a key with Alice, but actually establishes a key with Mallory: `K_Bob = b * M_A`
   - Mallory knows both keys: `K_Alice` and `K_Bob`

4. **The Consequences**:
   - Any message Alice sends (encrypted with `K_Alice`) can be decrypted by Mallory
   - Mallory can decrypt, read, modify, and re-encrypt messages before forwarding them
   - Bob receives messages that appear to be from Alice, but Mallory has full control
   - Neither Alice nor Bob knows they're being attacked

**Why This Attack Works:**
- There's no authentication - Alice and Bob have no way to verify they're talking to each other
- Public keys are just numbers - there's no proof of identity attached
- The attack is completely transparent to the victims

**What You'll See:**
- Alice and Bob both successfully derive keys (they think everything is fine)
- Mallory also derives both keys (she can decrypt everything)
- The keys don't match between Alice and Bob (they're talking to Mallory, not each other)
- Demonstration of message interception and decryption

**Cryptographic Concepts:**
- **MITM Attack**: A fundamental attack on unauthenticated key exchange protocols
- **Authentication Gap**: The missing piece that makes Phase 1 vulnerable
- **Trust Problem**: How do you know who you're talking to over an insecure channel?

**Run**:
```bash
python phase3_mitm/mallory_attack.py
```

---

### Phase 3: Authenticated Diffie-Hellman

**File**: `phase4_auth/authenticated_dh.py`

#### What Happens in This Phase

This phase fixes the critical vulnerability from Phase 2 by adding **digital signatures** for authentication. Now Alice and Bob can verify that they're actually talking to each other, not to Mallory.

**The Solution: Dual Keypair System**

Each participant now has **two** key pairs:
1. **X25519 key pair** (for Diffie-Hellman key exchange) - ephemeral, changes each session
2. **Ed25519 key pair** (for signing) - long-term, represents identity

**Step-by-Step Process:**

1. **Long-Term Identity Setup**:
   - Alice generates an Ed25519 signing key pair: `(signing_priv_A, signing_pub_A)`
   - Bob generates an Ed25519 signing key pair: `(signing_priv_B, signing_pub_B)`
   - These public keys represent their identities (like a username or certificate)

2. **Key Exchange with Authentication**:
   - Alice generates a new X25519 key pair for this session: `(dh_priv_A, dh_pub_A)`
   - Alice signs her DH public key: `signature_A = Sign(signing_priv_A, dh_pub_A)`
   - Alice sends to Bob: `(dh_pub_A, signing_pub_A, signature_A)`
   
   - Bob receives the message and verifies:
     - `Verify(signing_pub_A, signature_A, dh_pub_A)` - checks if the signature is valid
     - If valid, Bob knows this DH public key really came from Alice
     - Bob then derives the shared key: `K = b * dh_pub_A`

3. **Symmetric Process for Bob**:
   - Bob does the same: generates DH key pair, signs it, sends to Alice
   - Alice verifies Bob's signature before accepting his DH public key

4. **Mallory's Failure**:
   - Mallory can still intercept messages
   - But when she tries to replace Alice's DH public key with her own:
     - Mallory can't create a valid signature from Alice's signing key (she doesn't have `signing_priv_A`)
     - Bob verifies the signature and detects the forgery
     - Bob rejects the key exchange
   - The attack fails!

**Why This Works:**
- **Digital Signatures**: Provide cryptographic proof of identity
- **Non-repudiation**: Alice can't deny sending the message (only she has the private key)
- **Integrity**: Any modification to the signed data invalidates the signature
- **Authentication**: Bob can be certain the DH public key came from Alice

**Cryptographic Concepts:**
- **Ed25519**: Elliptic curve digital signature algorithm, providing 128-bit security
- **Signature Scheme**: Uses the EdDSA (Edwards-curve Digital Signature Algorithm) construction
- **Public Key Infrastructure (PKI)**: The signing public keys need to be distributed securely (this is where Phase 6/blockchain helps)

**What You'll See:**
- Successful authenticated key exchange between Alice and Bob
- Mallory's attack attempt fails - signatures don't verify
- Demonstration that authentication prevents MITM attacks

**Run**:
```bash
python phase4_auth/authenticated_dh.py
```

---

### Phase 4: Secure Channel with AEAD

**File**: `phase5_aead/secure_channel.py`

#### What Happens in This Phase

This phase completes the secure channel by adding **Authenticated Encryption with Associated Data (AEAD)**. Now we can not only establish a secure key, but also send encrypted messages with guaranteed confidentiality, integrity, and authentication.

**What is AEAD?**

AEAD provides three security properties in one operation:
1. **Confidentiality**: Messages are encrypted (only the key holder can read them)
2. **Integrity**: Any tampering is detected (the message is verified to be unmodified)
3. **Authentication**: The message is verified to come from the key holder

**The Complete Secure Channel:**

1. **Key Establishment** (from Phase 3):
   - Alice and Bob perform authenticated Diffie-Hellman key exchange
   - They derive a shared symmetric key `K`

2. **Message Encryption (Alice → Bob)**:
   - Alice wants to send message `M`
   - Generate a unique **nonce** (number used once): `nonce = counter + random_bytes`
   - Encrypt with ChaCha20-Poly1305: `(ciphertext, tag) = Encrypt(K, nonce, M, associated_data)`
     - **ChaCha20**: Stream cipher that encrypts the message
     - **Poly1305**: MAC (Message Authentication Code) that authenticates the ciphertext
     - **Associated Data**: Optional data that's authenticated but not encrypted (like headers)
   - Send: `(nonce, ciphertext)`

3. **Message Decryption (Bob receives)**:
   - Bob receives `(nonce, ciphertext)`
   - Decrypt and verify: `M = Decrypt(K, nonce, ciphertext, associated_data)`
   - The decryption process automatically:
     - Verifies the Poly1305 tag (detects tampering)
     - Decrypts the ChaCha20 ciphertext
     - Returns the plaintext only if verification succeeds

4. **Tampering Detection**:
   - If Mallory modifies the ciphertext in transit
   - Bob's decryption will fail with `InvalidTag` exception
   - The message is rejected - tampering is detected!

**Why ChaCha20-Poly1305?**

- **Fast**: Optimized for software, performs well on CPUs without hardware acceleration
- **Secure**: Designed by Daniel J. Bernstein, widely analyzed and trusted
- **Standardized**: RFC 8439, used in TLS 1.3, WireGuard, and many modern protocols
- **AEAD**: Provides all three security properties in one operation

**Nonce Management:**

- Each message must use a unique nonce
- Nonces are never reused with the same key
- This implementation uses: `nonce = 8-byte-counter || 4-byte-random`
- The counter ensures uniqueness, random bytes add extra security

**Cryptographic Concepts:**
- **AEAD**: Authenticated Encryption with Associated Data
- **ChaCha20**: Stream cipher based on the ChaCha stream cipher
- **Poly1305**: One-time authenticator (MAC) based on polynomial evaluation
- **Nonce**: Number used once - critical for security (reuse breaks security)
- **Tag/MAC**: Cryptographic checksum that proves authenticity and integrity

**What You'll See:**
- Successful encrypted message transmission
- Demonstration of tampering detection (modified messages are rejected)
- Complete secure channel: authentication + encryption + integrity

**Run**:
```bash
python phase5_aead/secure_channel.py
```

---

### Phase 5: Blockchain Integration

**File**: `phase6_solana/solana_registry_client.py`

#### What Happens in This Phase

This phase addresses a critical question from Phase 3: **How do Alice and Bob know each other's signing public keys?** Traditional PKI uses Certificate Authorities (CAs), but blockchain provides a decentralized alternative.

**The Problem: Key Distribution**

In Phase 3, we assumed Alice and Bob already know each other's Ed25519 signing public keys. But in reality:
- How does Alice get Bob's signing public key securely?
- How does Bob know Alice's signing public key is authentic?
- What if Mallory creates a fake key pair and claims to be Alice?

**The Blockchain Solution:**

Instead of trusting a central Certificate Authority, we use the Solana blockchain as a **decentralized, immutable key registry**.

**How It Works:**

1. **Key Registration**:
   - Alice generates her Ed25519 signing key pair
   - Alice creates a Solana transaction that stores her public key on-chain
   - The transaction is signed with Alice's Solana wallet (proving ownership)
   - Once confirmed, Alice's public key is permanently recorded on the blockchain

2. **Key Lookup**:
   - Bob wants to communicate with Alice
   - Bob queries the Solana blockchain for Alice's registered public key
   - Bob retrieves the on-chain public key
   - Bob uses this public key to verify Alice's signatures in Phase 3

3. **Trust Model**:
   - **No central authority**: The blockchain is decentralized
   - **Immutable**: Once registered, keys can't be retrospectively modified
   - **Transparent**: Anyone can verify what keys are registered
   - **Cryptographic proof**: The blockchain itself provides cryptographic guarantees

**Smart Contract Details:**

The Solana program (smart contract) provides:
- `register_key`: Store a public key associated with a user's wallet address
- `get_key`: Retrieve a registered public key for a given wallet address
- **Account structure**: Stores the Ed25519 public key in a Solana account

**Integration with Previous Phases:**

1. **Before Phase 3**: Alice and Bob register their Ed25519 signing public keys on Solana
2. **During Phase 3**: When Alice sends her signing public key to Bob, Bob can verify it matches the on-chain registry
3. **Attack Prevention**: Mallory can't register a key as Alice (she doesn't control Alice's Solana wallet)

**Why Blockchain for PKI?**

- **Decentralization**: No single point of failure or trust
- **Immutability**: Historical record of all key registrations
- **Transparency**: Public verification of key ownership
- **No CAs**: Eliminates the need for trusted third parties
- **Web3 Native**: Aligns with decentralized identity trends

**Cryptographic Concepts:**
- **Decentralized PKI**: Public key infrastructure without central authorities
- **Blockchain Registry**: Using blockchain as an immutable database
- **Wallet-based Identity**: Solana wallet addresses serve as identifiers
- **On-chain Verification**: Cryptographic proofs stored on blockchain

**What You'll See:**
- Key registration on Solana (simulated or real devnet)
- Key lookup and verification
- Integration with the authenticated key exchange from Phase 3

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

**📖 For detailed installation and running instructions, see [HOW_TO_RUN.md](HOW_TO_RUN.md)**

### Quick Start

1. **Prerequisites**: Python 3.10+
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the interactive frontend**:
   ```bash
   cd frontend
   python app.py
   ```
4. **Open browser**: `http://localhost:5000`

### Full Installation Guide

For comprehensive setup instructions, troubleshooting, and detailed explanations, please refer to **[HOW_TO_RUN.md](HOW_TO_RUN.md)**.

### Optional: Solana Setup (for Phase 5)

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

**Cryptography Course Assignment - University of Macedonia**  
**Academic Year 2025-2026**

---

## 📝 License

This project is created for educational purposes as part of the Cryptography course assignment at University of Macedonia.

---

## ⚠️ Security Notice

**This is a demonstration project for educational purposes.** The code should not be used in production environments without thorough security audits and additional hardening.

---

## 🤝 Contributing

This is an academic assignment. For questions or clarifications, please refer to the course materials and instructor.

---

**Last Updated**: December 2024


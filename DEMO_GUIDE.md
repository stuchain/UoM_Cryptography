# 🎯 Demo Guide - Mini Secure Channel Project

Complete step-by-step guide to running each phase of the secure channel demonstration.

---

## 📋 Prerequisites

Before running any demos, ensure you have:

1. **Python 3.10+** installed
2. **Dependencies installed**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python test_env.py
   ```
   Should print: `[SUCCESS] Cryptography and PyNaCl installed successfully!`

---

## 🚀 Quick Start: Run All Phases at Once

The easiest way to see everything is to run the complete demo:

```bash
python demo_all_phases.py
```

This will:
- Run all 5 phases sequentially
- Pause between each phase (press Enter to continue)
- Show complete output from each phase
- Display a summary at the end

**Press Ctrl+C at any time to cancel.**

---

## 📖 Individual Phase Demos

### Phase 1: Basic Diffie-Hellman Key Exchange

**File**: `phase2_dh/dh_exchange.py`

**What it demonstrates**:
- Two parties (Alice and Bob) establish a shared secret
- X25519 key exchange using elliptic curves
- HKDF key derivation

**How to run**:
```bash
cd phase2_dh
python dh_exchange.py
```

**Expected output**:
```
Alice public (hex): [32-byte hex string]
Bob   public (hex): [32-byte hex string]

Derived symmetric keys (hex):
Alice key: [64-char hex string]
Bob   key: [64-char hex string]

[SUCCESS] Alice and Bob derived the same symmetric key.
```

**What to observe**:
- Alice and Bob generate different public keys
- But they derive the **same** shared symmetric key
- This is the magic of Diffie-Hellman!

**Key takeaway**: Two parties can establish a shared secret without pre-sharing keys.

---

### Phase 2: Man-in-the-Middle (MITM) Attack

**File**: `phase3_mitm/mallory_attack.py`

**What it demonstrates**:
- How an attacker (Mallory) intercepts key exchange
- Mallory replaces public keys with her own
- Result: Alice and Bob unknowingly share keys with Mallory

**How to run**:
```bash
cd phase3_mitm
python mallory_attack.py
```

**Expected output**:
```
STEP 1: Alice generates keypair
Alice: Generated keypair
Alice: Public key (hex): [...]

STEP 2: Alice sends public key to Bob (intercepted by Mallory)
Mallory: [INTERCEPTED] Alice's public key
Mallory: Derived key with Alice (hex): [...]
Mallory: [FORWARDING] Fake Bob's public key to Alice

[... more steps ...]

ATTACK RESULTS
Alice's shared key (hex): [...]
Bob's shared key   (hex): [...]
Mallory's key with Alice (hex): [...]
Mallory's key with Bob   (hex): [...]

[ATTACK SUCCESS] Alice shares a key with Mallory (not Bob)
[ATTACK SUCCESS] Bob shares a key with Mallory (not Alice)
[CRITICAL] Alice and Bob have DIFFERENT keys!
```

**What to observe**:
- Mallory intercepts **both** public keys
- Alice and Bob derive **different** keys (unlike Phase 1)
- Mallory's keys match with Alice and Bob separately
- This means Mallory can decrypt all communication!

**Key takeaway**: Without authentication, MITM attacks are possible and dangerous.

---

### Phase 3: Authenticated Diffie-Hellman

**File**: `phase4_auth/authenticated_dh.py`

**What it demonstrates**:
- How digital signatures (Ed25519) prevent MITM attacks
- Signature verification before accepting keys
- Mallory's attack fails because she can't forge signatures

**How to run**:
```bash
cd phase4_auth
python authenticated_dh.py
```

**Expected output**:
```
STEP 1: Alice generates keypairs (DH + Ed25519)
Alice: Generated DH keypair and Ed25519 signing keypair
Alice: DH public key (hex): [...]
Alice: Ed25519 public key (hex): [...]

STEP 2: Alice signs DH public key and sends to Bob
Alice: Signed DH public key
Alice: Signature (hex): [...]

STEP 3: Bob verifies Alice's signature and derives key
Bob: [SUCCESS] Signature verification SUCCESS
Bob: Derived shared key (hex): [...]

[... more steps ...]

AUTHENTICATED KEY EXCHANGE RESULTS
[SUCCESS] Alice and Bob derived the same shared key

MITM ATTACK PREVENTION TEST
Mallory attempts to intercept and replace Alice's message to Bob
Bob receives Mallory's fake message and attempts verification
[SUCCESS] ATTACK PREVENTED: Bob correctly rejected Mallory's fake signature
```

**What to observe**:
- Each participant now has **TWO** keypairs (DH + signing)
- DH public keys are **signed** before sending
- Signatures are **verified** before accepting keys
- Mallory's fake signature is **rejected**
- Alice and Bob now derive the **same** key (attack prevented!)

**Key takeaway**: Digital signatures prevent MITM attacks by authenticating public keys.

---

### Phase 4: Secure Channel with AEAD Encryption

**File**: `phase5_aead/secure_channel.py`

**What it demonstrates**:
- Complete secure channel with authenticated encryption
- ChaCha20-Poly1305 for confidentiality + integrity
- Encrypted message exchange
- Tampering detection

**How to run**:
```bash
cd phase5_aead
python secure_channel.py
```

**Expected output**:
```
STEP 1: Alice generates keypairs
STEP 2: Alice sends authenticated DH public key to Bob
STEP 3: Bob verifies and establishes secure channel
Alice: Secure channel established. AEAD cipher initialized.
Bob: Secure channel established. AEAD cipher initialized.

SECURE MESSAGE EXCHANGE
Alice sends message to Bob
Alice: Plaintext: Hello Bob! This is a secret message.
Alice: Encrypted message (length: X bytes)
Alice: Nonce (hex): [...]

Bob receives and decrypts message
Bob: Decrypted message successfully
Bob: Decrypted: Hello Bob! This is a secret message.
[SUCCESS] Message integrity verified

TAMPERING DETECTION TEST
Mallory attempts to modify encrypted message...
Bob tries to decrypt tampered message...
[SUCCESS] Tampering detected! Message rejected.
```

**What to observe**:
- After key exchange, a **cipher** is initialized
- Messages are **encrypted** before sending
- Messages are **decrypted** after receiving
- **Tampered messages are rejected** (tampering detection works!)

**Key takeaway**: AEAD provides confidentiality (encryption) and integrity (tampering detection).

---

### Phase 5: Blockchain Integration (Solana)

**File**: `phase6_solana/solana_registry_client.py`

**What it demonstrates**:
- Solana blockchain as decentralized key registry
- Registering public keys on-chain
- Verifying keys against blockchain before accepting them

**How to run**:
```bash
cd phase6_solana
python solana_registry_client.py
```

**Expected output**:
```
Solana Key Registry Client initialized
RPC URL: https://api.devnet.solana.com
Program ID: KeyRegistry11111111111111111111111111111

STEP 1: Participants generate keypairs
STEP 2: Register keys on Solana blockchain
Alice: Registering signing key on Solana blockchain...
[SUCCESS] Alice: Key registered on-chain

[... more steps ...]

STEP 4: Bob verifies Alice's key via blockchain BEFORE accepting
Alice: Verifying peer's key via Solana blockchain...
  Peer Solana address: [...]
  Peer signing key (hex): [...]
[SUCCESS] Alice: Blockchain verification SUCCESS

BLOCKCHAIN-SECURED MESSAGE EXCHANGE
[SUCCESS] Secure communication established with blockchain verification
```

**What to observe**:
- Keys are **registered** on Solana blockchain
- Keys are **verified** against blockchain before use
- Adds an **additional trust layer** beyond just signatures
- Demonstrates **decentralized PKI** (no certificate authorities needed)

**Key takeaway**: Blockchain provides decentralized, immutable key registry.

**Note**: This phase uses mock Solana transactions for demonstration. For real blockchain integration, you would need:
- Solana CLI installed
- Anchor framework
- Devnet/testnet setup
- Funded wallet

---

## 🎨 Generate Visualizations

Create diagrams showing message flows and attack scenarios:

```bash
python visualizations/diagram_generator.py
```

This creates 5 diagrams in the `visualizations/` folder:
- `dh_exchange.png` - Basic DH flow
- `mitm_attack.png` - MITM attack scenario
- `authenticated_flow.png` - Authenticated protocol
- `secure_channel.png` - Complete secure channel
- `blockchain_integration.png` - Blockchain verification

**Requirements**: `matplotlib` must be installed (`pip install matplotlib`)

---

## 📊 Understanding the Output

### Common Patterns in All Phases

1. **Key Generation**
   - Each participant generates keypairs
   - Public keys are shown in hex (32 bytes = 64 hex characters)

2. **Key Exchange**
   - Public keys are "exchanged" (in demo, directly passed)
   - Shared keys are derived using HKDF

3. **Verification Steps**
   - Phase 3+: Signature verification
   - Phase 5+: Blockchain verification

4. **Success Indicators**
   - `[SUCCESS]` - Operation completed successfully
   - `[FAILED]` or `[ERROR]` - Something went wrong
   - `[ATTACK SUCCESS]` - Attack succeeded (expected in Phase 2)
   - `[ATTACK PREVENTED]` - Attack blocked (expected in Phase 3+)

---

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution**:
```bash
# Make sure you're in the project root
cd C:\Users\Stelios\Desktop\secure_channel

# Install dependencies
pip install -r requirements.txt
```

### Issue: Unicode encoding errors on Windows

**Solution**: Already fixed! The code uses ASCII-safe output now.

### Issue: Can't run individual phases

**Solution**: Run from project root:
```bash
# From project root, not from phase directories
python phase2_dh/dh_exchange.py
python phase3_mitm/mallory_attack.py
# etc.
```

### Issue: Visualization errors

**Solution**:
```bash
pip install matplotlib numpy
```

---

## 🎓 Learning Path

Recommended order for understanding:

1. **Start with Phase 1** - Understand basic DH
   - Read the output carefully
   - Notice that keys match

2. **Then Phase 2** - See the vulnerability
   - Notice that keys DON'T match
   - Understand why Mallory succeeds

3. **Phase 3** - See the fix
   - Notice signatures are required
   - See Mallory's attack fail

4. **Phase 4** - See full security
   - Messages are encrypted
   - Tampering is detected

5. **Phase 5** - See blockchain extension
   - Understand decentralized trust
   - See on-chain verification

---

## 💡 Tips for Presentation

### For Live Demo:
1. Run `demo_all_phases.py` and pause between phases to explain
2. Or run each phase individually to show specific concepts
3. Use visualizations (`diagram_generator.py`) for slides

### For Recorded Demo:
1. Record each phase separately
2. Add annotations explaining key concepts
3. Show the code alongside output

### Key Points to Emphasize:
- **Phase 1**: "Look - same key without pre-sharing!"
- **Phase 2**: "Watch - Mallory intercepts everything!"
- **Phase 3**: "See - signatures prevent the attack!"
- **Phase 4**: "Now messages are encrypted AND authenticated!"
- **Phase 5**: "Blockchain adds decentralized trust!"

---

## 📝 Demo Checklist

Before your presentation/demo:

- [ ] All dependencies installed
- [ ] Phase 1 runs successfully
- [ ] Phase 2 shows MITM attack
- [ ] Phase 3 shows attack prevention
- [ ] Phase 4 shows secure messaging
- [ ] Phase 5 shows blockchain integration
- [ ] Visualizations generated (if using slides)
- [ ] You understand what each phase demonstrates

---

## 🎯 Quick Reference Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run complete demo
python demo_all_phases.py

# Run individual phases (from project root)
python phase2_dh/dh_exchange.py
python phase3_mitm/mallory_attack.py
python phase4_auth/authenticated_dh.py
python phase5_aead/secure_channel.py
python phase6_solana/solana_registry_client.py

# Generate visualizations
python visualizations/diagram_generator.py

# Test environment
python test_env.py
```

---

**Good luck with your demo! 🚀**

For questions or issues, refer to the README.md or individual phase files.



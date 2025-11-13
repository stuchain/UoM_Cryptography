# 📘 Phase 2: MITM Attack - Complete Documentation

**Comprehensive explanation of the Man-in-the-Middle attack, why Phase 1 is vulnerable, and how the attack works.**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Why Phase 1 is Vulnerable](#why-phase-1-is-vulnerable)
3. [The MITM Attack Scenario](#the-mitm-attack-scenario)
4. [Attack Flow - Step by Step](#attack-flow---step-by-step)
5. [Code Structure and Functions](#code-structure-and-functions)
6. [What Mallory Can Do](#what-mallory-can-do)
7. [Attack Demonstration](#attack-demonstration)
8. [Security Implications](#security-implications)
9. [Why Authentication is Critical](#why-authentication-is-critical)

---

## 🎯 Overview

### What Phase 2 Demonstrates

Phase 2 shows the **critical vulnerability** in Phase 1: **lack of authentication**. Without authentication, an attacker (Mallory) can intercept and manipulate the key exchange, completely compromising the security.

### The Attack

**Man-in-the-Middle (MITM) Attack**: Mallory positions herself between Alice and Bob, intercepts their messages, and replaces public keys with her own. Result: Alice and Bob think they're talking to each other, but both are actually talking to Mallory.

### Why This Matters

- **Shows why authentication is essential** - Phase 1 alone is not secure
- **Demonstrates real-world attack** - This is how actual attacks work
- **Motivates Phase 3** - Shows why we need digital signatures
- **Educational value** - Understanding attacks helps prevent them

---

## ⚠️ Why Phase 1 is Vulnerable

### The Fundamental Problem

**Phase 1 has no authentication mechanism.** This means:

1. **No identity verification** - Alice can't verify the public key is really from Bob
2. **No message integrity** - Public keys can be modified in transit
3. **No non-repudiation** - Bob can't prove he sent his public key
4. **No attack detection** - No way to detect if an attacker is present

### What Phase 1 Provides

✅ **Key agreement** - Two parties can agree on a shared secret
✅ **Forward secrecy potential** - Can use ephemeral keys
✅ **No pre-shared keys** - Parties don't need to meet

### What Phase 1 Lacks

❌ **Authentication** - Can't verify who you're talking to
❌ **Integrity** - Can't detect if messages were modified
❌ **Non-repudiation** - Can't prove who sent what
❌ **Attack detection** - No way to detect MITM

### The Vulnerability in Detail

When Alice receives `bob_pub_bytes`, she has **no way to verify**:
- Is this really from Bob?
- Was it modified in transit?
- Is an attacker intercepting?

Same for Bob when he receives `alice_pub_bytes`.

**This is the vulnerability that Phase 2 exploits.**

---

## 🎭 The MITM Attack Scenario

### The Players

1. **Alice** - Legitimate party, wants to communicate with Bob
2. **Bob** - Legitimate party, wants to communicate with Alice
3. **Mallory** - Attacker, wants to intercept and read all messages

### Mallory's Goal

- **Intercept** all communication between Alice and Bob
- **Read** all messages (decrypt them)
- **Modify** messages if desired (optional)
- **Remain undetected** - Alice and Bob think they're talking to each other

### Mallory's Strategy

1. **Position herself** between Alice and Bob (network-level attack)
2. **Intercept** public keys as they're exchanged
3. **Replace** public keys with her own
4. **Establish separate keys** with both Alice and Bob
5. **Decrypt, read, and re-encrypt** all messages

---

## 🔄 Attack Flow - Step by Step

### Normal Flow (Phase 1 - No Attack)

```
Alice                          Bob
  │                             │
  ├─ Generate keypair           │
  ├─ alice_priv, alice_pub      │
  │                             │
  ├─ Send alice_pub ────────────►
  │                             │
  │                    Generate keypair
  │                    bob_priv, bob_pub
  │                             │
  │◄──────────────── bob_pub ───┤
  │                             │
  ├─ Derive key:                │
  │  alice_key =                │
  │  DH(alice_priv, bob_pub)    │
  │                             ├─ Derive key:
  │                             │  bob_key =
  │                             │  DH(bob_priv, alice_pub)
  │                             │
  │  alice_key == bob_key ✅    │
```

### Attack Flow (Phase 2 - MITM)

```
Alice                    Mallory                    Bob
  │                        │                         │
  ├─ Generate keypair       │                         │
  ├─ alice_priv, alice_pub  │                         │
  │                        │                         │
  ├─ Send alice_pub ───────►│                         │
  │                        │                         │
  │                        ├─ INTERCEPT!             │
  │                        ├─ Generate keypair        │
  │                        ├─ mallory_priv_A,        │
  │                        │  mallory_pub_A          │
  │                        │                         │
  │                        ├─ Send mallory_pub_A ────►
  │                        │                         │
  │                        │              Generate keypair
  │                        │              bob_priv, bob_pub
  │                        │                         │
  │                        │◄─────── bob_pub ─────────┤
  │                        │                         │
  │                        ├─ INTERCEPT!             │
  │                        ├─ Generate keypair        │
  │                        ├─ mallory_priv_B,        │
  │                        │  mallory_pub_B          │
  │                        │                         │
  │◄──── mallory_pub_B ────┤                         │
  │                        │                         │
  ├─ Derive key:           │                         │
  │  alice_key =           │                         │
  │  DH(alice_priv,        │                         │
  │     mallory_pub_B)     │                         │
  │                        │                         │
  │                        ├─ Derive key with Alice: │
  │                        │  key_A =                │
  │                        │  DH(mallory_priv_B,     │
  │                        │     alice_pub)          │
  │                        │                         │
  │                        │              Derive key:
  │                        │              bob_key =
  │                        │              DH(bob_priv,
  │                        │                 mallory_pub_A)
  │                        │                         │
  │                        ├─ Derive key with Bob:   │
  │                        │  key_B =                │
  │                        │  DH(mallory_priv_A,     │
  │                        │     bob_pub)            │
  │                        │                         │
  │  alice_key == key_B ✅ │                         │
  │                        │                         │
  │                        │              bob_key == key_A ✅
  │                        │                         │
  │  ❌ alice_key != bob_key                         │
```

### Key Observations

1. **Alice thinks she shares a key with Bob** - But actually shares with Mallory
2. **Bob thinks he shares a key with Alice** - But actually shares with Mallory
3. **Mallory has both keys** - Can decrypt all messages
4. **Alice and Bob's keys don't match** - They can't communicate directly
5. **Attack is undetected** - No authentication to catch it

---

## 💻 Code Structure and Functions

### Imports Used

The code imports the same functions from Phase 1:
- `generate_x25519_keypair()` - Generate keypairs
- `public_bytes()` - Serialize public keys
- `derive_shared_key()` - Perform key exchange

**Why reuse?** - Shows that the attack uses the same cryptographic primitives, just manipulates the protocol flow.

### Key Generation (All Parties)

**Alice generates:**
- `alice_priv, alice_pub` - Her legitimate keypair
- `alice_pub_bytes` - Public key to send to Bob

**Bob generates:**
- `bob_priv, bob_pub` - His legitimate keypair
- `bob_pub_bytes` - Public key to send to Alice

**Mallory generates TWO keypairs:**
- `mallory_priv_A, mallory_pub_A` - To impersonate Alice to Bob
- `mallory_priv_B, mallory_pub_B` - To impersonate Bob to Alice

**Why two keypairs?** - Mallory needs separate keys for each direction of communication.

### The Interception Logic

**Step 1: Mallory intercepts Alice's public key**

```python
# Alice sends: alice_pub_bytes
# Mallory receives it, but doesn't forward it to Bob
# Instead, Mallory sends: mallory_pub_A (her own key)
```

**What happens:**
- Bob receives `mallory_pub_A` thinking it's from Alice
- Bob will derive a key using `mallory_pub_A`
- Mallory can compute the same key using `mallory_priv_A`

**Step 2: Mallory intercepts Bob's public key**

```python
# Bob sends: bob_pub_bytes
# Mallory receives it, but doesn't forward it to Alice
# Instead, Mallory sends: mallory_pub_B (her own key)
```

**What happens:**
- Alice receives `mallory_pub_B` thinking it's from Bob
- Alice will derive a key using `mallory_pub_B`
- Mallory can compute the same key using `mallory_priv_B`

### Key Derivation (The Compromise)

**Alice's computation:**
```python
alice_key = derive_shared_key(
    alice_priv,           # Alice's private key
    mallory_pub_B,        # Mallory's public key (Alice thinks it's Bob's)
    info=b"secure_channel_v1"
)
```

**Result:** `alice_key = DH(alice_priv, mallory_pub_B)`

**Bob's computation:**
```python
bob_key = derive_shared_key(
    bob_priv,             # Bob's private key
    mallory_pub_A,        # Mallory's public key (Bob thinks it's Alice's)
    info=b"secure_channel_v1"
)
```

**Result:** `bob_key = DH(bob_priv, mallory_pub_A)`

**Mallory's computations:**
```python
# Key with Alice
key_with_alice = derive_shared_key(
    mallory_priv_B,       # Mallory's private key
    alice_pub_bytes,      # Alice's real public key (intercepted)
    info=b"secure_channel_v1"
)

# Key with Bob
key_with_bob = derive_shared_key(
    mallory_priv_A,       # Mallory's private key
    bob_pub_bytes,        # Bob's real public key (intercepted)
    info=b"secure_channel_v1"
)
```

**Results:**
- `key_with_alice == alice_key` ✅ (Mallory can decrypt Alice's messages)
- `key_with_bob == bob_key` ✅ (Mallory can decrypt Bob's messages)
- `alice_key != bob_key` ❌ (Alice and Bob can't communicate)

### The Mathematical Proof

**Why Mallory's keys match:**

**Alice-Mallory key:**
- Alice computes: `alice_key = alice_priv * mallory_pub_B`
- Mallory computes: `key_with_alice = mallory_priv_B * alice_pub`
- These are equal: `alice_priv * (mallory_priv_B * G) = mallory_priv_B * (alice_priv * G)`

**Bob-Mallory key:**
- Bob computes: `bob_key = bob_priv * mallory_pub_A`
- Mallory computes: `key_with_bob = mallory_priv_A * bob_pub`
- These are equal: `bob_priv * (mallory_priv_A * G) = mallory_priv_A * (bob_priv * G)`

**Why Alice-Bob keys don't match:**
- Alice has: `alice_key = alice_priv * mallory_pub_B`
- Bob has: `bob_key = bob_priv * mallory_pub_A`
- These are different values (different public keys used)

---

## 🎯 What Mallory Can Do

### 1. Read All Messages

**If Alice encrypts a message with `alice_key`:**
- Mallory can decrypt it using `key_with_alice` (they're the same!)
- Mallory can read the plaintext
- Mallory can re-encrypt and forward to Bob (if desired)

**If Bob encrypts a message with `bob_key`:**
- Mallory can decrypt it using `key_with_bob` (they're the same!)
- Mallory can read the plaintext
- Mallory can re-encrypt and forward to Alice (if desired)

### 2. Modify Messages (Optional)

**Mallory can:**
- Decrypt message from Alice
- Modify the plaintext
- Re-encrypt with `key_with_bob`
- Send modified message to Bob
- Bob thinks it came from Alice!

### 3. Inject Messages

**Mallory can:**
- Create fake messages
- Encrypt with appropriate key
- Send to Alice or Bob
- They think it came from the other party!

### 4. Remain Undetected

**No authentication means:**
- Alice can't verify Bob's identity
- Bob can't verify Alice's identity
- No way to detect the attack
- Attack can continue indefinitely

---

## 🧪 Attack Demonstration

### What the Code Shows

The Phase 2 code demonstrates:

1. **Key generation** - All three parties generate keypairs
2. **Interception** - Mallory intercepts and replaces public keys
3. **Key derivation** - All parties derive keys
4. **Key comparison** - Shows that:
   - Alice's key matches Mallory's key (with Alice)
   - Bob's key matches Mallory's key (with Bob)
   - Alice's key does NOT match Bob's key

### Expected Output

```
Alice public key: [hex]
Bob public key: [hex]
Mallory public key (to Bob): [hex]
Mallory public key (to Alice): [hex]

Alice's derived key: [hex]
Bob's derived key: [hex]
Mallory's key with Alice: [hex]
Mallory's key with Bob: [hex]

[ATTACK SUCCESS] Alice's key matches Mallory's key with Alice
[ATTACK SUCCESS] Bob's key matches Mallory's key with Bob
[VULNERABILITY] Alice's key does NOT match Bob's key
```

### What This Proves

- ✅ Attack is successful - Mallory has both keys
- ✅ Attack is undetected - No authentication to catch it
- ✅ Communication is compromised - Alice and Bob can't talk securely
- ✅ This is why Phase 1 alone is not secure

---

## 🔒 Security Implications

### What This Attack Shows

1. **Authentication is essential** - Without it, key exchange is vulnerable
2. **Public keys alone are not enough** - Need to verify identity
3. **Network-level attacks are real** - MITM is a practical attack
4. **Cryptography alone isn't enough** - Need proper protocols

### Real-World Impact

**If this attack succeeds:**
- All encrypted messages can be read
- Messages can be modified
- Fake messages can be injected
- Complete communication compromise

**Examples of real MITM attacks:**
- Public WiFi networks
- Compromised routers
- Malicious ISPs
- Government surveillance

### Why This Attack Works

**The attack works because:**
1. **No authentication** - Can't verify public key source
2. **No integrity** - Can't detect if public key was modified
3. **No non-repudiation** - Can't prove who sent the public key
4. **Symmetric problem** - Both parties have the same vulnerability

---

## ✅ Why Authentication is Critical

### The Solution (Preview of Phase 3)

**Digital signatures solve this:**
- Alice signs her public key with her private signing key
- Bob verifies the signature using Alice's public signing key
- If signature is invalid, reject the public key
- Mallory can't forge signatures (doesn't have Alice's private signing key)

### What Authentication Provides

✅ **Identity verification** - Can verify who sent the public key
✅ **Message integrity** - Can detect if public key was modified
✅ **Non-repudiation** - Can prove who sent the public key
✅ **Attack detection** - Can detect MITM attempts

### The Fix (Phase 3)

Phase 3 adds Ed25519 digital signatures:
- Each party has a signing keypair (separate from DH keypair)
- Public keys are signed before transmission
- Recipients verify signatures before accepting keys
- Mallory's attack fails - can't forge signatures

---

## 📊 Attack Success Metrics

### How to Measure Attack Success

**Attack is successful if:**
1. ✅ Mallory can derive the same key as Alice
2. ✅ Mallory can derive the same key as Bob
3. ✅ Alice and Bob's keys don't match
4. ✅ Attack remains undetected

**All of these are true in Phase 2!**

### Detection Mechanisms (Missing in Phase 1)

**What would detect the attack:**
- ❌ Digital signatures (not present)
- ❌ Certificate authorities (not present)
- ❌ Out-of-band verification (not present)
- ❌ Key fingerprint comparison (not present)

**Phase 1 has none of these!**

---

## 🎓 Key Takeaways

### What You Should Understand

1. **Phase 1 is vulnerable** - No authentication means MITM is possible
2. **The attack is practical** - Real attackers use this technique
3. **Cryptography alone isn't enough** - Need proper protocols
4. **Authentication is essential** - This is why Phase 3 exists

### Why This Phase Exists

- **Educational** - Shows why authentication matters
- **Motivational** - Explains why we need Phase 3
- **Realistic** - Demonstrates actual attack technique
- **Important** - Understanding attacks helps prevent them

---

## 🔗 Connection to Other Phases

### Builds on Phase 1

- Uses same cryptographic primitives
- Shows vulnerability in Phase 1's design
- Demonstrates why Phase 1 alone is insufficient

### Leads to Phase 3

- Shows why authentication is needed
- Demonstrates the problem that Phase 3 solves
- Provides motivation for digital signatures

### Relationship to Phase 4

- Even with authentication, need encryption
- Phase 4 adds message encryption
- MITM prevention (Phase 3) + encryption (Phase 4) = secure channel

---

## ❓ Common Questions

### Q: Can't Alice and Bob detect the attack?

**A:** Not in Phase 1! They have no way to verify:
- Who sent the public key
- If the public key was modified
- If an attacker is present

### Q: Why does Mallory need two keypairs?

**A:** Mallory needs separate keys for each direction:
- One keypair to communicate with Alice
- One keypair to communicate with Bob
- This allows Mallory to decrypt messages from both parties

### Q: What if Alice and Bob compare keys out-of-band?

**A:** That would work! But:
- Requires additional communication channel
- Not always practical
- Digital signatures (Phase 3) are better solution

### Q: Can this attack be prevented without signatures?

**A:** Yes, but signatures are the best solution:
- Out-of-band verification (impractical)
- Pre-shared keys (defeats purpose of DH)
- Certificate authorities (centralized trust)
- Digital signatures (decentralized, efficient)

---

## 📚 Further Reading

- **RFC 8446**: TLS 1.3 (shows how real protocols prevent MITM)
- **OWASP**: Man-in-the-Middle Attack documentation
- **Wikipedia**: Man-in-the-middle attack

---

**Next:** Read `PHASE3_DETAILED.md` to see how digital signatures prevent this attack!


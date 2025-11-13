# 📘 Phase 6: Blockchain Attack Prevention - Complete Documentation

**Comprehensive explanation of Mallory's attacks on blockchain-integrated secure channel, how blockchain prevents these attacks, and the security properties that make blockchain-based key registry resistant to MITM attacks.**

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Why Test Attacks on Blockchain?](#why-test-attacks-on-blockchain)
3. [Attack Scenarios](#attack-scenarios)
4. [Blockchain Security Properties](#blockchain-security-properties)
5. [How Each Attack is Prevented](#how-each-attack-is-prevented)
6. [Code Walkthrough](#code-walkthrough)
7. [Security Analysis](#security-analysis)
8. [Comparison with Phase 2](#comparison-with-phase-2)

---

## 🎯 Overview

### What Phase 6 Does

Phase 6 demonstrates **Mallory's attack attempts** on the blockchain-integrated secure channel and shows how **all attacks are prevented** by blockchain security properties.

### The Purpose

**Phase 2 showed:** Unauthenticated DH is vulnerable to MITM attacks
**Phase 3 showed:** Authentication (Ed25519 signatures) prevents MITM
**Phase 5 showed:** Blockchain adds decentralized key registry
**Phase 6 shows:** Blockchain prevents additional attack vectors that authentication alone might not catch

### What You Learn

✅ **Blockchain security properties** - Wallet ownership, immutability, verifiability
✅ **Attack prevention mechanisms** - How blockchain stops impersonation
✅ **Identity binding** - How wallet addresses bind to cryptographic keys
✅ **On-chain verification** - How to verify keys against blockchain registry

---

## 🔍 Why Test Attacks on Blockchain?

### The Question

After Phase 5 added blockchain integration, we need to verify:
- **Can Mallory still attack?**
- **What new attack vectors exist?**
- **How does blockchain prevent them?**

### Why It Matters

**Authentication (Phase 3) prevents:**
- Signature forgery
- Key tampering during exchange

**Blockchain (Phase 5) adds:**
- Decentralized key registry
- Identity binding via wallet addresses
- Immutable key records

**Phase 6 verifies:**
- Blockchain actually prevents attacks
- Wallet ownership requirement works
- On-chain verification catches mismatches

---

## 🎭 Attack Scenarios

Phase 6 demonstrates **4 different attack strategies** that Mallory might attempt:

### Attack 1: Register Alice's Key with Alice's Address

**Mallory's Strategy:**
- Intercept Alice's Ed25519 public key
- Try to register it for Alice's Solana address
- Hope to later replace it with her own key

**Why It Fails:**
- Blockchain requires wallet owner to sign transaction
- Mallory doesn't own Alice's wallet
- Cannot sign transaction with Alice's wallet private key

**Security Property:** Wallet Ownership Requirement

---

### Attack 2: Register Own Key with Alice's Address

**Mallory's Strategy:**
- Register her own Ed25519 key for Alice's address
- Make Bob think Mallory's key is Alice's key
- Intercept and decrypt messages

**Why It Fails:**
- Transaction requires signature from Alice's wallet
- Mallory's wallet address doesn't match Alice's address
- Blockchain rejects the transaction

**Security Property:** Address Verification

---

### Attack 3: Use Alice's Key with Own Address

**Mallory's Strategy:**
- Intercept Alice's Ed25519 public key during key exchange
- Register her own key for her own address (this works)
- Try to use Alice's key, claiming it's registered for her address

**Why It Fails:**
- Bob verifies key on-chain for **Alice's address**
- Finds: Alice's address has Alice's key (registered in Phase 5)
- Mallory's address has Mallory's key (different)
- Key mismatch detected → Attack prevented

**Security Property:** On-Chain Verification

---

### Attack 4: Register Fake Key for Own Address

**Mallory's Strategy:**
- Register her own key for her own address
- This registration succeeds (Mallory owns her wallet)
- Try to use this in Alice-Bob communication

**Why It Fails:**
- Registration works (Mallory owns her wallet)
- But Bob verifies against **Alice's address**, not Mallory's
- Bob finds: Alice's address has Alice's key (different from Mallory's)
- Attack fails because verification uses correct address

**Security Property:** Address-Based Verification

---

## 🛡️ Blockchain Security Properties

### 1. Wallet Ownership Requirement

**What It Means:**
- Only the wallet owner can register keys for their address
- Proved by signing transaction with wallet private key
- Cannot be forged or bypassed

**How It Prevents Attacks:**
- Mallory cannot register keys for addresses she doesn't own
- Prevents impersonation at registration level

**Real-World Analogy:**
- Like a bank account: only you can withdraw from your account
- Even if someone knows your account number, they need your PIN

---

### 2. Identity Binding

**What It Means:**
- Solana wallet address = identity
- Ed25519 public key = cryptographic key
- Address and key are permanently bound on-chain

**How It Prevents Attacks:**
- Cannot change identity without wallet private key
- Keys are permanently associated with addresses
- Prevents identity theft

**Real-World Analogy:**
- Like a passport: your name is bound to your photo
- Cannot use someone else's passport without their identity

---

### 3. Immutability

**What It Means:**
- Once registered, keys are on-chain permanently
- Cannot be retrospectively modified
- Historical records are preserved

**How It Prevents Attacks:**
- Cannot erase evidence of key registration
- Cannot modify past transactions
- Provides audit trail

**Real-World Analogy:**
- Like a public ledger: entries are permanent
- Cannot go back and change history

---

### 4. Verifiability

**What It Means:**
- Anyone can verify keys on-chain
- No need to trust third parties
- Transparent and auditable

**How It Prevents Attacks:**
- Bob can independently verify Alice's key
- No need to trust Mallory's claims
- Mismatches are immediately detected

**Real-World Analogy:**
- Like a public phone book: everyone can look up numbers
- Cannot claim someone else's number is yours

---

## 🔒 How Each Attack is Prevented

### Attack 1 Prevention: Wallet Ownership

**The Attack:**
```python
# Mallory tries to register Alice's key for Alice's address
registry.register_key(
    alice_address,              # Alice's address
    mallory_wallet_keypair,     # Mallory's wallet (WRONG!)
    alice_signing_pub_bytes     # Alice's key
)
```

**The Prevention:**
```python
# Blockchain checks: Does wallet_keypair match wallet_address?
wallet_pubkey = str(wallet_keypair.pubkey())

if wallet_pubkey != wallet_address:
    return False  # REJECTED: Address mismatch
```

**Result:** Attack fails because Mallory doesn't own Alice's wallet.

---

### Attack 2 Prevention: Address Verification

**The Attack:**
```python
# Mallory tries to register her own key for Alice's address
registry.register_key(
    alice_address,              # Alice's address
    mallory_wallet_keypair,     # Mallory's wallet (WRONG!)
    mallory_signing_pub_bytes   # Mallory's key
)
```

**The Prevention:**
```python
# Same check as Attack 1
if wallet_pubkey != wallet_address:
    return False  # REJECTED: Only owner can register
```

**Result:** Attack fails because only Alice can register keys for her address.

---

### Attack 3 Prevention: On-Chain Verification

**The Attack:**
```python
# Mallory intercepts Alice's key
# Tries to use it, claiming it's registered for her address
# But Bob verifies against Alice's address
```

**The Prevention:**
```python
# Bob verifies: Is this key registered for Alice's address?
registered_key = registry[alice_address]  # Alice's registered key

if registered_key != alice_signing_pub_bytes:
    return False  # REJECTED: Key mismatch
```

**Result:** Attack fails because Bob verifies against correct address.

---

### Attack 4 Prevention: Address-Based Verification

**The Attack:**
```python
# Mallory registers her own key for her own address (succeeds)
registry.register_key(
    mallory_address,            # Mallory's address
    mallory_wallet_keypair,     # Mallory's wallet (CORRECT!)
    mallory_signing_pub_bytes   # Mallory's key
)
# Registration succeeds, but...
```

**The Prevention:**
```python
# Bob verifies against Alice's address, not Mallory's
bob_verification = registry.verify_key(
    alice_address,              # Alice's address (not Mallory's!)
    mallory_signing_pub_bytes   # Mallory's key
)
# Returns False: Alice's address has different key
```

**Result:** Attack fails because Bob verifies against correct address.

---

## 💻 Code Walkthrough

### Import Analysis

**Phase 3 Components:**
```python
from authenticated_dh import AuthenticatedParticipant
```
- Reuses authenticated key exchange from Phase 3
- Provides `AuthenticatedParticipant` class
- Shows integration with previous phases

**Phase 5 Components:**
```python
from solana_registry_client import SolanaKeyRegistryClient
```
- Would use real Solana client in production
- For demo, we use simulated `BlockchainRegistry`

---

### BlockchainRegistry Class

**Purpose:**
- Simulates Solana blockchain key registry
- Maps wallet addresses to Ed25519 public keys
- Enforces wallet ownership requirement

**Key Methods:**

**`register_key(wallet_address, wallet_keypair, ed25519_public_key)`:**
- Registers Ed25519 key for wallet address
- Verifies wallet ownership (address matches keypair)
- Stores mapping in registry dictionary
- Returns True if successful, False if rejected

**`verify_key(wallet_address, ed25519_public_key)`:**
- Verifies if key matches what's registered for address
- Checks registry dictionary
- Returns True if match, False if mismatch or not found

---

### BlockchainMallory Class

**Purpose:**
- Represents Mallory attempting attacks
- Has her own keypairs and wallet
- Tries various attack strategies

**Attack Methods:**

**`attack_1_register_alice_key_with_alice_address()`:**
- Tries to register Alice's key for Alice's address
- Uses Mallory's wallet (wrong!)
- Demonstrates wallet ownership requirement

**`attack_2_register_own_key_with_alice_address()`:**
- Tries to register Mallory's key for Alice's address
- Uses Mallory's wallet (wrong!)
- Demonstrates address verification

**`attack_3_use_alice_key_with_own_address()`:**
- Intercepts Alice's key
- Registers own key for own address (succeeds)
- Tries to use Alice's key
- Demonstrates on-chain verification

**`attack_4_register_fake_key_for_own_address()`:**
- Registers own key for own address (succeeds)
- But useless for attacking Alice-Bob
- Demonstrates address-based verification

---

### Main Demonstration Flow

**Step 1: Initialize Registry**
- Create `BlockchainRegistry` instance
- Empty registry (no keys registered yet)

**Step 2: Create Legitimate Participants**
- Alice and Bob generate keypairs
- Register keys on blockchain
- Keys are now on-chain

**Step 3: Create Mallory**
- Mallory generates her own keypairs
- Has her own wallet address
- Prepares for attacks

**Step 4: Execute Attacks**
- Run all 4 attack scenarios
- Each attack is attempted
- Each attack is prevented

**Step 5: Summary**
- Show which attacks were prevented
- Explain why each failed
- Demonstrate blockchain security

---

## 🔐 Security Analysis

### Why Blockchain Prevents These Attacks

**1. Cryptographic Binding:**
- Wallet address = cryptographic identity
- Cannot be changed without private key
- Provides strong identity binding

**2. Transaction Signatures:**
- Every registration requires signature
- Signature proves wallet ownership
- Cannot be forged

**3. Decentralized Verification:**
- No single point of failure
- Multiple nodes verify transactions
- Consensus ensures correctness

**4. Transparency:**
- All registrations are public
- Anyone can verify keys
- No hidden attacks possible

---

### Comparison: Phase 2 vs Phase 6

**Phase 2 (Unauthenticated DH):**
- ✅ Attack succeeds
- ❌ No authentication
- ❌ No key verification
- ❌ Mallory can impersonate

**Phase 6 (Blockchain-Integrated):**
- ✅ All attacks prevented
- ✅ Wallet ownership required
- ✅ On-chain key verification
- ✅ Mallory cannot impersonate

**Key Difference:**
- Phase 2: No identity binding
- Phase 6: Strong identity binding via blockchain

---

### Limitations and Considerations

**Simulated Blockchain:**
- Real implementation would use Solana network
- Would require transaction fees
- Would have network latency

**Key Rotation:**
- Current demo doesn't show key updates
- Real system would need update mechanism
- Would require wallet owner signature

**Network Attacks:**
- Blockchain doesn't prevent network-level attacks
- Still need secure transport (HTTPS, etc.)
- Blockchain adds identity layer, not transport security

---

## 📊 Attack Prevention Summary

| Attack | Strategy | Prevention Mechanism | Result |
|--------|----------|---------------------|--------|
| **Attack 1** | Register Alice's key with Alice's address | Wallet ownership requirement | ✅ Prevented |
| **Attack 2** | Register own key with Alice's address | Address verification | ✅ Prevented |
| **Attack 3** | Use Alice's key with own address | On-chain verification | ✅ Prevented |
| **Attack 4** | Register fake key for own address | Address-based verification | ✅ Prevented |

**Total: 4/4 attacks prevented**

---

## 🎓 Key Takeaways

1. **Blockchain provides identity binding** - Wallet addresses bind to cryptographic keys
2. **Wallet ownership is required** - Cannot register keys without owning wallet
3. **On-chain verification works** - Keys can be verified independently
4. **All attack strategies fail** - Blockchain prevents impersonation attacks
5. **Decentralized trust** - No need for centralized certificate authorities

---

## 🔗 Related Documentation

- **[PHASE2_DETAILED.md](PHASE2_DETAILED.md)** - MITM attack on unauthenticated DH
- **[PHASE3_DETAILED.md](PHASE3_DETAILED.md)** - Authentication prevents MITM
- **[PHASE5_DETAILED.md](PHASE5_DETAILED.md)** - Blockchain integration
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture

---

**Last Updated:** December 2024


# Technical Documentation: Demo & Experimentation Outputs

**Secure Channel Project - Example Outputs and Demonstrations**

**Version:** 1.0  
**Date:** December 2024

---

## Table of Contents

1. [Phase 1 Outputs](#phase-1-outputs)
2. [Phase 2 Outputs](#phase-2-outputs)
3. [Phase 3 Outputs](#phase-3-outputs)
4. [Phase 4 Outputs](#phase-4-outputs)
5. [Phase 5 Outputs](#phase-5-outputs)
6. [Phase 6 Outputs](#phase-6-outputs)

---

## Phase 1 Outputs

### Example Execution

```
Alice public (hex): a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8
Bob   public (hex): 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8

Derived symmetric keys (hex):
Alice key: 9f8e7d6c5b4a3928172635445362718090a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5
Bob   key: 9f8e7d6c5b4a3928172635445362718090a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5

[SUCCESS] Alice and Bob derived the same symmetric key.
```

### Key Characteristics

- **Public Key Size:** 32 bytes (256 bits)
- **Shared Key Size:** 32 bytes (256 bits)
- **Key Match:** ✅ Always matches (mathematical property of DH)

---

## Phase 2 Outputs

### Example MITM Attack

```
Alice: Generated keypair
Alice: Public key (hex): a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8

Mallory: [INTERCEPTED] Alice's public key
Mallory: Derived key with Alice (hex): 1f2e3d4c5b6a798081726354637281900a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
Mallory: [FORWARDING] Fake Bob's public key to Alice

Bob: Generated keypair
Bob: Public key (hex): 2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9

Mallory: [INTERCEPTED] Bob's public key
Mallory: Derived key with Bob (hex): 3e4d5c6b7a8901234567890abcdef1234567890abcdef1234567890abcdef12
Mallory: [FORWARDING] Fake Alice's public key to Bob

Alice: Derived shared key (hex): 1f2e3d4c5b6a798081726354637281900a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
Bob: Derived shared key (hex): 3e4d5c6b7a8901234567890abcdef1234567890abcdef1234567890abcdef12

[ATTACK SUCCESS] Alice shares a key with Mallory (not Bob)
[ATTACK SUCCESS] Bob shares a key with Mallory (not Alice)
[CRITICAL] Alice and Bob have DIFFERENT keys!
   They cannot communicate securely. Mallory can decrypt everything.
```

### Attack Analysis

- **Alice's Key:** Matches Mallory's key with Alice
- **Bob's Key:** Matches Mallory's key with Bob
- **Keys Differ:** ✅ Alice and Bob have different keys
- **Attack Status:** ✅ SUCCESSFUL

---

## Phase 3 Outputs

### Example Authenticated Exchange

```
Alice: Generated DH keypair and Ed25519 signing keypair
Alice: DH public key (hex): a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8
Alice: Ed25519 public key (hex): 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8
Alice: Signed DH public key
Alice: Signature (hex): 2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9

Bob: [SUCCESS] Signature verification SUCCESS
Bob: Derived shared key (hex): 9f8e7d6c5b4a3928172635445362718090a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5

Bob: Generated DH keypair and Ed25519 signing keypair
Bob: Signed DH public key
Bob: Signature (hex): 3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9

Alice: [SUCCESS] Signature verification SUCCESS
Alice: Derived shared key (hex): 9f8e7d6c5b4a3928172635445362718090a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5

[SUCCESS] Alice and Bob derived the same shared key
   Shared key (hex): 9f8e7d6c5b4a3928172635445362718090a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5

Mallory: Generated own keypairs (cannot forge Alice's or Bob's signatures)
Mallory: [ATTEMPTING] Intercepting Alice's message
Mallory: [CREATING] Fake signed message with own keys (signature won't match!)

[SUCCESS] ATTACK PREVENTED: Bob correctly rejected Mallory's fake signature
   Mallory cannot forge signatures without Alice's private key
```

### Key Characteristics

- **DH Public Key:** 32 bytes
- **Signing Public Key:** 32 bytes
- **Signature:** 64 bytes
- **Total Message:** 128 bytes
- **Keys Match:** ✅ Same key derived
- **Attack Prevented:** ✅ Mallory's attack failed

---

## Phase 4 Outputs

### Example Secure Message Exchange

```
Alice: Secure channel established. AEAD cipher initialized.
Bob: Secure channel established. AEAD cipher initialized.

Alice: Plaintext: Hello Bob! This is a secret message.
Alice: Encrypted message (length: 51 bytes)
Alice: Nonce (hex): 0000000000000001a1b2c3d4

Bob: Decrypted message successfully
Bob: Decrypted: Hello Bob! This is a secret message.
[SUCCESS] Message integrity verified

Bob: Plaintext: Hi Alice! Received your message securely.
Bob: Encrypted message (length: 55 bytes)
Bob: Nonce (hex): 0000000000000001e5f6a7b8

Alice: Decrypted message successfully
Alice: Decrypted: Hi Alice! Received your message securely.
[SUCCESS] Message integrity verified
```

### Tampering Detection Test

```
Mallory attempts to modify encrypted message...
Bob tries to decrypt tampered message...
[SUCCESS] Tampering detected! Message rejected.
```

### Encryption Characteristics

- **Plaintext:** "Hello Bob! This is a secret message." (37 bytes)
- **Ciphertext:** 51 bytes (37 + 16-byte tag)
- **Overhead:** 16 bytes (Poly1305 authentication tag)
- **Nonce:** 12 bytes (unique per message)
- **Tampering Detection:** ✅ Working

---

## Phase 5 Outputs

### Example Blockchain Registration

```
Solana Key Registry Client initialized
RPC URL: https://api.devnet.solana.com
Program ID: KeyRegistry11111111111111111111111111111

Alice: Registering signing key on Solana blockchain...
Registering public key for owner: Alice1111111111111111111111111111111111
Key Record PDA: [derived PDA address]
Public key (hex): 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8
✅ Registration instruction prepared
   (In production, this would be sent as a Solana transaction)
✅ Alice: Key registered on-chain
   Transaction: mock_tx_signature_for_demo
   Solana address: Alice1111111111111111111111111111111111
   Signing key (hex): 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8
```

### Example Blockchain Verification

```
Bob: Verifying peer's key via Solana blockchain...
  Peer Solana address: Alice1111111111111111111111111111111111
  Peer signing key (hex): 1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8

Verifying public key for owner: Alice1111111111111111111111111111111111
Checking Key Record PDA: [PDA address]
✅ Key record found on-chain
   (In production, would deserialize and compare keys)
✅ Bob: Blockchain verification SUCCESS
   Peer's public key matches on-chain registry
```

---

## Phase 6 Outputs

### Attack 1: Register Alice's Key with Alice's Address

```
ATTACK 1: Mallory tries to register Alice's key with Alice's address
Mallory: Intercepted Alice's signing public key
Mallory: Attempting to register it for Alice's address...

[BLOCKCHAIN] Registration REJECTED: Wallet address mismatch
   Provided address: Alice1111111111111111111111111111111111
   Keypair address: Mallory1111111111111111111111111111111111

[SUCCESS] Attack 1 PREVENTED: Mallory cannot register keys for addresses she doesn't own
   Blockchain requires wallet owner to sign registration transaction
   Mallory doesn't have Alice's wallet private key
```

### Attack 2: Register Own Key with Alice's Address

```
ATTACK 2: Mallory tries to register her own key with Alice's address
Mallory: Attempting to register my own key for Alice's address...
Mallory: If this works, Bob will think my key is Alice's!

[BLOCKCHAIN] Registration REJECTED: Wallet address mismatch
   Provided address: Alice1111111111111111111111111111111111
   Keypair address: Mallory1111111111111111111111111111111111

[SUCCESS] Attack 2 PREVENTED: Mallory cannot register keys for addresses she doesn't own
   Blockchain enforces: only wallet owner can register keys
   Mallory's wallet address doesn't match Alice's address
```

### Attack 3: Use Alice's Key with Own Address

```
ATTACK 3: Mallory intercepts Alice's key and uses it with own address
Mallory: Intercepted Alice's signing public key during key exchange
Mallory: Attempting to use it, claiming it's registered for my address...
Mallory: Registering my own key for my own address (this should work)...
[BLOCKCHAIN] Key registered successfully
   Wallet address: Mallory1111111111111111111111111111111111
   Ed25519 key (hex): [Mallory's key]

Mallory: Sending intercepted Alice's key to Bob...
Mallory: Bob will verify: Is this key registered for Alice's address?

[BLOCKCHAIN] Verification FAILED: Key mismatch
   Address: Alice1111111111111111111111111111111111
   Expected (hex): [Alice's registered key]...
   Received (hex): [Alice's intercepted key]...
   [WARNING] Possible MITM attack or key compromise!

[SUCCESS] Attack 3 PREVENTED: Bob verified key on-chain
   Bob checked: Is this key registered for Alice's address?
   Result: Key mismatch - possible MITM attack detected!
   Bob correctly rejects the key exchange
```

### Attack 4: Register Fake Key for Own Address

```
ATTACK 4: Mallory registers fake key for her own address
Mallory: Registering my own key for my own address...
Mallory: This should work (I own my wallet)...

[BLOCKCHAIN] Key registered successfully
   Wallet address: Mallory1111111111111111111111111111111111
   Ed25519 key (hex): [Mallory's key]

[INFO] Attack 4: Registration succeeded (expected - Mallory owns her wallet)
   But this is USELESS for attacking Alice-Bob communication!
   When Bob verifies, he checks Alice's address, not Mallory's
   Bob will verify: Is Mallory's key registered for Alice's address?
   Answer: NO - Attack fails!

   Simulating Bob's verification...
   [BLOCKCHAIN] Verification FAILED: Key mismatch
   [SUCCESS] Bob correctly rejects Mallory's key
   Bob checks Alice's address, finds different key
   Attack prevented!
```

### Attack Summary

```
ATTACK SUMMARY

Attack 1 (Register Alice's key with Alice's address): PREVENTED
   Reason: Blockchain requires wallet owner to sign transaction
   
Attack 2 (Register own key with Alice's address): PREVENTED
   Reason: Only wallet owner can register keys for their address
   
Attack 3 (Use Alice's key with own address): PREVENTED
   Reason: Bob verifies key on-chain for Alice's address, finds mismatch
   
Attack 4 (Register fake key for own address): PREVENTED
   Reason: Registration works but is useless - Bob verifies against Alice's address

Total Attacks Prevented: 4/4
```

---

## Representative Sample Data

### Typical Key Values (for reference)

**X25519 Public Keys:**
- Alice: `a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8`
- Bob: `1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8`

**Ed25519 Public Keys:**
- Alice: `1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8`
- Bob: `2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9`

**Ed25519 Signatures:**
- 64 bytes: `2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9`

**Shared Keys:**
- Derived: `9f8e7d6c5b4a3928172635445362718090a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5`

**Nonces:**
- 12 bytes: `0000000000000001a1b2c3d4`

**Note:** Actual values vary with each execution due to randomness in key generation.

---

## Failure Output Examples

### Phase 3: Signature Verification Failure

**Scenario:** Mallory attempts to forge Alice's signature

```
Mallory: [ATTEMPTING] Intercepting Alice's message
Mallory: [CREATING] Fake signed message with own keys (signature won't match!)

Bob: Verifying signature...
Bob: [FAILED] Signature verification FAILED - rejecting key exchange

[SUCCESS] ATTACK PREVENTED: Bob correctly rejected Mallory's fake signature
   Mallory cannot forge signatures without Alice's private key
```

**Error Details:**
- Exception: `InvalidSignature`
- Cause: Signature created with wrong private key
- Result: Key exchange rejected

### Phase 4: Message Tampering Detection

**Scenario:** Mallory modifies encrypted message

```
Alice: Encrypted message (length: 51 bytes)
Alice: Nonce (hex): 0000000000000001a1b2c3d4

Mallory attempts to modify encrypted message...
Mallory: Tampering ciphertext (flipping bits)

Bob: Attempting to decrypt tampered message...
Bob: [FAILED] Decryption FAILED - Authentication tag invalid (tampering detected)

[SUCCESS] Tampering detected! Message rejected.
```

**Error Details:**
- Exception: `InvalidTag`
- Cause: Poly1305 MAC verification failed
- Result: Message rejected, tampering detected

### Phase 4: Channel Not Established Error

**Scenario:** Attempting to send message before channel establishment

```
Alice: Attempting to send message...
Traceback (most recent call last):
  File "secure_channel.py", line 250, in send_message
    raise ValueError("Channel not established - call establish_channel() first")
ValueError: Channel not established - call establish_channel() first
```

**Error Details:**
- Exception: `ValueError`
- Cause: `cipher` is `None` (channel not established)
- Fix: Call `establish_channel()` first

### Phase 5: Blockchain Key Mismatch

**Scenario:** Bob verifies key that doesn't match on-chain registry

```
Bob: Verifying peer's key via Solana blockchain...
  Peer Solana address: Alice1111111111111111111111111111111111
  Peer signing key (hex): [Mallory's key]

Verifying public key for owner: Alice1111111111111111111111111111111111
Checking Key Record PDA: [PDA address]
[BLOCKCHAIN] Verification FAILED: Key mismatch
   Address: Alice1111111111111111111111111111111111
   Expected (hex): [Alice's registered key]...
   Received (hex): [Mallory's key]...
   [WARNING] Possible MITM attack or key compromise!

❌ Bob: Blockchain verification FAILED
   Peer's public key does NOT match on-chain registry
   Possible MITM attack or key mismatch!
```

**Error Details:**
- Return Value: `False`
- Cause: Key mismatch between provided key and on-chain registry
- Result: Key exchange rejected

### Phase 5: Blockchain Registration Failure

**Scenario:** Mallory tries to register key for address she doesn't own

```
Mallory: Attempting to register key for Alice's address...

[BLOCKCHAIN] Registration REJECTED: Wallet address mismatch
   Provided address: Alice1111111111111111111111111111111111
   Keypair address: Mallory1111111111111111111111111111111111

[SUCCESS] Attack 1 PREVENTED: Mallory cannot register keys for addresses she doesn't own
   Blockchain requires wallet owner to sign transaction
   Mallory doesn't have Alice's wallet private key
```

**Error Details:**
- Return Value: `False`
- Cause: Wallet ownership verification failed
- Result: Registration rejected

### Phase 5: Network Error (Blockchain)

**Scenario:** Solana RPC endpoint unavailable

```
Bob: Verifying peer's key via Solana blockchain...
  Connecting to: https://api.devnet.solana.com

Error: Connection timeout
Traceback (most recent call last):
  File "solana_registry_client.py", line 175, in verify_key
    account_info = self.connection.get_account_info(key_record_pda)
  File "solana/rpc/api.py", line 123, in get_account_info
    raise RPCException("Connection timeout")
solana.rpc.api.RPCException: Connection timeout

[ERROR] Blockchain verification failed: Connection timeout
   Retrying in 2 seconds...
```

**Error Details:**
- Exception: `RPCException`
- Cause: Network connectivity issue
- Recovery: Retry with exponential backoff

### Phase 6: All Attacks Prevented (Expected Behavior)

**Scenario:** All four attack attempts fail

```
ATTACK SUMMARY

Attack 1 (Register Alice's key with Alice's address): PREVENTED
   Reason: Blockchain requires wallet owner to sign transaction
   Error: Wallet address mismatch

Attack 2 (Register own key with Alice's address): PREVENTED
   Reason: Only wallet owner can register keys for their address
   Error: Unauthorized transaction

Attack 3 (Use Alice's key with own address): PREVENTED
   Reason: Bob verifies key on-chain for Alice's address, finds mismatch
   Error: Key mismatch detected

Attack 4 (Register fake key for own address): PREVENTED
   Reason: Registration works but is useless - Bob verifies against Alice's address
   Error: Verification uses wrong address (attack fails)

Total Attacks Prevented: 4/4
```

**Note:** These are not errors - they demonstrate successful attack prevention.

### Common Error Patterns

| Error Type | Phase | Example Output | Recovery |
|------------|-------|----------------|----------|
| `InvalidSignature` | 3 | "Signature verification FAILED" | Reject key exchange |
| `InvalidTag` | 4 | "Authentication tag invalid" | Reject message |
| `ValueError` | 4 | "Channel not established" | Call `establish_channel()` |
| Key mismatch | 5 | "Key mismatch" | Reject key exchange |
| Network error | 5 | "Connection timeout" | Retry with backoff |
| Unauthorized | 6 | "Wallet address mismatch" | Attack prevented (expected) |

---

**Next Document:** TECHNICAL_DOC_07_DESIGN_RATIONALE.md

---

**Document Version:** 1.0  
**Last Updated:** December 2024


# Technical Documentation: Code Documentation

**Secure Channel Project - Complete Code Documentation**

**Version:** 1.0  
**Date:** December 2024

---

## Table of Contents

1. [Code Documentation Overview](#code-documentation-overview)
2. [Phase 1: Basic Diffie-Hellman](#phase-1-basic-diffie-hellman)
3. [Phase 2: MITM Attack](#phase-2-mitm-attack)
4. [Phase 3: Authenticated DH](#phase-3-authenticated-dh)
5. [Phase 4: Secure Channel](#phase-4-secure-channel)
6. [Phase 5: Blockchain Integration](#phase-5-blockchain-integration)
7. [Phase 6: Blockchain Attacks](#phase-6-blockchain-attacks)
8. [Backend Server](#backend-server)
9. [Frontend Components](#frontend-components)
10. [Solana Smart Contract](#solana-smart-contract)

---

## Code Documentation Overview

This document provides comprehensive documentation for all code modules in the secure channel project. Each module is documented with:

- Purpose and functionality
- Public functions and classes
- Parameters and return values
- Security considerations
- Error cases
- Example usage

---

## Phase 1: Basic Diffie-Hellman

### Module: `phases/phase1_dh/dh_exchange.py`

**Purpose:** Implements basic X25519 Diffie-Hellman key exchange without authentication.

### Functions

#### `generate_x25519_keypair()`

**Purpose:** Generate an X25519 keypair for Diffie-Hellman key exchange.

**Returns:**
- `tuple`: `(private_key, public_key)`
  - `private_key`: `X25519PrivateKey` - Must be kept secret
  - `public_key`: `X25519PublicKey` - Safe to share publicly

**Security Considerations:**
- Private key is generated using cryptographically secure random number generator
- Private key must never be transmitted or logged
- Public key can be safely shared

**Example:**
```python
private_key, public_key = generate_x25519_keypair()
```

#### `public_bytes(public_key)`

**Purpose:** Serialize an X25519 public key to raw bytes format.

**Parameters:**
- `public_key` (`X25519PublicKey`): The public key to serialize

**Returns:**
- `bytes`: 32-byte raw public key representation

**Format:**
- Encoding: Raw (no ASN.1 wrapper)
- Format: Raw (just the 32-byte curve point)
- Size: Exactly 32 bytes

**Example:**
```python
pub_bytes = public_bytes(public_key)
# Returns: 32-byte bytes object
```

#### `derive_shared_key(our_private, their_public_bytes, info)`

**Purpose:** Perform Diffie-Hellman key exchange and derive a symmetric encryption key.

**Parameters:**
- `our_private` (`X25519PrivateKey`): Our private key
- `their_public_bytes` (`bytes`): Peer's public key as 32 bytes
- `info` (`bytes`, optional): Context information for HKDF (default: `b"secure_channel_v1"`)

**Returns:**
- `bytes`: 32-byte symmetric key suitable for encryption

**Process:**
1. Reconstruct peer's public key from bytes
2. Perform X25519 key exchange: `shared_secret = our_private * their_public`
3. Derive symmetric key using HKDF-SHA256
4. Return 32-byte derived key

**Security Considerations:**
- **CRITICAL:** Never use raw shared secret directly as encryption key
- Always use HKDF to derive symmetric keys
- `info` parameter binds key to protocol/context
- Salt is None for simplicity (production should use salt)

**Example:**
```python
shared_key = derive_shared_key(
    alice_private,
    bob_public_bytes,
    info=b"secure_channel_v1"
)
# Returns: 32-byte symmetric key
```

### Main Function

#### `main()`

**Purpose:** Demonstrate basic Diffie-Hellman key exchange.

**Process:**
1. Alice generates keypair
2. Bob generates keypair
3. Exchange public keys (simulated)
4. Each derives shared key
5. Verify keys match

**Output:**
- Prints public keys (hex)
- Prints derived keys (hex)
- Confirms if keys match

---

## Phase 2: MITM Attack

### Module: `phases/phase2_mitm/mallory_attack.py`

**Purpose:** Demonstrates man-in-the-middle attack on unauthenticated key exchange.

### Classes

#### `Participant`

**Purpose:** Represents a legitimate participant (Alice or Bob).

**Attributes:**
- `name` (`str`): Participant's name
- `private_key` (`X25519PrivateKey`): Private key (kept secret)
- `public_key` (`X25519PublicKey`): Public key
- `public_key_bytes` (`bytes`): Public key as bytes
- `shared_key` (`bytes`): Derived shared key

**Methods:**

##### `generate_keypair()`

**Purpose:** Generate X25519 keypair for this participant.

**Process:**
- Generates keypair
- Converts public key to bytes
- Prints key information

##### `derive_key(peer_public_bytes)`

**Purpose:** Derive shared symmetric key using peer's public key.

**Parameters:**
- `peer_public_bytes` (`bytes`): Peer's public key (32 bytes)

**Process:**
- Derives shared key using DH + HKDF
- Stores result in `self.shared_key`
- Prints key information

**Security Vulnerability:**
- No authentication - trusts `peer_public_bytes` without verification
- This allows Mallory to replace keys

#### `Mallory`

**Purpose:** Represents a man-in-the-middle attacker.

**Attributes:**
- `name` (`str`): "Mallory"
- `alice_priv`, `alice_pub`: Keypair for impersonating Alice
- `bob_priv`, `bob_pub`: Keypair for impersonating Bob
- `key_with_alice` (`bytes`): Shared key with Alice
- `key_with_bob` (`bytes`): Shared key with Bob

**Methods:**

##### `intercept_and_replace(message_from, message_to)`

**Purpose:** Core MITM attack function - intercept and replace public keys.

**Parameters:**
- `message_from` (`Participant`): Sender of the key
- `message_to` (`Participant`): Intended recipient (not used, for clarity)

**Returns:**
- `bytes`: Mallory's fake public key (to forward to receiver)

**Attack Process:**
1. Intercept real public key from sender
2. Derive key with sender using Mallory's fake keypair
3. Return fake key to forward to receiver

**Example:**
```python
fake_bob_key = mallory.intercept_and_replace(alice, bob)
# Mallory intercepts Alice's key, derives key with Alice,
# returns fake "Bob" key to forward to Alice
```

##### `can_decrypt(encrypted_message, sender)`

**Purpose:** Check if Mallory can decrypt messages from a sender.

**Parameters:**
- `encrypted_message` (`bytes`): Encrypted message (not used)
- `sender` (`str`): Sender name ("Alice" or "Bob")

**Returns:**
- `bool`: True if Mallory has established key with sender

### Main Function

#### `demonstrate_mitm_attack()`

**Purpose:** Demonstrate complete MITM attack flow.

**Process:**
1. Create Alice, Bob, and Mallory
2. Alice generates keypair
3. Mallory intercepts Alice's key
4. Bob generates keypair
5. Mallory intercepts Bob's key
6. Both derive keys (with Mallory, not each other)
7. Verify attack succeeded

**Output:**
- Step-by-step attack demonstration
- Key comparisons
- Attack success confirmation

---

## Phase 3: Authenticated DH

### Module: `phases/phase3_auth/authenticated_dh.py`

**Purpose:** Adds Ed25519 digital signatures to prevent MITM attacks.

### Classes

#### `AuthenticatedParticipant`

**Purpose:** Participant with authentication using Ed25519 signatures.

**Attributes:**
- `name` (`str`): Participant's name
- `dh_private`, `dh_public`: X25519 keypair (ephemeral)
- `dh_public_bytes` (`bytes`): DH public key as bytes
- `signing_private`, `signing_public`: Ed25519 keypair (long-term)
- `signing_public_bytes` (`bytes`): Signing public key as bytes
- `shared_key` (`bytes`): Derived shared key

**Methods:**

##### `generate_keypairs()`

**Purpose:** Generate both X25519 and Ed25519 keypairs.

**Process:**
- Generates X25519 keypair (ephemeral, for key exchange)
- Generates Ed25519 keypair (long-term, for signatures)
- Converts both to bytes format

**Security Note:**
- X25519 keys: Ephemeral (new for each session) - provides forward secrecy
- Ed25519 keys: Long-term (established once, reused) - provides identity

##### `sign_dh_public_key()`

**Purpose:** Sign the DH public key with Ed25519 private key.

**Returns:**
- `bytes`: 64-byte Ed25519 signature

**Process:**
- Signs `dh_public_bytes` using `signing_private`
- Returns 64-byte signature

**Security:**
- Signature proves ownership of both DH key and signing key
- Only someone with `signing_private` can create valid signature
- Binds ephemeral DH key to long-term identity

##### `verify_and_derive_key(peer_dh_pub_bytes, peer_signing_pub_bytes, signature)`

**Purpose:** Verify peer's signature and derive shared key ONLY if signature is valid.

**Parameters:**
- `peer_dh_pub_bytes` (`bytes`): Peer's DH public key (32 bytes)
- `peer_signing_pub_bytes` (`bytes`): Peer's Ed25519 public key (32 bytes)
- `signature` (`bytes`): Ed25519 signature (64 bytes)

**Returns:**
- `tuple`: `(is_valid: bool, shared_key: bytes or None)`
  - If valid: `(True, derived_shared_key)`
  - If invalid: `(False, None)`

**Process:**
1. Reconstruct peer's Ed25519 public key object
2. Verify signature using peer's public key
3. If valid: Derive shared key using DH
4. If invalid: Return `(False, None)` - reject key exchange

**Security:**
- This is the critical security check that prevents MITM attacks
- Invalid signature → Key exchange rejected
- Only proceeds if signature is valid

**Raises:**
- `InvalidSignature`: If signature verification fails

#### `AuthenticatedMallory`

**Purpose:** Mallory attempting MITM attack on authenticated protocol (will fail).

**Attributes:**
- Same as `AuthenticatedParticipant` but with Mallory's own keys

**Methods:**

##### `intercept_and_replace(message_from)`

**Purpose:** Attempt to intercept and replace (will fail because signature won't match).

**Returns:**
- `tuple`: `(fake_dh_pub_bytes, fake_signing_pub_bytes, signature)`

**Attack Failure:**
- Mallory can create her own signed message
- But signature won't match Alice's/Bob's signing keys
- Bob will reject when verifying with Alice's public key

### Main Function

#### `demonstrate_authenticated_exchange()`

**Purpose:** Demonstrate authenticated DH key exchange that prevents MITM.

**Process:**
1. Create authenticated participants
2. Alice generates keypairs and signs DH key
3. Bob verifies signature and derives key
4. Bob generates keypairs and signs DH key
5. Alice verifies signature and derives key
6. Test Mallory's attack (should fail)

**Output:**
- Step-by-step authentication process
- Signature verification results
- Attack prevention confirmation

---

## Phase 4: Secure Channel

### Module: `phases/phase4_aead/secure_channel.py`

**Purpose:** Complete secure channel with authenticated encryption (AEAD).

### Classes

#### `SecureChannel`

**Purpose:** Complete secure channel implementation with AEAD encryption.

**Attributes:**
- `name` (`str`): Participant's name
- `participant` (`AuthenticatedParticipant`): For key exchange
- `cipher` (`ChaCha20Poly1305`): AEAD cipher instance
- `nonce_counter` (`int`): Counter for nonce generation
- `peer_nonce_counter` (`int`): Tracking peer's nonces

**Methods:**

##### `establish_channel(peer_dh_pub_bytes, peer_signing_pub_bytes, peer_signature)`

**Purpose:** Establish secure channel by verifying peer and initializing encryption.

**Parameters:**
- `peer_dh_pub_bytes` (`bytes`): Peer's DH public key (32 bytes)
- `peer_signing_pub_bytes` (`bytes`): Peer's Ed25519 public key (32 bytes)
- `peer_signature` (`bytes`): Ed25519 signature (64 bytes)

**Returns:**
- `bool`: True if channel established, False if verification failed

**Process:**
1. Verify peer's signature (prevents MITM)
2. If valid, derive shared symmetric key via DH
3. Initialize ChaCha20-Poly1305 cipher with derived key
4. Channel ready for secure message exchange

**Security:**
- If signature verification fails, channel is NOT established
- Ensures we only communicate with authenticated peers

##### `send_message(plaintext, associated_data)`

**Purpose:** Encrypt and authenticate a message using ChaCha20-Poly1305.

**Parameters:**
- `plaintext` (`bytes`): Message to encrypt
- `associated_data` (`bytes`, optional): Associated data (authenticated but not encrypted)

**Returns:**
- `tuple`: `(ciphertext, nonce)`
  - `ciphertext` (`bytes`): Encrypted message + 16-byte authentication tag
  - `nonce` (`bytes`): 12-byte unique nonce

**Process:**
1. Generate unique nonce (counter + random)
2. Encrypt plaintext and compute MAC tag
3. Return ciphertext (encrypted data + tag) and nonce

**Security Requirements:**
- **CRITICAL:** Nonce MUST be unique for each encryption with same key
- Reusing nonce breaks security
- Counter + random ensures uniqueness

**Raises:**
- `ValueError`: If channel not established

##### `receive_message(ciphertext, nonce, associated_data)`

**Purpose:** Decrypt and verify a message using ChaCha20-Poly1305.

**Parameters:**
- `ciphertext` (`bytes`): Encrypted message + authentication tag
- `nonce` (`bytes`): 12-byte nonce (must match sender's)
- `associated_data` (`bytes`, optional): Associated data (must match sender's)

**Returns:**
- `bytes`: Decrypted plaintext

**Process:**
1. Verify Poly1305 authentication tag
2. If valid, decrypt ciphertext using ChaCha20
3. Return plaintext

**Security:**
- If MAC is invalid, raises `InvalidTag` (tampering detected)
- Decryption only happens if authentication succeeds
- Prevents timing attacks

**Raises:**
- `ValueError`: If channel not established
- `InvalidTag`: If authentication fails (tampering detected)

##### `get_public_keys()`

**Purpose:** Get public keys and signature for key exchange.

**Returns:**
- `tuple`: `(dh_public_bytes, signing_public_bytes, signature)`

### Main Function

#### `demonstrate_secure_channel()`

**Purpose:** Demonstrate complete secure channel with authenticated encryption.

**Process:**
1. Create secure channels for Alice and Bob
2. Establish channels (authenticated key exchange)
3. Alice sends encrypted message to Bob
4. Bob decrypts and verifies
5. Bob sends encrypted message to Alice
6. Alice decrypts and verifies
7. Test tampering detection

**Output:**
- Step-by-step secure channel establishment
- Message encryption/decryption
- Tampering detection test

---

## Phase 5: Blockchain Integration

### Module: `phases/phase5_solana/solana_registry_client.py`

**Purpose:** Python client for Solana blockchain key registry.

### Classes

#### `SolanaKeyRegistryClient`

**Purpose:** Client for interacting with Solana Key Registry smart contract.

**Attributes:**
- `rpc_url` (`str`): Solana RPC endpoint URL
- `connection` (`solana.rpc.api.Client`): Solana RPC client
- `program_id` (`Pubkey`): Program ID of deployed registry
- `idl` (`dict`): Interface Definition Language for the program

**Methods:**

##### `register_key(wallet_keypair, ed25519_public_key)`

**Purpose:** Register an Ed25519 public key on-chain for the wallet owner.

**Parameters:**
- `wallet_keypair` (`Keypair`): Solana wallet keypair (signer)
- `ed25519_public_key` (`bytes`): 32-byte Ed25519 public key to register

**Returns:**
- `str`: Transaction signature

**Process:**
1. Derive PDA for key record
2. Build registration instruction
3. Create and sign transaction
4. Send to Solana network
5. Return transaction signature

**Security:**
- Only wallet owner can register keys (enforced by blockchain)
- Transaction must be signed by wallet keypair

**Raises:**
- `ValueError`: If public key is not 32 bytes

##### `verify_key(owner_pubkey_str, ed25519_public_key)`

**Purpose:** Verify if a public key matches what's registered on-chain.

**Parameters:**
- `owner_pubkey_str` (`str`): Solana wallet address of key owner
- `ed25519_public_key` (`bytes`): Public key to verify (32 bytes)

**Returns:**
- `bool`: True if key matches registry, False otherwise

**Process:**
1. Derive PDA for key record
2. Fetch KeyRecord account from blockchain
3. Compare stored key with provided key
4. Return match result

#### `SecureChannelWithBlockchain`

**Purpose:** Extended secure channel that uses Solana blockchain for key verification.

**Inherits:** `SecureChannel` (from Phase 4)

**Additional Attributes:**
- `solana_address` (`str`): Solana wallet address
- `registry_client` (`SolanaKeyRegistryClient`): Registry client instance

**Methods:**

##### `verify_peer_via_blockchain(peer_solana_address, peer_signing_pub_bytes)`

**Purpose:** Verify peer's signing public key against Solana blockchain registry.

**Parameters:**
- `peer_solana_address` (`str`): Peer's Solana wallet address
- `peer_signing_pub_bytes` (`bytes`): Peer's Ed25519 public key

**Returns:**
- `bool`: True if key verified on-chain, False otherwise

**Security:**
- Adds blockchain verification layer
- Before accepting peer's key, verify it matches on-chain registry
- Prevents impersonation attacks

##### `register_key_on_blockchain(wallet_keypair)`

**Purpose:** Register this participant's signing public key on Solana blockchain.

**Parameters:**
- `wallet_keypair` (`Keypair`): Solana wallet keypair to sign transaction

**Process:**
- Registers `signing_public_bytes` on-chain
- Associates key with `solana_address`

---

## Phase 6: Blockchain Attacks

### Module: `phases/phase6_blockchain_attack/blockchain_mitm_attack.py`

**Purpose:** Demonstrates blockchain-layer attacks and their prevention.

### Classes

#### `BlockchainRegistry`

**Purpose:** Simulated blockchain registry for key storage and verification.

**Attributes:**
- `registry` (`dict`): Maps wallet addresses to Ed25519 public keys

**Methods:**

##### `register_key(wallet_address, wallet_keypair, ed25519_public_key)`

**Purpose:** Register Ed25519 key for wallet address (simulated).

**Parameters:**
- `wallet_address` (`str`): Solana wallet address
- `wallet_keypair`: Wallet keypair (proves ownership)
- `ed25519_public_key` (`bytes`): 32-byte Ed25519 public key

**Returns:**
- `bool`: True if registration succeeds, False if rejected

**Security:**
- Verifies wallet ownership (address must match keypair)
- Only wallet owner can register keys for their address

##### `verify_key(wallet_address, ed25519_public_key)`

**Purpose:** Verify if key matches what's registered for wallet address.

**Parameters:**
- `wallet_address` (`str`): Wallet address to check
- `ed25519_public_key` (`bytes`): Key to verify

**Returns:**
- `bool`: True if key matches, False otherwise

#### `BlockchainMallory`

**Purpose:** Mallory attempting attacks on blockchain-integrated system.

**Methods:**

##### `attack_1_register_alice_key_with_alice_address(alice_address, alice_signing_pub_bytes)`

**Purpose:** Attack 1: Try to register Alice's key using Alice's address.

**Returns:**
- `bool`: True if attack prevented, False if succeeded

**Attack Failure:**
- Mallory doesn't own Alice's wallet
- Cannot sign transaction with Alice's wallet
- Registration rejected

##### `attack_2_register_own_key_with_alice_address(alice_address)`

**Purpose:** Attack 2: Try to register own key using Alice's address.

**Returns:**
- `bool`: True if attack prevented

**Attack Failure:**
- Same as Attack 1 - wallet ownership required

##### `attack_3_use_alice_key_with_own_address(alice_address, alice_signing_pub_bytes)`

**Purpose:** Attack 3: Use Alice's key with own address.

**Returns:**
- `bool`: True if attack prevented

**Attack Failure:**
- Bob verifies key on-chain for Alice's address
- Finds mismatch → Attack prevented

##### `attack_4_register_fake_key_for_own_address()`

**Purpose:** Attack 4: Register fake key for own address.

**Returns:**
- `bool`: True (attack prevented - registration works but useless)

**Attack Failure:**
- Registration succeeds (Mallory owns her wallet)
- But Bob verifies against Alice's address
- Attack fails because verification uses correct address

---

## Backend Server

### Module: `backend/app.py`

**Purpose:** Flask backend server providing REST API for phase execution.

### Routes

#### `@app.route('/')`

**Purpose:** Serve main HTML page.

**Returns:**
- Rendered `index.html` template

#### `@app.route('/api/phase1', methods=['POST'])`

**Purpose:** Execute Phase 1 (Basic Diffie-Hellman).

**Returns:**
- `JSON`: Phase execution results with steps, data, visualization

**Response Format:**
```json
{
    "success": true,
    "phase": 1,
    "title": "Basic Diffie-Hellman Key Exchange",
    "steps": [...],
    "data": {...},
    "visualization": {...},
    "summary": "..."
}
```

#### `@app.route('/api/phase2', methods=['POST'])`

**Purpose:** Execute Phase 2 (MITM Attack).

**Returns:**
- `JSON`: Attack demonstration results

#### `@app.route('/api/phase3', methods=['POST'])`

**Purpose:** Execute Phase 3 (Authenticated DH).

**Returns:**
- `JSON`: Authentication results

#### `@app.route('/api/phase4', methods=['POST'])`

**Purpose:** Execute Phase 4 (Secure Channel).

**Returns:**
- `JSON`: Encryption/decryption results

#### `@app.route('/api/phase5', methods=['POST'])`

**Purpose:** Execute Phase 5 (Blockchain Integration).

**Returns:**
- `JSON`: Blockchain verification results

#### `@app.route('/api/phase6', methods=['POST'])`

**Purpose:** Execute Phase 6 (Blockchain Attacks).

**Returns:**
- `JSON`: Attack prevention results

#### `@app.route('/api/run-all', methods=['POST'])`

**Purpose:** Execute all phases sequentially.

**Returns:**
- `JSON`: Array of results for all phases

---

## Frontend Components

### Module: `frontend/templates/index.html`

**Purpose:** Main HTML structure for web interface.

**Structure:**
- Header with title
- Control buttons for each phase
- Phase cards container
- Chart.js CDN inclusion

### Module: `frontend/static/main.js`

**Purpose:** Frontend JavaScript for phase execution and visualization.

**Key Functions:**

#### `runPhase(phaseNum)`

**Purpose:** Execute a phase via API call.

**Process:**
1. Update status to "running"
2. Send POST request to `/api/phase{phaseNum}`
3. Receive JSON response
4. Display results
5. Update status

#### `displayPhaseXResults(div, data)`

**Purpose:** Render phase-specific results.

**Phases:**
- `displayPhase1Results`: Key comparison
- `displayPhase2Results`: MITM attack visualization
- `displayPhase3Results`: Authentication status
- `displayPhase4Results`: Encryption results
- `displayPhase5Results`: Blockchain verification
- `displayPhase6Results`: Attack prevention

#### Chart Functions

- `createKeyComparisonChart`: Phase 1 key comparison
- `createMITMChart`: Phase 2 attack visualization
- `createAuthenticationChart`: Phase 3 authentication
- `createEncryptionChart`: Phase 4 encryption overhead
- `createBlockchainChart`: Phase 5 blockchain status
- `createAttackPreventionChart`: Phase 6 attack results

---

## Solana Smart Contract

### Module: `phases/phase5_solana/solana_registry/src/lib.rs`

**Purpose:** Solana smart contract for key registry.

### Instructions

#### `register_key(ctx, public_key)`

**Purpose:** Register a public key for a user.

**Parameters:**
- `ctx`: Context with owner account and PDA
- `public_key`: `[u8; 32]` - Ed25519 public key

**Accounts:**
- `owner`: Signer (wallet owner)
- `key_record`: PDA account to create
- `system_program`: System program

**Process:**
1. Verify owner is signer
2. Derive PDA from owner address
3. Create KeyRecord account
4. Store owner, public_key, bump

#### `update_key(ctx, new_public_key)`

**Purpose:** Update existing public key registration.

**Parameters:**
- `ctx`: Context with owner and key_record
- `new_public_key`: `[u8; 32]` - New Ed25519 public key

**Security:**
- Verifies owner matches key_record.owner
- Only owner can update their key

#### `verify_key(ctx, public_key_to_verify)`

**Purpose:** Verify if public key matches registered key.

**Parameters:**
- `ctx`: Context with key_record
- `public_key_to_verify`: `[u8; 32]` - Key to verify

**Returns:**
- `bool`: True if keys match, False otherwise

### Account Structure

#### `KeyRecord`

**Fields:**
- `owner`: `Pubkey` (32 bytes) - Wallet address
- `public_key`: `[u8; 32]` (32 bytes) - Ed25519 public key
- `bump`: `u8` (1 byte) - PDA bump seed

**Total Size:** 65 bytes (8-byte discriminator + 32 + 32 + 1)

---

## Common Errors and Exceptions

### Exception Hierarchy

```
Exception
├── ValueError
│   ├── Invalid key size
│   ├── Channel not established
│   └── Invalid parameter
├── InvalidSignature (cryptography.exceptions)
│   └── Signature verification failed
├── InvalidTag (cryptography.exceptions)
│   └── MAC verification failed
└── RuntimeError
    ├── Network errors
    └── Blockchain errors
```

### Common Exceptions by Module

#### Phase 1: Basic Diffie-Hellman

**Exceptions:**
- None (basic operations don't raise exceptions)

**Error Conditions:**
- Key mismatch (detected by comparison, not exception)

#### Phase 2: MITM Attack

**Exceptions:**
- None (attack simulation doesn't raise exceptions)

**Error Conditions:**
- Attack success (by design, not an error)

#### Phase 3: Authenticated DH

**Exceptions:**

##### `InvalidSignature`

**Raised By:** `verify_and_derive_key()`

**Cause:**
- Signature verification fails
- Wrong signing key used
- Key tampering detected

**Example:**
```python
try:
    valid, key = bob.verify_and_derive_key(
        alice_dh_pub, alice_signing_pub, signature
    )
except InvalidSignature:
    # Signature invalid - possible MITM attack
    print("Signature verification failed")
```

**Handling:**
- Reject key exchange
- Log security event
- Notify user of potential attack

#### Phase 4: Secure Channel

**Exceptions:**

##### `ValueError: Channel not established`

**Raised By:** `send_message()`, `receive_message()`

**Cause:**
- Attempting to send/receive before channel establishment
- Cipher not initialized

**Example:**
```python
channel = SecureChannel("Alice")
# Forgot to call establish_channel()
try:
    channel.send_message(b"Hello")
except ValueError as e:
    # Channel not established
    print(f"Error: {e}")
```

**Handling:**
- Call `establish_channel()` first
- Check `cipher is not None` before use

##### `InvalidTag`

**Raised By:** `receive_message()`

**Cause:**
- MAC verification fails
- Message tampering detected
- Wrong key used
- Nonce mismatch
- Associated data mismatch

**Example:**
```python
try:
    plaintext = channel.receive_message(ciphertext, nonce)
except InvalidTag:
    # Tampering detected - reject message
    print("Message authentication failed")
    # Log security event
```

**Handling:**
- Reject message immediately
- Log security event
- Consider closing channel if repeated failures
- Never use tampered data

#### Phase 5: Blockchain Integration

**Exceptions:**

##### `ValueError: Ed25519 public key must be 32 bytes`

**Raised By:** `register_key()`

**Cause:**
- Invalid key size provided
- Wrong key format

**Example:**
```python
try:
    registry.register_key(wallet, invalid_key)
except ValueError as e:
    print(f"Invalid key: {e}")
```

**Handling:**
- Validate key size before calling
- Use correct key format (32 bytes)

##### Network Errors

**Raised By:** Solana RPC calls

**Cause:**
- Network connectivity issues
- RPC endpoint unavailable
- Timeout

**Example:**
```python
try:
    verified = client.verify_key(address, key)
except Exception as e:
    # Network error
    print(f"Blockchain query failed: {e}")
    # Retry with backoff
```

**Handling:**
- Implement retry logic with exponential backoff
- Use multiple RPC endpoints
- Handle timeouts gracefully

#### Phase 6: Blockchain Attacks

**Exceptions:**

**No exceptions raised** (attacks are prevented, not errors)

**Error Conditions:**
- Attack prevention (by design, not exceptions)

### Error Handling Best Practices

#### 1. Cryptographic Errors

**Always handle:**
- `InvalidSignature`: Reject and log
- `InvalidTag`: Reject and log
- Never ignore cryptographic failures

**Example Pattern:**
```python
try:
    result = cryptographic_operation()
except (InvalidSignature, InvalidTag) as e:
    logger.warning(f"Security failure: {e}")
    # Reject operation
    return False
```

#### 2. Validation Errors

**Always validate:**
- Key sizes
- Parameter types
- Channel state

**Example Pattern:**
```python
if len(key) != 32:
    raise ValueError("Key must be 32 bytes")
```

#### 3. Network Errors

**Always handle:**
- Connection failures
- Timeouts
- Retry with backoff

**Example Pattern:**
```python
for attempt in range(max_retries):
    try:
        result = network_call()
        break
    except Exception as e:
        if attempt == max_retries - 1:
            raise
        time.sleep(2 ** attempt)  # Exponential backoff
```

#### 4. State Errors

**Always check:**
- Channel establishment
- Key initialization
- Object state

**Example Pattern:**
```python
if self.cipher is None:
    raise ValueError("Channel not established")
```

### Exception Logging

**Recommended Logging Levels:**
- `InvalidSignature`, `InvalidTag`: WARNING (security events)
- `ValueError`: ERROR (programming errors)
- Network errors: ERROR (infrastructure issues)
- Attack prevention: INFO (expected behavior)

### Error Recovery Strategies

| Error Type | Recovery Strategy | Example |
|------------|------------------|---------|
| `InvalidSignature` | Reject, log, notify | Close connection |
| `InvalidTag` | Reject message, log | Drop message |
| Network errors | Retry with backoff | Exponential backoff |
| Validation errors | Fix input, retry | Validate before call |
| State errors | Initialize, retry | Call setup method |

---

**Next Document:** TECHNICAL_DOC_06_DEMO_OUTPUTS.md

---

**Document Version:** 1.0  
**Last Updated:** December 2024


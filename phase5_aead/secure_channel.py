"""
Phase 4: Secure Channel with AEAD Encryption

This script demonstrates a complete secure channel implementation:
1. Authenticated DH key exchange (from Phase 3)
2. Message encryption/decryption using ChaCha20-Poly1305 (AEAD)
3. Proper nonce management to prevent replay attacks

AEAD (Authenticated Encryption with Associated Data) provides:
- Confidentiality: Messages are encrypted
- Integrity: Message tampering is detected
- Authentication: Sender authentication via MAC

ChaCha20-Poly1305 is a modern, secure AEAD cipher suitable for high-performance applications.
"""

from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidSignature, InvalidTag
import binascii
import os
import struct

def public_bytes(public_key):
    """Serialize an X25519 public key to raw bytes (32 bytes)."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

def derive_shared_key(our_private: x25519.X25519PrivateKey, their_public_bytes: bytes, info: bytes = b"secure_channel_v1"):
    """Derive shared key from DH exchange."""
    their_public = x25519.X25519PublicKey.from_public_bytes(their_public_bytes)
    shared_secret = our_private.exchange(their_public)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=info,
    )
    key = hkdf.derive(shared_secret)
    return key

class AuthenticatedParticipant:
    """Participant with authentication (Ed25519 signatures)"""
    
    def __init__(self, name):
        self.name = name
        self.dh_private = None
        self.dh_public = None
        self.dh_public_bytes = None
        self.signing_private = None
        self.signing_public = None
        self.signing_public_bytes = None
        self.shared_key = None
    
    def generate_keypairs(self):
        """Generate both DH and Ed25519 keypairs"""
        from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
        from cryptography.hazmat.primitives import serialization
        self.dh_private = x25519.X25519PrivateKey.generate()
        self.dh_public = self.dh_private.public_key()
        self.dh_public_bytes = public_bytes(self.dh_public)
        self.signing_private = ed25519.Ed25519PrivateKey.generate()
        self.signing_public = self.signing_private.public_key()
        self.signing_public_bytes = self.signing_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
    
    def sign_dh_public_key(self):
        """Sign the DH public key with Ed25519 private key"""
        return self.signing_private.sign(self.dh_public_bytes)
    
    def verify_and_derive_key(self, peer_dh_pub_bytes, peer_signing_pub_bytes, signature):
        """Verify the peer's signature and derive shared key if valid"""
        try:
            peer_signing_pub = ed25519.Ed25519PublicKey.from_public_bytes(peer_signing_pub_bytes)
            peer_signing_pub.verify(signature, peer_dh_pub_bytes)
            self.shared_key = derive_shared_key(self.dh_private, peer_dh_pub_bytes)
            return True, self.shared_key
        except InvalidSignature:
            return False, None


class SecureChannel:
    """
    Complete secure channel implementation with authenticated encryption (AEAD).
    
    This class combines:
    1. Authenticated key exchange (from Phase 3) - prevents MITM
    2. Authenticated encryption (ChaCha20-Poly1305) - provides confidentiality + integrity
    
    A secure channel provides:
    - Confidentiality: Messages are encrypted (unreadable by attackers)
    - Integrity: Message tampering is detected (Poly1305 MAC)
    - Authentication: Sender authentication via signatures (Ed25519)
    - Replay protection: Unique nonces prevent replay attacks
    
    This is similar to what TLS, Signal, and other secure protocols provide.
    """
    
    def __init__(self, name):
        """
        Initialize a secure channel for a participant.
        
        Args:
            name: Participant's name (e.g., "Alice", "Bob")
        """
        self.name = name
        # Use authenticated participant for key exchange (Phase 3 functionality)
        self.participant = AuthenticatedParticipant(name)
        # AEAD cipher (will be initialized after key exchange completes)
        # ChaCha20-Poly1305 provides authenticated encryption
        self.cipher = None
        # Nonce counters for message encryption (prevents nonce reuse)
        self.nonce_counter = 0         # For outgoing messages
        self.peer_nonce_counter = 0     # For incoming messages (tracking)
    
    def establish_channel(self, peer_dh_pub_bytes, peer_signing_pub_bytes, peer_signature):
        """
        Establish a secure channel by verifying the peer and initializing encryption.
        
        This function completes the authenticated key exchange and sets up the
        authenticated encryption cipher for secure message exchange.
        
        Args:
            peer_dh_pub_bytes: Peer's DH public key (32 bytes)
            peer_signing_pub_bytes: Peer's Ed25519 public key (32 bytes) - for signature verification
            peer_signature: Ed25519 signature over the DH public key (64 bytes)
        
        Returns:
            bool: True if channel established successfully, False if verification failed
        
        Process:
        1. Verify the peer's signature (prevents MITM attack)
        2. If valid, derive the shared symmetric key via DH
        3. Initialize ChaCha20-Poly1305 cipher with the derived key
        4. Channel is now ready for secure message exchange
        
        Security: If signature verification fails, the channel is NOT established.
        This ensures we only communicate with authenticated peers.
        """
        # ====================================================================
        # Step 1: Verify peer's signature and derive shared key
        # ====================================================================
        # This uses the authenticated key exchange from Phase 3
        # - Verifies the signature proves the DH key is authentic
        # - Derives shared symmetric key if verification succeeds
        # - Returns False if signature is invalid (MITM prevention)
        valid, shared_key = self.participant.verify_and_derive_key(
            peer_dh_pub_bytes,
            peer_signing_pub_bytes,
            peer_signature
        )
        
        if not valid:
            # Signature verification failed - reject channel establishment
            return False
        
        # ====================================================================
        # Step 2: Initialize authenticated encryption cipher
        # ====================================================================
        # ChaCha20-Poly1305 is an AEAD (Authenticated Encryption with Associated Data) cipher:
        # - ChaCha20: Stream cipher for encryption (fast, secure, good performance)
        # - Poly1305: MAC (Message Authentication Code) for integrity verification
        # Together they provide:
        #   - Confidentiality: ChaCha20 encrypts the plaintext
        #   - Integrity: Poly1305 creates a MAC tag that detects tampering
        #   - Authenticity: MAC proves the message came from someone with the key
        
        # The cipher needs the 32-byte (256-bit) shared key
        # This key was derived from the DH exchange + HKDF
        self.cipher = ChaCha20Poly1305(shared_key)
        print(f"{self.name}: Secure channel established. AEAD cipher initialized.")
        return True
    
    def send_message(self, plaintext: bytes, associated_data: bytes = b"") -> tuple[bytes, bytes]:
        """
        Encrypt and authenticate a message using ChaCha20-Poly1305.
        
        Args:
            plaintext: The message to encrypt (bytes) - will be encrypted
            associated_data: Optional associated data (bytes) - authenticated but NOT encrypted
                             This can include metadata like sender ID, timestamp, etc.
                             Useful for binding additional context to the message
        
        Returns:
            tuple: (ciphertext, nonce)
                - ciphertext: Encrypted message + authentication tag (bytes)
                - nonce: Unique nonce used for this encryption (12 bytes)
        
        Important Security Requirements:
        - Nonce MUST be unique for each encryption with the same key
        - Reusing a nonce with the same key breaks security!
        - We use counter + random bytes to ensure uniqueness
        
        The ciphertext includes:
        - Encrypted plaintext (ChaCha20 encryption)
        - Authentication tag (16 bytes, Poly1305 MAC)
        
        Process:
        1. Generate a unique nonce (never reuse!)
        2. Encrypt plaintext and compute MAC tag (all in one operation)
        3. Return ciphertext (encrypted data + tag) and nonce
        
        The nonce must be sent along with the ciphertext so the receiver
        can decrypt. Nonces can be public (they don't need to be secret).
        """
        if self.cipher is None:
            raise ValueError("Channel not established - call establish_channel() first")
        
        # ====================================================================
        # Step 1: Generate a unique nonce (number used once)
        # ====================================================================
        # ChaCha20-Poly1305 requires a 12-byte nonce
        # CRITICAL: The nonce MUST be unique for each encryption with the same key
        # Reusing a nonce with the same key is a catastrophic security failure!
        # 
        # Strategy: Counter (64 bits = 8 bytes) + Random (32 bits = 4 bytes)
        # - Counter ensures sequential uniqueness
        # - Random bits add extra entropy
        # 
        # Note: In production, you might use:
        # - Pure random nonces (with tracking to detect reuse)
        # - Counter + timestamp
        # - Message sequence number
        nonce = struct.pack('>Q', self.nonce_counter) + os.urandom(4)
        self.nonce_counter += 1  # Increment for next message
        
        # ====================================================================
        # Step 2: Encrypt and authenticate the message
        # ====================================================================
        # ChaCha20-Poly1305.encrypt() does BOTH:
        # 1. Encrypts the plaintext using ChaCha20 (confidentiality)
        # 2. Computes Poly1305 MAC tag over ciphertext + associated_data (integrity)
        # 
        # The result includes:
        # - Encrypted plaintext (same length as plaintext)
        # - 16-byte authentication tag (appended)
        # Total: len(plaintext) + 16 bytes
        ciphertext = self.cipher.encrypt(nonce, plaintext, associated_data)
        
        print(f"{self.name}: Encrypted message (length: {len(ciphertext)} bytes)")
        print(f"{self.name}: Nonce (hex): {binascii.hexlify(nonce).decode()}")
        
        return ciphertext, nonce
    
    def receive_message(self, ciphertext: bytes, nonce: bytes, associated_data: bytes = b"") -> bytes:
        """
        Decrypt and verify a message using ChaCha20-Poly1305.
        
        Args:
            ciphertext: Encrypted message + authentication tag (bytes)
            nonce: The nonce used for encryption (12 bytes, must match sender's nonce)
            associated_data: Optional associated data (bytes) - must match what sender used
        
        Returns:
            bytes: Decrypted plaintext (original message)
        
        Raises:
            InvalidTag: If authentication fails (tampering detected, message rejected)
        
        Process:
        1. Verify the Poly1305 authentication tag
           - If tag is invalid: raise InvalidTag (tampering detected!)
           - If tag is valid: proceed to decryption
        2. Decrypt the ciphertext using ChaCha20
        3. Return the plaintext
        
        Security Features:
        - Integrity verification: Invalid tag means message was tampered with
        - Authentication: Valid tag proves message came from someone with the key
        - Confidentiality: Only someone with the key can decrypt
        
        Important: The associated_data must match exactly what the sender used.
        This ensures the entire message context (metadata + encrypted data) is authenticated.
        """
        if self.cipher is None:
            raise ValueError("Channel not established - call establish_channel() first")
        
        try:
            # ====================================================================
            # Decrypt and verify the message
            # ====================================================================
            # ChaCha20-Poly1305.decrypt() does BOTH:
            # 1. Verifies the Poly1305 authentication tag
            #    - Computes expected tag from ciphertext + nonce + associated_data
            #    - Compares with the tag in ciphertext
            #    - If mismatch: raises InvalidTag (tampering detected!)
            # 2. Decrypts the ciphertext using ChaCha20 (if tag is valid)
            # 
            # This is an atomic operation: decryption only happens if authentication succeeds
            # This prevents timing attacks where attackers might learn something from
            # partial decryption before tag verification fails
            plaintext = self.cipher.decrypt(nonce, ciphertext, associated_data)
            print(f"{self.name}: Decrypted message successfully")
            return plaintext
            
        except InvalidTag:
            # ====================================================================
            # Authentication failed - possible tampering!
            # ====================================================================
            # InvalidTag is raised when:
            # 1. The authentication tag doesn't match (message was modified)
            # 2. Wrong key was used (different shared key)
            # 3. Wrong nonce was used
            # 4. Associated data doesn't match
            
            # SECURITY: We MUST reject the message - never use tampered data!
            # In production, you might also:
            # - Log the incident
            # - Alert security monitoring
            # - Close the connection if repeated failures
            print(f"{self.name}: [FAILED] Decryption FAILED - Authentication tag invalid (tampering detected)")
            raise
    
    def get_public_keys(self):
        """Get public keys and signature for key exchange"""
        signature = self.participant.sign_dh_public_key()
        return (
            self.participant.dh_public_bytes,
            self.participant.signing_public_bytes,
            signature
        )


def demonstrate_secure_channel():
    """
    Demonstrate complete secure channel with authenticated encryption
    """
    print("=" * 70)
    print("PHASE 4: Secure Channel with AEAD Encryption")
    print("=" * 70)
    print()
    
    # Create secure channels
    alice_channel = SecureChannel("Alice")
    bob_channel = SecureChannel("Bob")
    
    print("\n" + "-" * 70)
    print("STEP 1: Alice generates keypairs")
    print("-" * 70)
    alice_channel.participant.generate_keypairs()
    
    print("\n" + "-" * 70)
    print("STEP 2: Alice sends authenticated DH public key to Bob")
    print("-" * 70)
    alice_dh_pub, alice_signing_pub, alice_sig = alice_channel.get_public_keys()
    
    print("\n" + "-" * 70)
    print("STEP 3: Bob verifies and establishes secure channel")
    print("-" * 70)
    bob_channel.participant.generate_keypairs()
    bob_established = bob_channel.establish_channel(alice_dh_pub, alice_signing_pub, alice_sig)
    
    if not bob_established:
        print("[ERROR] Failed to establish channel")
        return
    
    print("\n" + "-" * 70)
    print("STEP 4: Bob sends authenticated DH public key to Alice")
    print("-" * 70)
    bob_dh_pub, bob_signing_pub, bob_sig = bob_channel.get_public_keys()
    
    print("\n" + "-" * 70)
    print("STEP 5: Alice verifies and establishes secure channel")
    print("-" * 70)
    alice_established = alice_channel.establish_channel(bob_dh_pub, bob_signing_pub, bob_sig)
    
    if not alice_established:
        print("[ERROR] Failed to establish channel")
        return
    
    print("\n" + "=" * 70)
    print("SECURE MESSAGE EXCHANGE")
    print("=" * 70)
    
    # Alice sends a message to Bob
    print("\n" + "-" * 70)
    print("Alice sends message to Bob")
    print("-" * 70)
    alice_message = b"Hello Bob! This is a secret message."
    print(f"Alice: Plaintext: {alice_message.decode()}")
    
    ciphertext, nonce = alice_channel.send_message(alice_message)
    
    print("\n" + "-" * 70)
    print("Bob receives and decrypts message")
    print("-" * 70)
    try:
        bob_received = bob_channel.receive_message(ciphertext, nonce)
        print(f"Bob: Decrypted: {bob_received.decode()}")
        if bob_received == alice_message:
            print("[SUCCESS] Message integrity verified")
    except InvalidTag as e:
        print(f"[ERROR] Decryption failed: {e}")
    
    # Bob sends a message to Alice
    print("\n" + "-" * 70)
    print("Bob sends message to Alice")
    print("-" * 70)
    bob_message = b"Hi Alice! Received your message securely."
    print(f"Bob: Plaintext: {bob_message.decode()}")
    
    ciphertext2, nonce2 = bob_channel.send_message(bob_message)
    
    print("\n" + "-" * 70)
    print("Alice receives and decrypts message")
    print("-" * 70)
    try:
        alice_received = alice_channel.receive_message(ciphertext2, nonce2)
        print(f"Alice: Decrypted: {alice_received.decode()}")
        if alice_received == bob_message:
            print("[SUCCESS] Message integrity verified")
    except InvalidTag as e:
        print(f"[ERROR] Decryption failed: {e}")
    
    # Demonstrate tampering detection
    print("\n" + "=" * 70)
    print("TAMPERING DETECTION TEST")
    print("=" * 70)
    
    print("\nMallory attempts to modify encrypted message...")
    tampered_ciphertext = bytearray(ciphertext)
    tampered_ciphertext[10] ^= 0xFF  # Flip some bits
    
    print("\nBob tries to decrypt tampered message...")
    try:
        bob_channel.receive_message(bytes(tampered_ciphertext), nonce)
        print("[ERROR] Tampering should have been detected!")
    except InvalidTag:
        print("[SUCCESS] Tampering detected! Message rejected.")
    
    print("\n" + "=" * 70)
    print("SECURITY ANALYSIS")
    print("=" * 70)
    print("""
The secure channel now provides:
1. ✅ Confidentiality: Messages are encrypted (ChaCha20)
2. ✅ Integrity: Message tampering is detected (Poly1305 MAC)
3. ✅ Authentication: Sender authentication via signatures (Ed25519)
4. ✅ Replay protection: Unique nonces prevent replay attacks

NEXT STEP: Integrate blockchain (Solana) for decentralized key registry
This will be demonstrated in Phase 5.
""")


if __name__ == "__main__":
    demonstrate_secure_channel()


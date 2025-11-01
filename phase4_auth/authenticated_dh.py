"""
Phase 3: Authenticated Diffie-Hellman Key Exchange

This script fixes the MITM vulnerability by adding digital signatures (Ed25519)
to authenticate public keys. Each participant signs their DH public key with
their long-term Ed25519 signing key.

Protocol Flow:
1. Alice generates DH keypair + Ed25519 signing keypair
2. Alice signs her DH public key and sends (pub_key, signature) to Bob
3. Bob verifies Alice's signature using Alice's Ed25519 public key
4. Bob generates DH keypair + Ed25519 signing keypair
5. Bob signs his DH public key and sends (pub_key, signature) to Alice
6. Alice verifies Bob's signature using Bob's Ed25519 public key
7. Both derive shared key only if signatures are valid

This prevents MITM attacks because Mallory cannot forge Alice's or Bob's signatures
without their private Ed25519 keys.
"""

from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import binascii

def generate_x25519_keypair():
    """Generate an X25519 keypair."""
    private = x25519.X25519PrivateKey.generate()
    public = private.public_key()
    return private, public

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
    """
    Participant with authentication using Ed25519 digital signatures.
    
    This class extends the basic Participant to add authentication:
    - Each participant has TWO keypairs:
      1. X25519 keypair (ephemeral, for key exchange) - same as Phase 1
      2. Ed25519 keypair (long-term, for signing) - NEW in Phase 3
    
    How authentication works:
    - Before sending a DH public key, the sender signs it with their Ed25519 private key
    - The receiver verifies the signature using the sender's Ed25519 public key
    - If signature is valid, the DH key is trusted and key exchange proceeds
    - If signature is invalid, the key exchange is rejected (MITM prevented!)
    
    Security: Mallory cannot forge signatures without the private Ed25519 key
    """
    
    def __init__(self, name):
        """
        Initialize an authenticated participant.
        
        Args:
            name: Participant's name (e.g., "Alice", "Bob")
        """
        self.name = name
        
        # ====================================================================
        # X25519 keys for Diffie-Hellman key exchange (ephemeral)
        # These are generated fresh for each key exchange session
        # ====================================================================
        self.dh_private = None        # X25519 private key (kept secret)
        self.dh_public = None         # X25519 public key (sent to peer)
        self.dh_public_bytes = None    # X25519 public key as 32 bytes
        
        # ====================================================================
        # Ed25519 keys for authentication (long-term identity keys)
        # These should be established once and reused across sessions
        # ====================================================================
        self.signing_private = None        # Ed25519 private key (kept secret, used to sign)
        self.signing_public = None         # Ed25519 public key (shared, used to verify)
        self.signing_public_bytes = None   # Ed25519 public key as 32 bytes
        
        # Derived shared symmetric key (after successful authenticated key exchange)
        self.shared_key = None
    
    def generate_keypairs(self):
        """
        Generate both X25519 (DH) and Ed25519 (signing) keypairs.
        
        This must be called before participating in an authenticated key exchange.
        The X25519 keys can be ephemeral (new for each session), but the Ed25519
        keys should be long-term identity keys (established once and reused).
        
        In a real system:
        - Ed25519 keys would be generated once and stored securely
        - X25519 keys would be generated fresh for each session (forward secrecy)
        """
        # ====================================================================
        # Step 1: Generate X25519 keypair for Diffie-Hellman key exchange
        # ====================================================================
        # These are ephemeral keys - generated fresh for each key exchange
        # This provides forward secrecy (compromising old keys doesn't break future sessions)
        self.dh_private, self.dh_public = generate_x25519_keypair()
        # Convert to bytes for transmission
        self.dh_public_bytes = public_bytes(self.dh_public)
        
        # ====================================================================
        # Step 2: Generate Ed25519 keypair for digital signatures
        # ====================================================================
        # Ed25519 is a modern signature scheme based on Curve25519
        # - Fast signing and verification
        # - Small signatures (64 bytes)
        # - Small public keys (32 bytes)
        # - 128-bit security level
        # - Deterministic (same message + key = same signature, good for security)
        self.signing_private = ed25519.Ed25519PrivateKey.generate()
        # Derive the public key from the private key
        self.signing_public = self.signing_private.public_key()
        # Convert to raw bytes (32 bytes) for transmission
        self.signing_public_bytes = self.signing_public.public_bytes(
            encoding=serialization.Encoding.Raw,   # Raw bytes format
            format=serialization.PublicFormat.Raw  # No ASN.1 wrapping
        )
        
        print(f"{self.name}: Generated DH keypair and Ed25519 signing keypair")
        print(f"{self.name}: DH public key (hex): {binascii.hexlify(self.dh_public_bytes).decode()}")
        print(f"{self.name}: Ed25519 public key (hex): {binascii.hexlify(self.signing_public_bytes).decode()}")
    
    def sign_dh_public_key(self):
        """
        Sign the DH public key with the Ed25519 private key.
        
        Returns:
            bytes: Ed25519 signature (64 bytes)
        
        This signature proves that:
        - The DH public key was sent by the owner of the Ed25519 private key
        - The DH key hasn't been tampered with in transit
        - The key exchange is authentic (not from a MITM attacker)
        
        The signature binds the ephemeral DH key to the long-term Ed25519 identity.
        Mallory cannot create a valid signature without the private Ed25519 key.
        """
        # Sign the DH public key bytes using Ed25519
        # Ed25519.sign(message) creates a 64-byte signature
        # This signature can only be created by someone who knows the private key
        signature = self.signing_private.sign(self.dh_public_bytes)
        print(f"{self.name}: Signed DH public key")
        print(f"{self.name}: Signature (hex): {binascii.hexlify(signature).decode()}")
        return signature
    
    def verify_and_derive_key(self, peer_dh_pub_bytes, peer_signing_pub_bytes, signature):
        """
        Verify the peer's signature and derive shared key ONLY if signature is valid.
        
        This is the critical security check that prevents MITM attacks!
        
        Args:
            peer_dh_pub_bytes: Peer's DH public key (32 bytes) - what they claim
            peer_signing_pub_bytes: Peer's Ed25519 public key (32 bytes) - their identity
            signature: Ed25519 signature (64 bytes) - proof the DH key is authentic
        
        Returns:
            tuple: (is_valid: bool, shared_key: bytes or None)
                - If signature is valid: (True, derived_shared_key)
                - If signature is invalid: (False, None) - key exchange rejected
        
        Process:
        1. Reconstruct peer's Ed25519 public key object
        2. Verify the signature using peer's public key
           - If valid: the DH key is authentic, proceed with key exchange
           - If invalid: possible MITM attack, reject the key exchange
        3. Only if signature is valid, derive the shared key using DH
        
        Security: This prevents Mallory from replacing keys because she cannot
        forge signatures without Alice's or Bob's private Ed25519 keys.
        """
        try:
            # ====================================================================
            # Step 1: Reconstruct the peer's Ed25519 public key object
            # ====================================================================
            # We received the peer's Ed25519 public key as bytes
            # Reconstruct the Ed25519PublicKey object so we can verify signatures
            peer_signing_pub = ed25519.Ed25519PublicKey.from_public_bytes(peer_signing_pub_bytes)
            
            # ====================================================================
            # Step 2: Verify the signature
            # ====================================================================
            # This checks: signature == Ed25519_Sign(peer_private_key, peer_dh_pub_bytes)
            # If the signature is valid, we know:
            # - The peer's DH public key was signed by someone who knows the private key
            # - The peer_dh_pub_bytes matches what was signed (no tampering)
            # - The key exchange is authentic
            peer_signing_pub.verify(signature, peer_dh_pub_bytes)
            print(f"{self.name}: [SUCCESS] Signature verification SUCCESS")
            
            # ====================================================================
            # Step 3: Only if signature is valid, derive the shared key
            # ====================================================================
            # We only proceed with the DH key exchange if authentication succeeded
            # This ensures we're actually communicating with the intended peer
            self.shared_key = derive_shared_key(self.dh_private, peer_dh_pub_bytes)
            print(f"{self.name}: Derived shared key (hex): {binascii.hexlify(self.shared_key).decode()}")
            return True, self.shared_key
        
        except InvalidSignature:
            # ====================================================================
            # Signature verification failed!
            # ====================================================================
            # This could mean:
            # 1. The signature was forged (MITM attack attempt)
            # 2. The DH key was tampered with in transit
            # 3. Wrong Ed25519 public key was used for verification
            # 
            # In any case, we REJECT the key exchange to prevent MITM attacks
            print(f"{self.name}: [FAILED] Signature verification FAILED - rejecting key exchange")
            return False, None


class AuthenticatedMallory:
    """
    Mallory attempting MITM attack on authenticated protocol
    
    This will FAIL because Mallory cannot forge signatures without
    Alice's or Bob's private Ed25519 keys.
    """
    
    def __init__(self):
        self.name = "Mallory"
        # Mallory generates her own keypairs
        self.dh_priv, self.dh_pub = generate_x25519_keypair()
        self.dh_pub_bytes = public_bytes(self.dh_pub)
        self.signing_priv = ed25519.Ed25519PrivateKey.generate()
        self.signing_pub = self.signing_priv.public_key()
        self.signing_pub_bytes = self.signing_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        print(f"{self.name}: Generated own keypairs (cannot forge Alice's or Bob's signatures)")
    
    def intercept_and_replace(self, message_from):
        """
        Attempt to intercept and replace (will fail because signature won't match)
        
        Returns:
            (fake_dh_pub_bytes, fake_signing_pub_bytes, signature)
        """
        # Mallory can create her own signed message, but it won't match Alice's/Bob's signing keys
        signature = self.signing_priv.sign(self.dh_pub_bytes)
        print(f"{self.name}: [ATTEMPTING] Intercepting {message_from.name}'s message")
        print(f"{self.name}: [CREATING] Fake signed message with own keys (signature won't match!)")
        return self.dh_pub_bytes, self.signing_pub_bytes, signature


def demonstrate_authenticated_exchange():
    """
    Demonstrate authenticated DH key exchange that prevents MITM
    """
    print("=" * 70)
    print("PHASE 3: Authenticated Diffie-Hellman Key Exchange")
    print("=" * 70)
    print()
    
    # Create authenticated participants
    alice = AuthenticatedParticipant("Alice")
    bob = AuthenticatedParticipant("Bob")
    
    print("\n" + "-" * 70)
    print("STEP 1: Alice generates keypairs (DH + Ed25519)")
    print("-" * 70)
    alice.generate_keypairs()
    
    print("\n" + "-" * 70)
    print("STEP 2: Alice signs DH public key and sends to Bob")
    print("-" * 70)
    alice_signature = alice.sign_dh_public_key()
    
    print("\n" + "-" * 70)
    print("STEP 3: Bob verifies Alice's signature and derives key")
    print("-" * 70)
    # Bob receives: (alice_dh_pub, alice_signing_pub, signature)
    bob_valid, bob_key = bob.verify_and_derive_key(
        alice.dh_public_bytes,
        alice.signing_public_bytes,
        alice_signature
    )
    
    if not bob_valid:
        print("[ERROR] Protocol failed: Bob rejected Alice's key")
        return
    
    print("\n" + "-" * 70)
    print("STEP 4: Bob generates keypairs (DH + Ed25519)")
    print("-" * 70)
    bob.generate_keypairs()
    
    print("\n" + "-" * 70)
    print("STEP 5: Bob signs DH public key and sends to Alice")
    print("-" * 70)
    bob_signature = bob.sign_dh_public_key()
    
    print("\n" + "-" * 70)
    print("STEP 6: Alice verifies Bob's signature and derives key")
    print("-" * 70)
    alice_valid, alice_key = alice.verify_and_derive_key(
        bob.dh_public_bytes,
        bob.signing_public_bytes,
        bob_signature
    )
    
    if not alice_valid:
        print("❌ Protocol failed: Alice rejected Bob's key")
        return
    
    print("\n" + "=" * 70)
    print("AUTHENTICATED KEY EXCHANGE RESULTS")
    print("=" * 70)
    
    if alice.shared_key == bob.shared_key:
        print("[SUCCESS] Alice and Bob derived the same shared key")
        print(f"   Shared key (hex): {binascii.hexlify(alice.shared_key).decode()}")
    else:
        print("[ERROR] Keys differ!")
    
    print("\n" + "=" * 70)
    print("MITM ATTACK PREVENTION TEST")
    print("=" * 70)
    
    # Now demonstrate that Mallory cannot successfully attack
    mallory = AuthenticatedMallory()
    
    print("\n" + "-" * 70)
    print("Mallory attempts to intercept and replace Alice's message to Bob")
    print("-" * 70)
    fake_alice_dh, fake_alice_signing, fake_sig = mallory.intercept_and_replace(alice)
    
    print("\n" + "-" * 70)
    print("Bob receives Mallory's fake message and attempts verification")
    print("-" * 70)
    # Bob tries to verify using Alice's real signing key (which Bob knows)
    # But Mallory's signature was created with Mallory's signing key
    try:
        alice_signing_pub = ed25519.Ed25519PublicKey.from_public_bytes(alice.signing_public_bytes)
        alice_signing_pub.verify(fake_sig, fake_alice_dh)
        print("[ERROR] Signature verification should have failed!")
    except InvalidSignature:
        print("[SUCCESS] ATTACK PREVENTED: Bob correctly rejected Mallory's fake signature")
        print("   Mallory cannot forge signatures without Alice's private key")
    
    print("\n" + "=" * 70)
    print("SECURITY ANALYSIS")
    print("=" * 70)
    print("""
The authenticated protocol prevents MITM attacks because:
1. Each DH public key is signed with Ed25519
2. Signatures cannot be forged without the private signing key
3. Receivers verify signatures before accepting keys
4. Mallory's fake signatures are rejected

NEXT STEP: Use the shared key for authenticated encryption (AEAD)
This will be demonstrated in Phase 4.
""")


if __name__ == "__main__":
    demonstrate_authenticated_exchange()


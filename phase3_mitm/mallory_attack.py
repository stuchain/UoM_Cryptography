"""
Phase 2: Man-in-the-Middle (MITM) Attack Demonstration

This script demonstrates how Mallory (an active attacker) can intercept
and manipulate the Diffie-Hellman key exchange between Alice and Bob.

Attack Scenario:
1. Alice generates her DH keypair and sends public key to Bob
2. Mallory intercepts Alice's public key
3. Mallory sends her own public key to Bob (impersonating Alice)
4. Bob generates his keypair and sends public key to Alice
5. Mallory intercepts Bob's public key
6. Mallory sends her own public key to Alice (impersonating Bob)

Result:
- Alice thinks she shares a key with Bob, but actually shares it with Mallory
- Bob thinks he shares a key with Alice, but actually shares it with Mallory
- Mallory can decrypt, read, and modify all messages between Alice and Bob
"""

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import binascii

def generate_x25519_keypair():
    """
    Generate an X25519 (Curve25519) keypair for Diffie-Hellman key exchange.
    
    Returns:
        tuple: (private_key, public_key)
            - private_key: X25519PrivateKey - MUST be kept secret, used for key exchange
            - public_key: X25519PublicKey - Safe to share publicly
    
    X25519 is an elliptic curve variant of Diffie-Hellman that provides:
    - 128-bit security level
    - Fast computation
    - 32-byte keys (compact)
    """
    # Generate a random private key (32 bytes, but mathematically constrained to Curve25519)
    private = x25519.X25519PrivateKey.generate()
    # Compute the corresponding public key from the private key
    # This is done via scalar multiplication: public = private * base_point
    public = private.public_key()
    return private, public

def public_bytes(public_key):
    """
    Serialize an X25519 public key to raw bytes format.
    
    Args:
        public_key: X25519PublicKey object
    
    Returns:
        bytes: 32-byte raw public key representation
        
    This format is what gets transmitted over the network. The Raw encoding
    means we get just the 32 bytes without any ASN.1 or other wrapping.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.Raw,  # Raw bytes, no encoding wrapper
        format=serialization.PublicFormat.Raw   # Raw format (just the curve point)
    )

def derive_shared_key(our_private: x25519.X25519PrivateKey, their_public_bytes: bytes, info: bytes = b"secure_channel_v1"):
    """
    Perform Diffie-Hellman key exchange and derive a symmetric encryption key.
    
    Steps:
    1. Reconstruct their public key from bytes
    2. Perform DH exchange: shared_secret = our_private * their_public
    3. Derive symmetric key using HKDF (HMAC-based Key Derivation Function)
    
    Args:
        our_private: Our X25519 private key
        their_public_bytes: Peer's public key as 32 bytes
        info: Context information to bind the key to this protocol/version
    
    Returns:
        bytes: 32-byte symmetric key suitable for encryption (ChaCha20-Poly1305, AES-256)
    
    Security Note: We NEVER use the raw shared_secret directly as an encryption key.
    HKDF ensures:
    - Proper key stretching
    - Context binding (via 'info')
    - Key separation (different contexts yield different keys)
    """
    # Step 1: Reconstruct the peer's public key object from raw bytes
    # This is safe because public keys are meant to be public
    their_public = x25519.X25519PublicKey.from_public_bytes(their_public_bytes)
    
    # Step 2: Perform the actual Diffie-Hellman exchange
    # This computes: shared_secret = our_private_key * their_public_key
    # The mathematical property: (a * G) * b = (b * G) * a = a * b * G
    # So both parties get the same shared secret despite different computation paths
    shared_secret = our_private.exchange(their_public)  # Returns 32 bytes
    
    # Step 3: Derive a symmetric encryption key from the shared secret using HKDF
    # HKDF = HMAC-based Key Derivation Function (RFC 5869)
    # This ensures the key is cryptographically strong and context-bound
    hkdf = HKDF(
        algorithm=hashes.SHA256(),  # Use SHA-256 as the underlying hash
        length=32,                   # Output 32 bytes (256 bits) for AES-256 or ChaCha20
        salt=None,                   # Optional salt (not used in this demo)
        info=info,                   # Context binding - prevents key reuse across protocols
    )
    # Derive the actual symmetric key from the shared secret
    key = hkdf.derive(shared_secret)  # Returns exactly 'length' bytes
    return key


class Participant:
    """
    Represents a legitimate participant in the key exchange (Alice or Bob).
    
    This class models a normal, honest participant who follows the protocol correctly.
    They generate keys and derive shared secrets but don't know they might be
    communicating with an attacker instead of their intended peer.
    """
    
    def __init__(self, name):
        """
        Initialize a participant.
        
        Args:
            name: Participant's name (e.g., "Alice", "Bob")
        """
        self.name = name
        # Private key - MUST be kept secret, used for DH exchange
        self.private_key = None
        # Public key - can be shared, used for DH exchange
        self.public_key = None
        # Public key in bytes format (what gets transmitted over network)
        self.public_key_bytes = None
        # Derived shared symmetric key (what we get after DH + HKDF)
        self.shared_key = None
    
    def generate_keypair(self):
        """
        Generate an X25519 keypair for this participant.
        
        This is called at the start of the protocol. Each participant generates
        their own keypair independently. The private key stays secret, the
        public key will be sent to the peer.
        """
        # Generate a fresh keypair using X25519
        self.private_key, self.public_key = generate_x25519_keypair()
        # Convert public key to bytes format for transmission
        self.public_key_bytes = public_bytes(self.public_key)
        print(f"{self.name}: Generated keypair")
        print(f"{self.name}: Public key (hex): {binascii.hexlify(self.public_key_bytes).decode()}")
    
    def derive_key(self, peer_public_bytes):
        """
        Derive the shared symmetric key using peer's public key.
        
        Args:
            peer_public_bytes: The peer's public key as 32 bytes
        
        This assumes we received the peer's public key over the network.
        We use our private key and their public key to compute the shared secret,
        then derive a symmetric encryption key using HKDF.
        
        SECURITY VULNERABILITY: In this phase, we trust the peer_public_bytes
        without any authentication. This allows Mallory to intercept and replace it!
        """
        # Derive the shared key using DH + HKDF
        self.shared_key = derive_shared_key(self.private_key, peer_public_bytes)
        print(f"{self.name}: Derived shared key (hex): {binascii.hexlify(self.shared_key).decode()}")


class Mallory:
    """
    Man-in-the-Middle (MITM) attacker.
    
    Mallory intercepts all communication between Alice and Bob and replaces
    public keys with her own. This attack succeeds because there's no authentication
    to verify that public keys actually belong to Alice or Bob.
    
    Attack Strategy:
    1. Intercept Alice's public key sent to Bob
    2. Replace it with Mallory's own public key (impersonating Alice)
    3. Derive a key with Alice using Bob's fake public key
    4. Intercept Bob's public key sent to Alice
    5. Replace it with Mallory's own public key (impersonating Bob)
    6. Derive a key with Bob using Alice's fake public key
    
    Result: Alice thinks she's talking to Bob, Bob thinks he's talking to Alice,
    but both are actually talking to Mallory. Mallory can decrypt and modify
    all messages in transit.
    """
    
    def __init__(self):
        """
        Initialize the MITM attacker.
        
        Mallory needs TWO keypairs:
        - One to impersonate Alice (when talking to Bob)
        - One to impersonate Bob (when talking to Alice)
        """
        self.name = "Mallory"
        
        # Generate first keypair - this will be used when impersonating Alice
        # When Bob thinks he's receiving Alice's key, he'll actually get this
        self.alice_priv, self.alice_pub = generate_x25519_keypair()
        
        # Generate second keypair - this will be used when impersonating Bob
        # When Alice thinks she's receiving Bob's key, she'll actually get this
        self.bob_priv, self.bob_pub = generate_x25519_keypair()
        
        # Convert to bytes format for transmission
        self.alice_pub_bytes = public_bytes(self.alice_pub)  # Fake "Alice" key
        self.bob_pub_bytes = public_bytes(self.bob_pub)      # Fake "Bob" key
        
        # These will store the shared keys Mallory establishes with each victim
        self.key_with_alice = None  # Key Mallory shares with Alice (derived using bob_priv)
        self.key_with_bob = None    # Key Mallory shares with Bob (derived using alice_priv)
        
        print(f"{self.name}: Generated keypairs for attack")
        print(f"{self.name}: Public key for impersonating Alice (hex): {binascii.hexlify(self.alice_pub_bytes).decode()}")
        print(f"{self.name}: Public key for impersonating Bob (hex): {binascii.hexlify(self.bob_pub_bytes).decode()}")
    
    def intercept_and_replace(self, message_from, message_to):
        """
        Core MITM attack function: intercept a public key and replace it with Mallory's fake key.
        
        This function performs the critical MITM attack step:
        1. Intercept the real public key from the sender
        2. Derive a key with the sender using Mallory's fake keypair
        3. Replace the real key with Mallory's fake key when forwarding to the receiver
        
        Args:
            message_from: Participant sending the key (Participant object: Alice or Bob)
            message_to: Participant who should receive the key (not used, but shown for clarity)
        
        Returns:
            bytes: Mallory's fake public key (to forward to the receiver)
        
        How the attack works:
        - When Alice sends her key to Bob, Mallory intercepts it
        - Mallory uses her "Bob" keypair to establish a shared key with Alice
          (Alice thinks she's talking to Bob, but it's actually Mallory)
        - Mallory forwards her fake "Bob" key to Alice
        - Similarly when Bob sends his key to Alice
        
        Result: Both Alice and Bob think they share keys with each other,
        but actually both share keys with Mallory!
        """
        # Get the real public key that the sender is trying to send
        real_pub_bytes = message_from.public_key_bytes
        
        # Handle the case where Alice is sending her key to Bob
        if message_from.name == "Alice":
            # Alice thinks she's sending her public key to Bob
            # But Mallory intercepts it and derives a key with Alice using Mallory's "Bob" keypair
            # This gives Mallory the key that Alice thinks she shares with Bob
            self.key_with_alice = derive_shared_key(
                self.bob_priv,      # Mallory's private key for impersonating Bob
                real_pub_bytes      # Alice's real public key
            )
            print(f"{self.name}: [INTERCEPTED] Alice's public key")
            print(f"{self.name}: Derived key with Alice (hex): {binascii.hexlify(self.key_with_alice).decode()}")
            # Instead of forwarding Alice's real key to Bob, Mallory sends her fake "Bob" key
            # Now Alice will derive a key using Mallory's fake key (thinking it's Bob's)
            print(f"{self.name}: [FORWARDING] Fake Bob's public key to Alice")
            return self.bob_pub_bytes  # Return fake "Bob" key
        
        # Handle the case where Bob is sending his key to Alice
        elif message_from.name == "Bob":
            # Bob thinks he's sending his public key to Alice
            # But Mallory intercepts it and derives a key with Bob using Mallory's "Alice" keypair
            # This gives Mallory the key that Bob thinks he shares with Alice
            self.key_with_bob = derive_shared_key(
                self.alice_priv,    # Mallory's private key for impersonating Alice
                real_pub_bytes      # Bob's real public key
            )
            print(f"{self.name}: [INTERCEPTED] Bob's public key")
            print(f"{self.name}: Derived key with Bob (hex): {binascii.hexlify(self.key_with_bob).decode()}")
            # Instead of forwarding Bob's real key to Alice, Mallory sends her fake "Alice" key
            # Now Bob will derive a key using Mallory's fake key (thinking it's Alice's)
            print(f"{self.name}: [FORWARDING] Fake Alice's public key to Bob")
            return self.alice_pub_bytes  # Return fake "Alice" key
    
    def can_decrypt(self, encrypted_message, sender):
        """
        Check if Mallory can decrypt a message from a given sender.
        
        Args:
            encrypted_message: The encrypted message (not used in check, shown for context)
            sender: Who sent the message ("Alice" or "Bob")
        
        Returns:
            bool: True if Mallory has established a key with this sender (she can decrypt)
        
        After the MITM attack succeeds, Mallory has shared keys with both Alice and Bob.
        This means she can:
        - Decrypt messages from Alice (using key_with_alice)
        - Decrypt messages from Bob (using key_with_bob)
        - Read, modify, and re-encrypt messages in transit
        - This is why MITM attacks are so dangerous!
        """
        if sender == "Alice":
            # Check if we've established a key with Alice
            return self.key_with_alice is not None
        elif sender == "Bob":
            # Check if we've established a key with Bob
            return self.key_with_bob is not None
        return False


def demonstrate_mitm_attack():
    """
    Demonstrate the complete MITM attack flow step-by-step.
    
    This function shows how Mallory can successfully intercept and manipulate
    the unauthenticated Diffie-Hellman key exchange between Alice and Bob.
    
    Attack Flow:
    1. Alice generates her keypair
    2. Alice tries to send her public key to Bob
       → Mallory intercepts it
       → Mallory derives a key with Alice
       → Mallory sends her fake "Bob" key to Alice instead
    3. Bob generates his keypair
    4. Bob tries to send his public key to Alice
       → Mallory intercepts it
       → Mallory derives a key with Bob
       → Mallory sends her fake "Alice" key to Bob instead
    5. Alice and Bob both derive keys, but they're actually sharing keys with Mallory
    
    Result: Alice ↔ Mallory ↔ Bob (Mallory can decrypt all traffic)
    """
    print("=" * 70)
    print("PHASE 2: Man-in-the-Middle Attack Demonstration")
    print("=" * 70)
    print()
    
    # Create the three actors: two legitimate participants and one attacker
    alice = Participant("Alice")      # Legitimate participant 1
    bob = Participant("Bob")         # Legitimate participant 2
    mallory = Mallory()               # MITM attacker (positioned between Alice and Bob)
    
    # ========================================================================
    # STEP 1: Alice generates her keypair
    # ========================================================================
    print("\n" + "-" * 70)
    print("STEP 1: Alice generates keypair")
    print("-" * 70)
    # Alice creates her X25519 keypair (private key stays secret, public key will be shared)
    alice.generate_keypair()
    
    # ========================================================================
    # STEP 2: Alice sends public key to Bob - MALLORY INTERCEPTS
    # ========================================================================
    print("\n" + "-" * 70)
    print("STEP 2: Alice sends public key to Bob (intercepted by Mallory)")
    print("-" * 70)
    # In a real attack, Mallory would be on the network path between Alice and Bob
    # Here we simulate the interception and replacement
    # Mallory:
    #   1. Receives Alice's real public key (meant for Bob)
    #   2. Derives a shared key with Alice using her fake "Bob" keypair
    #   3. Returns her fake "Bob" key (which will be sent to Alice)
    fake_bob_key_for_alice = mallory.intercept_and_replace(alice, bob)
    
    # ========================================================================
    # STEP 3: Bob generates his keypair
    # ========================================================================
    print("\n" + "-" * 70)
    print("STEP 3: Bob generates keypair")
    print("-" * 70)
    # Bob creates his X25519 keypair independently
    bob.generate_keypair()
    
    # ========================================================================
    # STEP 4: Bob sends public key to Alice - MALLORY INTERCEPTS
    # ========================================================================
    print("\n" + "-" * 70)
    print("STEP 4: Bob sends public key to Alice (intercepted by Mallory)")
    print("-" * 70)
    # Mallory intercepts Bob's key as well:
    #   1. Receives Bob's real public key (meant for Alice)
    #   2. Derives a shared key with Bob using her fake "Alice" keypair
    #   3. Returns her fake "Alice" key (which will be sent to Bob)
    fake_alice_key_for_bob = mallory.intercept_and_replace(bob, alice)
    
    # ========================================================================
    # STEP 5: Alice receives fake "Bob" key and derives shared key
    # ========================================================================
    print("\n" + "-" * 70)
    print("STEP 5: Alice receives fake 'Bob' key and derives shared key")
    print("-" * 70)
    # Alice thinks she received Bob's public key, but it's actually Mallory's fake key
    # Alice derives what she thinks is a shared key with Bob
    # But actually: alice.shared_key = DH(alice_private, mallory_fake_bob_public)
    # This equals: mallory.key_with_alice = DH(mallory_bob_private, alice_public)
    alice.derive_key(fake_bob_key_for_alice)  # Alice unknowingly shares key with Mallory
    
    # ========================================================================
    # STEP 6: Bob receives fake "Alice" key and derives shared key
    # ========================================================================
    print("\n" + "-" * 70)
    print("STEP 6: Bob receives fake 'Alice' key and derives shared key")
    print("-" * 70)
    # Bob thinks he received Alice's public key, but it's actually Mallory's fake key
    # Bob derives what he thinks is a shared key with Alice
    # But actually: bob.shared_key = DH(bob_private, mallory_fake_alice_public)
    # This equals: mallory.key_with_bob = DH(mallory_alice_private, bob_public)
    bob.derive_key(fake_alice_key_for_bob)  # Bob unknowingly shares key with Mallory
    
    print("\n" + "=" * 70)
    print("ATTACK RESULTS")
    print("=" * 70)
    
    print(f"\nAlice's shared key (hex): {binascii.hexlify(alice.shared_key).decode()}")
    print(f"Bob's shared key   (hex): {binascii.hexlify(bob.shared_key).decode()}")
    print(f"Mallory's key with Alice (hex): {binascii.hexlify(mallory.key_with_alice).decode()}")
    print(f"Mallory's key with Bob   (hex): {binascii.hexlify(mallory.key_with_bob).decode()}")
    
    # Verify the attack succeeded
    print("\n" + "-" * 70)
    if alice.shared_key == mallory.key_with_alice:
        print("[ATTACK SUCCESS] Alice shares a key with Mallory (not Bob)")
    else:
        print("[ERROR] Attack simulation failed")
    
    if bob.shared_key == mallory.key_with_bob:
        print("[ATTACK SUCCESS] Bob shares a key with Mallory (not Alice)")
    else:
        print("[ERROR] Attack simulation failed")
    
    if alice.shared_key != bob.shared_key:
        print("[CRITICAL] Alice and Bob have DIFFERENT keys!")
        print("   They cannot communicate securely. Mallory can decrypt everything.")
    else:
        print("[ERROR] Alice and Bob should have different keys after MITM attack")
    
    print("\n" + "=" * 70)
    print("SECURITY ANALYSIS")
    print("=" * 70)
    print("""
The MITM attack succeeded because:
1. The DH key exchange has NO authentication mechanism
2. Public keys are not bound to identities (Alice/Bob)
3. Mallory can impersonate either party without detection

SOLUTION: We need to add digital signatures (Ed25519) to authenticate
public keys. This will be demonstrated in Phase 3.
""")


if __name__ == "__main__":
    demonstrate_mitm_attack()


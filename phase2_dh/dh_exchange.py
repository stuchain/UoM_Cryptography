# phase2_dh/dh_exchange.py
"""
X25519 Diffie-Hellman Demo (heavily commented)

This script demonstrates a minimal, correct Diffie-Hellman key exchange
using X25519 (Curve25519). It shows how Alice and Bob each:
  1. generate an X25519 keypair (private + public)
  2. exchange public keys (simulated here by directly passing bytes)
  3. compute the raw shared secret via X25519
  4. derive a symmetric key from the raw shared secret using HKDF-SHA256

Important security notes:
- Never use the raw shared secret directly as an encryption key. Always
  run a key-derivation function (KDF) like HKDF to derive symmetric keys.
- In real protocols, include a salt and descriptive 'info' in HKDF to bind
  the key to protocol/context and provide forward secrecy benefits.
"""

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import binascii

# ---------------------------
# Helper functions
# ---------------------------

def generate_x25519_keypair():
    """
    Generate an X25519 keypair.

    Returns:
        (private_key, public_key)
    - private_key: X25519PrivateKey object (kept secret by the owner)
    - public_key : X25519PublicKey object (safe to share)
    """
    private = x25519.X25519PrivateKey.generate()  # generate private key
    public = private.public_key()                  # compute corresponding public key
    return private, public

def public_bytes(public_key):
    """
    Serialize an X25519 public key to raw bytes (32 bytes).

    We use Encoding.Raw + PublicFormat.Raw which for X25519 yields the 32-byte
    public key used in Curve25519. These raw bytes are what you'd send on the wire.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

def derive_shared_key(our_private: x25519.X25519PrivateKey, their_public_bytes: bytes, info: bytes = b"secure_channel_v1"):
    """
    Given our private key and the peer's public key bytes, compute the shared key.

    Steps:
    1. Recreate the peer's X25519PublicKey from raw bytes.
    2. Perform the X25519 key exchange: our_private.exchange(peer_public)
       -> returns a raw 32-byte shared secret (not yet suitable as an encryption key).
    3. Run HKDF-SHA256 on the shared secret to derive a symmetric key (32 bytes).
       - length=32 gives a 256-bit symmetric key suitable for AEAD (e.g., ChaCha20-Poly1305).
       - salt is left None here for simplicity; in production you should usually use a salt.
       - info should include protocol identifiers (we pass "secure_channel_v1" here).
    """
    # 1) Reconstruct peer's public key object from raw bytes
    their_public = x25519.X25519PublicKey.from_public_bytes(their_public_bytes)

    # 2) Compute raw shared secret (32 bytes)
    shared_secret = our_private.exchange(their_public)

    # 3) Derive a symmetric key using HKDF(SHA256)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,     # 256-bit symmetric key output
        salt=None,     # In demonstrations we can leave salt None; real apps should set it.
        info=info,     # context binding (protocol name, version, etc.)
    )
    key = hkdf.derive(shared_secret)  # returns 'length' bytes
    return key

# ---------------------------
# Main demo flow
# ---------------------------

def main():
    # --- Key generation (Alice) ---
    alice_priv, alice_pub = generate_x25519_keypair()
    # alice_priv: X25519PrivateKey (kept secret)
    # alice_pub : X25519PublicKey  (shared to Bob)

    # --- Key generation (Bob) ---
    bob_priv, bob_pub = generate_x25519_keypair()
    # bob_priv: X25519PrivateKey (kept secret)
    # bob_pub : X25519PublicKey  (shared to Alice)

    # Serialize public keys to raw bytes (what would be transmitted)
    alice_pub_bytes = public_bytes(alice_pub)  # 32 bytes
    bob_pub_bytes = public_bytes(bob_pub)      # 32 bytes

    # Print public keys in hex so you can visually inspect them
    print("Alice public (hex):", binascii.hexlify(alice_pub_bytes).decode())
    print("Bob   public (hex):", binascii.hexlify(bob_pub_bytes).decode())

    # Each side derives the symmetric key using their private key and the other's public bytes.
    # In a real network, Alice would receive bob_pub_bytes over the wire and vice versa.
    alice_key = derive_shared_key(alice_priv, bob_pub_bytes, info=b"secure_channel_v1")
    bob_key   = derive_shared_key(bob_priv, alice_pub_bytes, info=b"secure_channel_v1")

    # Show derived keys in hex for demonstration
    print("\nDerived symmetric keys (hex):")
    print("Alice key:", binascii.hexlify(alice_key).decode())
    print("Bob   key:", binascii.hexlify(bob_key).decode())

    # They MUST be identical if DH worked correctly and no tampering happened
    if alice_key == bob_key:
        print("\n[SUCCESS] Alice and Bob derived the same symmetric key.")
    else:
        print("\n[ERROR] Keys differ! (This would indicate a problem or an active attacker.)")

    # -----------------------
    # Quick demonstration: why we use HKDF
    # -----------------------
    # The raw shared_secret produced by X25519 can be the same across different protocol runs
    # or may lack the necessary key separation. HKDF stretches/derives a symmetric key
    # and lets you include 'info' and 'salt' to bind the key to the protocol context.
    #
    # If you later use this key in AEAD, include unique nonces for each message to keep encryption secure.

if __name__ == "__main__":
    main()

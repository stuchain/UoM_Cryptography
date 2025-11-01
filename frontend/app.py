"""
Flask Backend for Secure Channel Demo Frontend

This provides a REST API to run each phase and get results with visualization data.
"""

from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import sys
import os
import json
import io
from contextlib import redirect_stdout
import traceback

# Add project root to path so we can import phase modules
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)  # Enable CORS for frontend-backend communication

# Import phase modules
try:
    from phase2_dh.dh_exchange import generate_x25519_keypair, public_bytes, derive_shared_key
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
    from cryptography.exceptions import InvalidSignature, InvalidTag
    import binascii
    import struct
    import secrets
except ImportError as e:
    print(f"Warning: Could not import some modules: {e}")


@app.route('/')
def index():
    """Serve the main frontend page"""
    return render_template('index.html')


@app.route('/api/phase1', methods=['POST'])
def run_phase1():
    """
    Run Phase 1: Basic Diffie-Hellman Key Exchange
    
    Returns:
        JSON with keys, visualization data, and status
    """
    try:
        # Generate keypairs
        alice_priv, alice_pub = generate_x25519_keypair()
        bob_priv, bob_pub = generate_x25519_keypair()
        
        alice_pub_bytes = public_bytes(alice_pub)
        bob_pub_bytes = public_bytes(bob_pub)
        
        # Derive shared keys
        alice_key = derive_shared_key(alice_priv, bob_pub_bytes)
        bob_key = derive_shared_key(bob_priv, alice_pub_bytes)
        
        keys_match = alice_key == bob_key
        
        return jsonify({
            'success': True,
            'phase': 1,
            'title': 'Basic Diffie-Hellman Key Exchange',
            'data': {
                'alice': {
                    'public_key': binascii.hexlify(alice_pub_bytes).decode(),
                    'shared_key': binascii.hexlify(alice_key).decode()
                },
                'bob': {
                    'public_key': binascii.hexlify(bob_pub_bytes).decode(),
                    'shared_key': binascii.hexlify(bob_key).decode()
                },
                'keys_match': keys_match
            },
            'visualization': {
                'type': 'key_comparison',
                'labels': ['Alice Shared Key', 'Bob Shared Key'],
                'keys_match': keys_match,
                'alice_key_hex': binascii.hexlify(alice_key).decode(),
                'bob_key_hex': binascii.hexlify(bob_key).decode()
            },
            'summary': 'Alice and Bob successfully derived the same shared key using Diffie-Hellman.' if keys_match else 'ERROR: Keys do not match!'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/phase2', methods=['POST'])
def run_phase2():
    """
    Run Phase 2: MITM Attack Demonstration
    
    Returns:
        JSON with attack results and visualization data
    """
    try:
        # Generate participants
        alice_priv, alice_pub = generate_x25519_keypair()
        bob_priv, bob_pub = generate_x25519_keypair()
        mallory_alice_priv, mallory_alice_pub = generate_x25519_keypair()
        mallory_bob_priv, mallory_bob_pub = generate_x25519_keypair()
        
        alice_pub_bytes = public_bytes(alice_pub)
        bob_pub_bytes = public_bytes(bob_pub)
        mallory_alice_pub_bytes = public_bytes(mallory_alice_pub)
        mallory_bob_pub_bytes = public_bytes(mallory_bob_pub)
        
        # Mallory intercepts and establishes keys
        # Alice thinks she's talking to Bob, but it's Mallory (using bob key)
        alice_shared = derive_shared_key(alice_priv, mallory_bob_pub_bytes)
        mallory_key_with_alice = derive_shared_key(mallory_bob_priv, alice_pub_bytes)
        
        # Bob thinks he's talking to Alice, but it's Mallory (using alice key)
        bob_shared = derive_shared_key(bob_priv, mallory_alice_pub_bytes)
        mallory_key_with_bob = derive_shared_key(mallory_alice_priv, bob_pub_bytes)
        
        attack_success = (alice_shared == mallory_key_with_alice and 
                         bob_shared == mallory_key_with_bob and
                         alice_shared != bob_shared)
        
        return jsonify({
            'success': True,
            'phase': 2,
            'title': 'Man-in-the-Middle Attack',
            'data': {
                'alice': {
                    'public_key': binascii.hexlify(alice_pub_bytes).decode(),
                    'shared_key': binascii.hexlify(alice_shared).decode()
                },
                'bob': {
                    'public_key': binascii.hexlify(bob_pub_bytes).decode(),
                    'shared_key': binascii.hexlify(bob_shared).decode()
                },
                'mallory': {
                    'key_with_alice': binascii.hexlify(mallory_key_with_alice).decode(),
                    'key_with_bob': binascii.hexlify(mallory_key_with_bob).decode(),
                    'fake_alice_key': binascii.hexlify(mallory_alice_pub_bytes).decode(),
                    'fake_bob_key': binascii.hexlify(mallory_bob_pub_bytes).decode()
                },
                'attack_success': attack_success,
                'alice_bob_keys_differ': alice_shared != bob_shared
            },
            'visualization': {
                'type': 'mitm_comparison',
                'keys': {
                    'alice': binascii.hexlify(alice_shared).decode()[:16] + '...',
                    'bob': binascii.hexlify(bob_shared).decode()[:16] + '...',
                    'mallory_alice': binascii.hexlify(mallory_key_with_alice).decode()[:16] + '...',
                    'mallory_bob': binascii.hexlify(mallory_key_with_bob).decode()[:16] + '...'
                },
                'attack_success': attack_success
            },
            'summary': 'MITM attack succeeded: Alice and Bob have different keys, both sharing with Mallory!' if attack_success else 'Attack simulation error'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/phase3', methods=['POST'])
def run_phase3():
    """
    Run Phase 3: Authenticated Diffie-Hellman
    
    Returns:
        JSON with authentication results
    """
    try:
        # Generate keypairs (DH + Ed25519)
        alice_dh_priv, alice_dh_pub = generate_x25519_keypair()
        bob_dh_priv, bob_dh_pub = generate_x25519_keypair()
        
        alice_signing_priv = ed25519.Ed25519PrivateKey.generate()
        alice_signing_pub = alice_signing_priv.public_key()
        
        bob_signing_priv = ed25519.Ed25519PrivateKey.generate()
        bob_signing_pub = bob_signing_priv.public_key()
        
        alice_dh_pub_bytes = public_bytes(alice_dh_pub)
        bob_dh_pub_bytes = public_bytes(bob_dh_pub)
        alice_signing_pub_bytes = alice_signing_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        bob_signing_pub_bytes = bob_signing_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Sign and verify
        alice_signature = alice_signing_priv.sign(alice_dh_pub_bytes)
        
        # Verify Alice's signature (Bob's perspective)
        try:
            bob_signing_pub.verify(alice_signature, alice_dh_pub_bytes)
            alice_signature_valid = True
            bob_key = derive_shared_key(bob_dh_priv, alice_dh_pub_bytes)
        except InvalidSignature:
            alice_signature_valid = False
            bob_key = None
        
        # Bob signs
        bob_signature = bob_signing_priv.sign(bob_dh_pub_bytes)
        
        # Verify Bob's signature (Alice's perspective)
        try:
            alice_signing_pub.verify(bob_signature, bob_dh_pub_bytes)
            bob_signature_valid = True
            alice_key = derive_shared_key(alice_dh_priv, bob_dh_pub_bytes)
        except InvalidSignature:
            bob_signature_valid = False
            alice_key = None
        
        authenticated = alice_signature_valid and bob_signature_valid
        keys_match = authenticated and (alice_key == bob_key)
        
        # Test Mallory's attack (should fail)
        mallory_signing_priv = ed25519.Ed25519PrivateKey.generate()
        mallory_signature = mallory_signing_priv.sign(alice_dh_pub_bytes)
        
        try:
            alice_signing_pub.verify(mallory_signature, alice_dh_pub_bytes)
            mallory_attack_succeeds = True
        except InvalidSignature:
            mallory_attack_succeeds = False
        
        return jsonify({
            'success': True,
            'phase': 3,
            'title': 'Authenticated Diffie-Hellman',
            'data': {
                'alice': {
                    'dh_public_key': binascii.hexlify(alice_dh_pub_bytes).decode(),
                    'signing_public_key': binascii.hexlify(alice_signing_pub_bytes).decode(),
                    'shared_key': binascii.hexlify(alice_key).decode() if alice_key else None,
                    'signature_valid': bob_signature_valid
                },
                'bob': {
                    'dh_public_key': binascii.hexlify(bob_dh_pub_bytes).decode(),
                    'signing_public_key': binascii.hexlify(bob_signing_pub_bytes).decode(),
                    'shared_key': binascii.hexlify(bob_key).decode() if bob_key else None,
                    'signature_valid': alice_signature_valid
                },
                'authenticated': authenticated,
                'keys_match': keys_match,
                'mallory_attack_failed': not mallory_attack_succeeds
            },
            'visualization': {
                'type': 'authentication',
                'signatures_valid': alice_signature_valid and bob_signature_valid,
                'keys_match': keys_match,
                'attack_prevented': not mallory_attack_succeeds
            },
            'summary': 'Authentication successful! MITM attack prevented.' if authenticated and not mallory_attack_succeeds else 'Authentication or attack prevention failed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/phase4', methods=['POST'])
def run_phase4():
    """
    Run Phase 4: Secure Channel with AEAD
    
    Returns:
        JSON with encryption results
    """
    try:
        # Generate keypairs
        alice_dh_priv, alice_dh_pub = generate_x25519_keypair()
        bob_dh_priv, bob_dh_pub = generate_x25519_keypair()
        
        alice_signing_priv = ed25519.Ed25519PrivateKey.generate()
        bob_signing_priv = ed25519.Ed25519PrivateKey.generate()
        
        alice_dh_pub_bytes = public_bytes(alice_dh_pub)
        bob_dh_pub_bytes = public_bytes(bob_dh_pub)
        
        # Derive shared key
        shared_key = derive_shared_key(alice_dh_priv, bob_dh_pub_bytes)
        
        # Initialize cipher
        cipher = ChaCha20Poly1305(shared_key)
        
        # Encrypt a message
        test_message = b"Hello Bob! This is a secret message."
        nonce = os.urandom(12)
        associated_data = b""  # Empty associated data for this demo
        # ChaCha20Poly1305.encrypt() signature: encrypt(nonce, data, associated_data)
        ciphertext = cipher.encrypt(nonce, test_message, associated_data)
        
        # Decrypt message
        try:
            # ChaCha20Poly1305.decrypt() signature: decrypt(nonce, data, associated_data)
            decrypted = cipher.decrypt(nonce, ciphertext, associated_data)
            decryption_success = decrypted == test_message
        except InvalidTag:
            decryption_success = False
            decrypted = None
        
        # Test tampering detection
        tampered_ciphertext = bytearray(ciphertext)
        tampered_ciphertext[10] ^= 0xFF
        
        try:
            cipher.decrypt(nonce, bytes(tampered_ciphertext), associated_data)
            tampering_detected = False
        except InvalidTag:
            tampering_detected = True
        
        return jsonify({
            'success': True,
            'phase': 4,
            'title': 'Secure Channel with AEAD',
            'data': {
                'message_length': len(test_message),
                'ciphertext_length': len(ciphertext),
                'encryption_success': True,
                'decryption_success': decryption_success,
                'message_original': test_message.decode('utf-8'),
                'message_decrypted': decrypted.decode('utf-8') if decrypted else None,
                'tampering_detected': tampering_detected
            },
            'visualization': {
                'type': 'encryption',
                'message_sizes': {
                    'original': len(test_message),
                    'encrypted': len(ciphertext),
                    'overhead': len(ciphertext) - len(test_message)
                },
                'security_properties': {
                    'confidentiality': True,
                    'integrity': tampering_detected,
                    'authentication': True
                }
            },
            'summary': 'Secure channel established! Encryption and tampering detection working.' if decryption_success and tampering_detected else 'Some security properties failed'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/phase5', methods=['POST'])
def run_phase5():
    """
    Run Phase 5: Blockchain Integration (Simulated)
    
    Returns:
        JSON with blockchain simulation results
    """
    try:
        # Generate keys
        alice_signing_priv = ed25519.Ed25519PrivateKey.generate()
        alice_signing_pub = alice_signing_priv.public_key()
        alice_signing_pub_bytes = alice_signing_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        bob_signing_priv = ed25519.Ed25519PrivateKey.generate()
        bob_signing_pub = bob_signing_priv.public_key()
        bob_signing_pub_bytes = bob_signing_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Simulate blockchain registration
        blockchain_registry = {
            'alice_address': 'Alice1111111111111111111111111111111111',
            'bob_address': 'Bob11111111111111111111111111111111111111'
        }
        
        # Simulate verification
        alice_registered = True  # Simulated
        bob_registered = True  # Simulated
        alice_key_verified = True  # Simulated
        bob_key_verified = True  # Simulated
        
        return jsonify({
            'success': True,
            'phase': 5,
            'title': 'Blockchain Integration',
            'data': {
                'blockchain': {
                    'network': 'Solana (Devnet)',
                    'registry_program': 'KeyRegistry11111111111111111111111111111'
                },
                'alice': {
                    'address': blockchain_registry['alice_address'],
                    'public_key': binascii.hexlify(alice_signing_pub_bytes).decode(),
                    'registered': alice_registered,
                    'verified': alice_key_verified
                },
                'bob': {
                    'address': blockchain_registry['bob_address'],
                    'public_key': binascii.hexlify(bob_signing_pub_bytes).decode(),
                    'registered': bob_registered,
                    'verified': bob_key_verified
                }
            },
            'visualization': {
                'type': 'blockchain',
                'registrations': [
                    {'name': 'Alice', 'status': 'registered', 'verified': True},
                    {'name': 'Bob', 'status': 'registered', 'verified': True}
                ],
                'verification_success': alice_key_verified and bob_key_verified
            },
            'summary': 'Blockchain verification successful! Keys registered and verified on-chain.'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/api/run-all', methods=['POST'])
def run_all_phases():
    """
    Run all phases sequentially
    
    Returns:
        JSON with results from all phases
    """
    results = []
    
    for phase_num in range(1, 6):
        try:
            if phase_num == 1:
                result = run_phase1()
            elif phase_num == 2:
                result = run_phase2()
            elif phase_num == 3:
                result = run_phase3()
            elif phase_num == 4:
                result = run_phase4()
            elif phase_num == 5:
                result = run_phase5()
            
            data = result.get_json()
            results.append(data)
        except Exception as e:
            results.append({
                'success': False,
                'phase': phase_num,
                'error': str(e)
            })
    
    return jsonify({
        'success': True,
        'results': results
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Secure Channel Demo Frontend")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Open your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)


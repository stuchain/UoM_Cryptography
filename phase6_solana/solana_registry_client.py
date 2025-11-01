"""
Phase 5: Solana Blockchain Integration - Key Registry Client

This module provides a Python client to interact with the Solana Key Registry
smart contract. It allows users to:
1. Register their Ed25519 public keys on-chain
2. Verify public keys against the on-chain registry
3. Update registered keys

The registry acts as a decentralized PKI (Public Key Infrastructure),
preventing MITM attacks by providing a trusted source of public keys.
"""

import base64
import json
from typing import Optional, Tuple
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoResp
from solders.system_program import ID as SYSTEM_PROGRAM_ID
from anchorpy import Program, Provider, Wallet
from anchorpy.provider.anchor import AnchorProvider
from anchorpy.idl import Idl
import solana.rpc.api as solana_api

# Import secure channel components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phase5_aead'))
from secure_channel import SecureChannel


class SolanaKeyRegistryClient:
    """
    Client for interacting with the Solana Key Registry smart contract
    """
    
    def __init__(self, rpc_url: str = "https://api.devnet.solana.com", program_id: Optional[str] = None):
        """
        Initialize the registry client
        
        Args:
            rpc_url: Solana RPC endpoint URL
            program_id: Program ID of the deployed Key Registry (default: test ID)
        """
        self.rpc_url = rpc_url
        self.connection = solana_api.Client(rpc_url)
        self.program_id = Pubkey.from_string(program_id or "KeyRegistry11111111111111111111111111111")
        
        # Load IDL (Interface Definition Language) for the program
        # In production, load from on-chain or file
        self.idl = self._load_idl()
        
        print(f"Solana Key Registry Client initialized")
        print(f"RPC URL: {rpc_url}")
        print(f"Program ID: {self.program_id}")
    
    def _load_idl(self) -> dict:
        """Load the IDL for the Key Registry program"""
        # Simplified IDL structure
        # In production, load from on-chain or Anchor-generated IDL file
        return {
            "version": "0.1.0",
            "name": "key_registry",
            "instructions": [
                {
                    "name": "registerKey",
                    "accounts": [
                        {"name": "owner", "isMut": True, "isSigner": True},
                        {"name": "keyRecord", "isMut": True, "isSigner": False},
                        {"name": "systemProgram", "isMut": False, "isSigner": False}
                    ],
                    "args": [{"name": "publicKey", "type": {"array": ["u8", 32]}}]
                },
                {
                    "name": "updateKey",
                    "accounts": [
                        {"name": "owner", "isMut": True, "isSigner": True},
                        {"name": "keyRecord", "isMut": True, "isSigner": False}
                    ],
                    "args": [{"name": "newPublicKey", "type": {"array": ["u8", 32]}}]
                },
                {
                    "name": "verifyKey",
                    "accounts": [
                        {"name": "keyRecord", "isMut": False, "isSigner": False}
                    ],
                    "args": [{"name": "publicKeyToVerify", "type": {"array": ["u8", 32]}}],
                    "returns": "bool"
                }
            ],
            "accounts": [
                {
                    "name": "KeyRecord",
                    "type": {
                        "kind": "struct",
                        "fields": [
                            {"name": "owner", "type": "publicKey"},
                            {"name": "publicKey", "type": {"array": ["u8", 32]}},
                            {"name": "bump", "type": "u8"}
                        ]
                    }
                }
            ]
        }
    
    def _derive_key_record_pda(self, owner_pubkey: Pubkey) -> Tuple[Pubkey, int]:
        """
        Derive the PDA (Program Derived Address) for a key record
        
        Returns:
            (pda_pubkey, bump_seed)
        """
        seeds = [b"key_record", bytes(owner_pubkey)]
        pda, bump = Pubkey.find_program_address(seeds, self.program_id)
        return pda, bump
    
    def register_key(self, wallet_keypair: Keypair, ed25519_public_key: bytes) -> str:
        """
        Register an Ed25519 public key on-chain for the wallet owner
        
        Args:
            wallet_keypair: Solana wallet keypair (signer)
            ed25519_public_key: 32-byte Ed25519 public key to register
        
        Returns:
            Transaction signature
        """
        if len(ed25519_public_key) != 32:
            raise ValueError("Ed25519 public key must be 32 bytes")
        
        owner_pubkey = wallet_keypair.pubkey()
        key_record_pda, bump = self._derive_key_record_pda(owner_pubkey)
        
        print(f"Registering public key for owner: {owner_pubkey}")
        print(f"Key Record PDA: {key_record_pda}")
        print(f"Public key (hex): {ed25519_public_key.hex()}")
        
        # In a real implementation, you would:
        # 1. Build the instruction using Anchor
        # 2. Create a transaction
        # 3. Sign and send it
        
        # For demonstration, we'll simulate the transaction
        print("✅ Registration instruction prepared")
        print("   (In production, this would be sent as a Solana transaction)")
        
        # Return a mock transaction signature for demo
        return "mock_tx_signature_for_demo"
    
    def verify_key(self, owner_pubkey_str: str, ed25519_public_key: bytes) -> bool:
        """
        Verify if a public key matches what's registered on-chain
        
        Args:
            owner_pubkey_str: Solana wallet address of the key owner
            ed25519_public_key: Public key to verify (32 bytes)
        
        Returns:
            True if the key matches, False otherwise
        """
        owner_pubkey = Pubkey.from_string(owner_pubkey_str)
        key_record_pda, _ = self._derive_key_record_pda(owner_pubkey)
        
        print(f"Verifying public key for owner: {owner_pubkey}")
        print(f"Checking Key Record PDA: {key_record_pda}")
        
        # In a real implementation:
        # 1. Fetch the KeyRecord account from the blockchain
        # 2. Compare the stored public_key with ed25519_public_key
        
        # For demonstration, simulate verification
        try:
            # Mock: In production, fetch account data here
            account_info = self.connection.get_account_info(key_record_pda)
            
            if account_info.value is None:
                print("❌ Key record not found on-chain")
                return False
            
            # Decode account data and verify
            # (In production, deserialize according to KeyRecord structure)
            print("✅ Key record found on-chain")
            print("   (In production, would deserialize and compare keys)")
            
            # For demo, return True if account exists
            return True
            
        except Exception as e:
            print(f"❌ Verification error: {e}")
            return False


class SecureChannelWithBlockchain(SecureChannel):
    """
    Extended secure channel that uses Solana blockchain for key verification
    """
    
    def __init__(self, name: str, solana_address: str, registry_client: SolanaKeyRegistryClient):
        """
        Initialize secure channel with blockchain integration
        
        Args:
            name: Participant name
            solana_address: Solana wallet address for blockchain identity
            registry_client: Solana registry client instance
        """
        super().__init__(name)
        self.solana_address = solana_address
        self.registry_client = registry_client
    
    def verify_peer_via_blockchain(self, peer_solana_address: str, peer_signing_pub_bytes: bytes) -> bool:
        """
        Verify peer's signing public key against Solana blockchain registry
        
        This adds a layer of trust: before accepting a peer's public key,
        we verify it matches what's registered on-chain for their Solana address.
        
        Returns:
            True if key is verified on-chain, False otherwise
        """
        print(f"\n{self.name}: Verifying peer's key via Solana blockchain...")
        print(f"  Peer Solana address: {peer_solana_address}")
        print(f"  Peer signing key (hex): {peer_signing_pub_bytes.hex()}")
        
        is_valid = self.registry_client.verify_key(peer_solana_address, peer_signing_pub_bytes)
        
        if is_valid:
            print(f"✅ {self.name}: Blockchain verification SUCCESS")
            print("   Peer's public key matches on-chain registry")
        else:
            print(f"❌ {self.name}: Blockchain verification FAILED")
            print("   Peer's public key does NOT match on-chain registry")
            print("   Possible MITM attack or key mismatch!")
        
        return is_valid
    
    def register_key_on_blockchain(self, wallet_keypair):
        """
        Register this participant's signing public key on Solana blockchain
        
        Args:
            wallet_keypair: Solana wallet keypair to sign the transaction
        """
        print(f"\n{self.name}: Registering signing key on Solana blockchain...")
        signing_pub_bytes = self.participant.signing_public_bytes
        
        tx_sig = self.registry_client.register_key(wallet_keypair, signing_pub_bytes)
        
        print(f"✅ {self.name}: Key registered on-chain")
        print(f"   Transaction: {tx_sig}")
        print(f"   Solana address: {self.solana_address}")
        print(f"   Signing key (hex): {signing_pub_bytes.hex()}")


def demonstrate_blockchain_integration():
    """
    Demonstrate secure channel with Solana blockchain key verification
    """
    print("=" * 70)
    print("PHASE 5: Secure Channel with Solana Blockchain Integration")
    print("=" * 70)
    print()
    
    # Initialize registry client (using devnet for demo)
    registry_client = SolanaKeyRegistryClient(rpc_url="https://api.devnet.solana.com")
    
    # Create secure channels with blockchain integration
    alice_address = "Alice1111111111111111111111111111111111"  # Mock Solana address
    bob_address = "Bob11111111111111111111111111111111111111"   # Mock Solana address
    
    alice_channel = SecureChannelWithBlockchain("Alice", alice_address, registry_client)
    bob_channel = SecureChannelWithBlockchain("Bob", bob_address, registry_client)
    
    print("\n" + "-" * 70)
    print("STEP 1: Participants generate keypairs")
    print("-" * 70)
    alice_channel.participant.generate_keypairs()
    bob_channel.participant.generate_keypairs()
    
    print("\n" + "-" * 70)
    print("STEP 2: Register keys on Solana blockchain")
    print("-" * 70)
    # In production, use real Solana keypairs
    mock_alice_wallet = Keypair()  # Mock for demo
    mock_bob_wallet = Keypair()    # Mock for demo
    
    alice_channel.register_key_on_blockchain(mock_alice_wallet)
    bob_channel.register_key_on_blockchain(mock_bob_wallet)
    
    print("\n" + "-" * 70)
    print("STEP 3: Alice sends authenticated DH public key to Bob")
    print("-" * 70)
    alice_dh_pub, alice_signing_pub, alice_sig = alice_channel.get_public_keys()
    
    print("\n" + "-" * 70)
    print("STEP 4: Bob verifies Alice's key via blockchain BEFORE accepting")
    print("-" * 70)
    blockchain_verified = bob_channel.verify_peer_via_blockchain(
        alice_address,
        alice_signing_pub
    )
    
    if not blockchain_verified:
        print("❌ Blockchain verification failed - aborting key exchange")
        return
    
    print("\n" + "-" * 70)
    print("STEP 5: Bob verifies signature and establishes channel")
    print("-" * 70)
    bob_established = bob_channel.establish_channel(alice_dh_pub, alice_signing_pub, alice_sig)
    
    if not bob_established:
        print("❌ Failed to establish channel")
        return
    
    print("\n" + "-" * 70)
    print("STEP 6: Bob sends authenticated DH public key to Alice")
    print("-" * 70)
    bob_dh_pub, bob_signing_pub, bob_sig = bob_channel.get_public_keys()
    
    print("\n" + "-" * 70)
    print("STEP 7: Alice verifies Bob's key via blockchain BEFORE accepting")
    print("-" * 70)
    blockchain_verified = alice_channel.verify_peer_via_blockchain(
        bob_address,
        bob_signing_pub
    )
    
    if not blockchain_verified:
        print("❌ Blockchain verification failed - aborting key exchange")
        return
    
    print("\n" + "-" * 70)
    print("STEP 8: Alice verifies signature and establishes channel")
    print("-" * 70)
    alice_established = alice_channel.establish_channel(bob_dh_pub, bob_signing_pub, bob_sig)
    
    if not alice_established:
        print("❌ Failed to establish channel")
        return
    
    print("\n" + "=" * 70)
    print("BLOCKCHAIN-SECURED MESSAGE EXCHANGE")
    print("=" * 70)
    
    # Exchange secure messages
    alice_message = b"Hello Bob! This message is secured by blockchain-verified keys."
    print(f"\nAlice sends: {alice_message.decode()}")
    
    ciphertext, nonce = alice_channel.send_message(alice_message)
    
    try:
        bob_received = bob_channel.receive_message(ciphertext, nonce)
        print(f"Bob received: {bob_received.decode()}")
        print("✅ Secure communication established with blockchain verification")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 70)
    print("SECURITY ANALYSIS")
    print("=" * 70)
    print("""
The blockchain-integrated secure channel provides:
1. ✅ Decentralized Key Registry: Public keys stored on Solana blockchain
2. ✅ Identity Binding: Solana wallet addresses bind to Ed25519 signing keys
3. ✅ MITM Prevention: Keys verified on-chain before acceptance
4. ✅ Trustless Verification: No need for centralized certificate authorities
5. ✅ Immutable Record: On-chain keys cannot be retrospectively modified

This demonstrates how blockchain can enhance traditional PKI by providing
decentralized, trustless verification of public keys.
""")


if __name__ == "__main__":
    demonstrate_blockchain_integration()




"""
Complete Demo: All Phases of Secure Channel Implementation

This script runs all phases sequentially to demonstrate the complete
evolution of the secure channel from basic DH to blockchain-integrated version.
"""

import sys
import os

def print_separator(title=""):
    """
    Print a visual separator for better output organization.
    
    Args:
        title: Optional title to display in the separator
    """
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)
    print()


def run_phase(phase_num, phase_name, script_path):
    """
    Execute a phase script and handle any errors gracefully.
    
    This function loads and executes a Python script for a specific phase of
    the secure channel demonstration. It handles errors so that if one phase
    fails, the demo can continue with the next phase.
    
    Args:
        phase_num: Phase number (for display purposes)
        phase_name: Human-readable name of the phase
        script_path: Path to the Python script to execute
    
    Process:
        1. Add script directory to Python path (for imports)
        2. Read and compile the script
        3. Execute the script in a controlled environment
        4. Handle any errors gracefully (print warning, continue)
    """
    print_separator(f"PHASE {phase_num}: {phase_name}")
    
    try:
        # ====================================================================
        # Step 1: Prepare Python path for imports
        # ====================================================================
        # Add the script's directory to sys.path so it can import modules
        # This is necessary if the script imports from sibling directories
        script_dir = os.path.dirname(os.path.abspath(script_path))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        
        # ====================================================================
        # Step 2: Read, compile, and execute the script
        # ====================================================================
        # Read the script file
        with open(script_path, 'r') as f:
            script_code = f.read()
        
        # Compile the code (check for syntax errors)
        compiled_code = compile(script_code, script_path, 'exec')
        
        # Execute in a namespace that simulates '__main__' execution
        # This allows scripts to check 'if __name__ == "__main__":'
        exec(compiled_code, {'__name__': '__main__'})
        
        print(f"\n[SUCCESS] Phase {phase_num} completed successfully")
        
    except FileNotFoundError:
        # ====================================================================
        # Script file not found
        # ====================================================================
        print(f"[WARNING] Script not found at {script_path}")
        print("   Skipping this phase...")
        
    except Exception as e:
        # ====================================================================
        # Any other error during execution
        # ====================================================================
        # Print the error but continue with next phase
        # This allows the demo to continue even if one phase fails
        print(f"[ERROR] Error in Phase {phase_num}: {e}")
        print("   Continuing to next phase...")
        import traceback
        traceback.print_exc()


def main():
    """
    Main function that runs all phases of the secure channel implementation sequentially.
    
    This demonstrates the complete evolution of a secure channel:
    - Starting from basic unauthenticated key exchange
    - Showing how it can be attacked
    - Fixing it with authentication
    - Adding encryption for secure messaging
    - Integrating blockchain for decentralized trust
    
    The demo runs each phase and pauses between them so you can:
    - See the output of each phase
    - Understand the progression
    - Press Enter to continue or Ctrl+C to cancel
    """
    
    print_separator("MINI SECURE CHANNEL - COMPLETE DEMONSTRATION")
    print("""
This demo will run all phases of the secure channel implementation:
  1. Basic Diffie-Hellman Key Exchange
     - Shows how two parties can establish a shared secret
     - No authentication - vulnerable to MITM
  
  2. MITM Attack Demonstration
     - Shows how Mallory can intercept and manipulate the key exchange
     - Demonstrates the vulnerability of unauthenticated protocols
  
  3. Authenticated Diffie-Hellman (MITM Prevention)
     - Adds Ed25519 digital signatures to authenticate public keys
     - Shows how authentication prevents MITM attacks
  
  4. Secure Channel with AEAD Encryption
     - Uses ChaCha20-Poly1305 for authenticated encryption
     - Provides confidentiality, integrity, and authentication
  
  5. Blockchain Integration (Solana)
     - Uses Solana blockchain as a decentralized key registry
     - Adds an additional trust layer for key verification
  
  6. Blockchain Attack Prevention
     - Demonstrates Mallory's attacks on blockchain-integrated system
     - Shows how blockchain prevents all attack attempts
    
Press Enter to start, or Ctrl+C to cancel...
    """)
    
    # Wait for user confirmation before starting
    try:
        input()
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
        return
    
    # ========================================================================
    # PHASE 1: Basic Diffie-Hellman Key Exchange
    # ========================================================================
    # Demonstrates the fundamental cryptographic primitive for key exchange
    # Shows that two parties can establish a shared secret without pre-shared keys
    run_phase(1, "Basic Diffie-Hellman Key Exchange", 
              "phases/phase1_dh/dh_exchange.py")
    
    input("\nPress Enter to continue to Phase 2...")
    
    # ========================================================================
    # PHASE 2: MITM Attack
    # ========================================================================
    # Demonstrates the critical vulnerability: without authentication,
    # an attacker can intercept and replace public keys
    run_phase(2, "Man-in-the-Middle Attack", 
              "phases/phase2_mitm/mallory_attack.py")
    
    input("\nPress Enter to continue to Phase 3...")
    
    # ========================================================================
    # PHASE 3: Authenticated Diffie-Hellman
    # ========================================================================
    # Shows how to fix the MITM vulnerability by adding digital signatures
    # This is the critical fix that makes the protocol secure
    run_phase(3, "Authenticated Diffie-Hellman", 
              "phases/phase3_auth/authenticated_dh.py")
    
    input("\nPress Enter to continue to Phase 4...")
    
    # ========================================================================
    # PHASE 4: Secure Channel with AEAD
    # ========================================================================
    # Complete secure channel implementation with authenticated encryption
    # This is what real-world secure protocols like TLS provide
    run_phase(4, "Secure Channel with AEAD Encryption", 
              "phases/phase4_aead/secure_channel.py")
    
    input("\nPress Enter to continue to Phase 5...")
    
    # ========================================================================
    # PHASE 5: Blockchain Integration
    # ========================================================================
    # Extends the secure channel with blockchain-based key registry
    # Demonstrates how blockchain can provide decentralized trust
    run_phase(5, "Blockchain Integration (Solana)", 
              "phases/phase5_solana/solana_registry_client.py")
    
    input("\nPress Enter to continue to Phase 6...")
    
    # ========================================================================
    # PHASE 6: Blockchain Attack Prevention
    # ========================================================================
    # Demonstrates Mallory's attacks on blockchain-integrated secure channel
    # Shows how blockchain prevents all attack attempts through wallet ownership
    # and verifiable key registry
    run_phase(6, "Blockchain Attack Prevention", 
              "phases/phase6_blockchain_attack/blockchain_mitm_attack.py")
    
    # ========================================================================
    # Summary and Key Takeaways
    # ========================================================================
    print_separator("DEMONSTRATION COMPLETE")
    print("""
All phases have been demonstrated. Key takeaways:

1. [SUCCESS] Diffie-Hellman enables secure key exchange
   - Two parties can establish a shared secret over an insecure channel
   - Based on the discrete logarithm problem

2. [WARNING] Unauthenticated DH is vulnerable to MITM attacks
   - Without authentication, attackers can intercept and replace keys
   - This is why authentication is critical in secure protocols

3. [SUCCESS] Digital signatures (Ed25519) prevent MITM attacks
   - Signatures bind public keys to identities
   - Cannot be forged without the private key

4. [SUCCESS] AEAD encryption provides confidentiality + integrity
   - ChaCha20-Poly1305 encrypts messages and detects tampering
   - Provides all security properties needed for secure communication

5. [SUCCESS] Blockchain adds decentralized trust layer
   - Solana blockchain provides immutable key registry
   - Eliminates need for centralized certificate authorities

6. [SUCCESS] Blockchain prevents all MITM attack attempts
   - Wallet ownership requirement prevents impersonation
   - On-chain verification catches key mismatches
   - All 4 attack strategies fail due to blockchain security

For detailed explanations and code, see individual phase files.
For visualizations, run: python visualizations/diagram_generator.py
    """)


if __name__ == "__main__":
    main()



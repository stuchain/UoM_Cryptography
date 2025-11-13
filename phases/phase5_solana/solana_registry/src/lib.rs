use anchor_lang::prelude::*;

declare_id!("KeyRegistry11111111111111111111111111111");

#[program]
pub mod key_registry {
    use super::*;

    /// Register a public key for a user
    /// 
    /// This function allows a user to register their Ed25519 public key
    /// on-chain. The public key is stored as a 32-byte array (Ed25519 format).
    /// 
    /// # Arguments
    /// * `ctx` - Context containing the user's account and PDA
    /// * `public_key` - The Ed25519 public key (32 bytes)
    pub fn register_key(ctx: Context<RegisterKey>, public_key: [u8; 32]) -> Result<()> {
        let key_record = &mut ctx.accounts.key_record;
        key_record.owner = ctx.accounts.owner.key();
        key_record.public_key = public_key;
        key_record.bump = ctx.bumps.key_record;
        
        msg!("Registered public key for user: {}", ctx.accounts.owner.key());
        msg!("Public key (hex): {:02x?}", public_key);
        
        Ok(())
    }

    /// Update an existing public key registration
    /// 
    /// Allows the owner to update their registered public key.
    /// 
    /// # Arguments
    /// * `ctx` - Context containing the user's account and PDA
    /// * `new_public_key` - The new Ed25519 public key (32 bytes)
    pub fn update_key(ctx: Context<UpdateKey>, new_public_key: [u8; 32]) -> Result<()> {
        let key_record = &mut ctx.accounts.key_record;
        
        // Verify the signer is the owner
        require_keys_eq!(
            key_record.owner,
            ctx.accounts.owner.key(),
            KeyRegistryError::Unauthorized
        );
        
        key_record.public_key = new_public_key;
        
        msg!("Updated public key for user: {}", ctx.accounts.owner.key());
        msg!("New public key (hex): {:02x?}", new_public_key);
        
        Ok(())
    }

    /// Verify if a public key matches the registered key for a user
    /// 
    /// This is a view function that checks if the provided public key
    /// matches what's registered on-chain for the given user.
    /// 
    /// # Arguments
    /// * `ctx` - Context containing the key record PDA
    /// * `public_key_to_verify` - The public key to verify (32 bytes)
    pub fn verify_key(ctx: Context<VerifyKey>, public_key_to_verify: [u8; 32]) -> Result<bool> {
        let key_record = &ctx.accounts.key_record;
        let matches = key_record.public_key == public_key_to_verify;
        
        if matches {
            msg!("✅ Public key matches registered key for user: {}", key_record.owner);
        } else {
            msg!("❌ Public key does NOT match registered key for user: {}", key_record.owner);
        }
        
        Ok(matches)
    }
}

#[derive(Accounts)]
#[instruction(public_key: [u8; 32])]
pub struct RegisterKey<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,
    
    #[account(
        init,
        payer = owner,
        space = 8 + KeyRecord::LEN,
        seeds = [b"key_record", owner.key().as_ref()],
        bump
    )]
    pub key_record: Account<'info, KeyRecord>,
    
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(new_public_key: [u8; 32])]
pub struct UpdateKey<'info> {
    #[account(mut)]
    pub owner: Signer<'info>,
    
    #[account(
        mut,
        seeds = [b"key_record", owner.key().as_ref()],
        bump = key_record.bump,
        has_one = owner @ KeyRegistryError::Unauthorized
    )]
    pub key_record: Account<'info, KeyRecord>,
}

#[derive(Accounts)]
#[instruction(public_key_to_verify: [u8; 32])]
pub struct VerifyKey<'info> {
    #[account(
        seeds = [b"key_record", key_record.owner.as_ref()],
        bump = key_record.bump
    )]
    pub key_record: Account<'info, KeyRecord>,
}

#[account]
pub struct KeyRecord {
    pub owner: Pubkey,           // 32 bytes - the user's Solana wallet address
    pub public_key: [u8; 32],     // 32 bytes - Ed25519 public key
    pub bump: u8,                 // 1 byte - PDA bump seed
}

impl KeyRecord {
    pub const LEN: usize = 32 + 32 + 1; // owner + public_key + bump
}

#[error_code]
pub enum KeyRegistryError {
    #[msg("Unauthorized: You are not the owner of this key record")]
    Unauthorized,
}




import sympy

# Step 1: Choose two distinct prime numbers p and q
p = 61
q = 53

# Step 2: Compute n
n = p * q

# Step 3: Compute Euler's totient function phi(n)
phi_n = (p - 1) * (q - 1)

# Step 4: Choose an integer e such that 1 < e < phi(n) and gcd(e, phi(n)) = 1
e = 17

# Step 5: Compute d, the modular multiplicative inverse of e mod phi(n)
d = pow(e, -1, phi_n)

# Public and private keys
public_key = (e, n)
private_key = (d, n)

print("Public Key:", public_key)
print("Private Key:", private_key)

# Function to split a message into blocks
def split_message(message, block_size):
    message_str = str(message)
    blocks = [int(message_str[i:i+block_size]) for i in range(0, len(message_str), block_size)]
    return blocks

# Function to join blocks into a message
def join_blocks(blocks):
    message_str = ''.join(str(block).zfill(3) for block in blocks)
    return int(message_str)

# Example message
plaintext = 422256567432  # Example plaintext message

# Split the message into blocks
block_size = len(str(n)) - 1  # Ensure blocks are smaller than n
blocks = split_message(plaintext, block_size)
print("Blocks:", blocks)

# Encrypt each block
ciphertext_blocks = [pow(block, e, n) for block in blocks]
print("Encrypted blocks:", ciphertext_blocks)

# Decrypt each block
decrypted_blocks = [pow(block, d, n) for block in ciphertext_blocks]
print("Decrypted blocks:", decrypted_blocks)

# Join decrypted blocks into the original message
decrypted_message = join_blocks(decrypted_blocks)
print("Decrypted message:", decrypted_message)

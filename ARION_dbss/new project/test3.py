import pandas as pd
import sympy as sp

# Step 1: Ask for the encrypted data
def get_encrypted_data():
    while True:
        encrypted_data_with_key = input("Enter the encrypted data with the public key: ")
        if encrypted_data_with_key.isdigit() and len(encrypted_data_with_key) > 4:
            return encrypted_data_with_key
        else:
            print("Invalid input. Please enter the encrypted data with the public key.")

encrypted_data_with_key = get_encrypted_data()
public_key = int(encrypted_data_with_key[-4:])
encrypted_data = int(encrypted_data_with_key[:-4])

print(f"Encrypted data: {encrypted_data}")
print(f"Public key: {public_key}")

# Step 2: Verify the public key against the Excel sheet
df = pd.read_excel('keys.xlsx')

if public_key in df['Public Key'].values:
    private_key = df.loc[df['Public Key'] == public_key, 'Private Key'].values[0]
    print(f"Retrieved private key: {private_key}")
else:
    print("Public key verification failed.")
    exit()

# Step 3: Decrypt the data using the cubic equation
# Assuming the coefficients of the original cubic equation were stored during encryption
a = 6521
b = 7700
c = 464
d = 7090

# Define the cubic equation in terms of the private key (x)
x = sp.symbols('x')
cubic_eq = a*x**3 + b*x**2 + c*x + d - encrypted_data

# Solve the cubic equation
solutions = sp.solve(cubic_eq, x)
real_solutions = [sol.evalf() for sol in solutions if sol.is_real]

if not real_solutions:
    print("No real solutions found for the cubic equation.")
else:
    decrypted_x = real_solutions[0]
    print(f"Decrypted private key (x): {decrypted_x}")

    # Verify that the decrypted private key matches the stored private key
    if int(round(decrypted_x)) == private_key:
        print("Private key verification successful.")
        
        # Calculate the original parts a, b, c, d using decrypted private key
        original_a = int(a / private_key**3)
        original_b = int(b / private_key**2)
        original_c = int(c / private_key)
        original_d = d  # d remains the same
        
        # Combine the original parts to get the decrypted message
        decrypted_message = f"{original_a:04d}{original_b:04d}{original_c:04d}{original_d:04d}"
        print(f"Decrypted message: {decrypted_message}")
    else:
        print("Private key verification failed.")

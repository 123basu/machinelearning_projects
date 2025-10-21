import random
import pandas as pd
import openpyxl

# Step 1: Input the 16-digit number
def get_input_number():
    while True:
        number = input("Enter a 16-digit number: ")
        if len(number) == 16 and number.isdigit():
            return number
        else:
            print("Invalid input. Please enter a 16-digit number.")

number = get_input_number()

# Step 2: Break the 16-digit number into 4 parts
a = int(number[:4])
b = int(number[4:8])
c = int(number[8:12])
d = int(number[12:])

print(f"Parts: a={a}, b={b}, c={c}, d={d}")

# Step 3: Generate a random private key and store it in an Excel file
private_key = random.randint(1000, 9999)

# Create a DataFrame to store keys
data = {
    'Private Key': [private_key],
    'Public Key': [None]  # Placeholder for public key
}

# Save to Excel
df = pd.DataFrame(data)
df.to_excel('keys.xlsx', index=False)

print(f"Generated private key: {private_key}")

# Step 4: Apply the equation ax^3 + bx^2 + cx + d
encrypted_data = a*private_key**3 + b*private_key**2 + c*private_key + d
print(f"Encrypted data: {encrypted_data}")

# Step 5: Add a 4-digit public key and store both keys in the Excel file
public_key = random.randint(1000, 9999)
encrypted_data_with_key = f"{encrypted_data}{public_key}"

# Update the Excel file with the public key
df['Public Key'] = public_key
df.to_excel('keys.xlsx', index=False)

print(f"Public key added: {public_key}")
print(f"Encrypted data with public key: {encrypted_data_with_key}")

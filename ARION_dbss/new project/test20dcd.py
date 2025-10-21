import pandas as pd
import os
import json

# Load the symbols and letters dataset from JSON file
def load_symbol_to_number_mapping(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    symbol_to_number = {}
    if isinstance(data, dict):
        for number, symbols in data.items():
            for symbol in symbols:
                symbol_to_number[symbol] = number
    elif isinstance(data, list):
        for item in data:
            for number, symbols in item.items():
                for symbol in symbols:
                    symbol_to_number[symbol] = number
    else:
        raise ValueError("Unexpected JSON structure")

    return symbol_to_number

# Step 1: Ask for the encrypted data with the public key
def get_encrypted_data():
    while True:
        encrypted_data_with_key = input("Enter the encrypted data with the public key: ")
        if ',' in encrypted_data_with_key:
            return encrypted_data_with_key
        else:
            print("Invalid input. Please enter the encrypted data with the public key.")

# Step 2: Ask for the token number
def get_token_number():
    while True:
        token_number = input("Enter the token number: ")
        if token_number.isdigit():
            return int(token_number)
        else:
            print("Invalid input. Please enter a valid token number.")

# Convert symbols to numbers
def convert_to_numbers(symbol_str, symbol_to_number):
    return ''.join(symbol_to_number.get(symbol, '?') for symbol in symbol_str.split())

# Main function
def main():
    # Load the symbols and letters dataset
    file_path = r'D:\6 sem mini project_new\number_to_char_mapping.json'
    symbol_to_number = load_symbol_to_number_mapping(file_path)

    # Retrieve the encrypted data and token number
    encrypted_data_with_key = get_encrypted_data()
    token_number = get_token_number()
    parts = encrypted_data_with_key.split(',')
    combined_encrypted = parts[0].strip()
    lengths_with_symbols = parts[1].strip()
    public_key_with_symbols = parts[2].strip()
    token_number = int(parts[3].strip())

    print(f"Combined encrypted data: {combined_encrypted}")
    print(f"Lengths: {lengths_with_symbols}")
    print(f"Public key (symbols): {public_key_with_symbols}")
    print(f"Token number: {token_number}")

    # Convert each part and print intermediate results for debugging
    combined_encrypted_numbers = convert_to_numbers(combined_encrypted, symbol_to_number)
    print(f"Combined encrypted numbers: {combined_encrypted_numbers}")

    lengths_numbers = [symbol_to_number.get(symbol, '?') for symbol in lengths_with_symbols.split()]
    print(f"Lengths numbers: {lengths_numbers}")

    public_key_numbers = convert_to_numbers(public_key_with_symbols, symbol_to_number)
    print(f"Public key numbers: {public_key_numbers}")

    # Ensure all symbols were correctly mapped, otherwise handle the error
    if '?' in combined_encrypted_numbers or '?' in public_key_numbers or '?' in lengths_numbers:
        print("Error: Unrecognized symbols found during decryption. Please check the input.")
        print("Unrecognized symbols debug info:")
        if '?' in combined_encrypted_numbers:
            print(f"Unrecognized symbol in combined_encrypted: {combined_encrypted}")
        if '?' in public_key_numbers:
            print(f"Unrecognized symbol in public_key_numbers: {public_key_with_symbols}")
        if '?' in lengths_numbers:
            print(f"Unrecognized symbol in lengths_numbers: {lengths_with_symbols}")
        return

    # Convert lengths back to integers
    len_a = int(''.join(map(str, lengths_numbers[:2])))
    len_b = int(''.join(map(str, lengths_numbers[2:4])))
    len_c = int(''.join(map(str, lengths_numbers[4:6])))
    len_d = int(''.join(map(str, lengths_numbers[6:])))
    public_key = int(public_key_numbers)

    print(f"Extracted lengths - len_a: {len_a}, len_b: {len_b}, len_c: {len_c}, len_d: {len_d}")
    print(f"Extracted public key: {public_key}")

    # Extract encrypted parts using lengths
    start = 0
    encrypted_a = int(combined_encrypted_numbers[start:start + len_a])
    start += len_a
    encrypted_b = int(combined_encrypted_numbers[start:start + len_b])
    start += len_b
    encrypted_c = int(combined_encrypted_numbers[start:start + len_c])
    start += len_c
    encrypted_d = int(combined_encrypted_numbers[start:start + len_d])

    print(f"Encrypted data parts: {encrypted_a}, {encrypted_b}, {encrypted_c}, {encrypted_d}")

    # Step 4: Verify the token number and public key against the Excel sheet
    keys_file_path = r'D:\6 sem mini project_new\keys.xlsx'
    if not os.path.exists(keys_file_path):
        print("keys.xlsx file not found. Exiting.")
        return

    df = pd.read_excel(keys_file_path)

    # Verify token number and public key
    if token_number in df['Token Number'].values:
        row = df.loc[df['Token Number'] == token_number]
        if public_key == row['Public Key'].values[0]:
            private_key = row['Private Key'].values[0]
            print(f"Retrieved private key: {private_key}")
        else:
            print("Public key verification failed.")
            return
    else:
        print("Token number verification failed.")
        return

    # Step 5: Reverse the mathematical operations to get the original parts
    n = 1000  # Match the modulus used in encryption

    decrypted_a = (encrypted_a - n**4) // private_key**4
    decrypted_b = (encrypted_b - n**3) // private_key**3
    decrypted_c = (encrypted_c - n**2) // private_key**2
    decrypted_d = (encrypted_d - n)

    # Combine the decrypted parts to form the original 16-digit number
    decrypted_message = f"{decrypted_a:04d}{decrypted_b:04d}{decrypted_c:04d}{decrypted_d:04d}"
    print(f"Decrypted message: {decrypted_message}")

if __name__ == "__main__":
    main()

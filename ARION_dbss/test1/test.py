import requests
import json
import os

# Define the Flask server URL
BASE_URL = "http://127.0.0.1:5000"

# Function to read file content
def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

# Function to write file content
def write_file(file_path, data):
    with open(file_path, 'wb') as f:
        f.write(data)

# Function to encrypt file content
def encrypt_file(data):
    url = f"{BASE_URL}/encrypt"
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"data": data.decode('latin1')})
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()["token"]
    else:
        print("Failed to encrypt file")
        print(response.text)
        return None

# Function to decrypt file content
def decrypt_file(token):
    url = f"{BASE_URL}/decrypt"
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"token": token})
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        return response.json()["data"].encode('latin1')
    else:
        print("Failed to decrypt file")
        print(response.text)
        return None

def main():
    # Get the input file path from the user
    input_file_path = input("Enter the path of the file to encrypt: ")

    # Check if the file exists
    if not os.path.exists(input_file_path):
        print("File does not exist. Please check the file path and try again.")
        return

    # Read the content of the input file
    print("Reading input file...")
    file_content = read_file(input_file_path)
    
    print("Encrypting file...")
    token = encrypt_file(file_content)
    
    if token:
        print(f"File encrypted successfully. Token: {token}")
        
        # Save the encrypted file (this step is optional since the Flask app saves the encrypted file)
        encrypted_file_path = os.path.join('storage', f"{token}.enc")
        write_file(encrypted_file_path, file_content)
        
        # Get the output file path from the user for decrypted content
        decrypted_file_path = input("Enter the path to save the decrypted file: ")
        
        print("Decrypting file...")
        decrypted_data = decrypt_file(token)
        
        if decrypted_data:
            print("File decrypted successfully.")
            
            # Write the decrypted content to the output file
            write_file(decrypted_file_path, decrypted_data)
            
            # Verify that the decrypted content matches the original content
            if decrypted_data == file_content:
                print("Success: The decrypted content matches the original content!")
            else:
                print("Error: The decrypted content does not match the original content.")
        else:
            print("Decryption failed.")
    else:
        print("Encryption failed.")

if __name__ == "__main__":
    main()

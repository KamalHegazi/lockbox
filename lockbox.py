import os
import argparse
import pyperclip
from cryptography.fernet import Fernet
import random

# Function to generate a new encryption key
def generate_key():
    # Generate a new key using Fernet
    return Fernet.generate_key()

# Function to load an existing key from a file
def load_key(key_file):
    try:
        # Open the key file in binary read mode
        with open(key_file, "rb") as file:
            # Read and return the key
            return file.read()
    except FileNotFoundError:
        # Handle the case where the key file does not exist
        print(f"Key file {key_file} not found.")
        return None

# Function to save a key to a file
def save_key(key, key_file):
    # Open the key file in binary write mode
    with open(key_file, "wb") as file:
        # Write the key to the file
        file.write(key)

# Function to add salt to data at a random position
def add_salt(data, salt):
    # Generate a random position within the data
    position = random.randint(0, len(data))
    # Insert the salt at the random position
    return data[:position] + salt.encode() + data[position:]

# Function to remove salt from data
def remove_salt(data, salt):
    # Remove the first occurrence of the salt from the data
    return data.replace(salt.encode(), b'', 1)

# Function to encrypt a file with a given key and salt
def encrypt_file(file_path, key, salt):
    try:
        # Create a Fernet object with the provided key
        fernet = Fernet(key)
        # Open the file to encrypt in binary read mode
        with open(file_path, "rb") as file:
            # Read the file data
            file_data = file.read()
        # Add salt to the file data
        salted_data = add_salt(file_data, salt)
        # Encrypt the salted data
        encrypted_data = fernet.encrypt(salted_data)
        # Open the file in binary write mode to save the encrypted data
        with open(file_path, "wb") as file:
            # Write the encrypted data to the file
            file.write(encrypted_data)
        print(f"File {file_path} encrypted successfully.")
    except Exception as e:
        # Handle any exceptions that occur during encryption
        print(f"Error encrypting file: {e}")

# Function to decrypt a file with a given key and salt
def decrypt_file(file_path, key, salt):
    try:
        # Create a Fernet object with the provided key
        fernet = Fernet(key)
        # Open the file to decrypt in binary read mode
        with open(file_path, "rb") as file:
            # Read the encrypted data from the file
            encrypted_data = file.read()
        # Decrypt the data
        decrypted_data = fernet.decrypt(encrypted_data)
        # Remove the salt from the decrypted data
        unsalted_data = remove_salt(decrypted_data, salt)
        # Copy the unsalted data to the clipboard
        pyperclip.copy(unsalted_data.decode())
        print(f"File {file_path} decrypted and copied to clipboard.")
    except Exception as e:
        # Handle any exceptions that occur during decryption
        print(f"Error decrypting file: {e}")

# Main function to handle command-line arguments and perform encryption/decryption
def main():
    # Create an argument parser for command-line arguments
    parser = argparse.ArgumentParser(description="Encrypt or decrypt files.")
    # Add arguments for action (encrypt/decrypt) and file path
    parser.add_argument("action", choices=["encrypt", "decrypt"], help="Action to perform")
    parser.add_argument("file", help="File to encrypt or decrypt")
    # Add an optional argument for the key file, with a default value
    parser.add_argument("--key", help="Key file to use for encryption/decryption", default="secret.key")
    # Parse the command-line arguments
    args = parser.parse_args()

    # Prompt the user to enter the salt string
    salt = input("[?] Enter the salt string: ")

    if args.action == "encrypt":
        key_file = args.key
        if os.path.exists(key_file):
            # Load the existing key from the key file
            key = load_key(key_file)
            if key is None:
                return
            print(f"Using existing key from {key_file}")
        else:
            # Generate a new key and save it to the key file
            key = generate_key()
            save_key(key, key_file)
            print(f"Generated new key and saved to {key_file}")
        # Encrypt the file with the provided key and salt
        encrypt_file(args.file, key, salt)
    elif args.action == "decrypt":
        key_file = args.key
        # Load the existing key from the key file
        key = load_key(key_file)
        if key is None:
            return
        # Decrypt the file with the provided key and salt
        decrypt_file(args.file, key, salt)

# Entry point of the script
if __name__ == "__main__":
    main()

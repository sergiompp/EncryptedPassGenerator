import os
import json
from getpass import getpass
from cryptography.fernet import Fernet
import string
import random

# Function to generate a new password
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Function to load encryption key from a file or generate a new one
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            key = key_file.read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    return key

# Function to encrypt data
def encrypt(data, key):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

# Function to decrypt data
def decrypt(encrypted_data, key):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

# Function to save the new encrypted passwords in a file
def save_passwords(passwords, key):
    encrypted_data = encrypt(json.dumps(passwords), key)
    with open("passwords.enc", "wb") as file:
        file.write(encrypted_data)

# Function to load the new encrypted passwords from a file
def load_passwords(key):
    if os.path.exists("passwords.enc"):
        with open("passwords.enc", "rb") as file:
            encrypted_data = file.read()
        return json.loads(decrypt(encrypted_data, key))
    else:
        return {}

# Main function to manage passwords
def main():
    key = load_key()
    
    master_password = getpass("Enter master password: ")
    confirm_master_password = getpass("Confirm master password: ")
    
    if master_password != confirm_master_password:
        print("Passwords do not match. Exiting.")
        return
    
    passwords = load_passwords(key)
    
    while True:
        print("\nOptions:")
        print("1. Generate a new password")
        print("2. View all passwords")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            account = input("Enter the account name: ")
            length = int(input("Enter the desired password length: "))
            password = generate_password(length)
            passwords[account] = password
            save_passwords(passwords, key)
            print(f"Generated password for {account}: {password}")
        
        elif choice == "2":
            for account, password in passwords.items():
                print(f"Account: {account} - Password: {password}")
        
        elif choice == "3":
            break
        
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()

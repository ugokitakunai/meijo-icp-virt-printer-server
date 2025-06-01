from cryptography.fernet import Fernet
import win32crypt
import os

def create_secret():
    key = Fernet.generate_key()
    return key

def encrypt_secret(key):
    encrypted_key = win32crypt.CryptProtectData(
        key,   # data
        None,  # description
        None,  # entropy
        None,  # reserved
        None,  # prompt struct
        0      # flags
    )
    return encrypted_key

def main():
    key = create_secret()
    encrypted_key = encrypt_secret(key)

    if os.path.exists("fernet_key.dat"):
        return # 鍵をこわさないように大切に...！

    with open("fernet_key.dat", "wb") as f:
        f.write(encrypted_key)

if __name__ == "__main__":
    main()

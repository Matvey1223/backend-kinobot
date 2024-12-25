from cryptography.fernet import Fernet

SECRET_KEY = Fernet.generate_key()
cipher = Fernet(SECRET_KEY)

def encrypt_url(url: str) -> str:
    return cipher.encrypt(url.encode()).decode()

def decrypt_url(encrypted_url: str) -> str:
    return cipher.decrypt(encrypted_url.encode()).decode()

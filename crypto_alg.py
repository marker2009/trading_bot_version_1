from cryptography.fernet import Fernet


def load_key():
    # Загружаем ключ 'crypto.key' из текущего каталога
    return open('crypto.key', 'rb').read()


def encrypt(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data)
    return  encrypted_data


def decrypt(data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(data)
    return decrypted_data
def unlock_data(data):
    return decrypt(data.encode(), k).decode()
def lock_data(data):
    return encrypt(data.encode(), k).decode()

k = load_key()

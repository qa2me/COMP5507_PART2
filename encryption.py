import os

from key_generation import generate_keys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# RSA لوحده ما يقدر يشفر ملفات كبيرة (max 190 bytes), فنسوي hybrid:
# ملف = AES-GCM (سريع وبدون حد للحجم), والمفتاح الصغير = RSA.
NONCE_SIZE = 12


def encrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    # مفتاح AES عشوائي كل مرة، وهو اللي يشفر الملف نفسه
    aes_key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = AESGCM(aes_key).encrypt(nonce, plaintext, None)

    # RSA يستخدم بس عشان يشفر مفتاح AES (32 bytes فقط) بـ public key تاع Bob
    encrypted_aes_key = key.encrypt(aes_key,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))

    # شكل الملف بعد التشفير: [طول المفتاح][المفتاح المشفر][nonce][الملف المشفر]
    with open(file_path, 'wb') as file:
        file.write(len(encrypted_aes_key).to_bytes(2, 'big') + encrypted_aes_key + nonce + ciphertext)

def decrypt_file(file_path, key):
    with open(file_path, 'rb') as file:
        data = file.read()

    # نرجع نقسم الملف بنفس الترتيب اللي جمعناه فوق
    key_length = int.from_bytes(data[:2], 'big')
    encrypted_aes_key = data[2:2 + key_length]
    nonce = data[2 + key_length:2 + key_length + NONCE_SIZE]
    ciphertext = data[2 + key_length + NONCE_SIZE:]

    # نفك مفتاح AES بالـ private key تاع Bob
    aes_key = key.decrypt(
        encrypted_aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # بعدها نفك الملف بالـ AES (لو المفتاح غلط أو الملف خربان نطلع ValueError)
    try:
        plaintext = AESGCM(aes_key).decrypt(nonce, ciphertext, None)
    except Exception:
        raise ValueError("wrong key or corrupted file")

    with open(file_path, 'wb') as file:
        file.write(plaintext)


if __name__ == "__main__":
    #create a pair of keys for alice and bob (generate_keys returns private first, then public)
    private_of_alice,public_of_alice = generate_keys()
    private_of_bob,public_of_bob = generate_keys()


    #usage of how to use when alice want to send to bob
    encrypt_file('qais.txt', public_of_bob)

    print("File After Encryption:")
    with open('qais.txt', 'rb') as file:
        content = file.read()
        print(content)
    decrypt_file('qais.txt', private_of_bob)

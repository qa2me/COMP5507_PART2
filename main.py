import os

from key_generation import generate_keys
from encryption import encrypt_file, decrypt_file
from signatures import hash_message, sign_file
from verification import verify_message

# keys are kept in memory while the program runs
# Alice = sender (signs), Bob = receiver (decrypts)
keys = {
    "alice_private": None,
    "alice_public": None,
    "bob_private": None,
    "bob_public": None,
}

# the last message Alice signed and its signature (sent to Bob together)
signed = {"message": None, "signature": None}


def keys_ready():
    if keys["alice_private"] is None:
        print("No keys yet. Choose option 1 first.")
        return False
    return True


def ask_for_file():
    path = input("Enter file path: ").strip().strip('"')
    if not os.path.isfile(path):
        print("File not found:", path)
        return None
    return path


# 1. Generate key pair
def menu_generate_keys():
    # note: generate_keys() returns (private, public) in that order
    keys["alice_private"], keys["alice_public"] = generate_keys()
    keys["bob_private"], keys["bob_public"] = generate_keys()
    print("RSA-2048 key pairs generated for Alice and Bob.")
    print("Alice shares her public key with Bob, and Bob shares his public key with Alice.")


# 2. Encrypt message: Alice encrypts with Bob's PUBLIC key
def menu_encrypt():
    if not keys_ready():
        return
    path = ask_for_file()
    if path is None:
        return
    try:
        encrypt_file(path, keys["bob_public"])
        print("File encrypted with Bob's public key. Only Bob's private key can decrypt it.")
    except ValueError:
        print("Encryption failed: RSA-2048 with OAEP can only encrypt up to 190 bytes.")


# 3. Decrypt message: Bob decrypts with his PRIVATE key
def menu_decrypt():
    if not keys_ready():
        return
    path = ask_for_file()
    if path is None:
        return
    try:
        decrypt_file(path, keys["bob_private"])
        print("File decrypted with Bob's private key.")
    except ValueError:
        print("Decryption failed: the file is not encrypted, or it was encrypted with a different key.")


# 4. Sign message: Alice hashes + signs with her PRIVATE key
def menu_sign():
    if not keys_ready():
        return
    print("Enter message:")
    message = input()

    message_hash = hash_message(message)
    print("\nSHA-256 hash:")
    print(message_hash)

    print("\nGenerating digital signature...")
    signature = sign_file(message_hash.encode(), keys["alice_private"])

    print("\nSignature:")
    print(signature.hex())

    signed["message"] = message
    signed["signature"] = signature
    print("\nMessage signed. Choose option 5 to verify it.")


# 5. Verify signature: the user enters the original message and a (possibly modified) one.
#    The original is signed with Alice's PRIVATE key, then the second message is checked
#    against that SAME signature with Alice's PUBLIC key.
def menu_verify():
    if not keys_ready():
        return

    print("Original:")
    original = input()
    print("\nModified:")
    modified = input()

    signature = sign_file(hash_message(original).encode(), keys["alice_private"])

    print("\nOriginal hash: ", hash_message(original))
    print("Modified hash: ", hash_message(modified))

    print("\nSignature verification:")
    if verify_message(modified, signature, keys["alice_public"]):
        print("VALID")
    else:
        print("INVALID")


def main():
    actions = {
        "1": menu_generate_keys,
        "2": menu_encrypt,
        "3": menu_decrypt,
        "4": menu_sign,
        "5": menu_verify,
    }

    while True:
        print("\n===== Public-Key Cryptography =====")
        print("1. Generate key pair")
        print("2. Encrypt message")
        print("3. Decrypt message")
        print("4. Sign message")
        print("5. Verify signature")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "6":
            print("Goodbye.")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("Invalid choice, enter a number from 1 to 6.")


if __name__ == "__main__":
    main()

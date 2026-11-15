# COMP5507 Part 2 — Secure Key Exchange and Message Authentication

A menu-driven Python program that demonstrates public-key cryptography:
key pairs, encryption, decryption, hashing, digital signatures, and signature verification.

The program models two users:

- **Alice**, the sender, who signs messages and encrypts data for Bob
- **Bob**, the receiver, who decrypts data and verifies Alice's signatures

## Requirements

- Python 3.10 or newer (tested with Python 3.13)
- The [`cryptography`](https://pypi.org/project/cryptography/) library

```bash
pip install cryptography
```

## How to run

```bash
python main.py
```

```
===== Public-Key Cryptography =====
1. Generate key pair
2. Encrypt message
3. Decrypt message
4. Sign message
5. Verify signature
6. Exit
```

Choose **option 1 first**. The other options need the keys. Keys are kept in memory only, so they are lost when the program exits.

## Project structure

| File | Purpose |
|---|---|
| `key_generation.py` | `generate_keys()`: creates an RSA-2048 key pair (public exponent 65537) and returns `(private_key, public_key)` |
| `encryption.py` | `encrypt_file()` / `decrypt_file()`: RSA encryption with OAEP padding (SHA-256) |
| `signatures.py` | `hash_file()` / `hash_message()`: SHA-256 hashing; `sign_file()`: signs a hash with RSA (PKCS#1 v1.5, SHA-256) |
| `verification.py` | `verify_signature()`, `verify_file()`, `verify_message()`: check a signature with the sender's public key |
| `main.py` | The interactive menu that connects all modules |

## What each option does

| Option | Action | Key used |
|---|---|---|
| 1. Generate key pair | Creates RSA-2048 key pairs for Alice and Bob | — |
| 2. Encrypt message | Encrypts a file **in place** | Bob's **public** key |
| 3. Decrypt message | Decrypts the file back **in place** | Bob's **private** key |
| 4. Sign message | Hashes a typed message with SHA-256 and signs the hash | Alice's **private** key |
| 5. Verify signature | Signs an original file, then verifies a second file against that signature | Alice's **public** key |
| 6. Exit | Closes the program | — |

## Example runs

### Signing a message (option 4)

```
Enter message:
Transfer report.pdf

SHA-256 hash:
fb3a4807ab64ac2562624e9972f1dd6a35a73aa2a39ab23dc80deefbb2e4bb0d

Generating digital signature...

Signature:
530620fec9588bfc819ba9bf26f64b8f...   (256-byte RSA signature in hex)
```

### Detecting a modified file (option 5)

`original.txt` contains `Transfer report.pdf` and `modified.txt` contains `Transfer report_new.pdf`:

```
Original file:
Enter file path: original.txt

Modified file:
Enter file path: modified.txt

Original hash:  fb3a4807ab64ac2562624e9972f1dd6a35a73aa2a39ab23dc80deefbb2e4bb0d
Modified hash:  b887881e6ec9a0fe9856510a079856e141998e063faedcfe76d137aabc4ef836

Signature verification:
INVALID
```

If both files have the same content, the hashes match and the result is **VALID**.
Only the content is compared, not the file name, so this works with any file type (`.txt`, `.pdf`, `.docx`, ...).

This demonstrates:

- **Integrity:** any change to the content changes the hash, so the signature no longer matches.
- **Authentication:** only Alice's private key can create a signature that her public key accepts.

## How signing and verification work

```
Alice                                         Bob
-----                                         ---
message ──SHA-256──> hash                     received message ──SHA-256──> new hash
hash ──sign with Alice's PRIVATE key──> signature ─────────────> verify(signature, new hash)
                                                                 using Alice's PUBLIC key
                                                                        │
                                                                VALID / INVALID
```

## Known limitations

- **Encryption size limit:** RSA-2048 with OAEP (SHA-256) can encrypt at most **190 bytes**.
  Larger files, such as a PDF, show an error message instead of being encrypted.
  Real systems use *hybrid encryption* for large files: AES encrypts the file and RSA encrypts only the AES key.
- **In-place encryption:** options 2 and 3 overwrite the original file. Use a copy when testing.
- **Keys are not saved:** a new key pair is created each time the program runs, so a file encrypted in one run
  cannot be decrypted in a later run.
- **Double hashing:** `sign_file()` receives the SHA-256 hex digest, and the RSA signing step hashes it again with SHA-256.
  This is consistent between signing and verification, so it works correctly.

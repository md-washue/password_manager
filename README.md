# Secure CLI Password Manager

A lightweight, locally hosted command-line password manager built with Python. This tool provides secure credential storage by combining AES-GCM authenticated encryption with PBKDF2 key derivation, ensuring zero-knowledge local storage. 

## 🛡️ Core Security Architecture

* **Key Derivation:** Master passwords are never stored. Instead, they are passed through **PBKDF2-HMAC-SHA256** with 600,000 iterations and a cryptographically secure 16-byte random salt to generate the encryption key.
* **Authenticated Encryption:** Credentials are encrypted using **AES-GCM (Galois/Counter Mode)**. This provides both confidentiality and data authenticity, ensuring the ciphertext cannot be tampered with in the SQLite database without detection.
* **Secure Memory Handling:** Master passwords and target passwords are read using the `getpass` module to prevent echo in terminal histories or screen capture.
* **Cryptographic Randomness:** The built-in password generator uses the `secrets` module (rather than the predictable `random` module) to ensure high-entropy credential generation.

## ⚙️ Prerequisites

This project relies on the standard Python standard library (for SQLite3, `argparse`, and `secrets`) and requires the `cryptography` package for AES and KDF operations.


# CryptoProject

This repository contains a collection of **educational cryptography implementations** written in Python.  
Each project focuses on a core concept from modern cryptography or cryptanalysis, implemented from scratch for learning and experimentation.

 These implementations are **not production-secure** and are meant strictly for academic study.

## Project 1: Shamir's Secret Sharing (SSS)

**File:** `project.py`

### Goal
Implement Shamir’s Secret Sharing scheme to split a secret into multiple shares such that:
- Any `t` shares can reconstruct the secret
- Fewer than `t` shares reveal no information

### Features
- Polynomial-based secret encoding
- Lagrange interpolation for reconstruction
- Demonstrates information-theoretic security

### Limitations
- Works over small integers (not large finite fields)
- No cryptographic randomness guarantees
- No protection against malicious participants

## Project 2: Verifiable Secret Sharing (VSS)

**File:** `vss_basic.py`

### Goal
Extend basic secret sharing to allow participants to **verify** the correctness of received shares, even without trusted dealers.

### Features
- Basic verification mechanism without hash functions
- Demonstrates the idea of share consistency
- Educational alternative to Feldman/Pedersen VSS

### Limitations
- Not secure against active adversaries
- Does not use commitments or zero-knowledge proofs
- Intended purely as a conceptual demonstration

## Project 3: Differential Cryptanalysis of a Toy SPN Cipher

**File:** `differential_cryptanalysis.py`

### Goal
Implement a **full differential cryptanalysis attack** on a small Substitution–Permutation Network (SPN) cipher.

The cipher is intentionally small (16-bit block, 4 rounds) to keep the attack computationally feasible.

### Features
- Custom 4-round SPN cipher
- Difference Distribution Table (DDT) computation
- Automatic differential characteristic selection
- Plaintext–ciphertext pair generation
- Last-round subkey recovery using partial decryption

### Limitations
- Toy cipher (not comparable to AES/DES security)
- Uses a single high-probability characteristic
- Small sample size for practicality
- No key schedule cryptanalysis
- only 200 plaintext-ciphertext pairs, leads to inaccurate results

## Repository Structure
CryptoProject/
├── project.py # Shamir Secret Sharing
├── vss_basic.py # Verifiable Secret Sharing
├── differential_cryptanalysis.py
└── README.md

## Notes
Some parts of this repository were developed with the help of AI tools (e.g., ChatGPT), primarily for
debugging, structuring code, and clarifying cryptographic concepts. All implementations were written,
understood, and verified by me as part of my learning process.






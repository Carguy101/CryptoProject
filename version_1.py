import random
import secrets

# =========================
# CONFIG
# =========================
PRIME = 2**127 - 1  # Very large prime (enough for long secrets)

# =========================
# TEXT CONVERSION HELPERS
# =========================
def string_to_int(s):
    return int.from_bytes(s.encode('utf-8'), 'big')

def int_to_string(n):
    length = (n.bit_length() + 7) // 8  # number of bytes needed
    return n.to_bytes(length, 'big').decode('utf-8')

# =========================
# SHAMIR'S SECRET SHARING
# =========================
def generate_polynomial(secret_int, n, t, p=PRIME):
    coeffs = [secret_int] + [secrets.randbelow(p) for _ in range(t - 1)]
    shares = []
    for i in range(1, n + 1):  # i cannot be 0
        x = i
        y = sum(coeff * pow(x, power, p) for power, coeff in enumerate(coeffs)) % p
        shares.append((x, y))
    return shares

def recover_secret(shares, t, p=PRIME):
    secret = 0
    for i in range(t):
        xi, yi = shares[i]
        li = 1
        for j in range(t):
            if i != j:
                xj = shares[j][0]
                li *= (-xj * pow(xi - xj, -1, p)) % p
        secret += li * yi
        secret %= p
    return secret

# =========================
# MAIN DEMO
# =========================
def main():
    # Secret as string
    secret_text = "crypto is fun"
    t = 3
    n = 5

    # Convert to int
    secret_int = string_to_int(secret_text)

    shares = generate_polynomial(secret_int, n, t)
    print("Shares:", shares)

    # Randomly pick t shares
    selected = random.sample(shares, t)
    print("Selected shares:", selected)

    # Reconstruct
    recovered_int = recover_secret(selected, t)
    recovered_text = int_to_string(recovered_int)
    print("Recovered secret:", recovered_text)

if __name__ == "__main__":
    main()

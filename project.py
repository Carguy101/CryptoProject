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
def generate_polynomial(secret_int_1, secret_int_2 ,n, t, p=PRIME):
    coeffs_1 = [secret_int_1] + [secrets.randbelow(p) for _ in range(t - 1)]
    shares_1 = []
    coeffs_2 = [secret_int_2] + [secrets.randbelow(p) for _ in range(t - 1)]
    shares_2 = []
    for i in range(1, n + 1):  # i cannot be 0
        x = i
        y_1 = sum(coeff * pow(x, power, p) for power, coeff in enumerate(coeffs_1)) % p
        shares_1.append((x, y_1))
        y_2 = sum(coeff * pow(x, power, p) for power, coeff in enumerate(coeffs_2)) % p
        shares_2.append((x, y_2))
    shares=[shares_1,shares_2]
    return shares

def recover_secret(shares, t, p=PRIME):
    secret_1 = 0
    secret_2 = 0
    for i in range(t):
        xi, yi = shares[0][i]
        li = 1
        for j in range(t):
            if i != j:
                xj = shares[0][j][0]
                li *= (-xj * pow(xi - xj, -1, p)) % p
        secret_1 += li * yi
        secret_1 %= p
    
    for i in range(t):
        xi, yi = shares[1][i]
        li = 1
        for j in range(t):
            if i != j:
                xj = shares[1][j][0]
                li *= (-xj * pow(xi - xj, -1, p)) % p
        secret_2 += li * yi
        secret_2 %= p
    secret=[secret_1,secret_2]

    return secret

# =========================
# MAIN DEMO
# =========================
def main():
    # Secret as string
    secret_text_1 = "crypto is fun"
    secret_text_2 = "hello world"
    t = 3
    n = 5

    # Convert to int
    secret_int_1 = string_to_int(secret_text_1)
    secret_int_2 = string_to_int(secret_text_2)

    shares = generate_polynomial(secret_int_1, secret_int_2, n, t)
    print("Shares:", shares)

    # Randomly pick t shares
    selected_1 = random.sample(shares[0], t)
    selected_2 = random.sample(shares[1], t)
    selected=[selected_1,selected_2]
    print("Selected shares:", selected)

    # Reconstruct
    recovered_int_1,recovered_int_2 = recover_secret(selected, t)
    recovered_text_1 = int_to_string(recovered_int_1)
    recovered_text_2 = int_to_string(recovered_int_2)
    recovered_text=[recovered_text_1,recovered_text_2]
    print("Recovered secret:", recovered_text)

if __name__ == "__main__":
    main()


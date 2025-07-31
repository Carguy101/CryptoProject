import random
import secrets

# =========================
# CONFIG
# =========================
PRIME = 2**127 - 1  # Large enough prime for most secrets

# =========================
# TEXT CONVERSION HELPERS
# =========================
def string_to_int(s):
    return int.from_bytes(s.encode('utf-8'), 'big')

def int_to_string(n):
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, 'big').decode('utf-8', errors='replace')  # Avoid crashing on invalid utf-8

# =========================
# SHAMIR'S SECRET SHARING
# =========================
def generate_polynomial(secret_int_1, secret_int_2, n, t, p=PRIME):
    coeffs_1 = [secret_int_1] + [secrets.randbelow(p) for _ in range(t - 1)]
    coeffs_2 = [secret_int_2] + [secrets.randbelow(p) for _ in range(t - 1)]
    shares_1, shares_2 = [], []
    for i in range(1, n + 1):
        x = i
        y_1 = sum(coeff * pow(x, power, p) for power, coeff in enumerate(coeffs_1)) % p
        y_2 = sum(coeff * pow(x, power, p) for power, coeff in enumerate(coeffs_2)) % p
        shares_1.append((x, y_1))
        shares_2.append((x, y_2))
    return [shares_1, shares_2]

def recover_secret(shares, t, p=PRIME):
    def lagrange_interpolate(points):
        total = 0
        for i in range(t):
            xi, yi = points[i]
            li = 1
            for j in range(t):
                if i != j:
                    xj, _ = points[j]
                    li *= (-xj * pow(xi - xj, -1, p)) % p
            total += li * yi
            total %= p
        return total

    secret_1 = lagrange_interpolate(shares[0])
    secret_2 = lagrange_interpolate(shares[1])
    return [secret_1, secret_2]

# =========================
# MAIN DEMO
# =========================
def main():
    secret_text_1 = "crypto is fun"
    secret_text_2 = "hello world"
    t = 3
    n = 5

    secret_int_1 = string_to_int(secret_text_1)
    secret_int_2 = string_to_int(secret_text_2)

    shares = generate_polynomial(secret_int_1, secret_int_2, n, t)
    print("All Shares:\n", shares, "\n")

    # === Try 1: Using only 1 share ===
    selected = [random.sample(shares[0], 1), random.sample(shares[1], 1)]
    print("Attempt with 1 share (should fail):")
    try:
        secret_ints = recover_secret(selected, t=1)
        recovered = [int_to_string(s) for s in secret_ints]
        print("Recovered:", recovered)
    except Exception as e:
        print("Failed to recover:", str(e))
    print()

    # === Try 2: Using 2 shares ===
    selected = [random.sample(shares[0], 2), random.sample(shares[1], 2)]
    print("Attempt with 2 shares (should still fail):")
    try:
        secret_ints = recover_secret(selected, t=2)
        recovered = [int_to_string(s) for s in secret_ints]
        print("Recovered:", recovered)
    except Exception as e:
        print("Failed to recover:", str(e))
    print()

    # === Try 3: Using correct t shares ===
    selected = [random.sample(shares[0], t), random.sample(shares[1], t)]
    print("Attempt with 3 shares (should succeed):")
    try:
        secret_ints = recover_secret(selected, t=t)
        recovered = [int_to_string(s) for s in secret_ints]
        print("Recovered:", recovered)
    except Exception as e:
        print("Failed to recover:", str(e))

if __name__ == "__main__":
    main()



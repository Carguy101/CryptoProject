! pip install pycryptodome
from Crypto.Util import number
import random
import secrets

# ------------------ STEP 1: Prime and Generators ------------------

def generate_safe_prime(bits=256):
    while True:
        q = number.getPrime(bits)
        p = 2 * q + 1
        if number.isPrime(p):
            return p, q

def find_generator(p, q):
    while True:
        g = random.randrange(2, p - 1)
        if pow(g, q, p) == 1 and pow(g, 2, p) != 1:
            return g

def find_independent_generator(g, p, q):
    a = random.randrange(2, q)
    return pow(g, a, p)
#here, log isn't exactly unknown to the dealer, but it requires SHA which I haven't done yet 
# ------------------ STEP 2: Commitments ------------------

def commitment(a, b, g, h, p):
    return (pow(g, a,p) * pow(h, b,p)) % p

# ------------------ STEP 3: Secret Sharing ------------------

def generate_shares(secret_s, secret_t, n, t, p):
    coeffs_f = [secret_s] + [secrets.randbelow(q) for _ in range(t - 1)]
    coeffs_g = [secret_t] + [secrets.randbelow(q) for _ in range(t - 1)]
    shares = []

    for x in range(1, n + 1):
        fx = sum(coeff * pow(x, i, q) for i, coeff in enumerate(coeffs_f)) % q
        gx = sum(coeff * pow(x, i, q) for i, coeff in enumerate(coeffs_g)) % q
        shares.append((x, fx, gx))

    return shares, coeffs_f, coeffs_g

# ------------------ STEP 4: Verify ------------------

def verify_shares(shares, coeffs_f, coeffs_g, g, h, p, t):
    commitments = [commitment(coeffs_f[i], coeffs_g[i], g, h, p) for i in range(t)]

    for x, fx, gx in shares:
        lhs = commitment(fx, gx, g, h, p)
        rhs = 1
        for j in range(t):
            rhs = (rhs * pow(commitments[j], pow(x, j,), p)) % p
        if lhs != rhs:
            return False
    return True

# ------------------ STEP 5: Reconstruct ------------------

def lagrange_interpolate_zero(xs, ys, q):
    def modinv(a, q):
        return number.inverse(a, q)

    total = 0
    k = len(xs)
    for i in range(k):
        xi, yi = xs[i], ys[i]
        li = 1
        for j in range(k):
            if i != j:
                xj = xs[j]
                li *= (-xj) * modinv((xi - xj) % q, q)
                li %= q
        total += yi * li
        total %= q
    return total

# ------------------ DEMO ------------------

# 1. Setup
p, q = generate_safe_prime(256)
g = find_generator(p, q)
h = find_independent_generator(g, p, q)

# 2. Parameters
secret_s = 123456789  # Set manually to verify correctness
secret_t = 987654321  # Just used for hiding
n = 5
t = 3

# 3. Generate shares and commitments
shares, coeffs_f, coeffs_g = generate_shares(secret_s, secret_t, n, t, p)

# 4. Verify shares
print("Verifying shares...")
if verify_shares(shares, coeffs_f, coeffs_g, g, h, p, t):
    print("✅ All shares verified.")
else:
    print("❌ Verification failed!")

# 5. Reconstruct secret_s using only first t shares
subset = shares[:t]
xs = [x for x, _, _ in subset]
ys = [fx for _, fx, _ in subset]

recovered_s = lagrange_interpolate_zero(xs, ys, q)
print(f"Original secret_s : {secret_s}")
print(f"Recovered secret_s: {recovered_s}")










  




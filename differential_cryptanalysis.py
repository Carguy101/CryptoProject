import random
key=random.getrandbits(16)
SBOX = [0xC, 5, 6, 0xB,
        9, 0, 0xA, 0xD, 
        3, 0xE, 0xF, 8, 
        4, 7, 1, 2] 
PERM = [0, 4, 8, 12, 
        1, 5, 9, 13, 
        2, 6, 10,14, 
        3, 7, 11,15]
def S_box_layer(state):
    new_state = 0   #imp to keep newstate here, so that can directly OR the substituted nibble
    for i in range(4):
        nibble = (state >> (4*i)) & 0xF
        substituted_nibble = SBOX[nibble]
        new_state |= (substituted_nibble << (4*i))
    return new_state

def permute(state):
    new_state = 0
    for i in range(16):
        bit = (state >> PERM[i]) & 1
        new_state |= (bit << i)
    return new_state

def round_key(key, r):
    return ((key << r) | (key >> (16 - r))) & 0xFFFF

def encrypt(plaintext, key):
    state = plaintext
    for r in range(4):
        state ^= round_key(key, r)
        state = S_box_layer(state)
        state = permute(state)
    return state    
#first doing differential cryptanalysis
#made ddt
def compute_ddt():
  ddt=[[0]*16 for _ in range(16)]
  for x in range(16):
    for dx in range(16):
      dy=SBOX[x]^SBOX[dx^x]
      ddt[dx][dy]+=1
  return ddt
ddt=compute_ddt()
#have to choose differential characteristic
#start with certain candidates for dP based on DDT
#then have to check for slow diffusion
def best_dy(dx, ddt):
    row = ddt[dx]
    max_count = max(row)
    dy = row.index(max_count)
    return dy

dx_candidates = []
for dx in range(1, 16):

  if max(ddt[dx]) >= 4:
    # filter only
    dx_candidates.append(dx)

rounds = 3
diffusion_score = {}

for dx in dx_candidates:  
    state = dx << 12
    active = 0

    for _ in range(rounds):
        next_state = 0

        for j in range(4):
            nibble_dx = (state >> (4*j)) & 0xF
            if nibble_dx != 0:
                dy = best_dy(nibble_dx, ddt)
                next_state |= (dy << (4*j))
                active += 1

        state = permute(next_state)

    diffusion_score[dx] = active

ranked = sorted(diffusion_score.items(), key=lambda x: x[1])
#each entry of characteristic stores (round,s_box with dx!=0,dx,dy)
dP=ranked[0][0]

def build_characteristic(dx0, rounds, ddt):
    state = dx0 << 12      # activate S11
    characteristic = []    

    for r in range(1, rounds + 1):
        next_state = 0
        
        for j in range(4):
            dx = (state >> (4*j)) & 0xF   #this line to check which nibble, or alternately, which sbox is active
            if dx != 0:   # if dx=0, then obviously dy=0
                dy = best_dy(dx, ddt)                
                characteristic.append([r, j+1, dx, dy])
                next_state |= (dy << (4*j))          #this line to give embed output difference
                 
                

        state = permute(next_state)

    return characteristic

best_char=build_characteristic(dP,3,ddt)
w=len(best_char)
active_sbox_last=[]
for _ in range(w):
  if(best_char[_][0]==3):
    active_sbox_last.append(best_char[_][1])

def generate_pairs(N, dP, key):
    pairs = []

    for _ in range(N):
        P  = random.getrandbits(16)
        P2 = P ^ dP

        C  = encrypt(P, key)
        C2 = encrypt(P2, key)

        pairs.append((P, P2, C, C2))

    return pairs

#checked that 1,2 and 4 sboxes are active in the last round,
# so these will be target subkey bits
N = 200
pairs = generate_pairs(N, dP, key)
#guess for each s-box independently, not all together
def inv_sbox(nibble):
  return SBOX.index(nibble)
count_k=[[0 for _ in range(0,15)]]
#partial decryption in last round
expected_last = {}

for r, sbox, dx, dy in best_char:
  if r == 3:              # last characteristic round
    expected_last[sbox-1] = dy   # INPUT to round-4 S-box


count_k = {sbox: [0]*16 for sbox in expected_last}

for sbox in expected_last:
    expected = expected_last[sbox]

    for subkey in range(16):
        for i in range(N):
            C, Cp = pairs[i][2], pairs[i][3]

            c  = (C  >> (4*sbox)) & 0xF
            cp = (Cp >> (4*sbox)) & 0xF

            u  = inv_sbox(c  ^ subkey)
            up = inv_sbox(cp ^ subkey)

            if (u ^ up) == expected:
                count_k[sbox][subkey] += 1

for sbox in count_k:
    print(f"S-box {sbox}:", count_k[sbox])

#the one with the maximum count is the correct (expected) target subkey    

             

    

      
      



  
    

  
  











        

    












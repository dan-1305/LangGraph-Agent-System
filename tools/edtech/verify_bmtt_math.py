import numpy as np

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def affine_decrypt(c_text, a, b):
    a_inv = mod_inverse(a, 26)
    res = ""
    for c in c_text:
        c_val = ord(c) - 97
        p_val = (a_inv * (c_val - b)) % 26
        res += chr(p_val + 97)
    return res

def hill_encrypt(p_text, K):
    m = len(K)
    p_text = p_text.replace(" ", "")
    while len(p_text) % m != 0:
        p_text += "x"
    res = ""
    for i in range(0, len(p_text), m):
        block = [ord(c) - 97 for c in p_text[i:i+m]]
        vec = np.array(block).reshape(m, 1)
        c_vec = np.dot(K, vec) % 26
        for val in c_vec:
            res += chr(int(val[0]) + 97)
    return res

def rsa_encrypt(p_text, p, q, e):
    n = p * q
    res = []
    for c in p_text:
        m_val = ord(c) - 97
        c_val = (m_val ** e) % n
        res.append(c_val)
    return res

print("=== Q1: AFFINE ===")
print(affine_decrypt("rmpjvpwtwtmhgmpwtgfwgkzn", 19, 23))

print("\n=== Q2: HILL 2x2 ===")
K2 = np.array([[7, 3], [8, 7]])
c2 = hill_encrypt("doikhongnhulamo", K2)
print("Encrypted:", c2)
det2 = int(round(np.linalg.det(K2))) % 26
det2_inv = mod_inverse(det2, 26)
print("det K2:", det2, "inv det K2:", det2_inv)
adj2 = np.array([[K2[1,1], -K2[0,1]], [-K2[1,0], K2[0,0]]]) % 26
K2_inv = (det2_inv * adj2) % 26
print("K2_inv:\n", K2_inv)
print("Decrypted:", hill_encrypt(c2, K2_inv))

print("\n=== Q3: HILL 3x3 ===")
K3 = np.array([[5, 8, 9], [3, 7, 5], [6, 3, 9]])
c3 = hill_encrypt("khoacongnghekythuat", K3)
print("Encrypted:", c3)
det3 = int(round(np.linalg.det(K3))) % 26
det3_inv = mod_inverse(det3, 26)
print("det K3:", det3, "inv det K3:", det3_inv)
# Calculate cofactor matrix manually
adj3 = np.zeros((3, 3), dtype=int)
for i in range(3):
    for j in range(3):
        minor = np.delete(np.delete(K3, i, 0), j, 1)
        adj3[i, j] = ((-1)**(i+j) * int(round(np.linalg.det(minor)))) % 26
adj3 = adj3.T % 26
K3_inv = (det3_inv * adj3) % 26
print("K3_inv:\n", K3_inv)
print("Decrypted:", hill_encrypt(c3, K3_inv))

print("\n=== Q4: RSA ===")
p_rsa = 11
q_rsa = 13
e_rsa = 7
print(rsa_encrypt("chuccacbanthitotnhe", p_rsa, q_rsa, e_rsa))

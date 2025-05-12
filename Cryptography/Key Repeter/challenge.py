def enc(plaintext: bytes, key: bytes = b"AzCTF") -> str:
    """
    Repeating‑key XOR encrypt, then return lowercase hex.
    """
    ciphertext = bytes(
        plaintext[i] ^ key[i % len(key)]
        for i in range(len(plaintext))
    )
    return ciphertext.hex()

if __name__ == "__main__":
    pt = b"ORDER: AzCTF{Az-SENCS_is_lunching_a_new_era}"
    print(enc(pt))
    # → 0e280711147b5a022e05153c38153c6c29061a0512252a27192d0f2d372e2814240b271e1426231924082229

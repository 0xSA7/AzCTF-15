def dec(hex_cipher: str, key: bytes = b"AzCTF") -> str:
    """
    Repeating‑key XOR decrypt: take lowercase‑hex, XOR with key, return UTF‑8 string.
    """
    ct = bytes.fromhex(hex_cipher)
    pt = bytes(
        ct[i] ^ key[i % len(key)]
        for i in range(len(ct))
    )
    return pt.decode()

if __name__ == "__main__":
    ct_hex = "0e280711147b5a022e05153c38153c6c29061a0512252a27192d0f2d372e2814240b271e1426231924082229"
    print(dec(ct_hex))
    # → "ORDER: AzCTF{Az-SENCS_is_lunching_a_new_era}"

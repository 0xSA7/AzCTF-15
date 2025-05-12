# Flag : AzCTFP{a_g00d_start_with_shift_by_index}
def dec(ciphertext: str) -> str:
    plaintext = []
    for i, c in enumerate(ciphertext):
        if c.isalpha():
            # determine whether it’s upper‑ or lower‑case
            base = ord('A') if c.isupper() else ord('a')
            # subtract the index offset (i) instead of adding it
            p = chr((ord(c) - base - i) % 26 + base)
            plaintext.append(p)
        else:
            # non‑letters are left unchanged
            plaintext.append(c)
    return "".join(plaintext)

if __name__ == "__main__":
    # Read the content of palin.txt
    ciphertext = "a_i00i_zbjbe_jwix_kacap_zx_jpgic"
    # Decrypt the content
    plaintext = dec(ciphertext)

    # Print the decrypted text
    print("Decrypted text:", plaintext)
    
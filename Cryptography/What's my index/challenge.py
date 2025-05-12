def enc(plaintext):
    return "".join(
        chr((ord(c)
             - (base := ord('A') if c.isupper() else ord('a'))
             + i) % 26 + base)
        if c.isalpha() else c
        for i, c in enumerate(plaintext)
    )

# Read the content of palin.txt
plaintext = "a_g00d_start_with_shift_by_index"

# Encrypt the content
ciphertext = enc(plaintext)

# Print the encrypted text
print("Encrypted text:", ciphertext)

def text_to_cipher(text):
    cipher = []
    for char in text:
        binary = bin(ord(char))[2:].zfill(8)
        cipher_part = binary.replace('0', '-').replace('1', '_')
        cipher.append(cipher_part)
    return ''.join(cipher)

flag = "AzCTF{D0n't_use_@I_t00!z}"
ciphertext = text_to_cipher(flag)
with open('/home/sa7/Documents/AzCTF/Cryptography/Encoded Whisper/cipher.txt', 'w') as f:
    f.write(ciphertext)
print("Ciphertext:", ciphertext)

def cipher_to_text(cipher):
    binary = cipher.replace('-', '0').replace('_', '1')
    text = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        text.append(chr(int(byte, 2)))
    return ''.join(text)

with open('/home/sa7/Documents/AzCTF/Cryptography/Encoded Whisper/cipher.txt', 'r') as f:
    cipher = f.read().strip()

flag = cipher_to_text(cipher)
print("Flag:", flag)
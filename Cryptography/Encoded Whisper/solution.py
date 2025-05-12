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
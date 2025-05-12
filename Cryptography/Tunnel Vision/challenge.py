from scapy.all import Ether, IP, ICMP, Raw, UDP, DNS, DNSQR, wrpcap
from Crypto.Cipher import AES
import os

def encrypt_file(input_path, output_path):
    # Read and AES encrypt the file
    with open(input_path, "rb") as f:
        data = f.read()
    cipher = AES.new(b"milkmilkmilkmilk", AES.MODE_ECB)
    padded = data + b"\x00" * ((16 - len(data) % 16) % 16)  # Add padding
    encrypted = cipher.encrypt(padded)
    with open(output_path, "wb") as f:
        f.write(encrypted)
    print(f"✅ File encrypted and saved to '{output_path}'")

def decrypt_file(input_path, output_path):
    # Read and AES decrypt the file
    with open(input_path, "rb") as f:
        encrypted = f.read()
    cipher = AES.new(b"milkmilkmilkmilk", AES.MODE_ECB)
    decrypted = cipher.decrypt(encrypted)
    # Remove padding
    decrypted = decrypted.rstrip(b"\x00")
    with open(output_path, "wb") as f:
        f.write(decrypted)
    print(f"✅ File decrypted and saved to '{output_path}'")

def challenge():
    # Encrypt the file
    input_file = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/Your text.png"
    encrypted_file = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/encrypted.bin"
    encrypt_file(input_file, encrypted_file)

    # Read the encrypted file
    with open(encrypted_file, "rb") as f:
        encrypted = f.read()

    # Generate packets, interleave DNS
    pkts = []
    for i in range(0, len(encrypted), 400):
        chunk = encrypted[i:i+400]
        icmppkt = (Ether()/IP(src="10.0.0.%d" % (i % 256), dst="10.0.0.10")/
                   ICMP(type=8, id=int.from_bytes(os.urandom(2), "big"), seq=os.urandom(1)[0])/
                   Raw(load=chunk))
        dns = Ether()/IP(src="192.168.1.1", dst="8.8.4.4")/UDP(sport=5353, dport=5353)/DNS(rd=1, qd=DNSQR(qname="invoice.halib-al-khair.com"))
        pkts.extend([icmppkt, dns])
    wrpcap("/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/challenge.pcap", pkts)
    print("✅ Packets generated and saved to 'challenge.pcap'")

if __name__ == "__main__":
    challenge()

    # Decrypt the file (for testing purposes)
    encrypted_file = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/encrypted.bin"
    decrypted_file = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/restored.png"
    decrypt_file(encrypted_file, decrypted_file)
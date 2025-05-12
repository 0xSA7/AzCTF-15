# from scapy.all import rdpcap, ICMP, Raw
# from Crypto.Cipher import AES

# def extract_encrypted_data(pcap_file, output_file):
#     # Read the pcap file
#     packets = rdpcap(pcap_file)

#     # Extract ICMP Echo-Request packets with a Raw layer
#     icmp_packets = []
#     for pkt in packets:
#         if ICMP in pkt and pkt[ICMP].type == 8 and Raw in pkt:
#             icmp_packets.append(pkt)

#     # Sort packets by ICMP sequence number
#     icmp_packets.sort(key=lambda pkt: pkt[ICMP].seq)

#     # Combine the payloads
#     encrypted_data = b"".join(pkt[Raw].load for pkt in icmp_packets)

#     # Debug: Print the size of the extracted data
#     print(f"Extracted encrypted data size: {len(encrypted_data)} bytes")

#     # Save the extracted encrypted data to a file
#     with open(output_file, "wb") as f:
#         f.write(encrypted_data)
#     print(f"✅ Encrypted data extracted and saved to '{output_file}'")
#     return encrypted_data

# def decrypt_file(input_path, output_path):
#     # Read and AES decrypt the file
#     with open(input_path, "rb") as f:
#         encrypted = f.read()
#     cipher = AES.new(b"milkmilkmilkmilk", AES.MODE_ECB)
#     decrypted = cipher.decrypt(encrypted)
#     # Remove padding
#     decrypted = decrypted.rstrip(b"\x00")
#     with open(output_path, "wb") as f:
#         f.write(decrypted)
#     print(f"✅ File decrypted and saved to '{output_path}'")

# if __name__ == "__main__":
#     # File paths
#     pcap_file = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/challenge.pcap"
#     encrypted_output = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/extracted_encrypted.bin"
#     decrypted_output = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/restored.png"

#     # Extract encrypted data from ICMP packets
#     encrypted_data = extract_encrypted_data(pcap_file, encrypted_output)
#     open(encrypted_output, "wb").write(encrypted_data)
#     # Decrypt the extracted data
#     decrypt_file(encrypted_output, decrypted_output)
#!/usr/bin/env python3
"""
decrypt_challenge.py

Extracts AES‐ECB–encrypted data from ICMP payloads in a PCAP,
reassembles it, decrypts with key "milkmilkmilkmilk", and
writes the restored file.
"""

# from scapy.all import rdpcap, ICMP, Raw
# from Crypto.Cipher import AES

# AES_KEY = b"milkmilkmilkmilk"
# PCAP_PATH = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/challenge.pcap"
# OUTPUT_ENCRYPTED = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/extracted_encrypted.bin"
# OUTPUT_DECRYPTED = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/restored.png"

# def extract_encrypted_from_pcap(pcap_path: str) -> bytes:
#     """
#     Read the PCAP, pull out all ICMP Echo‐Request Raw payloads
#     in their capture order, and concatenate them.
#     """
#     pkts = rdpcap(pcap_path)
#     buf = bytearray()
#     for pkt in pkts:
#         if pkt.haslayer(ICMP) and pkt.haslayer(Raw):
#             # ICMP type 8 is Echo‐Request
#             if pkt[ICMP].type == 8:
#                 buf.extend(pkt[Raw].load)
#     return bytes(buf)

# def decrypt_aes_ecb(encrypted: bytes, key: bytes) -> bytes:
#     """
#     Decrypts AES‐ECB with zero padding removal.
#     """
#     if len(encrypted) % 16 != 0:
#         print("Warning: Encrypted data length is not aligned to 16 bytes. Padding with null bytes.")
#         encrypted += b"\x00" * (16 - len(encrypted) % 16)
#     cipher = AES.new(key, AES.MODE_ECB)
#     decrypted = cipher.decrypt(encrypted)
#     # strip trailing null bytes
#     return decrypted.rstrip(b"\x00")

# def main():
#     # 1. Extract encrypted bytes from PCAP
#     encrypted = extract_encrypted_from_pcap(PCAP_PATH)
#     with open(OUTPUT_ENCRYPTED, "wb") as f:
#         f.write(encrypted)
#     print(f"[+] Extracted encrypted data to '{OUTPUT_ENCRYPTED}'")

#     # 2. Decrypt and remove padding
#     decrypted = decrypt_aes_ecb(encrypted, AES_KEY)
#     with open(OUTPUT_DECRYPTED, "wb") as f:
#         f.write(decrypted)
#     print(f"[+] Decrypted file written to '{OUTPUT_DECRYPTED}'")

# if __name__ == "__main__":
#     main()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from scapy.all import rdpcap, wrpcap, Ether, IP, ICMP, Raw
from Crypto.Cipher import AES
import binascii
import shutil
import os

def extract_flag_packets(pcap_path):
    """
    Extracts ICMP Echo Request packets with specific source and destination IPs.

    Args:
        pcap_path (str): Path to the input PCAP file.

    Returns:
        list: List of extracted payloads.
    """
    print(f"📦 Reading PCAP file: {pcap_path}")
    packets = rdpcap(pcap_path)

    flag_packets = []
    for pkt in packets:
        # Check for ICMP Echo Request
        if pkt.haslayer(ICMP) and pkt[ICMP].type == 8:
            # Check for specific source and destination IPs
            if pkt[IP].src.startswith("10.0.0.") and pkt[IP].dst == "10.0.0.10":
                # Extract the payload
                payload = pkt[Raw].load
                flag_packets.append(payload)
                print(f"✅ Extracted payload from packet: {pkt.summary()}")

    if not flag_packets:
        print("⚠️  No flag packets found in the PCAP file.")
    else:
        print(f"📦 Total flag packets extracted: {len(flag_packets)}")

    return flag_packets

def save_extracted_data(data, output_path):
    """
    Saves binary data to a file.

    Args:
        data (bytes): Data to save.
        output_path (str): Path to the output file.
    """
    with open(output_path, "wb") as f:
        f.write(data)
    print(f"📦 Data saved to '{output_path}'")

def decrypt_data(encrypted_data, key, output_path):
    """
    Decrypts AES-encrypted data.

    Args:
        encrypted_data (bytes): Encrypted data.
        key (bytes): AES key.
        output_path (str): Path to save decrypted data.
    """
    print(f"🔐 Initializing AES cipher with key: {key}")
    cipher = AES.new(key, AES.MODE_ECB)

    print("🔓 Decrypting data...")
    decrypted = cipher.decrypt(encrypted_data)

    # Remove padding (assuming null byte padding)
    decrypted = decrypted.rstrip(b"\x00")
    print(f"🗑️  Removed padding: {len(encrypted_data) - len(decrypted)} bytes removed.")

    save_extracted_data(decrypted, output_path)

def rename_decrypted_file(current_path, new_filename):
    """
    Renames the decrypted file to a new filename.

    Args:
        current_path (str): Current path of the decrypted file.
        new_filename (str): New filename to rename to.
    """
    new_path = os.path.join(os.path.dirname(current_path), new_filename)
    shutil.move(current_path, new_path)
    print(f"📁 Decrypted file renamed to '{new_path}'")

def main():
    # Define file paths
    pcap_path = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/Tunnel Vision.pcap"
    extracted_flag_path = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/extracted_flag.bin"
    decrypted_flag_path = "decrypted_flag"
    final_flag_path = "/home/sa7/Documents/AzCTF/tests/task rabia/Tunnel Vision/decrypted_flag.png"

    # Step 1: Extract flag packets
    flag_packets = extract_flag_packets(pcap_path)

    if flag_packets:
        # Step 2: Save extracted payloads to a binary file
        concatenated_flag = b''.join(flag_packets)
        save_extracted_data(concatenated_flag, extracted_flag_path)

        # Step 3: Define AES key and decrypt the data
        key = b"milkmilkmilkmilk"
        decrypt_data(concatenated_flag, key, decrypted_flag_path)

        # Step 4: Rename the decrypted file to PNG
        rename_decrypted_file(decrypted_flag_path, final_flag_path)
    else:
        print("❌ Flag extraction failed. Please check the PCAP file and the extraction criteria.")

if __name__ == "__main__":
    main()
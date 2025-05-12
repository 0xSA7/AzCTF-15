import json
import base64
from scapy.all import rdpcap, TCP, Raw
import pyshark  # Optional: For more robust TCP stream reassembly

def extract_tcp_stream_pyshark(pcap_file, src_ip, dst_ip, src_port, dst_port):
    """
    Extract the TCP stream using pyshark for more reliable reassembly.
    """
    capture = pyshark.FileCapture(pcap_file)
    payloads = []
    for packet in capture:
        if 'tcp' in packet:
            if (packet.ip.src == src_ip and packet.ip.dst == dst_ip and
                packet.tcp.srcport == src_port and packet.tcp.dstport == dst_port):
                payload = packet.tcp.payload
                if payload:
                    payloads.append(payload)
            elif (packet.ip.src == dst_ip and packet.ip.dst == src_ip and
                  packet.tcp.srcport == dst_port and packet.tcp.dstport == src_port):
                payload = packet.tcp.payload
                if payload:
                    payloads.append(payload)
    return ''.join(payloads)

def decode_base64(encoded_str):
    """
    Decode a Base64 encoded string.
    """
    try:
        return base64.b64decode(encoded_str).decode('utf-8', errors='ignore')
    except base64.binascii.Error:
        return None

def extract_public_key(decoded_str):
    """
    Extract the public key JSON from the decoded string using the delimiter.
    """
    delimiter = "###PUBLIC_KEY_START###"
    parts = decoded_str.split(delimiter)
    if len(parts) >= 3:
        return parts[1]
    return None

def parse_public_key(public_key_json):
    """
    Parse the public key JSON and return the parameters.
    """
    try:
        public_key = json.loads(public_key_json)
        p = public_key.get("p")
        alpha = public_key.get("alpha")
        beta = public_key.get("beta")
        return p, alpha, beta
    except json.JSONDecodeError:
        return None, None, None

def main():
    # 1. Define PCAP file path
    pcap_file = "/home/sa7/Documents/AzCTF/tests/Elgamal Encryption/challenge.pcap"  # Replace with your PCAP file path

    # 2. Define IP and port information
    src_ip = "192.168.1.1"      # Client IP
    dst_ip = "192.168.1.100"    # Server IP
    src_port = 54321            # Client port
    dst_port = 12345            # Server port

    # 3. Extract the TCP stream using pyshark
    concatenated_payload = extract_tcp_stream_pyshark(pcap_file, src_ip, dst_ip, src_port, dst_port)
    print("Concatenated Payload:", concatenated_payload)

    # 4. Check for the embedded public key
    if "###PUBLIC_KEY_START###" in concatenated_payload:
        print("Embedded public key found in concatenated payload.")
        decoded_str = decode_base64(concatenated_payload)
        if decoded_str:
            public_key_json = extract_public_key(decoded_str)
            if public_key_json:
                p, alpha, beta = parse_public_key(public_key_json)
                if p and alpha and beta:
                    print(f"Public Key Parameters:\n- p: {p}\n- alpha: {p}\n- beta: {beta}")
                    return
                else:
                    print("Failed to parse public key parameters.")
            else:
                print("Delimiter not found in decoded string.")
        else:
            print("Failed to decode Base64 string.")
    else:
        print("Embedded public key not found in concatenated payload.")

    print("Public key not found in any data packets.")

if __name__ == "__main__":
    main()
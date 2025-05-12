import json
import base64
import random  # Import random for generating random payloads and sequence numbers
from scapy.all import IP, TCP, Raw, send, wrpcap
from datetime import datetime, timedelta

def serialize_public_key(p, alpha, beta):
    """
    Serialize the public key parameters into a JSON string.
    """
    public_key = {
        "p": p,
        "alpha": alpha,
        "beta": beta
    }
    return json.dumps(public_key)

def embed_public_key(original_data, public_key_json):
    """
    Embed the public key JSON into the original data using the specified delimiter.
    """
    delimiter = "###PUBLIC_KEY_START###"
    return f"{delimiter}{public_key_json}{delimiter}{original_data}"

def encode_base64(data):
    """
    Encode the input data in Base64.
    """
    return base64.b64encode(data.encode('utf-8')).decode('utf-8')

def create_syn_packet(src_ip, dst_ip, src_port, dst_port, seq, ack):
    """
    Create a SYN packet.
    """
    syn_packet = IP(src=src_ip, dst=dst_ip)/TCP(sport=src_port, dport=dst_port, flags='S', seq=seq, ack=ack)
    return syn_packet

def create_syn_ack_packet(syn_packet, seq, ack):
    """
    Create a SYN-ACK packet in response to the SYN packet.
    """
    syn_ack_packet = IP(src=syn_packet.dst, dst=syn_packet.src)/TCP(sport=syn_packet.dport, dport=syn_packet.sport, flags='SA', seq=seq, ack=ack)
    return syn_ack_packet

def create_ack_packet(syn_ack_packet, seq, ack):
    """
    Create an ACK packet in response to the SYN-ACK packet.
    """
    ack_packet = IP(src=syn_ack_packet.dst, dst=syn_ack_packet.src)/TCP(sport=syn_ack_packet.dport, dport=syn_ack_packet.sport, flags='A', seq=seq, ack=ack)
    return ack_packet

def create_data_packet(ack_packet, data, seq, ack):
    """
    Create a data packet containing the embedded public key.
    """
    data_packet = IP(src=ack_packet.dst, dst=ack_packet.src)/TCP(sport=ack_packet.dport, dport=ack_packet.sport, flags='PA', seq=seq, ack=ack)/Raw(load=data)
    return data_packet

def main():
    # 1. Define the public key parameters
    p = 467
    alpha = 2
    beta = 7

    # 2. Serialize the public key into JSON
    public_key_json = serialize_public_key(p, alpha, beta)
    print("Public Key JSON:", public_key_json)

    # 3. Define the original data
    original_data = "This is the original data that will be embedded with the public key."

    # 4. Embed the public key into the original data
    embedded_data = embed_public_key(original_data, public_key_json)
    print("Embedded Data:", embedded_data)

    # 5. Encode the embedded data in Base64
    encoded_data = encode_base64(embedded_data)
    print("Base64 Encoded Data:", encoded_data)

    # 6. Define IP and port information
    src_ip = "192.168.1.1"      # Client IP
    dst_ip = "192.168.1.100"    # Server IP
    src_port = 54321            # Client port
    dst_port = 12345            # Server port

    # 7. Initialize sequence and acknowledgment numbers
    seq = 1000
    ack = 0

    # 8. Create SYN Packet
    syn_packet = create_syn_packet(src_ip, dst_ip, src_port, dst_port, seq, ack)
    print("SYN Packet Created")

    # 9. Update sequence and acknowledgment numbers
    seq += 1
    ack = syn_packet.seq + 1

    # 10. Create SYN-ACK Packet
    syn_ack_packet = create_syn_ack_packet(syn_packet, seq, ack)
    print("SYN-ACK Packet Created")

    # 11. Update sequence and acknowledgment numbers
    ack = syn_ack_packet.seq + 1
    seq = syn_ack_packet.ack

    # 12. Create ACK Packet
    ack_packet = create_ack_packet(syn_ack_packet, seq, ack)
    print("ACK Packet Created")

    # 13. Add 200 random dummy packets to simulate real traffic
    dummy_packets = []
    for i in range(200):
        # Generate random payloads
        dummy_data = f"Dummy data packet {i + 1} - {random.randint(1000, 9999)}"
        dummy_packet = create_data_packet(ack_packet, dummy_data, seq, ack)
        dummy_packets.append(dummy_packet)
        seq += len(dummy_data)  # Increment sequence number based on payload length
        ack += random.randint(1, 5)  # Simulate acknowledgment increment with randomness

    # 14. Update sequence number for data packet
    seq = ack
    ack = ack_packet.seq + len(encoded_data)

    # 15. Create Data Packet
    data_packet = create_data_packet(ack_packet, encoded_data, seq, ack)
    print("Data Packet Created")

    # 16. Combine packets into a list
    packets = [syn_packet, syn_ack_packet, ack_packet] + dummy_packets + [data_packet]

    # 17. Save packets to PCAP file
    wrpcap("/home/sa7/Documents/AzCTF/tests/Elgamal Encryption/challenge.pcap", packets)
    print("PCAP file 'challenge.pcap' created")

    # 18. (Optional) Send packets
    # Uncomment the following line to send the packets
    # send(syn_packet, verbose=0)
    # send(syn_ack_packet, verbose=0)
    # send(ack_packet, verbose=0)
    # for pkt in dummy_packets:
    #     send(pkt, verbose=0)
    # send(data_packet, verbose=0)

if __name__ == "__main__":
    main()


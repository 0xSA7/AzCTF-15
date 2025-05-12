from scapy.all import Ether, IP, TCP, Raw, wrpcap
import random

    # XOR encode the flag file
flag = b"AzCTF{Cezar?!_He's_a_trap!}"
key = 0x19  # simple XOR key
encoded = bytes([b ^ key for b in flag])

# Create the evidence.txt file
evidence_file_path = "/home/sa7/Documents/AzCTF/tests/task rabia/Leaked Evidence/evidence.txt"
with open(evidence_file_path, "wb") as f:
    f.write(encoded)
        
# Create a fake FTP file upload simulation
def create_flag(file_path):
    with open(file_path, "rb") as f:
        data = f.read()

    chunk_size = 512
    ip_src = "10.0.0.5"
    ip_dst = "192.168.1.50"

    packets = []

    # Simulate FTP control session
    ftp_control = (
        Ether()/IP(src=ip_src, dst=ip_dst)/TCP(sport=12345, dport=21, flags="PA")/Raw(load="USER anonymous\r\n")
    )
    packets.append(ftp_control)

    ftp_control = (
        Ether()/IP(src=ip_src, dst=ip_dst)/TCP(sport=12345, dport=21, flags="PA")/Raw(load="PASS anonymous\r\n")
    )
    packets.append(ftp_control)

    ftp_control = (
        Ether()/IP(src=ip_src, dst=ip_dst)/TCP(sport=12345, dport=21, flags="PA")/Raw(load="STOR evidence.txt\r\n")
    )
    packets.append(ftp_control)

    # Simulate FTP data transfer (port 20 typically used)
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i+chunk_size]
        pkt = (
            Ether()/
            IP(src=ip_src, dst=ip_dst)/
            TCP(sport=random.randint(40000, 60000), dport=20, flags="PA")/
            Raw(load=chunk)
        )
        packets.append(pkt)

    print(f"[+] Generated {len(packets)} packets.")
    return packets

if __name__ == "__main__":
    # Generate packets and save to pcap
    packets = create_flag(evidence_file_path)
    wrpcap("/home/sa7/Documents/AzCTF/tests/task rabia/Leaked Evidence/challenge.pcap", packets)
    print("✅ FTP upload simulation saved to 'challenge.pcap'")
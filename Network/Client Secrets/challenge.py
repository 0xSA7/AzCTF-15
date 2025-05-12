from scapy.all import Ether, IP, TCP, Raw, wrpcap
import base64

# flag Cearation
def create_flag():
    flag = b"AzCTF{ua_header_leak}"
    b64 = base64.b64encode(flag).decode()
    # HTTP split
    part1 = b"GET / HTTP/1.1\r\nHost: halib-al-khair.com\r\nUser-Agent: " + b64[:8].encode()
    part2 = b64[8:].encode() + b"\r\n\r\n"

    pkts = []

    # TCP handshake
    pkts.append(IP(src="172.16.0.5", dst="172.16.0.10")/TCP(sport=5555, dport=8080, flags="S", seq=1000))
    pkts.append(IP(src="172.16.0.10", dst="172.16.0.5")/TCP(sport=8080, dport=5555, flags="SA", seq=2000, ack=1001))
    pkts.append(IP(src="172.16.0.5", dst="172.16.0.10")/TCP(sport=5555, dport=8080, flags="A", seq=1001, ack=2001))

    # HTTP payload split across two packets
    pkts.append(IP(src="172.16.0.5", dst="172.16.0.10")/TCP(sport=5555, dport=8080, flags="PA", seq=1001, ack=2001)/Raw(load=part1))
    pkts.append(IP(src="172.16.0.5", dst="172.16.0.10")/TCP(sport=5555, dport=8080, flags="PA", seq=1001+len(part1), ack=2001)/Raw(load=part2))

    return pkts

if __name__ == "__main__":
    create_flag()
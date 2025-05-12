## 6. Tunnel Vision
**Difficulty:** Hard  
**Category:** Crypto  

### Description
A covert ICMP tunnel form the attacker carried a .png file containing the incriminating evidence. he tried to hide it using ECB "milkmilkmilkmilk" 

### Obfuscation Layers Applied
- **AES Encrypt:** ZIP encrypted with key `milk`.
- **Packet Spreading:** Chunks interleaved with unrelated DNS traffic.
- **Port/ID Randomization:** ICMP ID/Seq randomized.

### PCAP Generator (`generate_icmp_tunnel.py`)
```python
from scapy.all import Ether, IP, ICMP, Raw, UDP, DNS, DNSQR, wrpcap
from Crypto.Cipher import AES
import os

# Read and AES encrypt zip
with open("evidence.zip","rb") as f: data = f.read()
cipher = AES.new(b"milkmilkmilkmilk", AES.MODE_ECB)
padded = data + b"\x00"*((16-len(data)%16)%16)
encrypted = cipher.encrypt(padded)
# Generate packets, interleave DNS
pkts=[]
for i in range(0,len(encrypted),400):
    chunk=encrypted[i:i+400]
    icmppkt = (Ether()/IP(src="10.0.0.%d"%i, dst="10.0.0.10")/
               ICMP(type=8,id=os.urandom(2),seq=os.urandom(1)[0])/
               Raw(load=chunk))
    dns = Ether()/IP(src="192.168.1.1", dst="8.8.4.4")/UDP(sport=5353,dport=5353)/DNS(rd=1,qd=DNSQR(qname="invoice.halib-al-khair.com"))
    pkts.extend([icmppkt, dns])
wrpcap("ptunnel_evidence.pcap", pkts)
```  

### Manual Wireshark Solution
1. **Filter** `icmp.type==8` and **export** all Raw payload chunks (manually or via script).
2. **Concatenate** the binary blobs in sequence order.
3. **Decrypt** with AES-ECB key `milkmilkmilkmilk` (external script).
4. `evidence_decrypted.png` to find it containing `AzCTF{i'm on highb0@rd}`.
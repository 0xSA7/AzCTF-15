## 5. Client Secrets
**Difficulty:** Easy
**Category:** Network (HTTP)  

### Description
The Scammer was browsing our page, What flag he left?

### Walkthrough
1. Filter for HTTP GET requests.  
2. Inspect the User-Agent string.


### `solution.py`
```python
from scapy.all import rdpcap, Raw

for pkt in rdpcap("client_network_http.pcap"):
    if Raw in pkt and b"User-Agent" in pkt[Raw].load:
        ua = pkt[Raw].load.split(b"User-Agent:")[1].split(b"\r\n")[0]
        print(ua.decode())
```  

### Manual Wireshark Solution
1. **Filter** for `http && tcp.port==8080` and identify the two TCP segments carrying `User-Agent`.
2. **Reassemble** HTTP by right-click → **Follow TCP Stream**.
3. **Copy** the Base64 string, decode it (`Analyze → Decode As → Base64` or external tool).  
4. **Read** `AzCTF{ua_header_leak}`.

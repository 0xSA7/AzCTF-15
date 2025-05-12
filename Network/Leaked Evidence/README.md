## 🧀 Challenge: **Leaked Evidence Upload**  
**Difficulty:** Easy-Medium  
**Category:** Network Forensics  

---

### 📜 Story:
While investigating suspicious activity on the Az-SENCS servers, you intercepted FTP traffic between a rogue insider and an unknown external IP. Hidden within this upload, you believe critical evidence about the fake dairy company **"Halib Al-Khair"** was transmitted. 

Recover the missing file to uncover a vital lead about the traitor.  
(Flag format: `AzCTF{...}`)

---
### 📋 Manual Walkthrough (Wireshark):  

**Step 1:**  
Open `challenge.pcap` in Wireshark.  

**Step 2:**  
Filter for FTP traffic:  
```wireshark
ftp-data
```
or if that’s too noisy:
```wireshark
tcp.port == 20 || tcp.port == 21
```

**Step 3:**  
Look for TCP streams showing a suspicious file transfer.

- Right-click → **Follow TCP Stream** on FTP-Data transfer.
- Save the stream contents **as raw binary**.

**Step 4:**  
If data looks strange (e.g., XORed), try simple XOR decoding with common patterns (`0x13`, `0x20`, etc.)

**Step 5:**  
Assemble the chunks, decode if necessary → The file will contain the flag.

---

### 🎯 Flag Example:  
Once recovered:
```text
AzCTF{It's_a_trap!}
```


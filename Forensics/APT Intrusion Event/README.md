## 🧀 Challenge: **Event Log Analysis for APT Intrusion**

**Difficulty:** Hard  
**Category:**   

---

### 📜 Story:
Az-SENCS’s mascot archives have been compromised by the APT group Kitty Lovers Group (KLG), who deployed stealth malware to exfiltrate personal photos of the club’s kitties. Joe Forensics has collected event logs and other artifacts—now it’s up to you to analyze them, identify the malware, and expose KLG before they strike again.
[file](https://mega.nz/file/6MgXlbZK#6WJk8iC9fozcJgc2iQBm3M8ZafS733ug9DA2G8EmP3w)


1. Which well-known RAT is the cisco_vpn.exe program?
2. What is the date and time that it appeared on Joe’s machine?
3. Did it run?

---

4. What is the r.exe program that was uploaded from the attacker onto Joe Forensics’ machine?
5. When was the date and time that it appeared on Joe’s machine?

---

7. Is there any evidence of the attacker’s backdoor?
8. Which running process(es) would you investigate if you had a memory sample of this system?

----

9. Which Trojan was the attacker using on this machine?

---

10. Where was the Trojan builder located on the machine?
11. Is there any evidence of a victim’s machine (IP address 172.16.1.135) connecting to the machine Joe was investigating?
12. When was the last time that machine was connected?

Falg:
```
AzCTF{TheRAT_appearance date and time_running date and time_ the program uploded from_ appearance date and time on jeo machine_Yes/No_****,*** and ****_Trojan/type.extention_Path of the trojen bulid_Yes/No_Date and time }
```

---

### 📋 Manual Walkthrough (Event Log Analysis):

### Part 1: Analysis of Cisco VPN Executable and R.exe Program

---

#### **1. Which well-known RAT is the cisco_vpn.exe program?**

**Step 1:** Identify the location and MD5 hash of the `cisco_vpn.exe` executable.
   - **Location:** `Disk/JoeForensics/C/Documents and Settings/Administrator/Desktop/cisco_vpn.exe`
   - **MD5 Hash:** `086ce6675cfb293d5947776d8638bd60`

**Step 2:** Search the MD5 hash on VirusTotal to identify the program.
   - **Result:** The hash corresponds to the **DarkKomet RAT**.

**Conclusion:** The `cisco_vpn.exe` program is the **DarkKomet RAT**.

---

##### **a. What is the date and time that it appeared on Joe’s machine?**

**Step 1:** Examine the MFT timeline for the creation of the `cisco_vpn.exe` file.
   - **Creation Time:** `2014-09-11 19:05:44.782711`

**Conclusion:** The `cisco_vpn.exe` file appeared on Joe’s machine on **September 11, 2014, at 19:05:44 UTC**.

---

##### **b. When did it run?**

**Step 1:** Use RegRipper’s `userassist` plugin to analyze the `NTUSER.dat` hive for execution history.
   - **Execution Time:** `Thu Sep 11 19:19:35 2014 Z`

**Conclusion:** The `cisco_vpn.exe` program ran on **September 11, 2014, at 19:19:35 UTC**.

---

#### **2. What is the r.exe program that was uploaded from the attacker onto Joe Forensics’ machine?**

**Step 1:** Identify the file through strings analysis or by checking the hash on VirusTotal.
   - **Result:** The tool is identified as **WinRAR**.

---

##### **a. When was the date and time that it appeared on Joe’s machine?**

**Step 1:** Search the timeline for the `r.exe` file.
   - **Location:** `/WINDOWS/system32/1076/r.exe`
   - **Creation Time:** `2014-09-11 19:37:48.116478`

**Conclusion:** The `r.exe` program appeared on Joe’s machine on **September 11, 2014, at 19:37:48 UTC**.

---

#### **3. Is security logging enabled on this machine? If so, which events can you expect to find?**

**Step 1:** Use the `auditpol` plugin to check the audit policy from the `SECURITY` hive.
   - **Command:**
     ```
     rip.pl -p auditpol -r <path/to/extracted/Disk.7z>/JoeForensics/C/WINDOWS/system32/config/SECURITY
     ```
   - **Output:**
     ```
     Auditing is enabled.
     Audit System Events = S/F
     Audit Logon Events = S/F
     Audit Object Access = S/F
     Audit Privilege Use = S/F
     Audit Process Tracking = S/F
     Audit Policy Change = S/F
     Audit Account Management = S/F
     Audit Dir Service Access = S/F
     Audit Account Logon Events = S/F
     ```

**Conclusion:** Yes, security logging is enabled on this machine. You can expect to find logs related to system events, logon events, object access, privilege use, process tracking, policy changes, account management, directory service access, and account logon events.

---

#### **4. Use the processed Security events to answer the following:**

##### **a. Is there any evidence of the attacker’s backdoor?**

**Step 1:** Analyze the `SecEvent.Evt` log and the exported output from `evtexport` (`SecEvent_exported.txt`).

**Step 2:** Look for events related to the `cisco_vpn.exe` process.
   - **Event 553:**
     - **Creation Time:** `Sep 11, 2014 19:19:35 UTC`
     - **Details:** A new process `cisco_vpn.exe` was created with `SeTakeOwnershipPrivilege` privileges.
   - **Event 554:**
     - **Creation Time:** `Sep 11, 2014 19:19:35 UTC`
     - **Details:** Privileged object operation with `SeTakeOwnershipPrivilege` privileges.

**Conclusion:** Yes, there is evidence of the attacker’s backdoor. The `cisco_vpn.exe` process was executed with elevated privileges, indicating malicious activity.

---

##### **b. Which running process(es) would you investigate if you had a memory sample of this system?**

**Step 1:** Identify processes with unexpected privileges or suspicious behavior.
   - **Process ID 2408:** Associated with `cisco_vpn.exe` (DarkKomet RAT).
   - **Process ID 324:** Associated with `msdcsc.exe`, which is a known component of the DarkKomet RAT.
   - **Process ID 1764:** Associated with `notepad`, which may have been used by the attacker for various purposes.

**Conclusion:** If you had a memory sample, you would investigate processes with IDs **2408**, **324**, and **1764**.

---

### Part 2: Analysis of Windows Defender Event Logs

---

#### **1. What Trojan was the attacker using on this machine?**

**Step 1:** Use `evtxdump.pl` to analyze the Windows Defender operational event log.
   - **Command:**
     ```
     evtxdump.pl Microsoft-Windows-Windows\ Defender%4Operational.evtx |less -I
     ```
   - **Result:** The Trojan identified is **TrojanDownloader:Win32/Small.AJI**.

**Conclusion:** The attacker was using the **TrojanDownloader:Win32/Small.AJI** on this machine.

---

#### **2. Where was the Trojan builder located on the machine?**

**Step 1:** Review the event log for the path of the Trojan builder.
   - **Path:** `C:\Users\IEUser\Desktop\tempsample\DarkComet.exe`

**Conclusion:** The Trojan builder was located at `C:\Users\IEUser\Desktop\tempsample\DarkComet.exe`.

---

### Part 3: Analysis of Network Connections

---

#### **1. Is there any evidence of a victim’s machine (IP address 172.16.1.135) connecting to the machine Joe was investigating?**

**Step 1:** Analyze the `Security` event log for network connection events.
   - **Event Details:**
     - **Event Time:** `2014-09-10T16:23:52.276Z`
     - **Logon Type:** `3` (Network)
     - **IpAddress:** `172.16.1.135`

**Conclusion:** Yes, there is evidence of a connection from the victim’s machine with IP address `172.16.1.135` to the machine Joe was investigating.

---

#### **2. When was the last time that machine was connected?**

**Step 1:** Identify the last event related to the IP address `172.16.1.135`.
   - **Last Event Time:** `2014-09-11T15:21:41.8763Z`

**Conclusion:** The last time the machine was connected was on **September 11, 2014, at 15:21:41 UTC**.
---

### 🎯 Flag Format:
Falg:
```
AzCTF{DarkKomet RAT_September 11, 2014, at 19:05:44 UTC_September 11, 2014, at 19:19:35 UTC_WinRAR_September 11, 2014, at 19:37:48 UTC_Yes_Yes_2408, 324, and 1764_TrojanDownloader/Small.AJI_C:\Users\IEUser\Desktop\tempsample\DarkComet.exe_Yes_September 11, 2014, at 15:21:41 UTC}
```
Falg:
```
AzCTF{DarkKomet_September 11, 2014, at 19:05:44_September 11, 2014, at 19:19:35_WinRAR_September 11, 2014, at 19:37:48_Yes_Yes_2408, 324, and 1764_Small.AJI_C:\Users\IEUser\Desktop\tempsample\DarkComet.exe_Yes_September 11, 2014, at 15:21:41}
```
flag:
```
AzCTF{DarkKomet_2014-09-11 19:05:44.782711_WinRAR_2014-09-11 19:37:48.116478_}


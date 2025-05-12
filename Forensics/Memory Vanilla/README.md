## 🧀 Challenge: **Memory Forensics with Volatility**

**Difficulty:** Hard  
**Category:** Memory Forensics  

---

### 📜 Story:
You have been given a memory sample from a system suspected of being infected with a keylogger. Your task is to analyze the memory image using Volatility to identify the keylogger process, determine the file where keystrokes are logged, and uncover the data recorded by the keylogger.
[file](https://mega.nz/file/7cZHBQDZ#6nHirqo0YfItBGrumaAfmOLfh5QrC3cgc1C8knPixD8)

Questions:
1. What is the process ID of the Dumpit.exe process? (hint: pslist)
2. What directory did Dumpit capture memory to? (hint: handles)
3. What was the full path of the file that Dumpit wrote? (hint: filescan and consoles)



```
Flag: AzCTF{process ID_directory Path_Full Path_offset_dll file_port}

```
##### Hint: 
```
Notes:
As an example, to run the ‘pslist’ plugin, the following command can be used:
$ volatility -f hands-on-plugins.raw --profile=Win7SP1x64 pslist
You just need to ensure that the –f option contains the real path to the memory sample.
```

---

### 📋 Manual Walkthrough (Volatility):

### Step-by-Step Answers to Your Questions

---

#### **1. What is the process ID (PID) of the Dumpit.exe process?**

**Step 1:** Use the `pslist` plugin to list all running processes.

**Step 2:** Pipe the output to `grep` to filter for the `Dumpit` process.

**Step 3:** Identify the PID from the filtered output.

**Command:**
```
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 pslist | grep -i dumpit
```

**Output:**
```
0xfffffa8006843b30 DumpIt.exe
1836 1624
2
45
1
1 2012-07-19 06:50:07 UTC+0000
```

**Conclusion:** The PID of the `Dumpit.exe` process is **1836**.

---

#### **2. What directory did Dumpit capture memory to?**

**Step 1:** Use the `handles` plugin to list all file handles opened by the `Dumpit` process.

**Step 2:** Specify the PID (`1836`) and filter for handles of type `File`.

**Step 3:** Identify the directory from the handle list.

**Command:**
```
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 handles -t File -p 1836
```

**Output:**
```
0xfffffa8003d41d40 1836 0x10 0x100020 File \Device\HarddiskVolume1\Windows
0xfffffa8006871710 1836 0x1c 0x100020 File \Device\HarddiskVolume1\Users\Andrew\Desktop\DumpIt
0xfffffa800681b070 1836 0xb4 0x1f01ff File \Device\DumpIt
```

**Conclusion:** The `Dumpit` process captured memory to the directory `\Device\HarddiskVolume1\Users\Andrew\Desktop\DumpIt`.

---

#### **3. What was the full path of the file that Dumpit wrote?**

**Step 1:** Use the `filescan` plugin to scan for file objects in the memory image.

**Step 2:** Use `grep` to filter for the term `Dumpit`.

**Step 3:** Identify the full path of the memory dump file.

**Command:**
```
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 filescan | grep -i dumpit
```

**Output:**
```
0x000000000ac5f730 1 1 RW-rw- \Device\HarddiskVolume1\Users\Andrew\Desktop\DumpIt\WIN-TK0PBVQLQNB-20120719-065010.raw
```

**Alternative Approach Using `consoles` Plugin:**

**Step 1:** Use the `consoles` plugin to retrieve command-line history.

**Step 2:** Identify the destination path from the `Dumpit` output.

**Command:**
```
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 consoles
```

**Output:**
```
Destination = \??\C:\Users\Andrew\Desktop\DumpIt\WIN-TK0PBVQLQNB-20120719-065010.raw
```

**Conclusion:** The full path of the file that `Dumpit` wrote is `\Device\HarddiskVolume1\Users\Andrew\Desktop\DumpIt\WIN-TK0PBVQLQNB-20120719-065010.raw`.

---

#### **4. What was the virtual offset of the usbccgp.sys driver?**

**Step 1:** Use the `modules` plugin to list all loaded modules.

**Step 2:** Pipe the output to `grep` to filter for the `usbccgp.sys` driver.

**Step 3:** Identify the virtual offset from the filtered output.

**Command:**
```
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 modules | grep -i usbccgp.sys
```

**Output:**
```
0xfffff88004293000 usbccgp.sys
```

**Conclusion:** The virtual offset of the `usbccgp.sys` driver is `0xfffff88004293000`.

---

#### **5. What file is mapped from the VAD starting at 0xfffffa80054a6b50 in the SpotifyWebHelp process?**

**Step 1:** Use the `pslist` plugin to identify the PID of the `SpotifyWebHelp` process.

**Step 2:** Use the `vadinfo` plugin to retrieve information about the VAD at the specified offset.

**Step 3:** Identify the mapped file from the VAD information.

**Commands:**
```
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 pslist | grep -i SpotifyWebHelp
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 vadinfo -p 1280 | less
```

**Output:**
```
VAD node @ 0xfffffa80054a6b50 Start 0x0000000076410000 End 0x000000007649efff Tag Vad
...
FileObject @fffffa80058ad8a0, Name: \Windows\SysWOW64\oleaut32.dll
```

**Conclusion:** The file mapped from the VAD starting at `0xfffffa80054a6b50` in the `SpotifyWebHelp` process is `\Windows\SysWOW64\oleaut32.dll`.

---

#### **6. What port is lsass listening on?**

**Step 1:** Use the `netscan` plugin to scan for network connections.

**Step 2:** Pipe the output to `grep` to filter for the `lsass` process.

**Step 3:** Identify the listening port from the filtered output.

**Command:**
```
volatility -f hands-on-plugins.raw --profile=Win7SP1x64 netscan | grep -i lsass
```

**Output:**
```
0xb161ad0 TCPv4 0.0.0.0:49154 0.0.0.0:0 LISTENING 508 lsass.exe
0xb161ad0 TCPv6 :::49154 :::* LISTENING 508 lsass.exe
0xc25e150 TCPv4 0.0.0.0:49154 0.0.0.0:0 LISTENING 508 lsass.exe
```

**Conclusion:** The `lsass` process is listening on port **49154**.

---
---

### 🎯 Flag Format:
Flag: 
```
AzCTF{1836_\Device\HarddiskVolume1\Users\Andrew\Desktop\DumpIt_\Device\HarddiskVolume1\Users\Andrew\Desktop\DumpIt\WIN-
TK0PBVQLQNB-20120719-065010.raw_0xfffffa80058f7820_oleaut32.dll_49154}
```
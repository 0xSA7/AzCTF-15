## 🧀 Challenge: **Traitor's Geolocation Gamble**  
**Difficulty:** Hard  
**Category:** OSINT  

---

### 📜 Story:
[challenge](https://youtu.be/BRoQva6wX24?si=mp2PnbeQp34vC8xc)
The rogue Az-SENCS Highboard member left a taunting video on the compromised server, bragging about their new "Halib Al-Khair" venture. Forensic traces revealed a hidden clip from a 2007 UNHCR report showing a white tent in a refugee camp a key clue to their hideout. Pinpoint its coordinates to expose where the scam was masterminded.  

*(Flag format: `AzCTF{Lat_Long}` using [Degrees_Minutes_Seconds]_[Direction] notation)*  

---

### 📋 Manual Walkthrough:

**Step 1:**  
Extract the video frame at 1:16 (YouTube timestamp `t=76`). Note the tent’s proximity to a volcanic hill and lake, narrowing the location to North Kivu, DRC.  

**Step 2:**  
Search UNHCR 2007 reports for camps near Goma:  
```google
site:unhcr.org "North Kivu" "camp" 2007
```  
Results confirm **Bulengo Camp** (6km west of Goma) as a key site.  

**Step 3:**  
Open Google Earth Pro. Navigate to **Goma, DRC**. Use historical imagery (2008) to inspect terrain. Match the hill’s slope and sparse vegetation to the video’s background.  

**Step 4:**  
Compare with UN aerial photos (e.g., `media.un.org/photo/en/asset/oun7/oun7665714`). Align the tent’s position relative to the hill’s ridge and footpaths.  

**Step 5:**  
Verify coordinates using EXIF data from a 2014 IWMF photo of Bulengo Camp (`1°37'25"S 29°07'42"E`). Historical satellite imagery confirms tents clustered here in 2007.  

---

🎯 **Flag:**  
`AzCTF{1_37_25_S_29_07_42_E}`
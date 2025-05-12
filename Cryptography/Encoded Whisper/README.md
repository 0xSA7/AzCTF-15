# Encoded Whisper

**Difficulty:** Medium

**Category:** Crptography

---

### 📜 Story:

Amid the ongoing Halib Al-Khair investigation, strange outbound traffic was detected from the Az-SENCS internal mail server late at night. After tracing it, we discovered an encoded message transmitted using an unusual pattern of dashes and underscores clearly an attempt to avoid detection by traditional filters.

We suspect it's a hidden message sent by the rogue Highboard member. Your task is to decode this suspicious ciphertext and extract the real message before they go dark.

[CipherText](cipher.txt)  

---

### Hint:

1. Not mores code

2. Looks binary? Think like a machine:

* `_` = `1`
* `-` = `0`
* Group every 8 symbols into a byte and convert to ASCII.

---

### Flag:

```text
AzCTF{D0n't_use_@I_t00!z}
```
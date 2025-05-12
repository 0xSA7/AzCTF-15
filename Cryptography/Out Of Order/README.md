# **Out Of Order**  
**Difficulty:** Hard  
**Category:** Crypto  

---

## **Description**  
A message was encrypted using the Elgamal encryption scheme. The ciphertext, public key, and domain parameters are known. Your task is to decrypt the message.  

**Resources**:  
- [out_of_order.pcap](https://mega.nz/file/yBBSADBQ#X74Frkvx2pniXBqAb1xpOI3vm7iiB-b0kdIdXChvaGY)  

**Ciphertext**:  
```
(kE = 3, y = 15)
```

---

## **Hints**  
1. Understand the Elgamal encryption scheme.  
2. Use the provided public key and domain parameters to compute the private key.  
3. Decrypt the ciphertext using modular arithmetic.

---

## **Solution**  
<details>
<summary>Click to reveal the solution</summary>

### **Step-by-Step Walkthrough**  
1. **Understand Elgamal Encryption**:  
   - Public Key:  
     ```
     p = 467  
     alpha = 2  
     beta = 7
     ```
   - Encryption formula:  
     ```
     kE = alpha^i mod p  
     kM = beta^i mod p  
     y = x * kM mod p
     ```
   - Where `i` is the ephemeral key, `kM` is the masking key, and `x` is the plaintext.

2. **Recover the Masking Key `kM`**:  
   - Compute `kM` using the private key `d`:  
     ```
     kM = beta^i mod p = 7^i mod 467
     ```
   - Since `beta = alpha^d mod p`, we have `d = 103`.

3. **Decrypt the Ciphertext**:  
   - Compute the plaintext `x` using the masking key:  
     ```
     x = y * kM^-1 mod p
     ```
   - The result is:  
     ```
     x = 26
     ```

4. **Reveal the Flag**:  
   - The flag is:  
     ```
     AzCTF{Elgamal_decrypted}
     ```

</details>
# AzCTF: What is my type

Reverse Engineering Challenge

## Challenge Description
The program requires a username and password combination to reveal the flag. Your task is to find the correct credentials that will properly decrypt the hidden flag.

**Hint**: The program uses bitwise operations to transform your inputs. Pay close attention to how the verification algorithm works.

**Hints**: (Available Separately)
Level 1: "The verification algorithm uses bitwise operations"

Level 2: "Focus on the transformation between user input and final verification value"

Level 3: "The magic number is 0x6d"

Initial Hint: "The program uses XOR transformations at multiple levels"

Intermediate Hint: "The final verification value must equal the XOR key used for flag encryption"

Final Hint: "Target verification value: 109 (0x6d in hex)"

## How to Play
1. Compile the challenge:
   ```bash
   gcc -o challenge challenge.c
Run the program:

```bash
./challenge
Input your username and password when prompted
```

## Solution Approach
Analyze the binary to understand the verification logic

Reverse engineer the decryption algorithm

Calculate the required XOR key

Craft inputs that satisfy the verification conditions

Flag Format
The flag follows the format: AzCTF{...}

Note: This challenge tests your understanding of XOR operations and basic reverse engineering skills.


**How to use these files:**
1. Run `python challenge_creation.py` to generate the C code
2. Compile with `gcc -o challenge challenge.c`
3. Test with `./challenge` and try to input credentials
4. Verify the solution with `python solution.py | ./challenge`

The challenge works by:
1. XORing the flag with value 109 during compilation
2. Using user input to calculate a verification key (i2)
3. Only revealing the flag when i2 = 109
4. The solution requires sending specific null bytes and a calculated first password byte

The included solution works by creating inputs that cancel out all verification math except the critical first byte calculation.
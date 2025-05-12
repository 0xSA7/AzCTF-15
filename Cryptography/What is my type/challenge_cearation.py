FLAG = "AzCTF{1t's_reverse_bt_u_did_it}"
I2_CORRECT = 109  # XOR key to encrypt the flag

encrypted_flag = [ord(c) ^ I2_CORRECT for c in FLAG]

c_code = f'''
#include <stdio.h>
#include <unistd.h>

#define FLAGSIZE {len(FLAG)}

int readflag(int i2) {{
  char flag[FLAGSIZE] = {{{', '.join([f'0x{x:02x}' for x in encrypted_flag])}}};
  for (int i = 0; i < FLAGSIZE; i++) {{
    printf("%c", flag[i] ^ i2);
  }}
  putchar('\\n');
  return 0;
}}

int main() {{
  int i2 = 0;
  char password[9];
  char username[9];
  
  printf("Enter username (8 chars):\\n");
  read(0, username, 8);
  
  printf("Enter password (8 chars):\\n");
  read(0, password, 8);

  char result[9] = {{0}};
  
  for (int i = 0; i < 9; i++) {{
    result[i] = password[i] ^ username[i];
    i2 += result[i] - (i * 4);
  }}
  
  readflag(i2);
  return 0;
}}
'''

with open('challenge.c', 'w') as f:
    f.write(c_code.strip())

print("Challenge code generated. Compile with: gcc -o challenge challenge.c")
#include <stdio.h>
#include <unistd.h>

#define FLAGSIZE 31

int readflag(int i2) {
  char flag[FLAGSIZE] = {0x2c, 0x17, 0x2e, 0x39, 0x2b, 0x16, 0x5c, 0x19, 0x4a, 0x1e, 0x32, 0x1f, 0x08, 0x1b, 0x08, 0x1f, 0x1e, 0x08, 0x32, 0x0f, 0x19, 0x32, 0x18, 0x32, 0x09, 0x04, 0x09, 0x32, 0x04, 0x19, 0x10};
  for (int i = 0; i < FLAGSIZE; i++) {
    printf("%c", flag[i] ^ i2);
  }
  putchar('\n');
  return 0;
}

int main() {
  int i2 = 0;
  char password[9];
  char username[9];
  
  printf("Enter username (8 chars):\n");
  read(0, username, 8);
  
  printf("Enter password (8 chars):\n");
  read(0, password, 8);

  char result[9] = {0};
  
  for (int i = 0; i < 9; i++) {
    result[i] = password[i] ^ username[i];
    i2 += result[i] - (i * 4);
  }
  
  readflag(i2);
  return 0;
}
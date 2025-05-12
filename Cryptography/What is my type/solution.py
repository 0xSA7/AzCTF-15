import sys

# Generate payload to produce i2 = 109 (0x6d)
username = b"\x00" * 8  # Null username
password = bytes([0xfd]) + b"\x00" * 7  # First byte 0xfd, rest null

# Send both inputs without newlines
sys.stdout.buffer.write(username + password)
sys.stdout.buffer.flush()
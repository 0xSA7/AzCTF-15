# Extract hidden message from WAV audio (reverse of HiddinWave Ver 1.0)
import wave

def extract_message(stego_audio_path):
    print("[*] Extracting secret message...")
    with wave.open(stego_audio_path, mode='rb') as waveaudio:
        frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))
        extracted_bits = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
        extracted_bytes = [extracted_bits[i:i+8] for i in range(0, len(extracted_bits), 8)]
        decoded_chars = [chr(int(''.join(map(str, byte)), 2)) for byte in extracted_bytes]
        message = ''.join(decoded_chars)
        secret_message = message.split("###")[0]  # Stop at padding
        print("\n[+] Secret Message Found:\n")
        print(secret_message)

# Example usage:
# extract_message("output.wav")

# If using argparse:
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract hidden text from WAV audio")
    parser.add_argument('-f', '--file', help='Path to stego audio file', required=True)
    args = parser.parse_args()
    extract_message(args.file)

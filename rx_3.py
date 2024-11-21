import subprocess
import serial

port = 'COM15'
baudrate = 460800
# Function to convert PCM byte array to MP3
def pcm_bytes_to_mp3(pcm_data_bytes, mp3_file, sample_rate=23040, channels=1, bit_depth=16):
    
    command = [
        'ffmpeg',
        '-f', 's16le',
        '-ar', str(23040),
        '-ac', str(1),
        '-i', 'pipe:0',
        '-codec:a', 'libmp3lame',
        '-qscale:a', '2',
        mp3_file
    ]

    try:
        process = subprocess.run(
            command,
            input=pcm_data_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        print(f"PCM to MP3 conversion successful! The MP3 file is saved as {mp3_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e.stderr.decode('utf-8')}")

# Function to read PCM data from UART
def read_pcm_from_uart(port, baudrate, max_bytes=100000):
    
    pcm_data = bytearray()
    received = 0

    with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
        print(f"Connected to {port} at {baudrate} baud.")
        print("Waiting for data... (Press Ctrl+C to stop)")

        while received < 100000:
            bytes_available = ser.in_waiting
            if bytes_available > 0:
                data = ser.read(bytes_available)
                print(data)
                print(f"Received ({bytes_available} bytes): {data}")
                pcm_data.extend(data)
                received += bytes_available
                print(f"Total bytes received: {received}")

        print("Finished reading data from UART.")
    return bytes(pcm_data)

# Main function
def main():
    # Configuration
    port = 'COM15'  # UART port
    baudrate = 460800  # Baudrate
    output_mp3_file = "output12.mp3"  # Output MP3 file

    # Step 1: Read PCM data from UART
    print("Step 1: Reading PCM data from UART...")
    pcm_data = read_pcm_from_uart(port, baudrate)

    # Step 2: Convert PCM data to MP3
    print("Step 2: Converting PCM data to MP3...")
    pcm_bytes_to_mp3(
        pcm_data_bytes=pcm_data,
        mp3_file=output_mp3_file,
        sample_rate=23040,
        channels=1,
        bit_depth=16
    )

# Run the main function
if __name__ == "__main__":
    main()

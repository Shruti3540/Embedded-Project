import serial
import subprocess

def write_binary_file(file_path, data):
    """
    Writes binary data to a file.
    """
    with open(file_path, 'wb') as file:
        file.write(data)

def decompress_video_from_h264(input_video_path, output_decompressed_path):
    """
    Decompresses a video from H.264 format using FFmpeg.
    """
    process = subprocess.run(
        [
            'ffmpeg',
            '-i', input_video_path,      # Input compressed video file
            '-c:v', 'libx264',            # Use H.264 codec
            '-preset', 'fast',            # Compression speed
            '-y',                         # Overwrite output file
            output_decompressed_path      # Decompressed video output file
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if process.returncode != 0:
        print(f"Error during decompression: {process.stderr.decode()}")
        return False

    print(f"Video decompressed successfully: {output_decompressed_path}")
    return True


def receive_video_over_uart(port, baudrate, expected_size):
    
    received = 0
    video_data = bytearray()  # To store the received data

    try:
        with serial.Serial(port, baudrate=baudrate, timeout=1) as ser:
            print(f"Connected to {port} at {baudrate} baud.")
            print(f"Receiving video data...")

            # Receive compressed video data
            while received < expected_size:
                bytes_available = ser.in_waiting
                data = ser.read(bytes_available)
                #if not data:
                    #print("No data received. Waiting...")
                    #continue
                video_data.extend(data)
                received += len(data)
                print(f"Received {received}/{expected_size} bytes.")

            print(f"Video data reception complete. Total received: {received} bytes.")
        return bytes(video_data)
    
    except Exception as e:
        print(f"Error receiving video data: {e}")
        return bytes()

# Main function
def main():
    # Configuration
    port = "COM7"                           # UART port (adjust as needed)
    baudrate = 115200                        # Baud rate
    expected_size = 193613                   # Size of the compressed video data (update as needed)
    compressed_video_file = "received.h264"  # Path for received compressed video
    decompressed_video_file = "output8_video.mp4"  # Path for decompressed video

    # Step 1: Receive the compressed video data over UART
    print("Step 1: Receiving video over UART...")
    video_data = receive_video_over_uart(port, baudrate, expected_size)

    if not video_data:
        print("No video data received. Exiting.")
        return

    # Step 2: Save the received compressed video data to file
    print("Step 2: Saving received compressed video data...")
    write_binary_file(compressed_video_file, video_data)

    # Step 3: Decompress the received video
    print("Step 3: Decompressing the received video...")
    success = decompress_video_from_h264(compressed_video_file, decompressed_video_file)

    if success:
        print("Video decompressed successfully. Playing the video...")

        # Step 4: Play the decompressed video
        try:
            subprocess.run(["ffplay", decompressed_video_file])
        except Exception as e:
            print(f"Error playing video: {e}")

# Run the main function
if __name__ == "__main__":
    main()

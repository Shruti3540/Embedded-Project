import serial
import time
import subprocess


def compress_video_to_h264(input_video_path, output_compressed_path, width, height, frame_rate):
    """
    Compresses a video file to H.264 format using FFmpeg.
    """
    process = subprocess.run(
        [
            'ffmpeg',
            '-i', input_video_path,          # Input video file
            '-vf', f'scale={width}:{height}', # Resize to specified resolution
            '-r', str(frame_rate),            # Set frame rate
            '-c:v', 'libx264',                # Use H.264 codec for compression
            '-crf', '28',                     # Compression quality
            '-preset', 'fast',                # Compression speed
            '-y',                             # Overwrite output file
            output_compressed_path            # Compressed video file output
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    if process.returncode != 0:
        print(f"Error during compression: {process.stderr.decode()}")
        return False

    print(f"Video compressed successfully: {output_compressed_path}")
    return True


def read_binary_file(file_path):
    """
    Reads a file as binary data.
    """
    with open(file_path, 'rb') as file:
        return file.read()


if __name__ == "__main__":
    # Video Configuration
    input_video_path = r"video.mp4"        # Input video file
    output_compressed_path = "compressed.h264" # Compressed video output file
    width, height = 640, 480                  # Resolution
    frame_rate = 30                           # Frame rate

    # UART Configuration
    uart_port = 'COM7'                       # Adjust for your system
    baudrate = 115200                         # Baud rate

    # Step 1: Compress the video
    print("Step 1: Compressing the video...")
    success = compress_video_to_h264(input_video_path, output_compressed_path, width, height, frame_rate)

    if success:
        # Step 2: Read compressed video data
        print("Step 2: Reading compressed video data...")
        compressed_video_data = read_binary_file(output_compressed_path)

        # Step 3: Transmit the compressed video data over UART
        try:
            ser = serial.Serial(uart_port, baudrate=baudrate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            print(f"Connected to {uart_port} at {baudrate} baud.")
            
            total_bytes = len(compressed_video_data)
            print(f"Total data to transmit: {total_bytes} bytes")

            # Transmit data byte-by-byte
            for i, byte in enumerate(compressed_video_data):
                ser.write(byte.to_bytes(1, 'little'))  # Send single byte
                time.sleep(0.00001)  # Optional delay to prevent UART overflow
                if (i + 1) % 1000 == 0:
                    print(f"Sent {i + 1}/{total_bytes} bytes.")

            print("Video transmission completed.")
            ser.close()
        except Exception as e:
            print(f"Error during UART transmission: {e}")

import serial
import time
import struct
import subprocess

# Function to read MP4 file as bytes
def read_mp4_as_bytes(mp4_file):
    with open(mp4_file, "rb") as file:
        mp4_bytes = file.read()
        print(mp4_bytes)
        print(f"MP4 file size in bytes: {len(mp4_bytes)}")
    return mp4_bytes
    






# def read_mp4_as_bytes(mp4_file):
#     video_file = "sec_1_nm.mp4"

# # FFmpeg command to convert video to raw bytes (RGB24 format)
#     command = [
#         "ffmpeg",
#         "-i", mp4_file,          # Input file
#         "-f", "rawvideo",          # Output format: raw video
#         "-pix_fmt", "rgb24",       # Pixel format: RGB24
#         "-an",                     # Disable audio
#         "pipe:1"                   # Output to stdout
#     ]

#     # Run FFmpeg as a subprocess
#     process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#     # Read video bytes
#     video_bytes, error = process.communicate()

#     # Check for errors
#     if process.returncode != 0:
#         print("FFmpeg error:", error.decode())
#     else:
#         print(f"Video converted to {len(video_bytes)} bytes")
    
#     return video_bytes


if __name__ == "__main__":
    mp4_file = "sec_1_namo.mp4"  # Path to the MP4 file
    uart_port = 'COM13'  # UART port
    baud_rate = 38400  # Baud rate

    # Read the MP4 file as bytes
    #pcm_data_bytes = read_mp4_as_bytes(mp4_file)
    #print(pcm_data_bytes)
    #print(pcm_data_bytes[10])
    
    # Open the serial port
    ser = serial.Serial('COM13', baudrate = 38400, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)

    # for i in range(0, 110000):
    #     ser.write(pcm_data_bytes[i].to_bytes(1, 'little'))
    #     time.sleep(0.00000001)
    #     #ser.write(pcm_data_bytes[i])
    #     print(f"Sent byte {i+1}: {pcm_data_bytes[i]}")

    
    # for i, byte in enumerate(pcm_data_bytes):
    #     ser.write(byte.to_bytes(1, 'little'))  # Convert to single-byte before sending
    #     #ser.write(b'\0x02\0x33')
    #     #time.sleep(0.00000001)  # Optional delay, adjust as needed
    #     print(f"Sent byte {i+1}: {hex(byte)}")
    # ser.close()  
    
    #for i in range(0, 10):
    #     ser.write(b'\xA1')
    #print(type(pcm_data_bytes))
    # for i, byte in enumerate(pcm_data_bytes):
    #     if i>15:
    #         break
    #     packed_byte = struct.pack("B", byte)  # Pack a single byte (unsigned char)
    #     ser.write(packed_byte)
    #     time.sleep(0.000001)  # Adjust the delay as needed
    #     print(packed_byte)
    # for i in range (0, 10):
    #     ser.write(b'\xaa')
    #     time.sleep(1)
    for i in range(0, 10):
        ser.write(b'\xA1')
    ser.close()
        
        


    
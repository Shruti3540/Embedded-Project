import serial
import time
import subprocess

#ser = serial.Serial('COM10', baudrate = 115200, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)




def mp3_to_pcm_bytes(mp3_file_path):
    
    process = subprocess.Popen(
             ['ffmpeg', '-i', mp3_file_path, '-f', 's16le', '-ar', '23040', '-ac', '1', '-'],
             stdout=subprocess.PIPE, stderr=subprocess.PIPE
         )
    
    raw_pcm_data, stderr = process.communicate()
    if process.returncode != 0:
             print(f"Error in converting MP3 to PCM: {stderr.decode()}")
             return None

    print("Successfully converted MP3 to raw PCM data.")
    return raw_pcm_data


def send_data_uart(uart_port, data_bytes):
    """Sends byte data over UART using pyserial."""
    # Set up the serial communication
    ser = serial.Serial(uart_port, 460800, timeout=1)  # Adjust baud rate if needed

    # Send the byte data over UART
    ser.write(data_bytes)
    ser.flush()  # Ensure the data is sent
    time.sleep(1)  # Wait for the data to be transmitted

    # Close the serial connection
    ser.close()
    print("Data sent successfully!")


if __name__ == "__main__":
    mp3_file_path = r"C:/Users/shrut/Downloads/sec_7_nm.mp3"  # Replace with your file path
    
    uart_port = 'COM13'  # Adjust this as per your system (e.g., COM1, COM2, etc.)

    #ser.write(pcm_data_bytes)
    ser = serial.Serial('COM13', baudrate = 460800, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE)
    pcm_data_bytes = mp3_to_pcm_bytes(mp3_file_path)
    pcm_size = len(pcm_data_bytes)
    print(pcm_size)
    #
    #pcm_data_bytes = b'\x0c\xf9a\xfe&\x07\xa4\x06j\x05\xe4\x03\x86'
    ser.write(pcm_data_bytes)
    print(pcm_data_bytes)
    # for i in range(100):
    #     ser.write(b'\xA1')
    #     time.sleep(1)
    #     ser.write(b'\x00')
    #     print("looping")
    ser.close()
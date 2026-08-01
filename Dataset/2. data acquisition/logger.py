import serial
import csv
import time
import sys

# --- CONFIGURATION ---
SERIAL_PORT = 'COM7'   # Replace with your ESP32's Port (e.g., /dev/ttyUSB0 on Linux/Mac)
BAUD_RATE = 115200
OUTPUT_FILE = 'Normal2_data.csv'
MAX_SAMPLES = 2000     # Number of samples to collect (approx 40 seconds at 50Hz)
# ---------------------

def collect_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT}")
    except serial.SerialException:
        print(f"Error: Could not open serial port {SERIAL_PORT}")
        sys.exit(1)

    print(f"Logging data to {OUTPUT_FILE}...")
    
    with open(OUTPUT_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write Header for Edge Impulse
        writer.writerow(['timestamp', 'accX', 'accY', 'accZ', 'gyroX', 'gyroY', 'gyroZ'])
        
        samples_collected = 0
        
        # Flush initial buffer
        ser.reset_input_buffer()
        
        try:
            while samples_collected < MAX_SAMPLES:
                line = ser.readline().decode('utf-8').strip()
                
                # Filter out non-data lines (like "CONNECTED")
                if line and ',' in line:
                    parts = line.split(',')
                    if len(parts) == 7: # Ensure complete packet
                        writer.writerow(parts)
                        samples_collected += 1
                        if samples_collected % 50 == 0:
                            print(f"Collected {samples_collected}/{MAX_SAMPLES} samples")
                
        except KeyboardInterrupt:
            print("\nRecording stopped by user.")
            
    print("Data collection complete.")
    ser.close()

if __name__ == "__main__":
    collect_data()
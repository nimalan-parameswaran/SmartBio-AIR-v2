/*
 * MYOSA Data Collector for Edge Impulse
 * Hardware: MYOSA ESP32, AccelAndGyro (MPU6050), 6V DC Motor/Pump
 * Output: CSV-formatted stream over Serial at 115200 baud
 */

#include <AccelAndGyro.h>

// Configuration
#define SERIAL_BAUD_RATE 115200
#define SAMPLING_FREQ_HZ 50
#define SAMPLING_PERIOD_MS (1000 / SAMPLING_FREQ_HZ)

// Motor Pin (Configure based on your physical connection)
// If utilizing a transistor/MOSFET for the 6V motor driven by a GPIO:
#define MOTOR_PIN 25 

// Create Sensor Object
AccelAndGyro Ag;

void setup() {
  // Initialize Serial Communication
  Serial.begin(SERIAL_BAUD_RATE);
  
  // Initialize I2C (Required for MYOSA Sensors)
  Wire.begin();
  Wire.setClock(100000); // 100kHz I2C Clock

  // Initialize Motor (Turn ON for data collection context)
  pinMode(MOTOR_PIN, OUTPUT);
  digitalWrite(MOTOR_PIN, HIGH); 

  // Initialize Sensor
  // Loop until connected
  while(true) {
    if(Ag.begin()) {
      Serial.println("CONNECTED: AccelAndGyro");
      break;
    }
    Serial.println("WAITING: AccelAndGyro");
    delay(500);
  }
}

void loop() {
  unsigned long loopStartTime = millis();

  // Check sensor connection
  if (Ag.ping()) {
    // Retrieve data with print=false to get raw float values
    // Library returns acceleration in cm/s^2. Convert to m/s^2 for standard ML.
    float ax = Ag.getAccelX(false) / 100.0f;
    float ay = Ag.getAccelY(false) / 100.0f;
    float az = Ag.getAccelZ(false) / 100.0f;
    
    // Library returns gyro in deg/s
    float gx = Ag.getGyroX(false);
    float gy = Ag.getGyroY(false);
    float gz = Ag.getGyroZ(false);

    // Stream Data: timestamp, accX, accY, accZ, gyroX, gyroY, gyroZ
    Serial.print(loopStartTime);
    Serial.print(",");
    Serial.print(ax, 4);
    Serial.print(",");
    Serial.print(ay, 4);
    Serial.print(",");
    Serial.print(az, 4);
    Serial.print(",");
    Serial.print(gx, 4);
    Serial.print(",");
    Serial.print(gy, 4);
    Serial.print(",");
    Serial.println(gz, 4);
  }

  // Enforce Sampling Frequency
  unsigned long loopEndTime = millis();
  unsigned long elapsedTime = loopEndTime - loopStartTime;
  if (elapsedTime < SAMPLING_PERIOD_MS) {
    delay(SAMPLING_PERIOD_MS - elapsedTime);
  }
}
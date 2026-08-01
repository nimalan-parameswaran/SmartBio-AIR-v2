/*
 * Project: Algae-Based Air Purification System (Step 1 Firmware)
 * Hardware: MYOSA ESP32, MPU6050, APDS9960, BMP180, MQ Sensors, L298N, OLED
 * Description: Acquires sensor data, runs Edge Impulse inference for motor health, 
 * communicates with Azure, and controls pump/display.
 */

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// --- MYOSA Libraries ---
#include <AccelAndGyro.h>
#include <LightProximityAndGesture.h>
#include <BarometricPressure.h>
#include <oled.h>

// --- Edge Impulse Library ---
// Ensure you have imported your Edge Impulse library .zip
#include <MYOSA-6vDMP-Fault-Detection_inferencing.h>

// --- WiFi Credentials ---
const char* ssid = "WIFI_SSID";
const char* password = "WIFI_PASSWORD";

// --- Azure Function Endpoint ---
// You will update this URL in Step 2 after deploying the Azure Function
String azureEndpoint = "KEY"; 

// --- Pin Definitions ---
// Note: ADC2 pins cannot be used when WiFi is active. Use ADC1 (GPIO 32-39).
#define PIN_MQ135       34 
#define PIN_MQ_GENERIC  35 // Shared analog line for MQ-2/3/7 or separate pins if available
#define PIN_MOTOR_ENA   14
#define PIN_MOTOR_IN1   27
#define PIN_MOTOR_IN2   26

// --- Sensor Objects ---
AccelAndGyro imu;
LightProximityAndGesture apds;
BarometricPressure bmp;
oLed display(128, 64); // Standard 0.96" OLED size

// --- Global Variables ---
float ax, ay, az;
float temperature_mpu;
uint16_t green_light_val;
float pressure_pa;
int mq135_val;
int mq_generic_val;
int motor_fault_status = 0; // 0: Normal, 1: Fault
int pump_speed = 0;         // 0-255
String ai_summary = "Initializing...";
String algae_status = "Scanning...";
String aq_status = "Unknown";
int aq_score = 0;

// --- Edge Impulse Configuration ---
#define EI_CLASSIFIER_SENSOR_AXES_COUNT 3
#define EI_CLASSIFIER_FREQUENCY 62.5 // Check your Impulse design frequency (e.g. 62.5Hz)
// Buffer to hold raw data for inference
static float features[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE];

void setup() {
  Serial.begin(115200);

  // 1. Initialize Motor Pins
  pinMode(PIN_MOTOR_ENA, OUTPUT);
  pinMode(PIN_MOTOR_IN1, OUTPUT);
  pinMode(PIN_MOTOR_IN2, OUTPUT);
  digitalWrite(PIN_MOTOR_IN1, LOW);
  digitalWrite(PIN_MOTOR_IN2, LOW); // Motor Off initially

  // 2. Initialize OLED
  if (!display.begin()) {
    Serial.println("OLED init failed");
  }
  display.clearDisplay();
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0, 0);
  display.println("MYOSA Purifier");
  display.println("Booting...");
  display.display();

  // 3. Initialize Sensors (MYOSA Libraries)
  // MPU6050
  if (imu.begin()) {
    Serial.println("MPU6050 Connected");
  } else {
    Serial.println("MPU6050 Failed");
  }

  // APDS9960
  if (apds.begin()) {
    Serial.println("APDS9960 Connected");
    apds.enableAmbientLightSensor(DISABLE); // Enable ALS for Green Channel
  } else {
    Serial.println("APDS9960 Failed");
  }

  // BMP180
  if (bmp.begin()) {
    Serial.println("BMP180 Connected");
  } else {
    Serial.println("BMP180 Failed");
  }

  // 4. Connect to WiFi
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi Connected");
  
  display.println("WiFi OK");
  display.display();
  delay(1000);
}

void loop() {
  // --- 1. Acquire Data ---
  acquireSensorData();

  // --- 2. Edge Impulse Inference ---
  // We collect a short buffer of vibration data for the motor check
  runMotorInference();

  // --- 3. Cloud Sync (Azure) ---
  syncWithAzure();

  // --- 4. Update Display & Actuators ---
  updateDisplay();
  controlMotor();

  // Wait before next cycle (e.g., 5 seconds)
  delay(5000); 
}

void acquireSensorData() {
  // Read Environmental Data
  bmp.getPressurePascal(false); // Update internal read
  pressure_pa = bmp.getPressurePascal(false);
  
  // Read Algae Color Indicator (Green Light)
  // APDS library requires reading ambient light first to update registers
  uint16_t amb;
  apds.readAmbientLight(&amb);
  green_light_val = apds.getGreenProportion(); 

  // Read Analog Gas Sensors
  mq135_val = analogRead(PIN_MQ135);
  mq_generic_val = analogRead(PIN_MQ_GENERIC);

  Serial.printf("P: %.2f Pa, G: %d, MQ135: %d\n", pressure_pa, green_light_val, mq135_val);
}

// Function to collect data and run Edge Impulse Classifier
void runMotorInference() {
  // We need to fill the feature buffer with vibration data (Accelerometer X, Y, Z)
  // Note: This is a blocking loop to fill the buffer exactly as the model expects.
  // Ideally, use a timer interrupt, but for simplicity in Step 1, we block.
  
  long frame_start_time;
  
  for (size_t i = 0; i < EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE; i += EI_CLASSIFIER_SENSOR_AXES_COUNT) {
      frame_start_time = micros();

      // Get raw accel data
      features[i + 0] = imu.getAccelX(false);
      features[i + 1] = imu.getAccelY(false);
      features[i + 2] = imu.getAccelZ(false);

      // Ensure sampling frequency is respected
      long time_taken = micros() - frame_start_time;
      long delay_us = (1000000 / EI_CLASSIFIER_FREQUENCY) - time_taken;
      if (delay_us > 0) {
          delayMicroseconds(delay_us);
      }
  }

  // Create signal from buffer
  signal_t signal;
  int err = numpy::signal_from_buffer(features, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
  if (err != 0) {
      Serial.printf("ERR: signal_from_buffer failed (%d)\n", err);
      return;
  }

  // Run classifier
  ei_impulse_result_t result = { 0 };
  err = run_classifier(&signal, &result, false /* debug */);
  if (err != EI_IMPULSE_OK) {
      Serial.printf("ERR: run_classifier failed (%d)\n", err);
      return;
  }

  // Analyze result
  // Assuming Class 0 = Normal, Class 1 = Fault
  // We check the confidence score.
  float fault_confidence = result.classification[1].value; // Index depends on your impulse classes
  
  if (fault_confidence > 0.7) {
    motor_fault_status = 1; // Fault detected
  } else {
    motor_fault_status = 0; // Normal
  }
  
  // Read temp from MPU as secondary health check
  temperature_mpu = imu.getTempC(false);
}

void syncWithAzure() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(azureEndpoint);
    http.addHeader("Content-Type", "application/json");

    // Prepare JSON Payload
    StaticJsonDocument<512> doc;
    doc["deviceId"] = "MYOSA_ESP32_01";
    doc["pressure"] = pressure_pa;
    doc["temp_mpu"] = temperature_mpu;
    doc["mq135"] = mq135_val;
    doc["mq_generic"] = mq_generic_val;
    doc["green_light"] = green_light_val;
    doc["motor_fault"] = motor_fault_status;

    String requestBody;
    serializeJson(doc, requestBody);

    // POST Data
    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println("Azure Response: " + response);
      
      // Parse Response (Expected JSON from Agent 1)
      // Example: {"motor_speed": 150, "ai_summary": "AQ improving", "algae_state": "Healthy", "aq_score": 85, "aq_status": "Good"}
      StaticJsonDocument<512> respDoc;
      DeserializationError error = deserializeJson(respDoc, response);
      if (!error) {
        pump_speed = respDoc["motor_speed"];
        const char* summary = respDoc["ai_summary"];
        const char* algae = respDoc["algae_state"];
        const char* status = respDoc["aq_status"];
        
        ai_summary = String(summary);
        algae_status = String(algae);
        aq_status = String(status);
        aq_score = respDoc["aq_score"];
      }
    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
    }
    http.end();
  }
}

void updateDisplay() {
  display.clearDisplay();

  // If Motor Fault is detected, override display with warning
  if (motor_fault_status == 1) {
    display.setTextSize(2);
    display.setCursor(10, 20);
    display.println("MOTOR");
    display.setCursor(10, 40);
    display.println("FAULT!");
    display.display();
    return;
  }

  // Normal Interface
  display.setTextSize(1);
  display.setCursor(0, 0);
  
  // Row 1: AQ Score & Status
  display.print("AQ: "); display.print(aq_score);
  display.print(" | "); display.println(aq_status);
  
  // Row 2: Separator
  display.drawLine(0, 9, 128, 9, SSD1306_WHITE);
  display.setCursor(0, 12);
  
  // Row 3: Algae Status
  display.print("Algae: "); display.println(algae_status);
  
  // Row 4: Pump Speed
  display.print("Pump: "); 
  display.print(map(pump_speed, 0, 255, 0, 100)); // Show %
  display.println("%");

  // Row 5: AI Summary (scrolling or truncated)
  display.setCursor(0, 45);
  display.println(ai_summary);

  display.display();
}

void controlMotor() {
  // If fault is detected, stop motor immediately
  if (motor_fault_status == 1) {
    digitalWrite(PIN_MOTOR_IN1, LOW);
    digitalWrite(PIN_MOTOR_IN2, LOW);
    analogWrite(PIN_MOTOR_ENA, 0);
  } else {
    // Standard operation driven by Azure Agent 1 decision
    digitalWrite(PIN_MOTOR_IN1, HIGH);
    digitalWrite(PIN_MOTOR_IN2, LOW);
    analogWrite(PIN_MOTOR_ENA, pump_speed);
  }
}

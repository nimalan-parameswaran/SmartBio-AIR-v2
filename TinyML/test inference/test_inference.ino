/*
 * MYOSA Real-Time Fault Detection (Motor Pump)
 * Hardware: MYOSA ESP32 Controller + Accelerometer/Gyroscope (MPU6050)
 * Model: Edge Impulse EON Classifier (Motion Classification)
 * * Requirements:
 * - MYOSA AccelAndGyro library
 * - ei-myosa-6vdmp-fault-detection-arduino library
 */

#include <MYOSA-6vDMP-Fault-Detection_inferencing.h>
#include <AccelAndGyro.h>
#include <Wire.h>

AccelAndGyro Ag;

// MYOSA library returns cm/s^2, EI expects m/s^2
#define ACCEL_DIVIDER 100.0f 

float features[EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE];

void setup() {
    Serial.begin(115200);
    while (!Serial);
    
    // --- FIX START ---
    // Initialize I2C communication for MYOSA sensors
    Wire.begin();           
    Wire.setClock(100000);  
    // --- FIX END ---

    Serial.println("MYOSA Real-Time Fault Detection System");
    Serial.print("Initializing Sensor...");

    // Retry loop until connected
    while (true) {
        if (Ag.begin()) {
            Serial.println("Connected!");
            break;
        }
        Serial.print(".");
        delay(500);
    }
}

void loop() {
    ei_printf("\nStarting sampling...\n");

    // Calculate delay (e.g. 62.5Hz = 16000 microseconds)
    float time_between_samples_us = (1000000.0f / EI_CLASSIFIER_FREQUENCY);

    for (size_t i = 0; i < EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE; i += EI_CLASSIFIER_RAW_SAMPLES_PER_FRAME) {
        uint64_t next_tick = micros() + (uint64_t)time_between_samples_us;

        // Read Raw Data (false = do not print to serial)
        float ax = Ag.getAccelX(false);
        float ay = Ag.getAccelY(false);
        float az = Ag.getAccelZ(false);
        float gx = Ag.getGyroX(false);
        float gy = Ag.getGyroY(false);
        float gz = Ag.getGyroZ(false);

        // Convert and fill buffer
        features[i + 0] = ax / ACCEL_DIVIDER;
        features[i + 1] = ay / ACCEL_DIVIDER;
        features[i + 2] = az / ACCEL_DIVIDER;
        features[i + 3] = gx; 
        features[i + 4] = gy;
        features[i + 5] = gz;

        while (micros() < next_tick) {
            // Busy wait for precise timing
        }
    }

    // Inference
    ei_impulse_result_t result = { 0 };
    signal_t signal;
    
    int err = numpy::signal_from_buffer(features, EI_CLASSIFIER_DSP_INPUT_FRAME_SIZE, &signal);
    if (err != 0) {
        ei_printf("ERR: Signal creation failed (%d)\n", err);
        return;
    }

    EI_IMPULSE_ERROR res = run_classifier(&signal, &result, false);
    if (res != EI_IMPULSE_OK) {
        ei_printf("ERR: Classifier failed (%d)\n", res);
        return;
    }

    // Prediction Output
    int best_idx = -1;
    float best_val = -1.0;

    for (size_t ix = 0; ix < EI_CLASSIFIER_LABEL_COUNT; ix++) {
        if (result.classification[ix].value > best_val) {
            best_val = result.classification[ix].value;
            best_idx = ix;
        }
    }

    String labelStr = String(result.classification[best_idx].label);
    labelStr.toLowerCase();

    if (labelStr.indexOf("normal") >= 0 || labelStr == "0") {
        Serial.println(">>> STATUS: NORMAL OPERATION");
    } 
    else if (labelStr.indexOf("fault") >= 0 || labelStr == "1") {
        Serial.println(">>> STATUS: !! FAULT DETECTED !!");
    }
    else {
        Serial.print(">>> STATUS: ");
        Serial.println(result.classification[best_idx].label);
    }
    
    delay(100); 
}
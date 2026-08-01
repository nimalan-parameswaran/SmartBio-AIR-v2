# TinyML Motor Pump Fault Detection  
**Normal vs Fault Classification using Edge Impulse**

https://github.com/user-attachments/assets/3eb5bc1c-ce33-423c-a051-8dfc26945e4b

---

## 1. Project Overview

This project presents a TinyML-based classification system for identifying **Normal** and **Fault** operating conditions of a **6V DC Motor Air Pump**.  
The complete pipeline is implemented using **Edge Impulse**, covering data ingestion, feature extraction, model training, evaluation, and embedded deployment.

The trained model is intended for real-time motor health monitoring on microcontroller platforms with constrained memory and power limits.

---

## 2. Dataset Description

The dataset consists of time-series sensor readings captured from the air pump under controlled operating conditions.

### Dataset Composition

| Class  | Samples |
|------|---------|
| Normal | 4000 |
| Fault  | 4000 |
| **Total** | **8000** |

The dataset is balanced across both classes.

### Data Split Strategy

- **Training + Validation:** 80%
- **Testing:** 20%

Internal split of training data:
- **Training:** 70%
- **Validation:** 10%

This split supports stable convergence and unbiased testing.

---

## 3. Data Upload to Edge Impulse

### Workflow

1. A new Edge Impulse project was created.
2. Raw sensor files were uploaded using the **Data Acquisition** interface.
3. Each sample was labeled as `normal` or `fault`.
4. Sample distribution and signal quality were verified.
5. Edge Impulse automatically assigned samples to training and test sets.

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/1.png" width="600">
</p>

---

## 4. Impulse Design

### 4.1 Create Impulse

The impulse defines the end-to-end data flow from raw input to classification output.

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/2.png" width="600">
</p>

The impulse consists of:
- **Input Block:** Raw sensor signal
- **Processing Block:** Feature extraction
- **Learning Block:** Neural network classifier

---

### 4.2 Raw Data Configuration

Sensor parameters were configured according to the acquisition setup.

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/3.png" width="600">
</p>

---

### 4.3 Feature Generation

Statistical and signal-domain features were extracted from the raw input.

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/4.png" width="600">
</p>

Feature inspection confirmed class separability before training.

---

### 4.4 Classifier Configuration

A neural network classifier was configured within Edge Impulse.

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/5.png" width="600">
</p>

---

## 5. Model Training Results

### Training Metrics

- **Training Accuracy:** 98.1%
- **Training Loss:** 0.06

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/6.1.png" width="600">
</p>

---

### Class-wise Performance

| Class | Precision | Recall | F1 Score |
|-----|----------|--------|----------|
| Normal | 0.97 | 0.98 | 0.97 |
| Fault | 0.98 | 0.98 | 0.98 |

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/6.2.png" width="600">
</p>

---

### Aggregate Metrics

- **Area under ROC Curve:** 0.98  
- **Weighted Precision:** 0.98  
- **Weighted Recall:** 0.98  
- **Weighted F1 Score:** 0.98  

### Confusion Matrix (%)

| Actual \ Predicted | Normal | Fault | Uncertain |
|------------------|--------|-------|-----------|
| Normal | 95.9% | 2.5% | 1.6% |
| Fault | 1.0% | 98.5% | 0.5% |

---

## 6. Model Testing Results

- **Test Accuracy:** 97.23%

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/7.png" width="600">
</p>

### Test Metrics

- **Area under ROC Curve:** 0.98  
- **Weighted Precision:** 0.98  
- **Weighted Recall:** 0.98  
- **Weighted F1 Score:** 0.98  

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/8.png" width="600">
</p>

The evaluation confirms stable behaviour on unseen samples.

---

## 7. Deployment Configuration

### Selected Deployment Option

- **Arduino Library**
- Offline execution
- Low inference latency
- Reduced memory footprint

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/9.png" width="600">
</p>

---

## 8. TensorFlow Lite Model Export

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/10.png" width="600">
</p>

### Quantized Model (INT8)

| Parameter | Value |
|--------|------|
| Inference Time | 1 ms |
| RAM Usage | 3.0 KB |
| Flash Usage | 34.4 KB |
| Accuracy | 97.60% |

### Float Model (FP32)

| Parameter | Value |
|--------|------|
| Inference Time | 1 ms |
| RAM Usage | 3.1 KB |
| Flash Usage | 35.0 KB |
| Accuracy | 97.23% |

**Target Hardware:** @MYOSA-EPS32

---

## 9. MYOSA Deployment

<p align="left">
  <img src="https://github.com/nimalan-parameswaran/SmartBio-Air/blob/main/TinyML_MotorPumpFaultDetection/src/11.png" width="600">
</p>

### Deployment Steps

1. The Arduino library was downloaded from Edge Impulse.
2. The library was added to the Arduino IDE.
3. The inference example sketch was opened.
4. The MYOSA board, motor, and sensors were connected.
5. Classification results were observed through the Serial Monitor.

---

## 10. Directory Structure

```TinyML_MotorPumpFaultDetection/


├── FaultDetection_Inferencing/
│ ├── Test_interface.ino
├── FaultDetection_ModelFile/
│ ├── ei-myosa-6vdmp-fault-detection-arduino-1.0.2-TFlite.zip !use 
│ ├── ei-myosa-6vdmp-fault-detection-arduino-1.0.2-EON.zip
├── src/
│ ├── 1.png
│ ├── 2.png
│ ├── ...
└── README.md
```


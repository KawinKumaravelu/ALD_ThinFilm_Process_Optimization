# ALD Thin-Film Process Optimization

## Overview

This project focuses on **data-driven optimization of Atomic Layer Deposition (ALD)** processes to improve thin-film quality, uniformity, process stability, and yield.

## Key Parameters

* Substrate temperature
* Precursor pulse time
* Purge time
* Reactant pulse time
* Chamber pressure
* Number of ALD cycles

## Key Film Metrics

* Growth Per Cycle (GPC)
* Film thickness
* Film uniformity
* Refractive index
* Film stress
* Surface roughness
* Defectivity

## Methodology

### 1. Data Collection & Preparation

ALD process data is collected containing deposition parameters and corresponding thin-film characteristics. The data is cleaned, organized, and checked for missing values and abnormal measurements.

### 2. DOE & Parameter Analysis

**Design of Experiments (DOE)** is used to study how changes in ALD parameters affect film properties. Statistical analysis is performed to identify the most influential process parameters and parameter interactions.

### 3. Process Window Optimization

The identified parameter effects are used to determine an **optimal operating window** that provides the desired film thickness, GPC, uniformity, and other quality requirements while minimizing variation.

### 4. Statistical Process Control

**SPC** techniques and control charts are used to monitor process behavior and identify process drift or abnormal variation during repeated deposition runs.

### 5. Process Capability Analysis

**Cp and Cpk** are used to evaluate whether the optimized process can consistently meet the defined specification limits.

### 6. Root Cause Analysis & FMEA

Abnormal variations are investigated using **Root Cause Analysis (RCA)**. **FMEA** is then used to identify potential failure modes, assess process risks, and prioritize areas for improvement.

### Overall Workflow

```text
ALD Process Data
       ↓
Data Cleaning & Analysis
       ↓
DOE / Parameter Effect Analysis
       ↓
Identify Critical Parameters
       ↓
Optimize Process Window
       ↓
SPC & Process Capability
       ↓
RCA & FMEA
       ↓
Improved Process Stability & Yield
```

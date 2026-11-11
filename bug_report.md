---
name: 'Phase Anomaly / Simulation Bug Report'
about: Report geometric scattering, phase drift, or validation variances within the GWC-1 lattice.
title: '[ANOMALY]: '
labels: 'bug, simulation'
assignees: ''
---

## 🛠️ Environmental Conditions
*   **Operating System / Distribution:** (e.g., Ubuntu 24.04, macOS Sonoma)
*   **MEEP / PyMeep Version:** (e.g., v1.28.0)
*   **Simulation Grid Resolution (DPY):** (e.g., 15 px/µm, 20 px/µm)

## 🌀 Description of the Geometric Anomaly
Provide a clear, analytical description of the wave behavior discrepancy. Are light photons leaking unexpectedly across the Fused Silica cladding, or is Master Center Node 1 experiencing phase-slip drift?

## 📊 Calibrated Metrics Check
*   **Observed Central Node Coherence Score:** (e.g., 0.8123 vs Expected 0.8800)
*   **Local Thermal Envelope Variance:** (Did the micro-calorimeter simulation register a deviation above 0.00W?)
*   **Track Parameters Used:** Node Radius = _________ µm | Track Width = _________ µm

## 🧪 Steps to Reproduce the Error
1. Run the targeted `Veda-G` configuration file: `_____________.vg`
2. Compile and execute using the local FDTD grid layout script.
3. Observe wave data distortion at internal Vesica Junction Index #_____.

## 🎥 Supporting Visual Materials
*Please attach or drop a link to your exported layout graphs (`gwc_complete_flower_19.png`) or stitched wave animations (`gwc_flower_wave_matrix.mp4`) showing the point of destructive scattering.*

## 💡 Proposed Geometric Readjustment
If you have calculated a phase modulation shift (\(\Delta\theta\)) or variable track width compensation to resolve this boundary leakage, please detail your mathematical suggestion here.

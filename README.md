# Project THOTH: The Geometric Wave Crystal Processor (GWC-1)

### The Open-Source Geometric Photonic Architecture for Neuro-Wavefront Computing

**Project THOTH** is a decentralized, open-source hardware initiative designed to transition artificial intelligence computing away from power-constrained digital transistor architectures (GPUs) into a zero-power analog substrate.

By arranging Silicon Nitride ($\\text{Si}\_3\\text{N}\_4$) nano-waveguides into a 19-circle 60-degree hexagonal lattice (Flower of Life topology), THOTH processes complex continuous wave fields ($E = A e^{i\\theta}$) through 121 intersecting Vesica Piscis junctions without classical binary switching penalties or transistor heat limits.

\---

## ⚖️ Dual-Licensing Framework

Project THOTH uses a dual-licensing scheme to ensure maximum open-source accessibility for software developers while protecting hardware designs under anti-monopoly, weakly reciprocal open-hardware standards:

|Layer|Target Files|License|File Reference|
|-|-|-|-|
|**Photonic Hardware \& EDA**|GDSFactory scripts, GDSII layouts, thermal trench specs, RISC-V pinouts, physical layer stack definitions.|**CERN-OHL-W v2.0**|[`LICENSE-HARDWARE`](./LICENSE-HARDWARE)|
|**Software, Drivers \& Models**|Python simulation suites, MEEP models, PCIe user-space drivers (`gwc\\\_core\\\_api.py`), PyTorch layers (`torch\\\_vedagcore.py`), Veda-G standard library modules.|**MIT License**|[`LICENSE-SOFTWARE`](./LICENSE-SOFTWARE)|

\---

## 🏛️ System Repository Layout

```text
project-thoth/
├── LICENSE-HARDWARE                 # CERN-OHL-W v2.0 for Photonic Masks \\\& EDA
├── LICENSE-SOFTWARE                 # MIT License for Drivers, Simulators \\\& Veda-G
├── README.md                        # Project documentation
├── Manifesto.md                     # Core philosophical proclamation
├── CONTRIBUTING.md                  # Contribution rules across software \\\& simulation
├── setup.sh                         # Automated environment installation script
├── bug\\\_report.md                    # Issue reporting template for phase drift/anomalies
├── eda/
│   ├── gdsfactory.py                # Monolithic 19-node Flower of Life layout generator
│   └── lattice\\\_generator.py         # Parametric N-ring hexagonal ONN mesh generator
├── hardware/
│   ├── gwc\\\_hal.h                    # C header and RISC-V inline assembly macro
│   └── riscv\\\_xgwc\\\_isa.txt           # RISC-V custom opcode encoding spec (0x0B)
├── driver/
│   └── gwc\\\_core\\\_api.py              # PCIe mmap interface for direct hardware execution
├── simulation/
│   ├── Bash.txt                     # Conda PyMeep installation flags
│   ├── gwc\\\_flower\\\_19\\\_circle.py      # Full 19-circle PyMeep wave propagation model
│   ├── gwc\\\_meep\\\_lattice.py          # Seed of Life 6-input FDTD grid script
│   ├── gwc\\\_meep\\\_export.py           # Visual PNG and HDF5 field data exporter
│   ├── gwc\\\_simulation.py            # 6D semantic vector-to-wave interference model
│   └── simulation.py.py             # Basic wave harmonic simulation and plotting script
├── software/
│   ├── Deep\\\_Multi-Layer\\\_Photonic\\\_Reservoir\\\_engine.txt  # Deep complex-valued reservoir model
│   ├── software\\\_tuned\\\_wavefront\\\_processor.py           # Thermo-optic active tuning model
│   └── torch\\\_vedagcore.py                              # PyTorch GWC-1 linear layer replacement
└── vedag/
    ├── core/
    │   ├── spatial\\\_vectors.vgl      # Spatial vector transformations
    │   ├── natural\\\_language.vgl     # String-to-waveform semantic encoders
    │   ├── neural\\\_layers.vgl        # Wave attention and physical activation filters
    │   ├── wave\\\_gradients.vgl       # Zero-cycle optical backpropagation derivatives
    │   ├── topological\\\_crypto.vgl   # Anyon space-time braid encryption
    │   └── geometric\\\_ledger.vgl     # Resonance-based instant transaction validation
    ├── examples/
    │   ├── hello\\\_cosmos.vg          # Wave interference code example
    │   └── prime\\\_sieve.vg           # Optical fractional prime sieve code
    └── tests/
        └── test\\\_attention\\\_accuracy.vg  # Phase accuracy diagnostic suite
```

\---

## 🛠️ Monolithic Layer Specifications

|Layer Index|Name|Thickness / Width|Purpose|
|-|-|-|-|
|**Layer 1 (1:0)**|Core Waveguide|$400,\\text{nm}$ height, $500,\\text{nm}$ width|Single-mode LPCVD Silicon Nitride ($\\text{Si}\_3\\text{N}\_4$) core ($n=2.00$).|
|**Layer 2 (2:0)**|Thermal Isolation|$2.0,\\mu\\text{m}$ trench width|Oxide-etched air boundaries preventing cross-node thermal interference.|
|**Layer 40 (40:0)**|Micro-Vias|$4.0,\\mu\\text{m} \\times 4.0,\\mu\\text{m}$|Upper oxide contact windows down to micro-heater elements.|
|**Layer 41 (41:0)**|Phase Control Metal|$2.5,\\mu\\text{m}$ trace width|Titanium/Gold ($\\text{Ti/Au}$) heaters for dynamic phase modulation ($\\Delta\\theta$).|

\---

## 🚀 Quickstart Guide

### 1\. Environment Setup

Execute the automated setup script or build the Conda environment manually:

```bash
# Automated Setup
chmod +x setup.sh
./setup.sh

# Manual Conda Environment Initialization
conda create -n meep -c conda-forge pymeep python=3.10 -y
conda activate meep
pip install torch numpy h5py gdsfactory matplotlib
```

### 2\. Run Optical Wave Simulation

Simulate wave propagation through the 19-circle layout using PyMeep FDTD:

```bash
conda activate meep
python simulation/gwc\\\_flower\\\_19\\\_circle.py
```

### 3\. Generate Photonic Mask Layouts (GDSII)

Compile foundry-ready GDSII layouts for chip fabrication:

```bash
# Compile monolithic 19-node Flower of Life chip layout
python eda/gdsfactory.py

# Generate parametric 37-node lattice chip layout
python eda/lattice\\\_generator.py
```

\---

## 🔬 System Processing Architecture

```text
 \\\[ Semantic Vector / Text Input ]
                │
                ▼
┌───────────────────────────────┐
│     Wave-Harmonic Encoder     │  <── f = f\\\_base \\\* (Φ^x), Phase Mapping
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│      19-Circle Photonic       │  <── Si3N4 Core Waveguides (ε = 4.00)
│    Lattice Mesh (GWC-1)       │  <── Fused Silica Cladding (ε = 2.10)
└───────────────┬───────────────┘
                │ Physical Interference (Vesica Junctions)
                ▼
┌───────────────────────────────┐
│  Photodiode Matrix Readout    │  <── Intensity (|E|²) \\\& Phase Angle Sampling
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│ Linear / Ridge Readout Engine │  <── Hardware Output Processing
└───────────────┬───────────────┘
                │
                ▼
┌───────────────────────────────┐
│    PyTorch Model / Driver     │  <── Integration via torch\\\_vedagcore.py
└───────────────────────────────┘
```


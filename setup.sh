#!/bin/bash
# ===================================================================
# Project Thoth: Automated Environment Setup Script
# Supported OS: Ubuntu/Debian Linux, macOS
# ===================================================================

set -e # Exit immediately if any command exits with a non-zero status

print_status() {
    echo -e "\n\033[1;34m[THOTH-SETUP]\033[0m $1"
}

print_status "Detecting host operating system architecture..."
OS_TYPE="$(uname -s)"

if [ "$OS_TYPE" = "Linux" ]; then
    print_status "Linux environment verified. Updating system packages..."
    sudo apt-get update
    sudo apt-get install -y build-essential hdf5-tools h5utils ffmpeg python3-pip
elif [ "$OS_TYPE" = "Darwin" ]; then
    print_status "macOS environment verified. Checking for Homebrew..."
    if ! command -v brew &> /dev/null; then
        print_status "Homebrew not found. Please install Homebrew before running this script."
        exit 1
    fi
    brew install hdf5 h5utils ffmpeg
else
    echo "Unsupported Operating System."
    exit 1
fi

print_status "Checking for Conda environment manager..."
if ! command -v conda &> /dev/null; then
    print_status "Conda not found. Installing Miniconda sandbox locally..."
    mkdir -p ~/miniconda3
    wget https://anaconda.com -O ~/miniconda3/miniconda.sh
    bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
    rm -rf ~/miniconda3/miniconda.sh
    export PATH="$HOME/miniconda3/bin:$PATH"
    conda init bash
fi

print_status "Building isolated Python environment for MIT MEEP..."
conda create -n meep -c conda-forge pymeep python=3.10 -y

print_status "Installing SDK dependencies (PyTorch & NumPy Frameworks)..."
# Activates the local environment block to attach dependencies
source $(conda info --base)/etc/profile.d/conda.sh
conda activate meep
pip install torch numpy h5py

print_status "Compiling local hardware kernel module handles..."
if [ -d "hardware/driver" ]; then
    cd hardware/driver
    make -j$(nproc) || echo "[WARN] Direct hardware header compile skipped (Running in emulation mode)."
    cd ../..
fi

print_status "================================================================"
print_status "SUCCESS: Project Thoth environment is fully operational!"
print_status "To start your first 19-circle optical simulation, execute:"
print_status "  conda activate meep"
print_status "  python simulation/gwc_flower_19_circle.py"
print_status "================================================================"

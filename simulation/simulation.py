import numpy as np
import matplotlib.pyplot as plt

# ===================================================================
# Project THOTH: GWC-1 Core Wave Interference Simulation
# Open-Source Project THOTH Release 1.4 (MIT License)
# ===================================================================

# Define Cosmic Constants
GOLDEN_RATIO = (1.0 + 5.0 ** 0.5) / 2.0  # Phi (~1.618)
F_BASE = 432.0                           # Base carrier frequency in Hz

# 6x6 Spatial Resonance Matrix based on Seed of Life node distances
RESONANCE_MATRIX = np.array([
    [1.0, 0.5, 0.2, 0.1, 0.2, 0.5],
    [0.5, 1.0, 0.5, 0.2, 0.1, 0.2],
    [0.2, 0.5, 1.0, 0.5, 0.2, 0.1],
    [0.1, 0.2, 0.5, 1.0, 0.5, 0.2],
    [0.2, 0.1, 0.2, 0.5, 1.0, 0.5],
    [0.5, 0.2, 0.1, 0.2, 0.5, 1.0]
])

def text_to_geometric_vector(prompt: str) -> np.ndarray:
    """Simulates turning text into a 6D normalized semantic vector."""
    np.random.seed(sum(ord(char) for char in prompt)) # Seed based on prompt text
    raw_vector = np.random.uniform(-1.0, 1.0, 6)
    return raw_vector / np.linalg.norm(raw_vector) # Normalize vector

def encode_to_wave_harmonics(vector: np.ndarray):
    """Formula 1 & 2: Translates the vector into Frequencies and Phase Angles."""
    frequencies = F_BASE * (GOLDEN_RATIO ** vector)
    
    phases = np.zeros(6)
    for i in range(6):
        phases[i] = np.pi * np.sum(vector[i] * vector * RESONANCE_MATRIX[i])
        
    return frequencies, phases

def simulate_central_node_interference(frequencies: np.ndarray, phases: np.ndarray) -> np.ndarray:
    """Simulates physical wave merging inside the Seed of Life channels."""
    simulated_intensities = np.abs(np.sin(phases) * (frequencies / F_BASE))
    return np.clip(simulated_intensities, 1e-5, None)

def decode_light_to_vector(intensities: np.ndarray) -> np.ndarray:
    """Inverse Formula: Reconstructs the semantic vector from light values."""
    reconstructed_vector = np.log(intensities) / np.log(GOLDEN_RATIO)
    return reconstructed_vector / np.linalg.norm(reconstructed_vector)

# ================= RUNNING THE SIMULATION CYCLE =================
if __name__ == "__main__":
    user_prompt = "Solve for structural balance and universal pattern symmetry"
    print(f"--- GWC-1 Simulation Started ---")
    print(f"1. Input User Prompt: '{user_prompt}'")
    
    # Step 1: Text -> 6D Space
    v_input = text_to_geometric_vector(user_prompt)
    print(f"2. Generated 6D Semantic Vector:\n   {np.round(v_input, 4)}")
    
    # Step 2: Encode into Wave Parameters
    freqs, phases = encode_to_wave_harmonics(v_input)
    print(f"3. Compiled Micro-Laser Commands:")
    for i in range(6):
        print(f"   - Node {i+2}: Freq = {freqs[i]:.2f} Hz | Phase = {np.degrees(phases[i]):.1f}°")
        
    # Step 3: Run Wave Interference inside the Chip
    light_output = simulate_central_node_interference(freqs, phases)
    print(f"4. Measured Central Pool Light Intensities:\n   {np.round(light_output, 4)}")
    
    # Step 4: Inverse Decode back to Vector
    v_output = decode_light_to_vector(light_output)
    print(f"5. Reconstructed Output Semantic Vector:\n   {np.round(v_output, 4)}")
    
    # Mathematical Check for Coherence
    cosine_similarity = np.dot(v_input, v_output)
    print(f"6. Verification: Geometric Field Alignment Accuracy = {cosine_similarity * 100:.2f}%")
    
    # Generate and save visual plot output
    plt.figure(figsize=(8, 5))
    plt.bar([f"Node {i+2}" for i in range(6)], light_output, color='deepskyblue', edgecolor='black')
    plt.title("GWC-1 Central Node Interference Spectrum")
    plt.ylabel("Optical Power Intensity (|E|^2)")
    plt.grid(True, alpha=0.3)
    plt.savefig("simulation_output.png")
    print("Visual output successfully saved to 'simulation_output.png'!")
```eof

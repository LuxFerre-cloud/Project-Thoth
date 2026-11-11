import numpy as np
import matplotlib.pyplot as plt

class ProgrammableGeometricReservoir:
    def __init__(self, n_nodes=19, spectral_radius=0.95, attenuation=0.2):
        """
        Simulates an active, programmable geometric optical mesh where 
        individual nodes can be actively tuned via simulated micro-heaters.
        """
        self.n_nodes = n_nodes
        self.gamma = attenuation
        rng = np.random.default_rng(seed=101)
        
        # Base Structural Lattice Matrix (Fixed Physics Baseline)
        amplitude_matrix = rng.uniform(0.3, 0.9, (n_nodes, n_nodes))
        base_phase_matrix = rng.uniform(-np.pi, np.pi, (n_nodes, n_nodes))
        W_complex = amplitude_matrix * np.exp(1j * base_phase_matrix)
        
        # Symmetrical interaction mask representing Vesica junctions
        mask = rng.uniform(0, 1, (n_nodes, n_nodes)) < 0.4
        np.fill_diagonal(mask, 1)
        W_masked = W_complex * mask
        
        # Normalize the structural network matrix using eigenvalues
        max_eigenval = np.max(np.abs(np.linalg.eigvals(W_masked)))
        self.W_base = W_masked * (spectral_radius / max_eigenval)
        
        # Fixed input mapping layer
        self.W_in = rng.uniform(0.1, 0.5, (n_nodes, 1)) * np.exp(1j * rng.uniform(-np.pi, np.pi, (n_nodes, 1)))
        
        # Clear field state vector
        self.x = np.zeros((n_nodes, 1), dtype=complex)
        
    def forward_step_with_tuning(self, input_signal, node_phase_shifts):
        """
        Runs one clock cycle step of wave propagation.
        node_phase_shifts: Array of size (n_nodes,) representing micro-heater phase updates.
        """
        # Apply the runtime electrical tuning vector across the diagonal of the matrix
        # This shifts the optical path phase delay through individual ring nodes
        tuning_matrix = np.diag(np.exp(1j * node_phase_shifts))
        W_tuned = np.dot(tuning_matrix, self.W_base)
        
        # Calculate coherent wave injection and internal recursive loop feedback
        in_injection = np.dot(self.W_in, input_signal)
        recirculating_feedback = np.dot(W_tuned, self.x)
        combined_fields = in_injection + recirculating_feedback
        
        # Wavefront non-linearity (Saturation behavior)
        amplitude = np.abs(combined_fields)
        phase = np.angle(combined_fields)
        self.x = (1 - self.gamma) * self.x + self.gamma * (np.tanh(amplitude) * np.exp(1j * phase))
        return self.x

# --- USER INFRASTRUCTURE EXPERIMENTATION ---
if __name__ == "__main__":
    time_steps = 200
    u_t = np.ones((time_steps,), dtype=complex) * 0.5  # Constant optical power injected into the array
    
    # Instantiate the 19-Node Programmable Core
    active_chip = ProgrammableGeometricReservoir(n_nodes=19)
    
    # Scenario A: UNTUNED baseline chip state (Zero heat applied to micro-heaters)
    zero_heat_shifts = np.zeros(19)
    states_untuned = np.zeros((19, time_steps), dtype=complex)
    
    for t in range(time_steps):
        states_untuned[:, t] = active_chip.forward_step_with_tuning(u_t[t], zero_heat_shifts).flatten()
        
    # Scenario B: TUNED programmed state (Injecting micro-amps into specific Layer 41 nodes)
    active_chip.reset_states()  # Reset optical field states
    heater_shifts = np.zeros(19)
    heater_shifts[0]  = np.pi / 2   # Apply 90-degree phase shift to the Central Aggregator Node
    heater_shifts[5]  = -np.pi / 4  # Apply -45-degree shift to Ring Node #5
    heater_shifts[12] = np.pi       # Invert Phase (180 degrees) on Outer Ring Node #12
    
    states_tuned = np.zeros((19, time_steps), dtype=complex)
    for t in range(time_steps):
        states_tuned[:, t] = active_chip.forward_step_with_tuning(u_t[t], heater_shifts).flatten()

    # --- VISUALIZE THERMO-OPTIC MODULATION DYNAMICS ---
    plt.figure(figsize=(14, 8))
    
    # Plot 1: Untuned Power Profile Matrix
    plt.subplot(2, 2, 1)
    plt.imshow(np.abs(states_untuned)**2, aspect='auto', cmap='magma')
    plt.title("Baseline State Matrix (|E|^2) - Untuned Heaters")
    plt.ylabel("Node ID Index")
    plt.colorbar(label="Intensity")
    
    # Plot 2: Tuned Power Profile Matrix (Showing shifted interference patterns)
    plt.subplot(2, 2, 2)
    plt.imshow(np.abs(states_tuned)**2, aspect='auto', cmap='magma')
    plt.title("Programmed State Matrix (|E|^2) - Micro-Heaters Activated")
    plt.ylabel("Node ID Index")
    plt.colorbar(label="Intensity")
    
    # Plot 3: Specific Node Tracking Comparison over Time
    plt.subplot(2, 1, 2)
    plt.plot(np.abs(states_untuned[0, :])**2, label="Central Node #0 (Untuned Baseline)", color='black', alpha=0.5)
    plt.plot(np.abs(states_tuned[0, :])**2, label="Central Node #0 (Active Thermo-Optic Shift)", color='crimson', lw=2)
    plt.title("Real-Time Transient Power Convergence at the Central Node Cavity")
    plt.xlabel("Simulated Propagation Time-Steps")
    plt.ylabel("Optical Power Output")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    plt.tight_layout()
    plt.show()

import numpy as np
import matplotlib.pyplot as plt

class ComplexGeometricReservoirLayer:
    def __init__(self, n_nodes=19, n_inputs=1, spectral_radius=0.95, attenuation=0.1, layer_id=1):
        """
        Represents a single 19-node geometric optical mesh operating completely
        within the Complex Wave Domain (Phase + Amplitude).
        """
        self.n_nodes = n_nodes
        self.n_inputs = n_inputs
        self.gamma = attenuation  # Scattering and material insertion loss
        self.layer_id = layer_id
        
        rng = np.random.default_rng(seed=42 + layer_id)
        
        # Internal Matrix (W_res): Complex numbers model amplitude splitting and phase shifting
        # z = amplitude * exp(i * phase)
        amplitude_matrix = rng.uniform(0.1, 1.0, (n_nodes, n_nodes))
        phase_matrix = rng.uniform(-np.pi, np.pi, (n_nodes, n_nodes))
        W_complex = amplitude_matrix * np.exp(1j * phase_matrix)
        
        # Enforce structural lattice mesh constraints (Sparsity of the Vesica junctions)
        mask = rng.uniform(0, 1, (n_nodes, n_nodes)) < 0.45
        np.fill_diagonal(mask, 1)
        W_masked = W_complex * mask
        
        # Scale the spectral radius using the absolute magnitude of eigenvalues
        eigenvalues = np.linalg.eigvals(W_masked)
        max_eigenval = np.max(np.abs(eigenvalues))
        self.W_res = W_masked * (spectral_radius / max_eigenval)
        
        # Input coupling matrix mapping data into complex phase/amplitude space
        in_amp = rng.uniform(0.2, 0.8, (n_nodes, n_inputs))
        in_phase = rng.uniform(-np.pi, np.pi, (n_nodes, n_inputs))
        self.W_in = in_amp * np.exp(1j * in_phase)
        
        # State vector initialized to zero optical field (No photons)
        self.x = np.zeros((n_nodes, 1), dtype=complex)

    def reset_states(self):
        self.x = np.zeros((self.n_nodes, 1), dtype=complex)

    def _wave_nonlinearity(self, fields):
        """
        Simulates two-photon absorption or localized index saturation.
        Limits exponential power growth while preserving wave phase integrity.
        """
        amplitude = np.abs(fields)
        phase = np.angle(fields)
        saturated_amplitude = np.tanh(amplitude)
        return saturated_amplitude * np.exp(1j * phase)

    def forward_step(self, input_signal):
        """
        Propagates complex electric fields through the node network for one time-step.
        """
        # Mix input wave injection with internally recirculating coherent waves
        in_injection = np.dot(self.W_in, input_signal)
        recirculating_feedback = np.dot(self.W_res, self.x)
        
        combined_fields = in_injection + recirculating_feedback
        
        # Apply physical propagation attenuation and the localized non-linear phase mixing
        self.x = (1 - self.gamma) * self.x + self.gamma * self._wave_nonlinearity(combined_fields)
        return self.x


class DeepMultiLayerPhotonicProcessor:
    def __init__(self, layer_configs):
        """
        Manages the deep cascade stack of individual complex optical matrices.
        """
        self.layers = []
        for i, config in enumerate(layer_configs):
            self.layers.append(
                ComplexGeometricReservoirLayer(
                    n_nodes=config['n_nodes'],
                    n_inputs=config['n_inputs'],
                    spectral_radius=config['spectral_radius'],
                    attenuation=config['attenuation'],
                    layer_id=i+1
                )
            )
        self.W_out = None

    def process_stack(self, input_sequence):
        """
        Cascades wave-fronts sequentially through the integrated device stack.
        """
        n_steps = len(input_sequence)
        final_layer_nodes = self.layers[-1].n_nodes
        collected_states = np.zeros((final_layer_nodes, n_steps), dtype=complex)
        
        # Clear residual fields across all layers
        for layer in self.layers:
            layer.reset_states()
            
        for t in range(n_steps):
            current_wave = np.array([[input_sequence[t]]], dtype=complex)
            
            # Cascade sequentially through the geometric stack
            for layer in self.layers:
                current_wave = layer.forward_step(current_wave)
                
            collected_states[:, t] = current_wave.flatten()
            
        return collected_states

    def train_stack(self, input_sequence, target_sequence, regularization=1e-4):
        """
        Trains the digital readout matrix using the optical intensities (Power)
        harvested by the photodiode array at the final layer's edge.
        """
        X_complex = self.process_stack(input_sequence)
        X_intensity = np.abs(X_complex) ** 2
        Y_target = np.array(target_sequence).reshape(1, -1)
        
        # Discard the initial stabilization window (Warm-up phase)
        n_steps = X_intensity.shape[1]
        warmup = int(n_steps * 0.1)
        X_clean = X_intensity[:, warmup:]
        Y_clean = Y_target[:, warmup:]
        
        # Run optimized Ridge Regression on the intensity profiles
        identity = np.eye(self.layers[-1].n_nodes)
        covariance = np.dot(X_clean, X_clean.T) + regularization * identity
        cross_variance = np.dot(Y_clean, X_clean.T)
        
        self.W_out = np.dot(cross_variance, np.linalg.inv(covariance))
        print(f"Deep Stack Training Complete. Readout mapped to final layer output.")

    def predict_stack(self, input_sequence):
        X_complex = self.process_stack(input_sequence)
        X_intensity = np.abs(X_complex) ** 2
        return np.dot(self.W_out, X_intensity).flatten()


# --- COMPILE, RUN, AND TEST THE PROCESSOR STACK ---
if __name__ == "__main__":
    # Generate an intricate, non-linear multi-frequency time-series sequence
    n_steps = 1200
    t = np.linspace(0, 80, n_steps)
    raw_wavefront = np.sin(t) * np.sin(t / 3.0) + 0.4 * np.cos(t * 2.1)
    
    # 80/20 Train/Test Data Split
    split = int(n_steps * 0.8)
    train_in, train_target = raw_wavefront[:split-1], raw_wavefront[1:split]
    test_in, test_target = raw_wavefront[split:-1], raw_wavefront[split+1:]

    # Define a 3-Layer Cascaded Network Architecture Configuration
    network_blueprint = [
        {'n_nodes': 19, 'n_inputs': 1,  'spectral_radius': 0.98, 'attenuation': 0.3}, # Layer 1
        {'n_nodes': 19, 'n_inputs': 19, 'spectral_radius': 0.95, 'attenuation': 0.4}, # Layer 2
        {'n_nodes': 19, 'n_inputs': 19, 'spectral_radius': 0.90, 'attenuation': 0.5}  # Layer 3
    ]

    # Instantiate the deep chip model
    photonic_chip = DeepMultiLayerPhotonicProcessor(network_blueprint)

    # Train the hybrid digital-analog system
    photonic_chip.train_stack(train_in, train_target, regularization=1e-5)

    # Run inference predictions on unseen tracking sequences
    predictions = photonic_chip.predict_stack(test_in)

    # --- Plotting the Complex Wave States and Intensities ---
    plt.figure(figsize=(14, 8))
    
    # Subplot 1: Output prediction tracking vs. Target truth
    plt.subplot(3, 1, 1)
    plt.plot(test_target, label="True Physical Waveform Target", color='black', lw=1.5)
    plt.plot(predictions, label="Deep Geometrical Stack Prediction", color='deepskyblue', linestyle='--')
    plt.title("Deep Multi-Layer Complex Photonic System Prediction Tracking")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, alpha=0.2)
    
    # Subplot 2: Real-world Power/Intensity Matrix (|E|^2) hitting the photodiodes
    plt.subplot(3, 1, 2)
    final_layer_complex_states = photonic_chip.process_stack(test_in)
    final_layer_intensity = np.abs(final_layer_complex_states) ** 2
    plt.imshow(final_layer_intensity, aspect='auto', cmap='magma', interpolation='nearest')
    plt.title("Measurable Power Output (|E|^2) at Layer 3 Edge Portals")
    plt.ylabel("Node ID")
    plt.colorbar(label="Intensity")

    # Subplot 3: Phase distribution profile showing constructive and destructive patterns
    plt.subplot(3, 1, 3)
    final_layer_phase = np.angle(final_layer_complex_states)
    plt.imshow(final_layer_phase, aspect='auto', cmap='twilight', interpolation='nearest')
    plt.title("Phase Distribution [-\u03c0, +\u03c0] across Layer 3 Nodes (Coherent Interference Footprint)")
    plt.xlabel("Execution Time Steps")
    plt.ylabel("Node ID")
    plt.colorbar(label="Phase (Radians)")

    plt.tight_layout()
    plt.show()

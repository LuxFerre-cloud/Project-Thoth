import os
import fcntl
import mmap
import ctypes
import numpy as np

# Memory map boundaries matching the hardware specification
GWC_REGISTER_SIZE = 4096
GWC_REG_CONTROL = 0x0000
GWC_REG_STATUS = 0x0010
GWC_REG_INPUT_BASE = 0x0020
GWC_REG_OUTPUT_BASE = 0x0050

class GWCDriverInterface:
    def __init__(self, device_path: str = "/dev/gwc0"):
        """Initializes the physical link to the GWC-1 PCIe host adapter."""
        if not os.path.exists(device_path):
            raise FileNotFoundError(f"GWC-1 Casing not detected at {device_path}")
            
        self.fd = os.open(device_path, os.O_RDWR | os.O_SYNC)
        # Memory-map the PCIe board configuration registers directly to application space
        self.mem = mmap.mmap(self.fd, GWC_REGISTER_SIZE, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE)
        self._initialize_hardware()

    def _initialize_hardware(self):
        """Fires the initialization sequence over the hardware pinout."""
        # Write to 0x0000: Enable global system array, lasers, and fluid pump (0x07)
        self.mem[GWC_REG_CONTROL:GWC_REG_CONTROL+4] = ctypes.c_uint32(0x07)
        
        # Read status from 0x0010 to confirm array resonance alignment
        status = ctypes.c_uint32.from_buffer(self.mem, GWC_REG_STATUS).value
        if not (status & 0x01):
            raise ConnectionError("GWC-1 Grid Failed to reach base optical resonance.")
        print("[GWC-1 API] Hardware handshakes complete. Geometric array locked in phase coherence.")

    def execute_spatial_merge(self, vector_a: np.ndarray, vector_b: np.ndarray) -> np.ndarray:
        """Pushes data to spatial_vectors.vgl over the bus for zero-cycle matrix merging."""
        assert len(vector_a) == 3 and len(vector_b) == 3, "Each sub-tensor must match 3 degrees of node layout."
        
        # Merge arrays into a single 6-dimensional input coordinate slice
        unified_input = np.concatenate([vector_a, vector_b]).astype(np.float32)
        
        # Direct memory write to registers 0x0020 through 0x004F
        input_bytes = unified_input.tobytes()
        self.mem[GWC_REG_INPUT_BASE:GWC_REG_INPUT_BASE + len(input_bytes)] = input_bytes
        
        # Trigger execution bit on the control bus
        self.mem[GWC_REG_CONTROL:GWC_REG_CONTROL+4] = ctypes.c_uint32(0x0F) # Add EXECUTE flag
        
        # Poll status register until calculation field collapse bit clears
        while True:
            status = ctypes.c_uint32.from_buffer(self.mem, GWC_REG_STATUS).value
            if not (status & 0x08): # Check if calculation flag is down
                break
                
        # Read back raw spatial intensities from registers 0x0050 through 0x007F [1]
        output_bytes = self.mem[GWC_REG_OUTPUT_BASE:GWC_REG_OUTPUT_BASE + 24]
        raw_output = np.frombuffer(output_bytes, dtype=np.float32)
        
        return raw_output

    def close(self):
        """Safely spins down the lasers and power rails."""
        self.mem[GWC_REG_CONTROL:GWC_REG_CONTROL+4] = ctypes.c_uint32(0x00)
        self.mem.close()
        os.close(self.fd)

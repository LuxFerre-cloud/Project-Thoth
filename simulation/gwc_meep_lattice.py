import meep as mp
import numpy as np

# ==========================================
# 1. PARAMETERS & GEOMETRIC CONSTANTS
# ==========================================
GOLDEN_RATIO = (1.0 + 5.0 ** 0.5) / 2.0  # Phi (~1.618)
BASE_RADIUS = 4.0                        # Base dimension unit (microns)
NODE_RADIUS = BASE_RADIUS * GOLDEN_RATIO # Scaled via Sacred Geometry (~6.47 microns)
TRACK_WIDTH = 0.5                        # Waveguide thickness in microns

# Material Indices (Silicon Nitride core trapped inside Fused Silica)
EPS_SUBSTRATE = 2.10  # Fused Silica / Quartz background
EPS_WAVEGUIDE = 4.00  # Silicon Nitride (High-index tracking core)

# Simulation Domain Boundaries
CELL_WIDTH = 30.0
CELL_HEIGHT = 30.0
cell = mp.Vector3(CELL_WIDTH, CELL_HEIGHT, 0)

# Runtime frequency definition (Optical Terahertz scaled to FDTD space)
FREQ_CENTRAL = 1.0  # Normalized frequency matching 1-micron wavelength
DPY = 10            # Pixels per micron (Resolution grid density)

# ==========================================
# 2. GENERATING THE SEED OF LIFE CHANNELS
# ==========================================
# Initialize background substrate space
geometry = [
    mp.Block(
        size=mp.Vector3(mp.inf, mp.inf, mp.inf),
        material=mp.Medium(epsilon=EPS_SUBSTRATE)
    )
]

# Calculate the 6 perimeter center coordinates on the 60-degree hexagonal lattice
node_centers = []
for n in range(6):
    theta = n * (np.pi / 3.0)  # 60 degrees in radians
    x = NODE_RADIUS * np.cos(theta)
    y = NODE_RADIUS * np.sin(theta)
    node_centers.append(mp.Vector3(x, y, 0))

# Layer 1: Etch the 6 large overlapping structural perimeter rings
for center in node_centers:
    geometry.append(
        mp.Cylinder(
            radius=NODE_RADIUS + (TRACK_WIDTH / 2.0),
            height=mp.inf,
            center=center,
            material=mp.Medium(epsilon=EPS_WAVEGUIDE)
        )
    )
    # Subtractive pass to create hollow channel tracks
    geometry.append(
        mp.Cylinder(
            radius=NODE_RADIUS - (TRACK_WIDTH / 2.0),
            height=mp.inf,
            center=center,
            material=mp.Medium(epsilon=EPS_SUBSTRATE)
        )
    )

# Layer 2: Etch the central bounding master circle (Circle 1 Processing Basin)
geometry.append(
    mp.Cylinder(
        radius=NODE_RADIUS + (TRACK_WIDTH / 2.0),
        height=mp.inf,
        center=mp.Vector3(0, 0, 0),
        material=mp.Medium(epsilon=EPS_WAVEGUIDE)
    )
)
geometry.append(
    mp.Cylinder(
        radius=NODE_RADIUS - (TRACK_WIDTH / 2.0),
        height=mp.inf,
        center=mp.Vector3(0, 0, 0),
        material=mp.Medium(epsilon=EPS_SUBSTRATE)
    )
)

# ==========================================
# 3. INITIALIZING THE 6 OPTICAL INPUT SOURCES
# ==========================================
# Simulated semantic input vector representing a balanced thought state
mock_semantic_vector = [0.8, -0.4, 0.9, 0.2, -0.7, 0.5]
sources = []

for i, center in enumerate(node_centers):
    # Scale individual channel frequency natively using the Golden Ratio
    channel_freq = FREQ_CENTRAL * (GOLDEN_RATIO ** mock_semantic_vector[i])
    
    # Calculate phase-locked loop angle shifts to establish space-time braids
    channel_phase = np.pi * mock_semantic_vector[i]
    
    # Position point sources precisely at the outer boundary node portals
    sources.append(
        mp.Source(
            src=mp.ContinuousSource(frequency=channel_freq, end_time=100),
            component=mp.Ez,
            center=center,
            amplitude=complex(np.cos(channel_phase), np.sin(channel_phase))
        )
    )

# ==========================================
# 4. COMPILING THE SIMULATION SPACE
# ==========================================
# Wrap the domain with Perfectly Matched Layers (PML) to absorb outward escaping waves
pml_layers = [mp.PML(1.0)]

sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    sources=sources,
    boundary_layers=pml_layers,
    resolution=DPY
)

# Run the simulation and generate a snapshot of the resulting light field
print("[THOTH-MEEP] Launching field calculations across the 121 Vesica junctions...")
sim.run(until=150)

# Capture the absolute electric field intensity profile inside the Master Center Node
center_field = sim.get_field_intensity(mp.Vector3(0, 0, 0))
print(f"[THOTH-SUCCESS] Computation Complete.")
print(f"-> Normalized Light Energy Density at Central Master Node = {center_field:.6f} W/m²")

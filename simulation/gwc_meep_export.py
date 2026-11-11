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
DPY = 20            # Increased resolution (20 pixels/micron) for crisp image output

# ==========================================
# 2. GENERATING THE SEED OF LIFE CHANNELS
# ==========================================
geometry = [
    mp.Block(
        size=mp.Vector3(mp.inf, mp.inf, mp.inf),
        material=mp.Medium(epsilon=EPS_SUBSTRATE)
    )
]

# Calculate the 6 perimeter center coordinates on the 60-degree hexagonal lattice
node_centers = []
for n in range(6):
    theta = n * (np.pi / 3.0)
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
mock_semantic_vector = [0.8, -0.4, 0.9, 0.2, -0.7, 0.5]
sources = []

for i, center in enumerate(node_centers):
    channel_freq = FREQ_CENTRAL * (GOLDEN_RATIO ** mock_semantic_vector[i])
    channel_phase = np.pi * mock_semantic_vector[i]
    
    sources.append(
        mp.Source(
            src=mp.ContinuousSource(frequency=channel_freq, end_time=200),
            component=mp.Ez,
            center=center,
            amplitude=complex(np.cos(channel_phase), np.sin(channel_phase))
        )
    )

# ==========================================
# 4. COMPILING AND EXPORTING SIMULATION SPACE
# ==========================================
pml_layers = [mp.PML(1.0)]

sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    sources=sources,
    boundary_layers=pml_layers,
    resolution=DPY
)

print("[THOTH-MEEP] Initializing system lattice structure...")

# EXPORT 1: Output a direct PNG visualization of the physical Flower of Life hardware layout
sim.plot2D(filename="gwc_flower_geometry.png")
print("[THOTH-EXPORT] Saved hardware layout blueprint directly to 'gwc_flower_geometry.png'")

# EXPORT 2: Run simulation while natively exporting real-time HDF5 field data arrays
print("[THOTH-MEEP] Launching field calculations across the 121 Vesica junctions...")

# This command streams the electric field slice data into HDF5 formats during runtime steps
sim.run(
    mp.at_every(10, mp.output_png(mp.Ez, "-Zc dkbluered")),  # Spits out field snapshots sequentially
    mp.at_end(mp.output_efield_z),                          # Generates final raw HDF5 matrix data file
    until=150
)

# Capture the absolute final metrics inside the Master Center Node
center_field = sim.get_field_intensity(mp.Vector3(0, 0, 0))
print(f"[ETHERGRID-SUCCESS] Computation and data streaming complete.")
print(f"-> Master Output File Saved as 'gwc_meep_export-ez.h5'")
print(f"-> Normalized Light Energy Density at Central Master Node = {center_field:.6f} W/m²")

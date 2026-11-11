import numpy as np
import gdsfactory as gf

def generate_hex_grid_nodes(rings: int, pitch: float) -> list:
    """
    Algorithmatically computes center coordinates (x, y) for concentric
    hexagonal rings of waveguides (0 rings = 1 node, 1 ring = 7 nodes, 
    2 rings = 19 nodes, 3 rings = 37 nodes, 4 rings = 61 nodes).
    """
    nodes = [(0.0, 0.0)]  # Central Core Neuron Base
    
    # Hexagonal spatial basis vectors
    dx = pitch
    dy = pitch * np.sin(np.radians(60))
    
    for r in range(1, rings + 1):
        # Start at the top vertex of the current shell layer
        x = 0.0
        y = r * pitch
        
        # Define the 6 directional steps to traverse a perfect hexagon boundary
        directions = [
            (dx * np.cos(np.radians(-30)), -dy),  # Down-Right
            (0.0, -pitch),                        # Down straight
            (-dx * np.cos(np.radians(-30)), -dy), # Down-Left
            (-dx * np.cos(np.radians(-30)), dy),  # Up-Left
            (0.0, pitch),                         # Up straight
            (dx * np.cos(np.radians(-30)), dy)    # Up-Right
        ]
        
        for step_x, step_y in directions:
            for _ in range(r):
                x += step_x
                y += step_y
                # Avoid numerical rounding drifting offsets near boundaries
                nodes.append((round(x, 4), round(y, 4)))
                
    # Remove duplicate edge cases generated during hex corner transitions
    unique_nodes = list(set(nodes))
    return unique_nodes

@gf.cell
def open_source_parametric_onn_mesh(
    rings: int = 3,             # 2 = 19 Nodes, 3 = 37 Nodes, 4 = 61 Nodes
    pitch: float = 20.0,        # Spatial center-to-center distance
    ring_radius: float = 20.0,  # Curvature radius of the waveguide loop
    wg_width: float = 0.5,      # Track structural cross section width
    trench_width: float = 2.0,  # Air boundary width
    via_size: float = 4.0
) -> gf.Component:
    
    c = gf.Component(f"parametric_onn_rings_{rings}")
    
    # Layer definitions matching GitHub specification standards
    LAYER_SI_CORE = (1, 0)
    LAYER_THERMAL_TRENCH = (2, 0)
    LAYER_VIA = (40, 0)
    LAYER_METAL = (41, 0)
    
    # Compute the grid
    node_coordinates = generate_hex_grid_nodes(rings, pitch)
    print(f"🔄 Compiling Grid: Generated {len(node_coordinates)} processing nodes across {rings} rings.")
    
    # Instantiate layout blocks across all computed spatial vectors
    for idx, (x, y) in enumerate(node_coordinates):
        # 1. Base Ring Channel Geometry
        ring_core = gf.components.ring(
            radius=ring_radius - (wg_width / 2),
            width=wg_width,
            layer=LAYER_SI_CORE
        )
        rc_ref = c << ring_core
        rc_ref.move((x, y))
        
        # 2. Thermal Isolation Boundary Cladding
        trench_out = gf.components.ring(
            radius=ring_radius + wg_width + (trench_width / 2),
            width=trench_width,
            layer=LAYER_THERMAL_TRENCH
        )
        to_ref = c << trench_out
        to_ref.move((x, y))
        
        # 3. Dynamic Modulation Vias
        via = gf.components.rectangle(size=(via_size, via_size), layer=LAYER_VIA, centered=True)
        v_ref = c << via
        v_ref.move((x, y + ring_radius))
        
        # 4. Outbound Radial Metal Trace Lines
        angle = np.arctan2(y, x) if (x != 0 or y != 0) else 0.0
        metal_route = gf.components.straight(length=30.0, width=2.5, layer=LAYER_METAL)
        mr_ref = c << metal_route
        mr_ref.move((x, y + ring_radius))
        mr_ref.rotate(np.degrees(angle), center=(x, y + ring_radius))

    return c

if __name__ == "__main__":
    # Example: Compiling a 37-Node Lattice Cluster (3 Rings out from center core node)
    onn_chip = open_source_parametric_onn_mesh(rings=3, pitch=20.0, ring_radius=20.0)
    onn_chip.write_gds("open_source_37_node_mesh.gds")
    print("📁 Production ready file saved as: open_source_37_node_mesh.gds")

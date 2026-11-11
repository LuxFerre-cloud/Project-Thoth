import numpy as np
import gdsfactory as gf

@gf.cell
def flower_of_life_chip(
    pitch: float = 20.0,
    ring_radius: float = 20.0,  # Based on layout log scaling
    wg_width: float = 0.5,
    trench_width: float = 2.0,
    via_size: float = 4.0,
    metal_width: float = 2.5
) -> gf.Component:
    
    c = gf.Component("monolithic_flower_of_life")
    
    # Define GDS Foundry Layers (Layer, DataType)
    LAYER_SI_CORE = (1, 0)
    LAYER_THERMAL_TRENCH = (2, 0)
    LAYER_VIA = (40, 0)
    LAYER_METAL = (41, 0)
    
    # 11x11 Grid Coordinate Matrix for the 19 Node Centers (relative to Row 6, Col 6 @ 0,0)
    nodes = {
        1:  (0.0, 0.0),
        2:  (0.0, -2.0 * pitch),
        3:  (+2.0 * pitch * np.cos(np.radians(30)), -1.0 * pitch),
        4:  (+2.0 * pitch * np.cos(np.radians(30)), +1.0 * pitch),
        5:  (0.0, +2.0 * pitch),
        6:  (-2.0 * pitch * np.cos(np.radians(30)), +1.0 * pitch),
        7:  (-2.0 * pitch * np.cos(np.radians(30)), -1.0 * pitch),
        8:  (0.0, -4.0 * pitch),
        9:  (+3.0 * pitch * np.cos(np.radians(30)), -3.0 * pitch * np.sin(np.radians(30))),
        10: (+5.0 * pitch * np.cos(np.radians(30)), -2.0 * pitch * np.sin(np.radians(30))),
        11: (+4.0 * pitch * np.cos(np.radians(30)), 0.0),
        12: (+5.0 * pitch * np.cos(np.radians(30)), +2.0 * pitch * np.sin(np.radians(30))),
        13: (+3.0 * pitch * np.cos(np.radians(30)), +3.0 * pitch * np.sin(np.radians(30))),
        14: (0.0, +4.0 * pitch),
        15: (-3.0 * pitch * np.cos(np.radians(30)), +3.0 * pitch * np.sin(np.radians(30))),
        16: (-5.0 * pitch * np.cos(np.radians(30)), +2.0 * pitch * np.sin(np.radians(30))),
        17: (-4.0 * pitch * np.cos(np.radians(30)), 0.0),
        18: (-5.0 * pitch * np.cos(np.radians(30)), -2.0 * pitch * np.sin(np.radians(30))),
        19: (-3.0 * pitch * np.cos(np.radians(30)), -3.0 * pitch * np.sin(np.radians(30)))
    }
    
    # Generate Stack Geometry for each Active Compute Node
    for node_id, (x, y) in nodes.items():
        # 1. Core Waveguide Ring
        ring_core = gf.components.ring(
            radius=ring_radius - (wg_width / 2),
            width=wg_width,
            layer=LAYER_SI_CORE
        )
        rc_ref = c << ring_core
        rc_ref.move((x, y))
        
        # 2. Concentric Deep Thermal Air Isolation Trenches (Inner and Outer boundaries)
        trench_out = gf.components.ring(
            radius=ring_radius + wg_width + (trench_width / 2),
            width=trench_width,
            layer=LAYER_THERMAL_TRENCH
        )
        to_ref = c << trench_out
        to_ref.move((x, y))
        
        # 3. Electro-Optic Phase Tuning Elements (Micro-Vias & Metal Micro-Heaters)
        via = gf.components.rectangle(size=(via_size, via_size), layer=LAYER_VIA, centered=True)
        v_ref = c << via
        v_ref.move((x, y + ring_radius))  # Anchor contacts to the crown of each node
        
        # Radial Electrical Interconnect Routing to periphery
        angle = np.arctan2(y, x) if (x != 0 or y != 0) else 0.0
        metal_route = gf.components.straight(
            length=40.0,
            width=metal_width,
            layer=LAYER_METAL
        )
        mr_ref = c << metal_route
        mr_ref.move((x, y + ring_radius))
        mr_ref.rotate(np.degrees(angle), center=(x, y + ring_radius))

    # 4. Fiber I/O Adiabatic Taper Interfaces (4 Cardinal Edge Boundaries)
    ports = {
        "West_In":    (-180.0, 0.0, 0),
        "East_Out":   (180.0, 0.0, 180),
        "North_Out":  (0.0, 180.0, 270),
        "South_Out":  (0.0, -180.0, 90)
    }
    
    for name, (px, py, orientation) in ports.items():
        taper = gf.components.taper(
            length=150.0,
            width1=0.15,  # Sub-wavelength adiabatic tip
            width2=wg_width,
            layer=LAYER_SI_CORE
        )
        t_ref = c << taper
        t_ref.move((px, py))
        t_ref.rotate(orientation, center=(px, py))
        
    return c

if __name__ == "__main__":
    # Compile Layout Blueprint
    component = flower_of_life_chip()
    # Save GDSII file for foundry delivery
    component.write_gds("monolithic_flower_of_life_chip.gds")
    print("SUCCESS: Monolithic 11x11 Photonic Stack Compiled.")

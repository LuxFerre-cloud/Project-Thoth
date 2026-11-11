#ifndef GWC_HAL_H
#define GWC_HAL_H

#include <stdint.h>

// Define register file mapping offsets matching the PCIe Bus spec
#define GWC_MMIO_BASE  0x40000000
#define GWC_REG_CTRL   ((volatile uint32_t*)(GWC_MMIO_BASE + 0x0000))
#define GWC_REG_STATUS ((volatile uint32_t*)(GWC_MMIO_BASE + 0x0010))

// Structural abstraction for a 6-axis geometric vector
typedef struct {
    float components[6];
} GWC_Vector6D;

// Inline assembly macro executing the custom RISC-V 'gwc.merge' opcode
static inline float riscv_gwc_merge(uint32_t addr_a, uint32_t addr_b) {
    float resonance_score;
    // Opcode 0x0B (0001011) registers custom RISC-V hardware execution extension
    __asm__ volatile (
        ".insn r 0x0B, 0, 1, %0, %1, %2"
        : "=f"(resonance_score)
        : "r"(addr_a), "r"(addr_b)
    );
    return resonance_score;
}

#endif // GWC_HAL_H

# ALD Thin-Film Process Optimization
# Step 6: Complete ALD Process Parameter Model
# Temperature + Pressure + TMA + H2O + Purge

import os
import numpy as np
import matplotlib.pyplot as plt

os.makedirs("results", exist_ok=True)


# ============================================================
# Baseline ALD Recipe
# ============================================================

MATERIAL = "Al2O3"
PRECURSOR = "TMA"
REACTANT = "H2O"

baseline_temperature_C = 200.0
baseline_pressure_Torr = 1.0

baseline_precursor_pulse_s = 1.0
baseline_purge_s = 10.0
baseline_reactant_pulse_s = 1.0

num_cycles = 100

baseline_GPC_nm_per_cycle = 0.10


# ============================================================
# Temperature Effect
# ============================================================

def temperature_factor(temperature_C):

    if temperature_C < 180:

        factor = 0.70 + 0.30 * (
            (temperature_C - 150) / 30
        )

        return np.clip(factor, 0.50, 1.00)

    elif temperature_C <= 220:

        return 1.00

    else:

        increase = 0.20 * (
            (temperature_C - 220) / 30
        )

        return 1.00 + increase


# ============================================================
# Pressure Effect
# ============================================================

def pressure_factor(pressure_Torr):

    """
    Simplified pressure-response model.

    The model assumes an optimum process region
    around the baseline pressure of 1 Torr.

    Lower or higher pressure produces a gradual
    reduction in effective growth.
    """

    optimum_pressure = 1.0

    # Width controls how rapidly the process
    # response decreases away from the optimum.
    pressure_width = 0.75

    factor = np.exp(
        -0.5
        * (
            (pressure_Torr - optimum_pressure)
            / pressure_width
        ) ** 2
    )

    # Keep the model from producing unrealistically
    # low growth values.
    return np.clip(factor, 0.70, 1.00)


# ============================================================
# TMA Precursor Pulse Saturation
# ============================================================

def precursor_pulse_factor(precursor_pulse_s):

    saturation_time = 1.0

    factor = 1.0 - np.exp(
        -precursor_pulse_s / saturation_time
    )

    baseline_factor = 1.0 - np.exp(
        -baseline_precursor_pulse_s / saturation_time
    )

    factor = factor / baseline_factor

    return np.clip(factor, 0.50, 1.05)


# ============================================================
# H2O Reactant Pulse Saturation
# ============================================================

def reactant_pulse_factor(reactant_pulse_s):

    saturation_time = 1.0

    factor = 1.0 - np.exp(
        -reactant_pulse_s / saturation_time
    )

    baseline_factor = 1.0 - np.exp(
        -baseline_reactant_pulse_s / saturation_time
    )

    factor = factor / baseline_factor

    return np.clip(factor, 0.50, 1.05)


# ============================================================
# Purge Effect
# ============================================================

def purge_factor(purge_s):

    minimum_effective_purge = 5.0

    if purge_s < minimum_effective_purge:

        factor = 0.70 + 0.30 * (
            purge_s / minimum_effective_purge
        )

        return np.clip(factor, 0.50, 1.00)

    else:

        return 1.00


# ============================================================
# Combined GPC Model
# ============================================================

def calculate_gpc(
    temperature_C,
    pressure_Torr,
    precursor_pulse_s,
    reactant_pulse_s,
    purge_s
):

    temp_factor = temperature_factor(
        temperature_C
    )

    pressure_response = pressure_factor(
        pressure_Torr
    )

    precursor_factor = precursor_pulse_factor(
        precursor_pulse_s
    )

    reactant_factor = reactant_pulse_factor(
        reactant_pulse_s
    )

    purge_efficiency = purge_factor(
        purge_s
    )

    gpc = (
        baseline_GPC_nm_per_cycle
        * temp_factor
        * pressure_response
        * precursor_factor
        * reactant_factor
        * purge_efficiency
    )

    return gpc


# ============================================================
# Cycle Time
# ============================================================

def calculate_cycle_time(
    precursor_pulse_s,
    purge_s,
    reactant_pulse_s
):

    return (
        precursor_pulse_s
        + purge_s
        + reactant_pulse_s
        + purge_s
    )


# ============================================================
# Total Process Time
# ============================================================

def calculate_total_process_time(
    precursor_pulse_s,
    purge_s,
    reactant_pulse_s,
    cycles
):

    cycle_time = calculate_cycle_time(
        precursor_pulse_s,
        purge_s,
        reactant_pulse_s
    )

    return cycle_time * cycles


# ============================================================
# Relative Throughput
# ============================================================

def calculate_throughput(cycle_time_s):

    return 3600 / cycle_time_s


# ============================================================
# Baseline Calculation
# ============================================================

baseline_gpc = calculate_gpc(
    baseline_temperature_C,
    baseline_pressure_Torr,
    baseline_precursor_pulse_s,
    baseline_reactant_pulse_s,
    baseline_purge_s
)

baseline_thickness = (
    baseline_gpc * num_cycles
)

baseline_cycle_time = calculate_cycle_time(
    baseline_precursor_pulse_s,
    baseline_purge_s,
    baseline_reactant_pulse_s
)

baseline_total_time = calculate_total_process_time(
    baseline_precursor_pulse_s,
    baseline_purge_s,
    baseline_reactant_pulse_s,
    num_cycles
)

baseline_throughput = calculate_throughput(
    baseline_cycle_time
)


# ============================================================
# Display Baseline Results
# ============================================================

print("=" * 70)
print("ALD THIN-FILM PROCESS MODEL")
print("=" * 70)

print(f"Material              : {MATERIAL}")
print(f"Precursor             : {PRECURSOR}")
print(f"Reactant              : {REACTANT}")

print("\nBASELINE PROCESS PARAMETERS")
print("-" * 70)

print(f"Temperature            : {baseline_temperature_C:.1f} °C")
print(f"Chamber Pressure       : {baseline_pressure_Torr:.2f} Torr")
print(f"TMA Pulse              : {baseline_precursor_pulse_s:.2f} s")
print(f"Purge Time             : {baseline_purge_s:.2f} s")
print(f"H2O Pulse              : {baseline_reactant_pulse_s:.2f} s")
print(f"Number of Cycles       : {num_cycles}")

print("\nMODEL OUTPUT")
print("-" * 70)

print(f"GPC                    : {baseline_gpc:.3f} nm/cycle")
print(f"Film Thickness         : {baseline_thickness:.2f} nm")
print(f"ALD Cycle Time         : {baseline_cycle_time:.2f} s")
print(f"Total Deposition Time  : {baseline_total_time:.2f} s")
print(f"Relative Throughput    : {baseline_throughput:.2f} cycles/hour")

print("=" * 70)


# ============================================================
# Plot 1: GPC vs Temperature
# ============================================================

temperatures = np.arange(150, 251, 1)

gpc_temperature = np.array([
    calculate_gpc(
        T,
        baseline_pressure_Torr,
        baseline_precursor_pulse_s,
        baseline_reactant_pulse_s,
        baseline_purge_s
    )
    for T in temperatures
])

plt.figure(figsize=(9, 5))

plt.plot(
    temperatures,
    gpc_temperature,
    linewidth=2,
    label="Modeled GPC"
)

plt.axvspan(
    180,
    220,
    alpha=0.2,
    label="Modeled ALD Window"
)

plt.axvline(
    baseline_temperature_C,
    linestyle="--",
    linewidth=1.5,
    label="Baseline: 200 °C"
)

plt.xlabel("Substrate Temperature (°C)")
plt.ylabel("Growth Per Cycle (nm/cycle)")
plt.title("Modeled ALD GPC vs Temperature")

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/gpc_vs_temperature.png",
    dpi=300
)

plt.show()


# ============================================================
# Plot 2: GPC vs TMA Pulse
# ============================================================

precursor_pulses = np.linspace(0.1, 2.0, 100)

gpc_precursor = np.array([
    calculate_gpc(
        baseline_temperature_C,
        baseline_pressure_Torr,
        pulse,
        baseline_reactant_pulse_s,
        baseline_purge_s
    )
    for pulse in precursor_pulses
])

plt.figure(figsize=(9, 5))

plt.plot(
    precursor_pulses,
    gpc_precursor,
    linewidth=2,
    label="Modeled GPC"
)

plt.axvline(
    baseline_precursor_pulse_s,
    linestyle="--",
    linewidth=1.5,
    label="Baseline: 1.0 s"
)

plt.xlabel("TMA Precursor Pulse Time (s)")
plt.ylabel("Growth Per Cycle (nm/cycle)")
plt.title("Modeled ALD GPC vs TMA Precursor Pulse")

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/gpc_vs_precursor_pulse.png",
    dpi=300
)

plt.show()


# ============================================================
# Plot 3: GPC vs H2O Pulse
# ============================================================

reactant_pulses = np.linspace(0.1, 2.0, 100)

gpc_reactant = np.array([
    calculate_gpc(
        baseline_temperature_C,
        baseline_pressure_Torr,
        baseline_precursor_pulse_s,
        pulse,
        baseline_purge_s
    )
    for pulse in reactant_pulses
])

plt.figure(figsize=(9, 5))

plt.plot(
    reactant_pulses,
    gpc_reactant,
    linewidth=2,
    label="Modeled GPC"
)

plt.axvline(
    baseline_reactant_pulse_s,
    linestyle="--",
    linewidth=1.5,
    label="Baseline: 1.0 s"
)

plt.xlabel("H2O Reactant Pulse Time (s)")
plt.ylabel("Growth Per Cycle (nm/cycle)")
plt.title("Modeled ALD GPC vs H2O Reactant Pulse")

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/gpc_vs_reactant_pulse.png",
    dpi=300
)

plt.show()


# ============================================================
# Plot 4: GPC vs Purge Time
# ============================================================

purge_times = np.linspace(1, 20, 100)

gpc_purge = np.array([
    calculate_gpc(
        baseline_temperature_C,
        baseline_pressure_Torr,
        baseline_precursor_pulse_s,
        baseline_reactant_pulse_s,
        purge
    )
    for purge in purge_times
])

plt.figure(figsize=(9, 5))

plt.plot(
    purge_times,
    gpc_purge,
    linewidth=2,
    label="Modeled GPC"
)

plt.axvline(
    baseline_purge_s,
    linestyle="--",
    linewidth=1.5,
    label="Baseline: 10 s"
)

plt.xlabel("Purge Time (s)")
plt.ylabel("Growth Per Cycle (nm/cycle)")
plt.title("Modeled ALD GPC vs Purge Time")

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/gpc_vs_purge_time.png",
    dpi=300
)

plt.show()


# ============================================================
# Plot 5: Cycle Time vs Purge Time
# ============================================================

cycle_times = np.array([
    calculate_cycle_time(
        baseline_precursor_pulse_s,
        purge,
        baseline_reactant_pulse_s
    )
    for purge in purge_times
])

plt.figure(figsize=(9, 5))

plt.plot(
    purge_times,
    cycle_times,
    linewidth=2
)

plt.axvline(
    baseline_purge_s,
    linestyle="--",
    linewidth=1.5,
    label="Baseline: 10 s"
)

plt.xlabel("Purge Time (s)")
plt.ylabel("ALD Cycle Time (s)")
plt.title("ALD Cycle Time vs Purge Time")

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/cycle_time_vs_purge.png",
    dpi=300
)

plt.show()


# ============================================================
# Plot 6: GPC vs Chamber Pressure
# ============================================================

pressures = np.linspace(
    0.5,
    2.0,
    100
)

gpc_pressure = np.array([
    calculate_gpc(
        baseline_temperature_C,
        pressure,
        baseline_precursor_pulse_s,
        baseline_reactant_pulse_s,
        baseline_purge_s
    )
    for pressure in pressures
])

plt.figure(figsize=(9, 5))

plt.plot(
    pressures,
    gpc_pressure,
    linewidth=2,
    label="Modeled GPC"
)

plt.axvline(
    baseline_pressure_Torr,
    linestyle="--",
    linewidth=1.5,
    label="Baseline: 1.0 Torr"
)

plt.xlabel("Chamber Pressure (Torr)")
plt.ylabel("Growth Per Cycle (nm/cycle)")
plt.title("Modeled ALD GPC vs Chamber Pressure")

plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

plt.savefig(
    "results/gpc_vs_pressure.png",
    dpi=300
)

plt.show()
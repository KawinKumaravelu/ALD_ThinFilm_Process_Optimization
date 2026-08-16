# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 8: XPS-BASED FILM CHARACTERIZATION
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

INPUT_FILE = "results/DOE_film_quality_results.csv"

# Baseline ALD condition
BASELINE_TEMPERATURE = 200.0
BASELINE_PRESSURE = 1.00
BASELINE_TMA_PULSE = 1.00
BASELINE_H2O_PULSE = 1.00
BASELINE_PURGE = 10.0


# ============================================================
# LOAD DOE DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("XPS-BASED FILM CHARACTERIZATION")
print("=" * 75)

print(
    f"DOE experiments loaded : {len(df)}"
)


# ============================================================
# SELECT BASELINE FILM
# ============================================================

baseline = df[
    (df["Temperature_C"] == BASELINE_TEMPERATURE)
    &
    (df["Pressure_Torr"] == BASELINE_PRESSURE)
    &
    (df["TMA_Pulse_s"] == BASELINE_TMA_PULSE)
    &
    (df["H2O_Pulse_s"] == BASELINE_H2O_PULSE)
    &
    (df["Purge_s"] == BASELINE_PURGE)
]


if len(baseline) == 0:
    raise ValueError(
        "Baseline ALD condition was not found."
    )


baseline = baseline.iloc[0]


# ============================================================
# REFERENCE CHEMICAL COMPOSITION
# ============================================================

# Idealized Al2O3 composition
reference_al_fraction = 2 / 5
reference_o_fraction = 3 / 5

reference_o_al_ratio = 3 / 2


print()
print("=" * 75)
print("REFERENCE Al2O3 COMPOSITION")
print("=" * 75)

print(
    f"Reference Al fraction : "
    f"{reference_al_fraction:.3f}"
)

print(
    f"Reference O fraction  : "
    f"{reference_o_fraction:.3f}"
)

print(
    f"Reference O/Al ratio  : "
    f"{reference_o_al_ratio:.3f}"
)


# ============================================================
# XPS BINDING ENERGY RANGE
# ============================================================

binding_energy = np.linspace(
    0,
    1200,
    6000
)


# ============================================================
# GAUSSIAN PEAK FUNCTION
# ============================================================

def gaussian(
    x,
    amplitude,
    center,
    sigma
):

    return (
        amplitude
        *
        np.exp(
            -0.5
            *
            (
                (x - center)
                /
                sigma
            ) ** 2
        )
    )


# ============================================================
# SIMULATED XPS PEAK POSITIONS
# ============================================================
#
# Simplified representative peak positions:
#
# Al 2p  -> ~74 eV
# O 1s   -> ~531 eV
# C 1s   -> ~285 eV
#
# The C 1s peak represents a small surface
# hydrocarbon contamination signal.
# ============================================================

al2p_center = 74.0
o1s_center = 531.0
c1s_center = 285.0


# ============================================================
# PEAK WIDTHS
# ============================================================

al2p_sigma = 1.3
o1s_sigma = 1.5
c1s_sigma = 1.4


# ============================================================
# PEAK INTENSITIES
# ============================================================

al2p_amplitude = 1.00
o1s_amplitude = 1.55
c1s_amplitude = 0.18


# ============================================================
# BACKGROUND
# ============================================================

background = (
    0.015
    +
    0.00001
    *
    binding_energy
)


# ============================================================
# GENERATE IDEAL XPS SPECTRUM
# ============================================================

al2p_peak = gaussian(
    binding_energy,
    al2p_amplitude,
    al2p_center,
    al2p_sigma
)

o1s_peak = gaussian(
    binding_energy,
    o1s_amplitude,
    o1s_center,
    o1s_sigma
)

c1s_peak = gaussian(
    binding_energy,
    c1s_amplitude,
    c1s_center,
    c1s_sigma
)


ideal_spectrum = (
    background
    +
    al2p_peak
    +
    o1s_peak
    +
    c1s_peak
)


# ============================================================
# ADD SIMULATED MEASUREMENT NOISE
# ============================================================

np.random.seed(42)

noise = np.random.normal(
    0,
    0.008,
    len(binding_energy)
)


measured_spectrum = (
    ideal_spectrum
    +
    noise
)


measured_spectrum = np.clip(
    measured_spectrum,
    0,
    None
)


# ============================================================
# PEAK FITTING FUNCTION
# ============================================================

def peak_model(
    x,
    amplitude,
    center,
    sigma,
    offset,
    slope
):

    return (
        offset
        +
        slope * x
        +
        gaussian(
            x,
            amplitude,
            center,
            sigma
        )
    )


# ============================================================
# FIT INDIVIDUAL PEAK
# ============================================================

def fit_peak(
    center,
    window_low,
    window_high
):

    mask = (
        (binding_energy >= window_low)
        &
        (binding_energy <= window_high)
    )

    x = binding_energy[mask]
    y = measured_spectrum[mask]


    initial_guess = [

        np.max(y),

        center,

        1.5,

        np.min(y),

        0.0
    ]


    lower_bounds = [

        0.0,

        center - 5,

        0.3,

        0.0,

        -0.01
    ]


    upper_bounds = [

        10.0,

        center + 5,

        5.0,

        1.0,

        0.01
    ]


    fitted_parameters, _ = curve_fit(

        peak_model,

        x,

        y,

        p0=initial_guess,

        bounds=(
            lower_bounds,
            upper_bounds
        ),

        maxfev=10000
    )


    return fitted_parameters


# ============================================================
# FIT Al 2p
# ============================================================

al_fit = fit_peak(
    al2p_center,
    65,
    85
)


al_amplitude = al_fit[0]
al_binding_energy = al_fit[1]
al_sigma = al_fit[2]


# ============================================================
# FIT O 1s
# ============================================================

o_fit = fit_peak(
    o1s_center,
    520,
    545
)


o_amplitude = o_fit[0]
o_binding_energy = o_fit[1]
o_sigma = o_fit[2]


# ============================================================
# FIT C 1s
# ============================================================

c_fit = fit_peak(
    c1s_center,
    275,
    295
)


c_amplitude = c_fit[0]
c_binding_energy = c_fit[1]
c_sigma = c_fit[2]


# ============================================================
# XPS QUANTIFICATION
# ============================================================
#
# For a simplified educational model:
#
# Al signal area ∝ Al concentration
# O signal area  ∝ O concentration
#
# Integrated Gaussian area:
#
# Area = A * sigma * sqrt(2*pi)
# ============================================================

al_area = (
    al_amplitude
    *
    al_sigma
    *
    np.sqrt(2 * np.pi)
)


o_area = (
    o_amplitude
    *
    o_sigma
    *
    np.sqrt(2 * np.pi)
)


c_area = (
    c_amplitude
    *
    c_sigma
    *
    np.sqrt(2 * np.pi)
)


# ============================================================
# SENSITIVITY FACTORS
# ============================================================
#
# Real XPS quantification requires sensitivity factors.
# We use simplified sensitivity factors here.
# ============================================================

al_sensitivity = 1.00
o_sensitivity = 1.00
c_sensitivity = 1.00


al_corrected = (
    al_area
    /
    al_sensitivity
)


o_corrected = (
    o_area
    /
    o_sensitivity
)


c_corrected = (
    c_area
    /
    c_sensitivity
)


total_signal = (
    al_corrected
    +
    o_corrected
    +
    c_corrected
)


al_atomic_percent = (
    al_corrected
    /
    total_signal
    *
    100
)


o_atomic_percent = (
    o_corrected
    /
    total_signal
    *
    100
)


c_atomic_percent = (
    c_corrected
    /
    total_signal
    *
    100
)


# ============================================================
# O/Al RATIO
# ============================================================

o_al_ratio = (
    o_atomic_percent
    /
    al_atomic_percent
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 75)
print("XPS PEAK FITTING RESULTS")
print("=" * 75)

print(
    f"Al 2p binding energy  : "
    f"{al_binding_energy:.2f} eV"
)

print(
    f"O 1s binding energy   : "
    f"{o_binding_energy:.2f} eV"
)

print(
    f"C 1s binding energy   : "
    f"{c_binding_energy:.2f} eV"
)

print()

print(
    f"Al 2p peak area       : "
    f"{al_area:.4f}"
)

print(
    f"O 1s peak area        : "
    f"{o_area:.4f}"
)

print(
    f"C 1s peak area        : "
    f"{c_area:.4f}"
)


print()
print("=" * 75)
print("XPS COMPOSITION ANALYSIS")
print("=" * 75)

print(
    f"Al atomic %           : "
    f"{al_atomic_percent:.2f}%"
)

print(
    f"O atomic %            : "
    f"{o_atomic_percent:.2f}%"
)

print(
    f"C atomic %            : "
    f"{c_atomic_percent:.2f}%"
)

print(
    f"O/Al ratio            : "
    f"{o_al_ratio:.3f}"
)

print(
    f"Reference O/Al ratio  : "
    f"{reference_o_al_ratio:.3f}"
)


# ============================================================
# STOICHIOMETRY ERROR
# ============================================================

o_al_error = (
    abs(
        o_al_ratio
        -
        reference_o_al_ratio
    )
    /
    reference_o_al_ratio
    *
    100
)


print(
    f"O/Al ratio error      : "
    f"{o_al_error:.2f}%"
)


# ============================================================
# CARBON CONTAMINATION
# ============================================================

print()
print(
    f"Surface C contamination : "
    f"{c_atomic_percent:.2f}%"
)


# ============================================================
# SAVE XPS DATA
# ============================================================

xps_data = pd.DataFrame({

    "Binding_Energy_eV":
        binding_energy,

    "Measured_Intensity":
        measured_spectrum,

    "Ideal_Spectrum":
        ideal_spectrum
})


xps_data.to_csv(
    "results/simulated_XPS_data.csv",
    index=False
)


# ============================================================
# SAVE XPS SUMMARY
# ============================================================

xps_summary = pd.DataFrame({

    "Parameter": [

        "Al 2p Binding Energy",
        "O 1s Binding Energy",
        "C 1s Binding Energy",
        "Al Atomic %",
        "O Atomic %",
        "C Atomic %",
        "O/Al Ratio",
        "Reference O/Al Ratio"
    ],

    "Value": [

        al_binding_energy,
        o_binding_energy,
        c_binding_energy,
        al_atomic_percent,
        o_atomic_percent,
        c_atomic_percent,
        o_al_ratio,
        reference_o_al_ratio
    ],

    "Unit": [

        "eV",
        "eV",
        "eV",
        "%",
        "%",
        "%",
        "ratio",
        "ratio"
    ]
})


xps_summary.to_csv(
    "results/XPS_characterization_summary.csv",
    index=False
)


# ============================================================
# PLOT FULL XPS SPECTRUM
# ============================================================

plt.figure(
    figsize=(11, 6)
)


plt.plot(
    binding_energy,
    measured_spectrum,
    label="Simulated XPS"
)


plt.xlabel(
    "Binding Energy (eV)"
)

plt.ylabel(
    "Intensity (a.u.)"
)

plt.title(
    "Simulated XPS Spectrum of Al₂O₃ Thin Film"
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()


# XPS spectra are commonly displayed
# with high binding energy on the left.

plt.gca().invert_xaxis()


plt.tight_layout()


plt.savefig(
    "results/XPS_full_spectrum.png",
    dpi=300
)


plt.close()


# ============================================================
# PLOT HIGH-RESOLUTION Al 2p REGION
# ============================================================

mask_al = (
    (binding_energy >= 60)
    &
    (binding_energy <= 90)
)


plt.figure(
    figsize=(8, 5)
)


plt.plot(
    binding_energy[mask_al],
    measured_spectrum[mask_al]
)


plt.xlabel(
    "Binding Energy (eV)"
)

plt.ylabel(
    "Intensity (a.u.)"
)

plt.title(
    "XPS Al 2p Region"
)

plt.grid(
    True,
    alpha=0.3
)

plt.gca().invert_xaxis()

plt.tight_layout()


plt.savefig(
    "results/XPS_Al2p.png",
    dpi=300
)


plt.close()


# ============================================================
# PLOT HIGH-RESOLUTION O 1s REGION
# ============================================================

mask_o = (
    (binding_energy >= 515)
    &
    (binding_energy <= 550)
)


plt.figure(
    figsize=(8, 5)
)


plt.plot(
    binding_energy[mask_o],
    measured_spectrum[mask_o]
)


plt.xlabel(
    "Binding Energy (eV)"
)

plt.ylabel(
    "Intensity (a.u.)"
)

plt.title(
    "XPS O 1s Region"
)

plt.grid(
    True,
    alpha=0.3
)

plt.gca().invert_xaxis()

plt.tight_layout()


plt.savefig(
    "results/XPS_O1s.png",
    dpi=300
)


plt.close()


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("XPS ANALYSIS COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/simulated_XPS_data.csv"
)

print(
    "  results/XPS_characterization_summary.csv"
)

print(
    "  results/XPS_full_spectrum.png"
)

print(
    "  results/XPS_Al2p.png"
)

print(
    "  results/XPS_O1s.png"
)

print("=" * 75)
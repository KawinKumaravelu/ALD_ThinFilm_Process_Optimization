# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 7: XRR-BASED FILM CHARACTERIZATION
# ============================================================

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.optimize import least_squares


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

# Cu K-alpha X-ray wavelength
X_RAY_WAVELENGTH_NM = 0.15406


# ============================================================
# LOAD DOE DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("XRR-BASED FILM CHARACTERIZATION")
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
# REFERENCE FILM PARAMETERS
# ============================================================

true_thickness = float(
    baseline["Film_Thickness_nm"]
)

true_density = float(
    baseline["Film_Density_g_cm3"]
)

true_roughness = float(
    baseline["Surface_Roughness_nm_RMS"]
)


print()
print("=" * 75)
print("REFERENCE FILM PARAMETERS")
print("=" * 75)

print(
    f"Thickness              : "
    f"{true_thickness:.3f} nm"
)

print(
    f"Density                : "
    f"{true_density:.3f} g/cm³"
)

print(
    f"Surface roughness      : "
    f"{true_roughness:.3f} nm RMS"
)


# ============================================================
# XRR ANGLE RANGE
# ============================================================

theta_deg = np.linspace(
    0.05,
    5.0,
    2000
)

theta_rad = np.deg2rad(
    theta_deg
)


# ============================================================
# SIMPLIFIED XRR MODEL
# ============================================================
#
# The model contains:
#
# 1. Critical-angle dependence on density
# 2. Thin-film interference depending on thickness
# 3. Roughness damping
# 4. Fresnel-like decay
#
# This is an educational thin-film XRR model.
# It is NOT a full Parratt multilayer calculation.
# ============================================================

def xrr_model(
    theta_deg,
    thickness_nm,
    density_g_cm3,
    roughness_nm
):

    theta_rad = np.deg2rad(
        theta_deg
    )

    # --------------------------------------------------------
    # Approximate critical angle
    # --------------------------------------------------------

    # Reference critical angle for Al2O3-like material
    reference_density = 3.0

    critical_angle_deg = (
        0.55
        *
        np.sqrt(
            density_g_cm3
            /
            reference_density
        )
    )

    critical_angle_rad = np.deg2rad(
        critical_angle_deg
    )


    # --------------------------------------------------------
    # Fresnel-like reflectivity
    # --------------------------------------------------------

    sin_theta = np.sin(
        theta_rad
    )

    sin_critical = np.sin(
        critical_angle_rad
    )

    q_ratio = (
        sin_theta
        /
        (
            sin_critical
            + 1e-12
        )
    )


    # Below critical angle
    below_critical = (
        q_ratio <= 1
    )


    fresnel = np.where(
        below_critical,
        0.90,
        0.90
        /
        (
            1
            +
            q_ratio ** 4
        )
    )


    # --------------------------------------------------------
    # Thin-film interference
    # --------------------------------------------------------

    phase = (
        4
        * np.pi
        * thickness_nm
        * sin_theta
        /
        X_RAY_WAVELENGTH_NM
    )


    interference = (
        0.5
        +
        0.5
        *
        np.cos(phase)
    )


    # --------------------------------------------------------
    # Roughness damping
    # --------------------------------------------------------

    damping = np.exp(
        -(
            4
            * np.pi
            * roughness_nm
            * sin_theta
            /
            X_RAY_WAVELENGTH_NM
        ) ** 2
    )


    # --------------------------------------------------------
    # Combine
    # --------------------------------------------------------

    reflectivity = (
        fresnel
        *
        (
            0.20
            +
            0.80
            * interference
        )
        *
        damping
    )


    # Prevent zero/negative values
    reflectivity = np.clip(
        reflectivity,
        1e-10,
        1.0
    )


    return reflectivity


# ============================================================
# GENERATE IDEAL XRR CURVE
# ============================================================

true_reflectivity = xrr_model(
    theta_deg,
    true_thickness,
    true_density,
    true_roughness
)


# ============================================================
# SIMULATE MEASUREMENT NOISE
# ============================================================

np.random.seed(42)

noise = np.random.normal(
    0,
    0.015,
    len(true_reflectivity)
)


# Use multiplicative noise so the signal remains physical

measured_reflectivity = (
    true_reflectivity
    *
    (
        1
        +
        noise
    )
)


measured_reflectivity = np.clip(
    measured_reflectivity,
    1e-10,
    1.0
)


# ============================================================
# XRR FITTING
# ============================================================
#
# We fit:
#
# thickness
# density
# roughness
#
# by minimizing:
#
# SSE = Σ [R_measured - R_model]^2
#
# ============================================================

def residual_function(
    parameters
):

    thickness = parameters[0]

    density = parameters[1]

    roughness = parameters[2]


    predicted = xrr_model(
        theta_deg,
        thickness,
        density,
        roughness
    )


    # Fit logarithmic reflectivity because XRR
    # normally spans several orders of magnitude.

    measured_log = np.log10(
        measured_reflectivity
    )

    predicted_log = np.log10(
        predicted
    )


    return (
        predicted_log
        -
        measured_log
    )


# Initial guess intentionally differs
# from the true parameters.

initial_guess = [

    9.0,     # thickness

    2.90,    # density

    0.30     # roughness
]


# Physically reasonable fitting bounds

lower_bounds = [

    5.0,     # minimum thickness

    2.50,    # minimum density

    0.05     # minimum roughness
]


upper_bounds = [

    15.0,    # maximum thickness

    3.50,    # maximum density

    1.00     # maximum roughness
]


fit_result = least_squares(
    residual_function,
    initial_guess,
    bounds=(
        lower_bounds,
        upper_bounds
    ),
    max_nfev=5000
)


# ============================================================
# EXTRACT FITTED PARAMETERS
# ============================================================

fitted_thickness = (
    fit_result.x[0]
)

fitted_density = (
    fit_result.x[1]
)

fitted_roughness = (
    fit_result.x[2]
)


# ============================================================
# CALCULATE FITTED CURVE
# ============================================================

fitted_reflectivity = xrr_model(
    theta_deg,
    fitted_thickness,
    fitted_density,
    fitted_roughness
)


# ============================================================
# CALCULATE FIT ERRORS
# ============================================================

thickness_error = (
    abs(
        fitted_thickness
        -
        true_thickness
    )
    /
    true_thickness
    *
    100
)


density_error = (
    abs(
        fitted_density
        -
        true_density
    )
    /
    true_density
    *
    100
)


roughness_error = (
    abs(
        fitted_roughness
        -
        true_roughness
    )
    /
    true_roughness
    *
    100
)


# ============================================================
# CALCULATE FIT QUALITY
# ============================================================

log_measured = np.log10(
    measured_reflectivity
)

log_fitted = np.log10(
    fitted_reflectivity
)


rmse = np.sqrt(
    np.mean(
        (
            log_measured
            -
            log_fitted
        ) ** 2
    )
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 75)
print("XRR FITTING RESULTS")
print("=" * 75)

print(
    f"Optimization successful : "
    f"{fit_result.success}"
)

print(
    f"Number of iterations    : "
    f"{fit_result.nfev}"
)

print()

print(
    f"{'Parameter':<25}"
    f"{'Reference':>15}"
    f"{'Fitted':>15}"
    f"{'Error':>12}"
)

print("-" * 67)

print(
    f"{'Thickness (nm)':<25}"
    f"{true_thickness:>15.3f}"
    f"{fitted_thickness:>15.3f}"
    f"{thickness_error:>11.2f}%"
)

print(
    f"{'Density (g/cm³)':<25}"
    f"{true_density:>15.3f}"
    f"{fitted_density:>15.3f}"
    f"{density_error:>11.2f}%"
)

print(
    f"{'Roughness (nm RMS)':<25}"
    f"{true_roughness:>15.3f}"
    f"{fitted_roughness:>15.3f}"
    f"{roughness_error:>11.2f}%"
)

print()

print(
    f"Log-scale RMSE         : "
    f"{rmse:.6f}"
)


# ============================================================
# SAVE SIMULATED XRR DATA
# ============================================================

xrr_data = pd.DataFrame({

    "Theta_deg":
        theta_deg,

    "2Theta_deg":
        2 * theta_deg,

    "Measured_Reflectivity":
        measured_reflectivity,

    "Fitted_Reflectivity":
        fitted_reflectivity
})


xrr_data.to_csv(
    "results/simulated_XRR_data.csv",
    index=False
)


# ============================================================
# SAVE XRR CHARACTERIZATION SUMMARY
# ============================================================

summary = pd.DataFrame({

    "Parameter": [

        "Film Thickness",
        "Film Density",
        "Surface Roughness",
        "Log Scale RMSE"
    ],

    "Reference_Value": [

        true_thickness,
        true_density,
        true_roughness,
        np.nan
    ],

    "Fitted_Value": [

        fitted_thickness,
        fitted_density,
        fitted_roughness,
        rmse
    ],

    "Unit": [

        "nm",
        "g/cm3",
        "nm RMS",
        "-"
    ]
})


summary.to_csv(
    "results/XRR_characterization_summary.csv",
    index=False
)


# ============================================================
# PLOT 1 — XRR FIT
# ============================================================

plt.figure(
    figsize=(10, 6)
)

plt.semilogy(
    2 * theta_deg,
    measured_reflectivity,
    label="Simulated measurement"
)

plt.semilogy(
    2 * theta_deg,
    fitted_reflectivity,
    label="XRR fitted model"
)

plt.xlabel(
    "2θ (degrees)"
)

plt.ylabel(
    "Reflectivity"
)

plt.title(
    "XRR Fit — Al₂O₃ Thin Film"
)

plt.grid(
    True,
    alpha=0.3
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "results/XRR_fit.png",
    dpi=300
)

plt.close()


# ============================================================
# PLOT 2 — XRR RESIDUAL
# ============================================================

residuals = (
    log_measured
    -
    log_fitted
)


plt.figure(
    figsize=(10, 5)
)

plt.plot(
    2 * theta_deg,
    residuals
)

plt.axhline(
    0,
    linestyle="--"
)

plt.xlabel(
    "2θ (degrees)"
)

plt.ylabel(
    "Log10 Residual"
)

plt.title(
    "XRR Fit Residual"
)

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    "results/XRR_fit_residual.png",
    dpi=300
)

plt.close()


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("XRR ANALYSIS COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/simulated_XRR_data.csv"
)

print(
    "  results/XRR_characterization_summary.csv"
)

print(
    "  results/XRR_fit.png"
)

print(
    "  results/XRR_fit_residual.png"
)

print("=" * 75)
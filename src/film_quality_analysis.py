# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 6: FILM QUALITY ANALYSIS
# ============================================================

import os
import numpy as np
import pandas as pd

from ald_model import calculate_gpc


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

DOE_FILE = "results/DOE_results.csv"

NUM_WAFER_POINTS = 25


# ============================================================
# LOAD DOE DATA
# ============================================================

df = pd.read_csv(DOE_FILE)

print("=" * 75)
print("ALD FILM QUALITY ANALYSIS")
print("=" * 75)

print(
    f"DOE experiments loaded : {len(df)}"
)


# ============================================================
# FILM QUALITY MODEL
# ============================================================

def calculate_film_quality(row):

    temperature = row["Temperature_C"]
    pressure = row["Pressure_Torr"]
    tma_pulse = row["TMA_Pulse_s"]
    h2o_pulse = row["H2O_Pulse_s"]
    purge = row["Purge_s"]

    gpc = row["GPC_nm_per_cycle"]

    thickness = row["Film_Thickness_nm"]


    # --------------------------------------------------------
    # 1. Thickness Uniformity
    # --------------------------------------------------------
    #
    # Ideal process conditions are assumed to produce
    # better within-wafer uniformity.
    #
    # Uniformity is represented as 1-sigma variation (%).
    # Lower value = better uniformity.
    # --------------------------------------------------------

    temperature_penalty = abs(
        temperature - 200
    ) / 40

    pressure_penalty = abs(
        pressure - 1.0
    ) / 0.4

    pulse_penalty = (
        abs(tma_pulse - 1.0)
        +
        abs(h2o_pulse - 1.0)
    ) / 2.0

    purge_penalty = max(
        0,
        (5.0 - purge) / 2.5
    )

    uniformity_sigma = (
        1.0
        +
        0.8 * temperature_penalty
        +
        0.5 * pressure_penalty
        +
        0.6 * pulse_penalty
        +
        0.8 * purge_penalty
    )


    # --------------------------------------------------------
    # 2. Film Stress
    # --------------------------------------------------------
    #
    # Simplified residual-stress model.
    #
    # Lower absolute stress = better.
    # --------------------------------------------------------

    stress_MPa = (
        50
        + 25 * (temperature - 200) / 40
        + 20 * (pressure - 1.0) / 0.4
        + 15 * (tma_pulse - 1.0)
        + 15 * (h2o_pulse - 1.0)
    )


    # --------------------------------------------------------
    # 3. Film Density
    # --------------------------------------------------------
    #
    # Target density is approximately represented by
    # the baseline value.
    # --------------------------------------------------------

    density_g_cm3 = (
        3.00
        - 0.10 * temperature_penalty
        - 0.05 * pressure_penalty
        - 0.05 * pulse_penalty
    )


    # --------------------------------------------------------
    # 4. Surface Roughness
    # --------------------------------------------------------
    #
    # Lower roughness = smoother film.
    #
    # Unit: nm RMS
    # --------------------------------------------------------

    roughness_nm_RMS = (
        0.20
        + 0.08 * temperature_penalty
        + 0.05 * pressure_penalty
        + 0.06 * pulse_penalty
        + 0.08 * purge_penalty
    )


    # --------------------------------------------------------
    # 5. Defectivity
    # --------------------------------------------------------
    #
    # Simplified defect-density model.
    #
    # Unit: defects/cm²
    # Lower value = better.
    # --------------------------------------------------------

    defect_density = (
        5
        + 15 * temperature_penalty
        + 10 * pressure_penalty
        + 12 * pulse_penalty
        + 20 * purge_penalty
    )


    return (
        uniformity_sigma,
        stress_MPa,
        density_g_cm3,
        roughness_nm_RMS,
        defect_density
    )


# ============================================================
# APPLY FILM QUALITY MODEL
# ============================================================

quality_results = []

for _, row in df.iterrows():

    (
        uniformity,
        stress,
        density,
        roughness,
        defects
    ) = calculate_film_quality(row)

    quality_results.append({

        "Thickness_Uniformity_1sigma_%":
            uniformity,

        "Film_Stress_MPa":
            stress,

        "Film_Density_g_cm3":
            density,

        "Surface_Roughness_nm_RMS":
            roughness,

        "Defect_Density_per_cm2":
            defects
    })


quality_df = pd.DataFrame(
    quality_results
)


# ============================================================
# COMBINE WITH DOE DATA
# ============================================================

combined_df = pd.concat(
    [
        df,
        quality_df
    ],
    axis=1
)


# ============================================================
# SAVE RESULTS
# ============================================================

output_file = (
    "results/DOE_film_quality_results.csv"
)

combined_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# DISPLAY SUMMARY
# ============================================================

print()
print("=" * 75)
print("FILM QUALITY SUMMARY")
print("=" * 75)

print(
    f"Uniformity minimum    : "
    f"{combined_df['Thickness_Uniformity_1sigma_%'].min():.3f} %"
)

print(
    f"Uniformity maximum    : "
    f"{combined_df['Thickness_Uniformity_1sigma_%'].max():.3f} %"
)

print(
    f"Stress minimum        : "
    f"{combined_df['Film_Stress_MPa'].min():.2f} MPa"
)

print(
    f"Stress maximum        : "
    f"{combined_df['Film_Stress_MPa'].max():.2f} MPa"
)

print(
    f"Density minimum       : "
    f"{combined_df['Film_Density_g_cm3'].min():.3f} g/cm³"
)

print(
    f"Density maximum       : "
    f"{combined_df['Film_Density_g_cm3'].max():.3f} g/cm³"
)

print(
    f"Roughness minimum     : "
    f"{combined_df['Surface_Roughness_nm_RMS'].min():.3f} nm"
)

print(
    f"Roughness maximum     : "
    f"{combined_df['Surface_Roughness_nm_RMS'].max():.3f} nm"
)

print(
    f"Defect density min    : "
    f"{combined_df['Defect_Density_per_cm2'].min():.2f} defects/cm²"
)

print(
    f"Defect density max    : "
    f"{combined_df['Defect_Density_per_cm2'].max():.2f} defects/cm²"
)


# ============================================================
# BEST FILM QUALITY CONDITION
# ============================================================

# Normalize each quality metric between 0 and 1.
# Higher score = better.

def normalize_lower_better(series):

    minimum = series.min()
    maximum = series.max()

    return (
        (maximum - series)
        / (maximum - minimum)
    )


def normalize_target(series, target):

    maximum_error = max(
        abs(series - target).max(),
        1e-12
    )

    return (
        1
        -
        abs(series - target)
        / maximum_error
    )


uniformity_score = normalize_lower_better(
    combined_df[
        "Thickness_Uniformity_1sigma_%"
    ]
)

stress_score = normalize_lower_better(
    abs(
        combined_df[
            "Film_Stress_MPa"
        ]
    )
)

roughness_score = normalize_lower_better(
    combined_df[
        "Surface_Roughness_nm_RMS"
    ]
)

defect_score = normalize_lower_better(
    combined_df[
        "Defect_Density_per_cm2"
    ]
)

density_score = normalize_target(
    combined_df[
        "Film_Density_g_cm3"
    ],
    3.00
)


# ============================================================
# OVERALL FILM QUALITY SCORE
# ============================================================

combined_df[
    "Film_Quality_Score"
] = (
    0.25 * uniformity_score
    + 0.20 * stress_score
    + 0.20 * density_score
    + 0.20 * roughness_score
    + 0.15 * defect_score
)


# ============================================================
# FIND BEST FILM QUALITY CONDITION
# ============================================================

best_quality_row = combined_df.loc[
    combined_df[
        "Film_Quality_Score"
    ].idxmax()
]


print()
print("=" * 75)
print("BEST FILM QUALITY CONDITION")
print("=" * 75)

print(
    f"Experiment            : "
    f"{int(best_quality_row['Experiment'])}"
)

print(
    f"Temperature           : "
    f"{best_quality_row['Temperature_C']:.2f} °C"
)

print(
    f"Pressure              : "
    f"{best_quality_row['Pressure_Torr']:.2f} Torr"
)

print(
    f"TMA Pulse             : "
    f"{best_quality_row['TMA_Pulse_s']:.2f} s"
)

print(
    f"H2O Pulse             : "
    f"{best_quality_row['H2O_Pulse_s']:.2f} s"
)

print(
    f"Purge                 : "
    f"{best_quality_row['Purge_s']:.2f} s"
)

print(
    f"GPC                   : "
    f"{best_quality_row['GPC_nm_per_cycle']:.4f} nm/cycle"
)

print(
    f"Thickness             : "
    f"{best_quality_row['Film_Thickness_nm']:.2f} nm"
)

print(
    f"Uniformity            : "
    f"{best_quality_row['Thickness_Uniformity_1sigma_%']:.3f} %"
)

print(
    f"Stress                : "
    f"{best_quality_row['Film_Stress_MPa']:.2f} MPa"
)

print(
    f"Density               : "
    f"{best_quality_row['Film_Density_g_cm3']:.3f} g/cm³"
)

print(
    f"Roughness             : "
    f"{best_quality_row['Surface_Roughness_nm_RMS']:.3f} nm"
)

print(
    f"Defect Density        : "
    f"{best_quality_row['Defect_Density_per_cm2']:.2f}"
    f" defects/cm²"
)

print(
    f"Film Quality Score    : "
    f"{best_quality_row['Film_Quality_Score']:.4f}"
)


# ============================================================
# FINAL SAVE
# ============================================================

combined_df.to_csv(
    output_file,
    index=False
)


print()
print("=" * 75)
print("FILM QUALITY ANALYSIS COMPLETE")
print("=" * 75)

print(
    f"Results saved to: {output_file}"
)

print("=" * 75)
# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 11: OPTIMUM ALD PROCESS WINDOW
# ============================================================

import os
import numpy as np
import pandas as pd


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

INPUT_FILE = "results/DOE_film_quality_results.csv"

TARGET_THICKNESS = 10.0       # nm

# Engineering constraints
MAX_THICKNESS_ERROR = 5.0     # %
MAX_UNIFORMITY = 2.0          # %
MAX_ABS_STRESS = 80.0         # MPa
MIN_DENSITY = 2.90             # g/cm3
MAX_ROUGHNESS = 0.30           # nm RMS
MAX_DEFECT_DENSITY = 20.0      # defects/cm2
MIN_THROUGHPUT = 150.0         # cycles/hour


# ============================================================
# LOAD DOE DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("ALD PROCESS OPTIMIZATION")
print("=" * 75)

print(
    f"DOE experiments loaded : {len(df)}"
)


# ============================================================
# CALCULATE THICKNESS ERROR
# ============================================================

df["Thickness_Error_%"] = (
    abs(
        df["Film_Thickness_nm"]
        - TARGET_THICKNESS
    )
    /
    TARGET_THICKNESS
    *
    100
)


# ============================================================
# APPLY PROCESS CONSTRAINTS
# ============================================================

df["Thickness_OK"] = (
    df["Thickness_Error_%"]
    <= MAX_THICKNESS_ERROR
)

df["Uniformity_OK"] = (
    df["Thickness_Uniformity_1sigma_%"]
    <= MAX_UNIFORMITY
)

df["Stress_OK"] = (
    abs(
        df["Film_Stress_MPa"]
    )
    <= MAX_ABS_STRESS
)

df["Density_OK"] = (
    df["Film_Density_g_cm3"]
    >= MIN_DENSITY
)

df["Roughness_OK"] = (
    df["Surface_Roughness_nm_RMS"]
    <= MAX_ROUGHNESS
)

df["Defectivity_OK"] = (
    df["Defect_Density_per_cm2"]
    <= MAX_DEFECT_DENSITY
)

df["Throughput_OK"] = (
    df["Relative_Throughput_cycles_per_hour"]
    >= MIN_THROUGHPUT
)


# ============================================================
# OVERALL PROCESS ACCEPTANCE
# ============================================================

df["Process_Qualified"] = (
    df["Thickness_OK"]
    &
    df["Uniformity_OK"]
    &
    df["Stress_OK"]
    &
    df["Density_OK"]
    &
    df["Roughness_OK"]
    &
    df["Defectivity_OK"]
    &
    df["Throughput_OK"]
)


# ============================================================
# DISPLAY CONSTRAINTS
# ============================================================

print()
print("=" * 75)
print("PROCESS CONSTRAINTS")
print("=" * 75)

print(
    f"Target thickness       : "
    f"{TARGET_THICKNESS:.2f} nm"
)

print(
    f"Maximum thickness error: "
    f"{MAX_THICKNESS_ERROR:.2f} %"
)

print(
    f"Maximum uniformity     : "
    f"{MAX_UNIFORMITY:.2f} %"
)

print(
    f"Maximum |stress|       : "
    f"{MAX_ABS_STRESS:.2f} MPa"
)

print(
    f"Minimum density        : "
    f"{MIN_DENSITY:.2f} g/cm³"
)

print(
    f"Maximum roughness      : "
    f"{MAX_ROUGHNESS:.2f} nm RMS"
)

print(
    f"Maximum defect density : "
    f"{MAX_DEFECT_DENSITY:.2f} defects/cm²"
)

print(
    f"Minimum throughput     : "
    f"{MIN_THROUGHPUT:.2f} cycles/hour"
)


# ============================================================
# NORMALIZATION FUNCTIONS
# ============================================================

def higher_is_better(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:

        return pd.Series(
            1.0,
            index=series.index
        )

    return (
        (series - minimum)
        /
        (maximum - minimum)
    )


def lower_is_better(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:

        return pd.Series(
            1.0,
            index=series.index
        )

    return (
        (maximum - series)
        /
        (maximum - minimum)
    )


def target_is_better(
    series,
    target
):

    error = abs(
        series - target
    )

    maximum_error = error.max()

    if maximum_error == 0:

        return pd.Series(
            1.0,
            index=series.index
        )

    return (
        1
        -
        error / maximum_error
    )


# ============================================================
# MULTI-OBJECTIVE SCORING
# ============================================================

# Thickness close to target
df["Score_Thickness"] = target_is_better(
    df["Film_Thickness_nm"],
    TARGET_THICKNESS
)


# Lower uniformity variation is better
df["Score_Uniformity"] = lower_is_better(
    df["Thickness_Uniformity_1sigma_%"]
)


# Lower absolute stress is better
df["Score_Stress"] = lower_is_better(
    abs(
        df["Film_Stress_MPa"]
    )
)


# Higher density is better
df["Score_Density"] = higher_is_better(
    df["Film_Density_g_cm3"]
)


# Lower roughness is better
df["Score_Roughness"] = lower_is_better(
    df["Surface_Roughness_nm_RMS"]
)


# Lower defectivity is better
df["Score_Defectivity"] = lower_is_better(
    df["Defect_Density_per_cm2"]
)


# Higher throughput is better
df["Score_Throughput"] = higher_is_better(
    df["Relative_Throughput_cycles_per_hour"]
)


# ============================================================
# WEIGHTED OPTIMIZATION SCORE
# ============================================================
#
# Total score = 100%
#
# Thickness       = 25%
# Uniformity      = 15%
# Stress          = 10%
# Density         = 15%
# Roughness       = 15%
# Defectivity     = 10%
# Throughput      = 10%
#
# ============================================================

df["Optimization_Score"] = (

    0.25
    *
    df["Score_Thickness"]

    +

    0.15
    *
    df["Score_Uniformity"]

    +

    0.10
    *
    df["Score_Stress"]

    +

    0.15
    *
    df["Score_Density"]

    +

    0.15
    *
    df["Score_Roughness"]

    +

    0.10
    *
    df["Score_Defectivity"]

    +

    0.10
    *
    df["Score_Throughput"]
)


# ============================================================
# SELECT QUALIFIED CONDITIONS
# ============================================================

qualified = df[
    df["Process_Qualified"]
].copy()


print()
print("=" * 75)
print("QUALIFIED PROCESS CONDITIONS")
print("=" * 75)

print(
    f"Qualified experiments  : "
    f"{len(qualified)}"
)


# ============================================================
# SORT QUALIFIED CONDITIONS
# ============================================================

qualified = qualified.sort_values(
    "Optimization_Score",
    ascending=False
)


# ============================================================
# SELECT BEST CONDITION
# ============================================================

if len(qualified) > 0:

    best = qualified.iloc[0]

else:

    print()
    print(
        "WARNING: No experiment satisfies "
        "all process constraints."
    )

    print(
        "Selecting the highest overall "
        "optimization score instead."
    )

    best = df.sort_values(
        "Optimization_Score",
        ascending=False
    ).iloc[0]


# ============================================================
# DISPLAY OPTIMUM PROCESS
# ============================================================

print()
print("=" * 75)
print("OPTIMUM ALD PROCESS CONDITION")
print("=" * 75)

print(
    f"Experiment            : "
    f"{int(best['Experiment'])}"
)

print(
    f"Temperature           : "
    f"{best['Temperature_C']:.2f} °C"
)

print(
    f"Pressure              : "
    f"{best['Pressure_Torr']:.2f} Torr"
)

print(
    f"TMA Pulse             : "
    f"{best['TMA_Pulse_s']:.2f} s"
)

print(
    f"H2O Pulse             : "
    f"{best['H2O_Pulse_s']:.2f} s"
)

print(
    f"Purge                 : "
    f"{best['Purge_s']:.2f} s"
)

print()
print("-" * 75)

print(
    f"GPC                   : "
    f"{best['GPC_nm_per_cycle']:.4f} nm/cycle"
)

print(
    f"Film Thickness        : "
    f"{best['Film_Thickness_nm']:.3f} nm"
)

print(
    f"Thickness Error       : "
    f"{best['Thickness_Error_%']:.2f} %"
)

print(
    f"Uniformity            : "
    f"{best['Thickness_Uniformity_1sigma_%']:.3f} %"
)

print(
    f"Film Stress           : "
    f"{best['Film_Stress_MPa']:.2f} MPa"
)

print(
    f"Film Density          : "
    f"{best['Film_Density_g_cm3']:.3f} g/cm³"
)

print(
    f"Surface Roughness     : "
    f"{best['Surface_Roughness_nm_RMS']:.3f} nm RMS"
)

print(
    f"Defect Density        : "
    f"{best['Defect_Density_per_cm2']:.2f} defects/cm²"
)

print(
    f"Cycle Time            : "
    f"{best['Cycle_Time_s']:.2f} s"
)

print(
    f"Throughput            : "
    f"{best['Relative_Throughput_cycles_per_hour']:.2f}"
    f" cycles/hour"
)

print(
    f"Optimization Score    : "
    f"{best['Optimization_Score']:.4f}"
)


# ============================================================
# RECOMMENDED PROCESS WINDOW
# ============================================================

if len(qualified) > 0:

    print()
    print("=" * 75)
    print("RECOMMENDED ALD PROCESS WINDOW")
    print("=" * 75)

    print(
        f"Temperature : "
        f"{qualified['Temperature_C'].min():.2f}"
        f" – "
        f"{qualified['Temperature_C'].max():.2f} °C"
    )

    print(
        f"Pressure    : "
        f"{qualified['Pressure_Torr'].min():.2f}"
        f" – "
        f"{qualified['Pressure_Torr'].max():.2f} Torr"
    )

    print(
        f"TMA Pulse   : "
        f"{qualified['TMA_Pulse_s'].min():.2f}"
        f" – "
        f"{qualified['TMA_Pulse_s'].max():.2f} s"
    )

    print(
        f"H2O Pulse   : "
        f"{qualified['H2O_Pulse_s'].min():.2f}"
        f" – "
        f"{qualified['H2O_Pulse_s'].max():.2f} s"
    )

    print(
        f"Purge       : "
        f"{qualified['Purge_s'].min():.2f}"
        f" – "
        f"{qualified['Purge_s'].max():.2f} s"
    )


# ============================================================
# SHOW ALL QUALIFIED CONDITIONS
# ============================================================

if len(qualified) > 0:

    print()
    print("=" * 75)
    print("ALL QUALIFIED CONDITIONS")
    print("=" * 75)

    columns_to_show = [

        "Experiment",

        "Temperature_C",

        "Pressure_Torr",

        "TMA_Pulse_s",

        "H2O_Pulse_s",

        "Purge_s",

        "GPC_nm_per_cycle",

        "Film_Thickness_nm",

        "Thickness_Error_%",

        "Thickness_Uniformity_1sigma_%",

        "Film_Stress_MPa",

        "Film_Density_g_cm3",

        "Surface_Roughness_nm_RMS",

        "Defect_Density_per_cm2",

        "Cycle_Time_s",

        "Relative_Throughput_cycles_per_hour",

        "Optimization_Score"
    ]


    print(
        qualified[
            columns_to_show
        ].to_string(
            index=False
        )
    )


# ============================================================
# SAVE QUALIFIED CONDITIONS
# ============================================================

qualified_output = (
    "results/qualified_process_conditions.csv"
)

qualified.to_csv(
    qualified_output,
    index=False
)


# ============================================================
# SAVE OPTIMUM CONDITION
# ============================================================

best_output = (
    "results/optimum_ALD_process.csv"
)

pd.DataFrame(
    [best]
).to_csv(
    best_output,
    index=False
)


# ============================================================
# SAVE COMPLETE OPTIMIZATION DATASET
# ============================================================

optimization_output = (
    "results/process_optimization_results.csv"
)

df.to_csv(
    optimization_output,
    index=False
)


# ============================================================
# TOP 10 CONDITIONS
# ============================================================

top10 = df.sort_values(
    "Optimization_Score",
    ascending=False
).head(10)


top10_output = (
    "results/top10_ALD_conditions.csv"
)

top10.to_csv(
    top10_output,
    index=False
)


# ============================================================
# DISPLAY TOP 10
# ============================================================

print()
print("=" * 75)
print("TOP 10 PROCESS CONDITIONS")
print("=" * 75)

top10_columns = [

    "Experiment",

    "Temperature_C",

    "Pressure_Torr",

    "TMA_Pulse_s",

    "H2O_Pulse_s",

    "Purge_s",

    "GPC_nm_per_cycle",

    "Film_Thickness_nm",

    "Thickness_Uniformity_1sigma_%",

    "Film_Stress_MPa",

    "Film_Density_g_cm3",

    "Surface_Roughness_nm_RMS",

    "Defect_Density_per_cm2",

    "Relative_Throughput_cycles_per_hour",

    "Optimization_Score"
]


print(
    top10[
        top10_columns
    ].to_string(
        index=False
    )
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("PROCESS OPTIMIZATION COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/qualified_process_conditions.csv"
)

print(
    "  results/optimum_ALD_process.csv"
)

print(
    "  results/process_optimization_results.csv"
)

print(
    "  results/top10_ALD_conditions.csv"
)

print("=" * 75)
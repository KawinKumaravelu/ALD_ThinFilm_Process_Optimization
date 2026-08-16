# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 7: DESIGN OF EXPERIMENTS (DOE)
# ============================================================

import os
import itertools
import pandas as pd

from ald_model import (
    calculate_gpc,
    calculate_cycle_time
)


# ============================================================
# CREATE RESULTS DIRECTORY
# ============================================================

os.makedirs("results", exist_ok=True)


# ============================================================
# DOE FACTOR LEVELS
# ============================================================
#
# Each factor has:
# LOW -> CENTER -> HIGH
#
# The levels are selected so that the DOE covers
# both normal and process-edge conditions.
# ============================================================

temperature_levels = [
    160,
    200,
    240
]

pressure_levels = [
    0.60,
    1.00,
    1.40
]

precursor_pulse_levels = [
    0.50,
    1.00,
    1.50
]

reactant_pulse_levels = [
    0.50,
    1.00,
    1.50
]

purge_levels = [
    2.5,
    5.0,
    10.0
]


# Number of ALD cycles used for every virtual experiment
num_cycles = 100


# ============================================================
# DISPLAY DOE DESIGN
# ============================================================

print("=" * 75)
print("ALD PROCESS DOE")
print("=" * 75)

print("\nDOE FACTOR LEVELS")
print("-" * 75)

print(
    f"Temperature (°C)     : "
    f"{temperature_levels}"
)

print(
    f"Pressure (Torr)      : "
    f"{pressure_levels}"
)

print(
    f"TMA Pulse (s)        : "
    f"{precursor_pulse_levels}"
)

print(
    f"H2O Pulse (s)        : "
    f"{reactant_pulse_levels}"
)

print(
    f"Purge Time (s)       : "
    f"{purge_levels}"
)


# ============================================================
# GENERATE FULL FACTORIAL DOE
# ============================================================

experiments = list(
    itertools.product(
        temperature_levels,
        pressure_levels,
        precursor_pulse_levels,
        reactant_pulse_levels,
        purge_levels
    )
)


print("\nDOE DESIGN")
print("-" * 75)

print(
    f"Number of factors    : 5"
)

print(
    f"Levels per factor    : 3"
)

print(
    f"Total experiments    : {len(experiments)}"
)

print(
    "Calculation          : 3^5 = 243"
)


# ============================================================
# RUN ALL DOE EXPERIMENTS
# ============================================================

results = []


for experiment_id, values in enumerate(
    experiments,
    start=1
):

    (
        temperature,
        pressure,
        precursor_pulse,
        reactant_pulse,
        purge
    ) = values


    # --------------------------------------------------------
    # Calculate GPC
    # --------------------------------------------------------

    gpc = calculate_gpc(
        temperature,
        pressure,
        precursor_pulse,
        reactant_pulse,
        purge
    )


    # --------------------------------------------------------
    # Calculate Film Thickness
    # --------------------------------------------------------

    thickness = (
        gpc * num_cycles
    )


    # --------------------------------------------------------
    # Calculate ALD Cycle Time
    # --------------------------------------------------------

    cycle_time = calculate_cycle_time(
        precursor_pulse,
        purge,
        reactant_pulse
    )


    # --------------------------------------------------------
    # Calculate Total Process Time
    # --------------------------------------------------------

    total_process_time = (
        cycle_time * num_cycles
    )


    # --------------------------------------------------------
    # Calculate Relative Throughput
    # --------------------------------------------------------

    throughput = (
        3600 / cycle_time
    )


    # --------------------------------------------------------
    # Store Results
    # --------------------------------------------------------

    results.append({

        "Experiment": experiment_id,

        "Temperature_C": temperature,

        "Pressure_Torr": pressure,

        "TMA_Pulse_s": precursor_pulse,

        "H2O_Pulse_s": reactant_pulse,

        "Purge_s": purge,

        "GPC_nm_per_cycle": gpc,

        "Film_Thickness_nm": thickness,

        "Cycle_Time_s": cycle_time,

        "Total_Process_Time_s": total_process_time,

        "Relative_Throughput_cycles_per_hour":
            throughput
    })


# ============================================================
# CREATE PANDAS DATAFRAME
# ============================================================

df = pd.DataFrame(
    results
)


# ============================================================
# SAVE DOE DATASET
# ============================================================

output_file = (
    "results/DOE_results.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# DISPLAY FIRST 10 EXPERIMENTS
# ============================================================

print("\n")
print("=" * 75)

print(
    f"DOE dataset saved to: {output_file}"
)

print("=" * 75)

print("\nFIRST 10 DOE EXPERIMENTS")
print("-" * 75)

print(
    df.head(10).to_string(
        index=False
    )
)


# ============================================================
# DOE SUMMARY
# ============================================================

print("\n")
print("=" * 75)
print("DOE SUMMARY")
print("=" * 75)


print(
    f"Experiments           : "
    f"{len(df)}"
)

print(
    f"GPC minimum           : "
    f"{df['GPC_nm_per_cycle'].min():.4f} nm/cycle"
)

print(
    f"GPC maximum           : "
    f"{df['GPC_nm_per_cycle'].max():.4f} nm/cycle"
)

print(
    f"Thickness minimum     : "
    f"{df['Film_Thickness_nm'].min():.2f} nm"
)

print(
    f"Thickness maximum     : "
    f"{df['Film_Thickness_nm'].max():.2f} nm"
)

print(
    f"Cycle time minimum    : "
    f"{df['Cycle_Time_s'].min():.2f} s"
)

print(
    f"Cycle time maximum    : "
    f"{df['Cycle_Time_s'].max():.2f} s"
)

print(
    f"Throughput minimum    : "
    f"{df['Relative_Throughput_cycles_per_hour'].min():.2f}"
)

print(
    f"Throughput maximum    : "
    f"{df['Relative_Throughput_cycles_per_hour'].max():.2f}"
)


# ============================================================
# FIND MAXIMUM GPC EXPERIMENT
# ============================================================

max_gpc_row = df.loc[
    df["GPC_nm_per_cycle"].idxmax()
]


print("\n")
print("=" * 75)
print("HIGHEST GPC DOE CONDITION")
print("=" * 75)

print(
    f"Experiment            : "
    f"{int(max_gpc_row['Experiment'])}"
)

print(
    f"Temperature           : "
    f"{max_gpc_row['Temperature_C']:.2f} °C"
)

print(
    f"Pressure              : "
    f"{max_gpc_row['Pressure_Torr']:.2f} Torr"
)

print(
    f"TMA Pulse             : "
    f"{max_gpc_row['TMA_Pulse_s']:.2f} s"
)

print(
    f"H2O Pulse             : "
    f"{max_gpc_row['H2O_Pulse_s']:.2f} s"
)

print(
    f"Purge                 : "
    f"{max_gpc_row['Purge_s']:.2f} s"
)

print(
    f"GPC                   : "
    f"{max_gpc_row['GPC_nm_per_cycle']:.4f} nm/cycle"
)

print(
    f"Film Thickness        : "
    f"{max_gpc_row['Film_Thickness_nm']:.2f} nm"
)


# ============================================================
# FIND MINIMUM CYCLE TIME
# ============================================================

min_cycle_row = df.loc[
    df["Cycle_Time_s"].idxmin()
]


print("\n")
print("=" * 75)
print("FASTEST DOE CONDITION")
print("=" * 75)

print(
    f"Experiment            : "
    f"{int(min_cycle_row['Experiment'])}"
)

print(
    f"Temperature           : "
    f"{min_cycle_row['Temperature_C']:.2f} °C"
)

print(
    f"Pressure              : "
    f"{min_cycle_row['Pressure_Torr']:.2f} Torr"
)

print(
    f"TMA Pulse             : "
    f"{min_cycle_row['TMA_Pulse_s']:.2f} s"
)

print(
    f"H2O Pulse             : "
    f"{min_cycle_row['H2O_Pulse_s']:.2f} s"
)

print(
    f"Purge                 : "
    f"{min_cycle_row['Purge_s']:.2f} s"
)

print(
    f"Cycle Time            : "
    f"{min_cycle_row['Cycle_Time_s']:.2f} s"
)

print(
    f"Throughput            : "
    f"{min_cycle_row['Relative_Throughput_cycles_per_hour']:.2f}"
    f" cycles/hour"
)


# ============================================================
# FINAL MESSAGE
# ============================================================

print("\n")
print("=" * 75)
print("DOE ANALYSIS DATA GENERATION COMPLETE")
print("=" * 75)

print(
    "\nFile created:"
)

print(
    "results/DOE_results.csv"
)

print(
    "\nNext step:"
)

print(
    "Run ANOVA analysis using:"
)

print(
    "python src\\anova_analysis.py"
)

print("=" * 75)
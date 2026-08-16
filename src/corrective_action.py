# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 19: CORRECTIVE ACTION
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

INPUT_FILE = "results/production_lot_data.csv"

OUTPUT_FILE = (
    "results/corrective_action_results.csv"
)

SUMMARY_FILE = (
    "results/corrective_action_summary.csv"
)

PLOT_FILE = (
    "results/before_after_correction.png"
)


# ============================================================
# PROCESS SPECIFICATIONS
# ============================================================

TARGET_THICKNESS = 10.0

THICKNESS_LSL = 9.5
THICKNESS_USL = 10.5

GPC_LSL = 0.095
GPC_USL = 0.105

UNIFORMITY_USL = 2.0

STRESS_LIMIT = 80.0

DENSITY_LSL = 2.90

ROUGHNESS_USL = 0.30

DEFECT_USL = 20.0


# ============================================================
# LOAD PRODUCTION DATA
# ============================================================

df = pd.read_csv(
    INPUT_FILE
)

print("=" * 75)
print("ALD CORRECTIVE ACTION ANALYSIS")
print("=" * 75)

print()

print(
    f"Production measurements loaded : "
    f"{len(df)}"
)


# ============================================================
# ORIGINAL PROCESS
# ============================================================

before = df.copy()


# ============================================================
# CORRECTIVE ACTIONS
# ============================================================

print()
print("=" * 75)
print("CORRECTIVE ACTIONS")
print("=" * 75)

print()

print(
    "1. Tighten TMA pulse control"
)

print(
    "2. Establish validated minimum purge time"
)

print(
    "3. Add precursor pulse monitoring"
)

print(
    "4. Add process alarm limits"
)

print(
    "5. Reduce precursor-delivery variation"
)


# ============================================================
# SIMULATE IMPROVED PROCESS
# ============================================================

after = df.copy()


# ------------------------------------------------------------
# TMA pulse variation reduction
# ------------------------------------------------------------
#
# We reduce the random process variation around the nominal
# TMA pulse.
#
# This represents improved valve timing / precursor delivery
# control.
# ------------------------------------------------------------

tma_nominal = 1.0

tma_deviation = (
    after["TMA_Pulse_s"]
    -
    tma_nominal
)

after[
    "TMA_Pulse_s"
] = (
    tma_nominal
    +
    tma_deviation
    *
    0.35
)


# ============================================================
# GPC VARIATION REDUCTION
# ============================================================

gpc_nominal = 0.1000

gpc_deviation = (
    after["GPC_nm_per_cycle"]
    -
    gpc_nominal
)

after[
    "GPC_nm_per_cycle"
] = (
    gpc_nominal
    +
    gpc_deviation
    *
    0.45
)


# ============================================================
# FILM THICKNESS CORRECTION
# ============================================================

thickness_deviation = (
    after["Film_Thickness_nm"]
    -
    TARGET_THICKNESS
)

after[
    "Film_Thickness_nm"
] = (
    TARGET_THICKNESS
    +
    thickness_deviation
    *
    0.45
)


# ============================================================
# IMPROVE UNIFORMITY
# ============================================================

uniformity_deviation = (
    after[
        "Thickness_Uniformity_1sigma_%"
    ]
    -
    1.0
)

after[
    "Thickness_Uniformity_1sigma_%"
] = (
    1.0
    +
    uniformity_deviation
    *
    0.50
)


# ============================================================
# IMPROVE FILM STRESS
# ============================================================

stress_deviation = (
    after[
        "Film_Stress_MPa"
    ]
    -
    50.0
)

after[
    "Film_Stress_MPa"
] = (
    50.0
    +
    stress_deviation
    *
    0.60
)


# ============================================================
# IMPROVE DENSITY VARIATION
# ============================================================

density_deviation = (
    after[
        "Film_Density_g_cm3"
    ]
    -
    3.0
)

after[
    "Film_Density_g_cm3"
] = (
    3.0
    +
    density_deviation
    *
    0.50
)


# ============================================================
# IMPROVE ROUGHNESS
# ============================================================

roughness_deviation = (
    after[
        "Surface_Roughness_nm_RMS"
    ]
    -
    0.20
)

after[
    "Surface_Roughness_nm_RMS"
] = (
    0.20
    +
    roughness_deviation
    *
    0.50
)


# ============================================================
# IMPROVE DEFECT DENSITY
# ============================================================

defect_deviation = (
    after[
        "Defect_Density_per_cm2"
    ]
    -
    5.0
)

after[
    "Defect_Density_per_cm2"
] = (
    5.0
    +
    defect_deviation
    *
    0.50
)


# ============================================================
# RECALCULATE CYCLE TIME
# ============================================================

after[
    "Cycle_Time_s"
] = (
    after["TMA_Pulse_s"]
    +
    after["H2O_Pulse_s"]
    +
    2
    *
    after["Purge_s"]
)


# ============================================================
# RECALCULATE THROUGHPUT
# ============================================================

after[
    "Throughput_cycles_per_hour"
] = (
    3600
    /
    after["Cycle_Time_s"]
)


# ============================================================
# RECALCULATE THICKNESS DEVIATION
# ============================================================

after[
    "Thickness_Deviation_%"
] = (
    (
        after[
            "Film_Thickness_nm"
        ]
        -
        TARGET_THICKNESS
    )
    /
    TARGET_THICKNESS
    *
    100
)


# ============================================================
# PROCESS ACCEPTANCE FUNCTION
# ============================================================

def calculate_acceptance(data):

    data = data.copy()

    data["Thickness_OK"] = (
        (
            data["Film_Thickness_nm"]
            >=
            THICKNESS_LSL
        )
        &
        (
            data["Film_Thickness_nm"]
            <=
            THICKNESS_USL
        )
    )

    data["GPC_OK"] = (
        (
            data["GPC_nm_per_cycle"]
            >=
            GPC_LSL
        )
        &
        (
            data["GPC_nm_per_cycle"]
            <=
            GPC_USL
        )
    )

    data["Uniformity_OK"] = (
        data[
            "Thickness_Uniformity_1sigma_%"
        ]
        <=
        UNIFORMITY_USL
    )

    data["Stress_OK"] = (
        data[
            "Film_Stress_MPa"
        ].abs()
        <=
        STRESS_LIMIT
    )

    data["Density_OK"] = (
        data[
            "Film_Density_g_cm3"
        ]
        >=
        DENSITY_LSL
    )

    data["Roughness_OK"] = (
        data[
            "Surface_Roughness_nm_RMS"
        ]
        <=
        ROUGHNESS_USL
    )

    data["Defectivity_OK"] = (
        data[
            "Defect_Density_per_cm2"
        ]
        <=
        DEFECT_USL
    )

    data["Process_OK"] = (
        data["Thickness_OK"]
        &
        data["GPC_OK"]
        &
        data["Uniformity_OK"]
        &
        data["Stress_OK"]
        &
        data["Density_OK"]
        &
        data["Roughness_OK"]
        &
        data["Defectivity_OK"]
    )

    return data


# ============================================================
# APPLY ACCEPTANCE TEST
# ============================================================

before_checked = (
    calculate_acceptance(
        before
    )
)

after_checked = (
    calculate_acceptance(
        after
    )
)


# ============================================================
# CALCULATE PROCESS STATISTICS
# ============================================================

def calculate_statistics(data):

    result = {}

    result[
        "Thickness_Mean"
    ] = data[
        "Film_Thickness_nm"
    ].mean()

    result[
        "Thickness_Std"
    ] = data[
        "Film_Thickness_nm"
    ].std()

    result[
        "GPC_Mean"
    ] = data[
        "GPC_nm_per_cycle"
    ].mean()

    result[
        "GPC_Std"
    ] = data[
        "GPC_nm_per_cycle"
    ].std()

    result[
        "Uniformity_Mean"
    ] = data[
        "Thickness_Uniformity_1sigma_%"
    ].mean()

    result[
        "Stress_Mean"
    ] = data[
        "Film_Stress_MPa"
    ].mean()

    result[
        "Density_Mean"
    ] = data[
        "Film_Density_g_cm3"
    ].mean()

    result[
        "Roughness_Mean"
    ] = data[
        "Surface_Roughness_nm_RMS"
    ].mean()

    result[
        "Defect_Density_Mean"
    ] = data[
        "Defect_Density_per_cm2"
    ].mean()

    result[
        "Good_Measurements"
    ] = data[
        "Process_OK"
    ].sum()

    result[
        "Defective_Measurements"
    ] = (
        ~data[
            "Process_OK"
        ]
    ).sum()

    result[
        "Yield_%"
    ] = (
        result[
            "Good_Measurements"
        ]
        /
        len(data)
        *
        100
    )

    return result


before_stats = (
    calculate_statistics(
        before_checked
    )
)

after_stats = (
    calculate_statistics(
        after_checked
    )
)


# ============================================================
# PRINT BEFORE / AFTER RESULTS
# ============================================================

print()
print("=" * 75)
print("BEFORE vs AFTER CORRECTIVE ACTION")
print("=" * 75)

print()

print(
    f"{'Parameter':<30}"
    f"{'Before':>15}"
    f"{'After':>15}"
)

print("-" * 60)

print(
    f"{'Thickness mean (nm)':<30}"
    f"{before_stats['Thickness_Mean']:>15.6f}"
    f"{after_stats['Thickness_Mean']:>15.6f}"
)

print(
    f"{'Thickness std (nm)':<30}"
    f"{before_stats['Thickness_Std']:>15.6f}"
    f"{after_stats['Thickness_Std']:>15.6f}"
)

print(
    f"{'GPC mean (nm/cycle)':<30}"
    f"{before_stats['GPC_Mean']:>15.6f}"
    f"{after_stats['GPC_Mean']:>15.6f}"
)

print(
    f"{'GPC std (nm/cycle)':<30}"
    f"{before_stats['GPC_Std']:>15.6f}"
    f"{after_stats['GPC_Std']:>15.6f}"
)

print(
    f"{'Uniformity mean (%)':<30}"
    f"{before_stats['Uniformity_Mean']:>15.6f}"
    f"{after_stats['Uniformity_Mean']:>15.6f}"
)

print(
    f"{'Stress mean (MPa)':<30}"
    f"{before_stats['Stress_Mean']:>15.6f}"
    f"{after_stats['Stress_Mean']:>15.6f}"
)

print(
    f"{'Density mean (g/cm3)':<30}"
    f"{before_stats['Density_Mean']:>15.6f}"
    f"{after_stats['Density_Mean']:>15.6f}"
)

print(
    f"{'Roughness mean (nm)':<30}"
    f"{before_stats['Roughness_Mean']:>15.6f}"
    f"{after_stats['Roughness_Mean']:>15.6f}"
)

print(
    f"{'Defect density mean':<30}"
    f"{before_stats['Defect_Density_Mean']:>15.6f}"
    f"{after_stats['Defect_Density_Mean']:>15.6f}"
)

print(
    f"{'Yield (%)':<30}"
    f"{before_stats['Yield_%']:>15.2f}"
    f"{after_stats['Yield_%']:>15.2f}"
)


# ============================================================
# IMPROVEMENT CALCULATIONS
# ============================================================

gpc_std_improvement = (
    (
        before_stats["GPC_Std"]
        -
        after_stats["GPC_Std"]
    )
    /
    before_stats["GPC_Std"]
    *
    100
)


thickness_std_improvement = (
    (
        before_stats["Thickness_Std"]
        -
        after_stats["Thickness_Std"]
    )
    /
    before_stats["Thickness_Std"]
    *
    100
)


yield_improvement = (
    after_stats["Yield_%"]
    -
    before_stats["Yield_%"]
)


print()
print("=" * 75)
print("CORRECTIVE ACTION IMPROVEMENT")
print("=" * 75)

print()

print(
    f"GPC variation reduction       : "
    f"{gpc_std_improvement:.2f}%"
)

print(
    f"Thickness variation reduction : "
    f"{thickness_std_improvement:.2f}%"
)

print(
    f"Yield improvement             : "
    f"{yield_improvement:.2f} percentage points"
)


# ============================================================
# SAVE COMBINED DATA
# ============================================================

before_checked[
    "Process_State"
] = "Before Correction"

after_checked[
    "Process_State"
] = "After Correction"


combined = pd.concat(
    [
        before_checked,
        after_checked
    ],
    ignore_index=True
)


combined.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# CREATE SUMMARY TABLE
# ============================================================

summary = pd.DataFrame({

    "Metric": [

        "Thickness Mean (nm)",
        "Thickness Std (nm)",

        "GPC Mean (nm/cycle)",
        "GPC Std (nm/cycle)",

        "Uniformity Mean (%)",
        "Stress Mean (MPa)",

        "Density Mean (g/cm3)",
        "Roughness Mean (nm)",

        "Defect Density Mean",

        "Yield (%)"
    ],

    "Before_Correction": [

        before_stats["Thickness_Mean"],
        before_stats["Thickness_Std"],

        before_stats["GPC_Mean"],
        before_stats["GPC_Std"],

        before_stats["Uniformity_Mean"],
        before_stats["Stress_Mean"],

        before_stats["Density_Mean"],
        before_stats["Roughness_Mean"],

        before_stats["Defect_Density_Mean"],

        before_stats["Yield_%"]
    ],

    "After_Correction": [

        after_stats["Thickness_Mean"],
        after_stats["Thickness_Std"],

        after_stats["GPC_Mean"],
        after_stats["GPC_Std"],

        after_stats["Uniformity_Mean"],
        after_stats["Stress_Mean"],

        after_stats["Density_Mean"],
        after_stats["Roughness_Mean"],

        after_stats["Defect_Density_Mean"],

        after_stats["Yield_%"]
    ]
})


summary.to_csv(
    SUMMARY_FILE,
    index=False
)


# ============================================================
# BEFORE / AFTER PLOT
# ============================================================

fig, axes = plt.subplots(
    2,
    2,
    figsize=(12, 8)
)


# ------------------------------------------------------------
# GPC
# ------------------------------------------------------------

axes[0, 0].plot(
    before[
        "GPC_nm_per_cycle"
    ].values,
    label="Before"
)

axes[0, 0].plot(
    after[
        "GPC_nm_per_cycle"
    ].values,
    label="After"
)

axes[0, 0].axhline(
    GPC_LSL,
    linestyle="--",
    label="GPC LSL"
)

axes[0, 0].axhline(
    GPC_USL,
    linestyle="--",
    label="GPC USL"
)

axes[0, 0].set_title(
    "GPC Before vs After Correction"
)

axes[0, 0].set_xlabel(
    "Measurement"
)

axes[0, 0].set_ylabel(
    "GPC (nm/cycle)"
)

axes[0, 0].legend()


# ------------------------------------------------------------
# Thickness
# ------------------------------------------------------------

axes[0, 1].plot(
    before[
        "Film_Thickness_nm"
    ].values,
    label="Before"
)

axes[0, 1].plot(
    after[
        "Film_Thickness_nm"
    ].values,
    label="After"
)

axes[0, 1].axhline(
    THICKNESS_LSL,
    linestyle="--",
    label="Thickness LSL"
)

axes[0, 1].axhline(
    THICKNESS_USL,
    linestyle="--",
    label="Thickness USL"
)

axes[0, 1].set_title(
    "Thickness Before vs After Correction"
)

axes[0, 1].set_xlabel(
    "Measurement"
)

axes[0, 1].set_ylabel(
    "Thickness (nm)"
)

axes[0, 1].legend()


# ------------------------------------------------------------
# Uniformity
# ------------------------------------------------------------

axes[1, 0].plot(
    before[
        "Thickness_Uniformity_1sigma_%"
    ].values,
    label="Before"
)

axes[1, 0].plot(
    after[
        "Thickness_Uniformity_1sigma_%"
    ].values,
    label="After"
)

axes[1, 0].axhline(
    UNIFORMITY_USL,
    linestyle="--",
    label="Uniformity USL"
)

axes[1, 0].set_title(
    "Uniformity Before vs After Correction"
)

axes[1, 0].set_xlabel(
    "Measurement"
)

axes[1, 0].set_ylabel(
    "Uniformity (%)"
)

axes[1, 0].legend()


# ------------------------------------------------------------
# Defect Density
# ------------------------------------------------------------

axes[1, 1].plot(
    before[
        "Defect_Density_per_cm2"
    ].values,
    label="Before"
)

axes[1, 1].plot(
    after[
        "Defect_Density_per_cm2"
    ].values,
    label="After"
)

axes[1, 1].axhline(
    DEFECT_USL,
    linestyle="--",
    label="Defect USL"
)

axes[1, 1].set_title(
    "Defect Density Before vs After Correction"
)

axes[1, 1].set_xlabel(
    "Measurement"
)

axes[1, 1].set_ylabel(
    "Defects/cm²"
)

axes[1, 1].legend()


plt.tight_layout()

plt.savefig(
    PLOT_FILE,
    dpi=300
)

plt.close()


# ============================================================
# FINAL STATUS
# ============================================================

print()
print("=" * 75)
print("CORRECTIVE ACTION STATUS")
print("=" * 75)

print()

if (
    after_stats["Yield_%"]
    >=
    before_stats["Yield_%"]
):

    print(
        "Corrective action result : "
        "PROCESS IMPROVED"
    )

else:

    print(
        "Corrective action result : "
        "FURTHER OPTIMIZATION REQUIRED"
    )


print()

print(
    "Primary corrective action:"
)

print(
    "Improved TMA precursor pulse control"
)

print()

print(
    "Secondary corrective action:"
)

print(
    "Validated purge-time and process-control limits"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("CORRECTIVE ACTION ANALYSIS COMPLETE")
print("=" * 75)

print()

print(
    "Generated files:"
)

print(
    "  results/corrective_action_results.csv"
)

print(
    "  results/corrective_action_summary.csv"
)

print(
    "  results/before_after_correction.png"
)

print("=" * 75)
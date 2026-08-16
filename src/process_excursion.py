# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 16: PROCESS EXCURSION SIMULATION
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
    "results/process_excursion_data.csv"
)

SUMMARY_FILE = (
    "results/process_excursion_summary.csv"
)

PLOT_FILE = (
    "results/process_excursion_GPC.png"
)

SPC_PLOT_FILE = (
    "results/process_excursion_SPC.png"
)


# ============================================================
# EXCURSION SETTINGS
# ============================================================

# Lot where the excursion occurs
EXCURSION_LOT = 17

# Simulated process issue:
# TMA pulse delivery becomes lower than the nominal value.
#
# This reduces the effective GPC.
#
# The excursion is intentionally strong enough to create
# GPC specification violations.

TMA_PULSE_SHIFT = -0.08

GPC_SHIFT_FACTOR = 0.90


# ============================================================
# GPC SPECIFICATION
# ============================================================

GPC_LSL = 0.095
GPC_USL = 0.105


# ============================================================
# LOAD PRODUCTION DATA
# ============================================================

df = pd.read_csv(
    INPUT_FILE
)

print("=" * 75)
print("ALD PROCESS EXCURSION SIMULATION")
print("=" * 75)

print()

print(
    f"Production measurements loaded : "
    f"{len(df)}"
)

print(
    f"Excursion lot                 : "
    f"{EXCURSION_LOT}"
)


# ============================================================
# SAVE ORIGINAL GPC
# ============================================================

df[
    "Original_GPC_nm_per_cycle"
] = df[
    "GPC_nm_per_cycle"
]


df[
    "Original_TMA_Pulse_s"
] = df[
    "TMA_Pulse_s"
]


# ============================================================
# IDENTIFY EXCURSION LOT
# ============================================================

excursion_mask = (
    df["Lot"]
    ==
    EXCURSION_LOT
)


excursion_points = (
    excursion_mask.sum()
)


print()

print(
    f"Measurements in excursion lot : "
    f"{excursion_points}"
)


# ============================================================
# APPLY PROCESS EXCURSION
# ============================================================

# TMA pulse delivery deviation

df.loc[
    excursion_mask,
    "TMA_Pulse_s"
] = (
    df.loc[
        excursion_mask,
        "TMA_Pulse_s"
    ]
    +
    TMA_PULSE_SHIFT
)


# GPC decreases because of the
# reduced effective precursor delivery.

df.loc[
    excursion_mask,
    "GPC_nm_per_cycle"
] = (
    df.loc[
        excursion_mask,
        "GPC_nm_per_cycle"
    ]
    *
    GPC_SHIFT_FACTOR
)


# ============================================================
# UPDATE FILM THICKNESS
# ============================================================

# Since thickness depends on GPC:

df.loc[
    excursion_mask,
    "Film_Thickness_nm"
] = (
    df.loc[
        excursion_mask,
        "Film_Thickness_nm"
    ]
    *
    GPC_SHIFT_FACTOR
)


# ============================================================
# UPDATE THICKNESS DEVIATION
# ============================================================

df[
    "Thickness_Deviation_%"
] = (
    (
        df[
            "Film_Thickness_nm"
        ]
        -
        10.0
    )
    /
    10.0
    *
    100
)


# ============================================================
# GPC SPECIFICATION CHECK
# ============================================================

df[
    "GPC_OK"
] = (
    (
        df[
            "GPC_nm_per_cycle"
        ]
        >=
        GPC_LSL
    )
    &
    (
        df[
            "GPC_nm_per_cycle"
        ]
        <=
        GPC_USL
    )
)


# ============================================================
# THICKNESS SPECIFICATION CHECK
# ============================================================

df[
    "Thickness_OK"
] = (
    (
        df[
            "Film_Thickness_nm"
        ]
        >=
        9.5
    )
    &
    (
        df[
            "Film_Thickness_nm"
        ]
        <=
        10.5
    )
)


# ============================================================
# EXCURSION STATUS
# ============================================================

df[
    "Excursion_Status"
] = np.where(

    excursion_mask,

    "EXCURSION",

    "NORMAL"
)


# ============================================================
# DETECTION STATUS
# ============================================================

df[
    "GPC_Excursion_Detected"
] = np.where(

    (
        df[
            "GPC_nm_per_cycle"
        ]
        <
        GPC_LSL
    )
    |
    (
        df[
            "GPC_nm_per_cycle"
        ]
        >
        GPC_USL
    ),

    "DETECTED",

    "NORMAL"
)


# ============================================================
# PRINT EXCURSION DETAILS
# ============================================================

normal_gpc = df.loc[
    ~excursion_mask,
    "GPC_nm_per_cycle"
].mean()


excursion_gpc = df.loc[
    excursion_mask,
    "GPC_nm_per_cycle"
].mean()


print()

print("=" * 75)
print("EXCURSION DETAILS")
print("=" * 75)

print()

print(
    f"Normal mean GPC          : "
    f"{normal_gpc:.6f} nm/cycle"
)

print(
    f"Excursion mean GPC       : "
    f"{excursion_gpc:.6f} nm/cycle"
)

print(
    f"GPC shift                : "
    f"{excursion_gpc - normal_gpc:.6f} nm/cycle"
)

print()

print(
    f"Normal TMA pulse mean    : "
    f"{df.loc[~excursion_mask, 'Original_TMA_Pulse_s'].mean():.4f} s"
)

print(
    f"Excursion TMA pulse mean : "
    f"{df.loc[excursion_mask, 'TMA_Pulse_s'].mean():.4f} s"
)


# ============================================================
# DETECT GPC SPECIFICATION VIOLATIONS
# ============================================================

gpc_failures = (
    ~df["GPC_OK"]
)


total_gpc_failures = (
    gpc_failures.sum()
)


excursion_gpc_failures = (
    gpc_failures
    &
    excursion_mask
).sum()


normal_gpc_failures = (
    gpc_failures
    &
    ~excursion_mask
).sum()


print()

print("=" * 75)
print("EXCURSION DETECTION")
print("=" * 75)

print()

print(
    f"Total GPC specification failures : "
    f"{total_gpc_failures}"
)

print(
    f"Failures in excursion lot        : "
    f"{excursion_gpc_failures}"
)

print(
    f"Failures outside excursion lot   : "
    f"{normal_gpc_failures}"
)


# ============================================================
# CALCULATE SPC LIMITS
# ============================================================

baseline_gpc = df.loc[
    ~excursion_mask,
    "GPC_nm_per_cycle"
]


spc_mean = (
    baseline_gpc.mean()
)


spc_std = (
    baseline_gpc.std(
        ddof=1
    )
)


ucl = (
    spc_mean
    +
    3 * spc_std
)


lcl = (
    spc_mean
    -
    3 * spc_std
)


# ============================================================
# SPC DETECTION
# ============================================================

df[
    "SPC_Status"
] = np.where(

    (
        df[
            "GPC_nm_per_cycle"
        ]
        >
        ucl
    )
    |
    (
        df[
            "GPC_nm_per_cycle"
        ]
        <
        lcl
    ),

    "OUT_OF_CONTROL",

    "IN_CONTROL"
)


spc_ooc = (
    df[
        "SPC_Status"
    ]
    ==
    "OUT_OF_CONTROL"
)


total_spc_ooc = (
    spc_ooc.sum()
)


excursion_spc_ooc = (
    spc_ooc
    &
    excursion_mask
).sum()


normal_spc_ooc = (
    spc_ooc
    &
    ~excursion_mask
).sum()


# ============================================================
# DISPLAY SPC RESULTS
# ============================================================

print()

print("=" * 75)
print("SPC EXCURSION DETECTION")
print("=" * 75)

print()

print(
    f"Baseline GPC mean       : "
    f"{spc_mean:.6f}"
)

print(
    f"Baseline GPC std        : "
    f"{spc_std:.6f}"
)

print(
    f"Lower Control Limit     : "
    f"{lcl:.6f}"
)

print(
    f"Upper Control Limit     : "
    f"{ucl:.6f}"
)

print()

print(
    f"Total SPC violations    : "
    f"{total_spc_ooc}"
)

print(
    f"Excursion violations    : "
    f"{excursion_spc_ooc}"
)

print(
    f"Normal-period violations: "
    f"{normal_spc_ooc}"
)


# ============================================================
# CALCULATE EXCURSION DETECTION RATE
# ============================================================

if excursion_points > 0:

    detection_rate = (
        excursion_spc_ooc
        /
        excursion_points
        *
        100
    )

else:

    detection_rate = 0


print()

print(
    f"Excursion detection rate: "
    f"{detection_rate:.2f}%"
)


# ============================================================
# PLOT GPC WITH EXCURSION
# ============================================================

plt.figure(
    figsize=(12, 6)
)


x = np.arange(
    1,
    len(df) + 1
)


plt.plot(
    x,
    df[
        "GPC_nm_per_cycle"
    ],
    linewidth=1,
    label="GPC"
)


plt.axhline(
    spc_mean,
    linestyle="--",
    linewidth=2,
    label="Center Line"
)


plt.axhline(
    ucl,
    linestyle="--",
    linewidth=2,
    label="UCL"
)


plt.axhline(
    lcl,
    linestyle="--",
    linewidth=2,
    label="LCL"
)


# Highlight excursion

excursion_indices = (
    np.where(
        excursion_mask
    )[0]
    +
    1
)


plt.scatter(
    excursion_indices,
    df.loc[
        excursion_mask,
        "GPC_nm_per_cycle"
    ],
    s=30,
    label="Excursion Lot"
)


plt.title(
    "GPC SPC Chart with Process Excursion"
)

plt.xlabel(
    "Production Measurement"
)

plt.ylabel(
    "GPC (nm/cycle)"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    PLOT_FILE,
    dpi=300
)

plt.close()


# ============================================================
# PLOT EXCURSION VS NORMAL
# ============================================================

plt.figure(
    figsize=(12, 6)
)


plt.plot(
    x,
    df[
        "GPC_nm_per_cycle"
    ],
    linewidth=1
)


plt.axhline(
    GPC_LSL,
    linestyle="--",
    linewidth=2,
    label="GPC LSL"
)


plt.axhline(
    GPC_USL,
    linestyle="--",
    linewidth=2,
    label="GPC USL"
)


plt.axvspan(
    excursion_indices[0],
    excursion_indices[-1],
    alpha=0.2,
    label="Excursion Lot 17"
)


plt.title(
    "GPC Specification Monitoring During Process Excursion"
)

plt.xlabel(
    "Production Measurement"
)

plt.ylabel(
    "GPC (nm/cycle)"
)

plt.legend()

plt.grid(
    True,
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    SPC_PLOT_FILE,
    dpi=300
)

plt.close()


# ============================================================
# CREATE SUMMARY DATA
# ============================================================

summary = pd.DataFrame({

    "Parameter": [

        "Excursion_Lot",

        "TMA_Pulse_Shift_s",

        "GPC_Shift_Factor",

        "Baseline_GPC_Mean",

        "Excursion_GPC_Mean",

        "GPC_LSL",

        "GPC_USL",

        "SPC_LCL",

        "SPC_UCL",

        "Total_GPC_Failures",

        "Excursion_GPC_Failures",

        "Normal_GPC_Failures",

        "Total_SPC_Violations",

        "Excursion_SPC_Violations",

        "Normal_SPC_Violations",

        "Excursion_Detection_Rate_percent"
    ],

    "Value": [

        EXCURSION_LOT,

        TMA_PULSE_SHIFT,

        GPC_SHIFT_FACTOR,

        normal_gpc,

        excursion_gpc,

        GPC_LSL,

        GPC_USL,

        lcl,

        ucl,

        total_gpc_failures,

        excursion_gpc_failures,

        normal_gpc_failures,

        total_spc_ooc,

        excursion_spc_ooc,

        normal_spc_ooc,

        detection_rate
    ]
})


# ============================================================
# SAVE SUMMARY
# ============================================================

summary.to_csv(
    SUMMARY_FILE,
    index=False
)


# ============================================================
# SAVE EXCURSION DATA
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL INTERPRETATION
# ============================================================

print()

print("=" * 75)
print("PROCESS EXCURSION ANALYSIS")
print("=" * 75)

if (
    excursion_spc_ooc
    >
    0
):

    print(
        "RESULT                  : "
        "EXCURSION DETECTED"
    )

else:

    print(
        "RESULT                  : "
        "EXCURSION NOT DETECTED"
    )


print()

print(
    "Likely process mechanism : "
    "Reduced TMA pulse delivery"
)

print(
    "Primary affected metric  : "
    "GPC"
)

print(
    "Affected production lot  : "
    f"{EXCURSION_LOT}"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("PROCESS EXCURSION SIMULATION COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/process_excursion_data.csv"
)

print(
    "  results/process_excursion_summary.csv"
)

print(
    "  results/process_excursion_GPC.png"
)

print(
    "  results/process_excursion_SPC.png"
)

print("=" * 75)
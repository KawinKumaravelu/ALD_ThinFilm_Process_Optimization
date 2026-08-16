# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 20: PROCESS RE-QUALIFICATION
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

INPUT_FILE = "results/corrective_action_results.csv"

QUALIFICATION_DATA_FILE = (
    "results/requalification_data.csv"
)

SUMMARY_FILE = (
    "results/requalification_summary.csv"
)

COMPARISON_FILE = (
    "results/requalification_before_after.csv"
)

PLOT_FILE = (
    "results/requalification_comparison.png"
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
# REQUALIFICATION SETTINGS
# ============================================================

NUMBER_OF_LOTS = 30

WAFERS_PER_LOT = 10

MEASUREMENTS_PER_WAFER = 5

RANDOM_SEED = 2026


# ============================================================
# LOAD CORRECTED PROCESS DATA
# ============================================================

df = pd.read_csv(
    INPUT_FILE
)

after_correction = df[
    df["Process_State"]
    ==
    "After Correction"
].copy()


print("=" * 75)
print("ALD PROCESS RE-QUALIFICATION")
print("=" * 75)

print()

print(
    f"Corrected process measurements loaded : "
    f"{len(after_correction)}"
)


# ============================================================
# CALCULATE CORRECTED PROCESS NOMINAL VALUES
# ============================================================

nominal_temperature = (
    after_correction[
        "Temperature_C"
    ].mean()
)

nominal_pressure = (
    after_correction[
        "Pressure_Torr"
    ].mean()
)

nominal_tma = (
    after_correction[
        "TMA_Pulse_s"
    ].mean()
)

nominal_h2o = (
    after_correction[
        "H2O_Pulse_s"
    ].mean()
)

nominal_purge = (
    after_correction[
        "Purge_s"
    ].mean()
)

nominal_gpc = (
    after_correction[
        "GPC_nm_per_cycle"
    ].mean()
)

nominal_thickness = (
    after_correction[
        "Film_Thickness_nm"
    ].mean()
)


# ============================================================
# DISPLAY QUALIFIED RECIPE
# ============================================================

print()
print("=" * 75)
print("CORRECTED PROCESS RECIPE")
print("=" * 75)

print()

print(
    f"Temperature       : "
    f"{nominal_temperature:.4f} °C"
)

print(
    f"Pressure          : "
    f"{nominal_pressure:.4f} Torr"
)

print(
    f"TMA Pulse         : "
    f"{nominal_tma:.4f} s"
)

print(
    f"H2O Pulse         : "
    f"{nominal_h2o:.4f} s"
)

print(
    f"Purge             : "
    f"{nominal_purge:.4f} s"
)

print(
    f"Nominal GPC       : "
    f"{nominal_gpc:.6f} nm/cycle"
)

print(
    f"Nominal Thickness : "
    f"{nominal_thickness:.6f} nm"
)


# ============================================================
# GENERATE NEW QUALIFICATION DATA
# ============================================================

np.random.seed(
    RANDOM_SEED
)


qualification_records = []

measurement_id = 1


for lot in range(
    1,
    NUMBER_OF_LOTS + 1
):

    # Small lot-to-lot variation
    lot_temperature = (
        nominal_temperature
        +
        np.random.normal(
            0,
            0.15
        )
    )

    lot_pressure = (
        nominal_pressure
        +
        np.random.normal(
            0,
            0.01
        )
    )

    lot_tma = (
        nominal_tma
        +
        np.random.normal(
            0,
            0.008
        )
    )

    lot_h2o = (
        nominal_h2o
        +
        np.random.normal(
            0,
            0.008
        )
    )

    lot_purge = (
        nominal_purge
        +
        np.random.normal(
            0,
            0.03
        )
    )

    # Corrected process has reduced variation
    lot_gpc = (
        nominal_gpc
        +
        np.random.normal(
            0,
            0.00045
        )
    )

    lot_uniformity = (
        1.0
        +
        np.random.normal(
            0,
            0.045
        )
    )

    lot_stress = (
        50.0
        +
        np.random.normal(
            0,
            1.5
        )
    )

    lot_density = (
        3.0
        +
        np.random.normal(
            0,
            0.004
        )
    )

    lot_roughness = (
        0.20
        +
        np.random.normal(
            0,
            0.006
        )
    )

    lot_defects = (
        5.0
        +
        np.random.normal(
            0,
            0.25
        )
    )

    cycle_time = (
        lot_tma
        +
        lot_h2o
        +
        2 * lot_purge
    )

    throughput = (
        3600
        /
        cycle_time
    )

    for wafer in range(
        1,
        WAFERS_PER_LOT + 1
    ):

        for measurement in range(
            1,
            MEASUREMENTS_PER_WAFER + 1
        ):

            # Measurement-level variation
            gpc = (
                lot_gpc
                +
                np.random.normal(
                    0,
                    0.00025
                )
            )

            thickness = (
                gpc
                *
                100
            )

            thickness += np.random.normal(
                0,
                0.025
            )

            uniformity = (
                lot_uniformity
                +
                np.random.normal(
                    0,
                    0.025
                )
            )

            stress = (
                lot_stress
                +
                np.random.normal(
                    0,
                    0.8
                )
            )

            density = (
                lot_density
                +
                np.random.normal(
                    0,
                    0.002
                )
            )

            roughness = (
                lot_roughness
                +
                np.random.normal(
                    0,
                    0.003
                )
            )

            defects = (
                lot_defects
                +
                np.random.normal(
                    0,
                    0.15
                )
            )

            thickness_deviation = (
                (
                    thickness
                    -
                    TARGET_THICKNESS
                )
                /
                TARGET_THICKNESS
                *
                100
            )

            qualification_records.append({

                "Qualification_Measurement":
                    measurement_id,

                "Lot":
                    lot,

                "Wafer":
                    wafer,

                "Measurement":
                    measurement,

                "Temperature_C":
                    lot_temperature,

                "Pressure_Torr":
                    lot_pressure,

                "TMA_Pulse_s":
                    lot_tma,

                "H2O_Pulse_s":
                    lot_h2o,

                "Purge_s":
                    lot_purge,

                "GPC_nm_per_cycle":
                    gpc,

                "Film_Thickness_nm":
                    thickness,

                "Thickness_Uniformity_1sigma_%":
                    uniformity,

                "Film_Stress_MPa":
                    stress,

                "Film_Density_g_cm3":
                    density,

                "Surface_Roughness_nm_RMS":
                    roughness,

                "Defect_Density_per_cm2":
                    defects,

                "Cycle_Time_s":
                    cycle_time,

                "Throughput_cycles_per_hour":
                    throughput,

                "Thickness_Deviation_%":
                    thickness_deviation
            })

            measurement_id += 1


qualification_df = pd.DataFrame(
    qualification_records
)


# ============================================================
# ACCEPTANCE CHECK
# ============================================================

qualification_df[
    "Thickness_OK"
] = (
    (
        qualification_df[
            "Film_Thickness_nm"
        ]
        >=
        THICKNESS_LSL
    )
    &
    (
        qualification_df[
            "Film_Thickness_nm"
        ]
        <=
        THICKNESS_USL
    )
)


qualification_df[
    "GPC_OK"
] = (
    (
        qualification_df[
            "GPC_nm_per_cycle"
        ]
        >=
        GPC_LSL
    )
    &
    (
        qualification_df[
            "GPC_nm_per_cycle"
        ]
        <=
        GPC_USL
    )
)


qualification_df[
    "Uniformity_OK"
] = (
    qualification_df[
        "Thickness_Uniformity_1sigma_%"
    ]
    <=
    UNIFORMITY_USL
)


qualification_df[
    "Stress_OK"
] = (
    qualification_df[
        "Film_Stress_MPa"
    ].abs()
    <=
    STRESS_LIMIT
)


qualification_df[
    "Density_OK"
] = (
    qualification_df[
        "Film_Density_g_cm3"
    ]
    >=
    DENSITY_LSL
)


qualification_df[
    "Roughness_OK"
] = (
    qualification_df[
        "Surface_Roughness_nm_RMS"
    ]
    <=
    ROUGHNESS_USL
)


qualification_df[
    "Defectivity_OK"
] = (
    qualification_df[
        "Defect_Density_per_cm2"
    ]
    <=
    DEFECT_USL
)


qualification_df[
    "Qualification_OK"
] = (
    qualification_df["Thickness_OK"]
    &
    qualification_df["GPC_OK"]
    &
    qualification_df["Uniformity_OK"]
    &
    qualification_df["Stress_OK"]
    &
    qualification_df["Density_OK"]
    &
    qualification_df["Roughness_OK"]
    &
    qualification_df["Defectivity_OK"]
)


# ============================================================
# PROCESS CAPABILITY FUNCTION
# ============================================================

def calculate_cp_cpk(
    values,
    lsl,
    usl
):

    mean = np.mean(
        values
    )

    std = np.std(
        values,
        ddof=1
    )

    cp = (
        (usl - lsl)
        /
        (6 * std)
    )

    cpu = (
        (usl - mean)
        /
        (3 * std)
    )

    cpl = (
        (mean - lsl)
        /
        (3 * std)
    )

    cpk = min(
        cpu,
        cpl
    )

    return (
        mean,
        std,
        cp,
        cpk
    )


# ============================================================
# CAPABILITY ANALYSIS
# ============================================================

thickness_mean, thickness_std, thickness_cp, thickness_cpk = (
    calculate_cp_cpk(
        qualification_df[
            "Film_Thickness_nm"
        ],
        THICKNESS_LSL,
        THICKNESS_USL
    )
)


gpc_mean, gpc_std, gpc_cp, gpc_cpk = (
    calculate_cp_cpk(
        qualification_df[
            "GPC_nm_per_cycle"
        ],
        GPC_LSL,
        GPC_USL
    )
)


uniformity_mean = (
    qualification_df[
        "Thickness_Uniformity_1sigma_%"
    ].mean()
)


uniformity_std = (
    qualification_df[
        "Thickness_Uniformity_1sigma_%"
    ].std()
)


uniformity_cpk = (
    (
        UNIFORMITY_USL
        -
        uniformity_mean
    )
    /
    (
        3
        *
        uniformity_std
    )
)


defect_mean = (
    qualification_df[
        "Defect_Density_per_cm2"
    ].mean()
)


defect_std = (
    qualification_df[
        "Defect_Density_per_cm2"
    ].std()
)


defect_cpk = (
    (
        DEFECT_USL
        -
        defect_mean
    )
    /
    (
        3
        *
        defect_std
    )
)


# ============================================================
# REQUALIFICATION STATISTICS
# ============================================================

total_measurements = len(
    qualification_df
)

qualified_measurements = (
    qualification_df[
        "Qualification_OK"
    ].sum()
)

rejected_measurements = (
    total_measurements
    -
    qualified_measurements
)

qualification_yield = (
    qualified_measurements
    /
    total_measurements
    *
    100
)


# ============================================================
# LOT-LEVEL SUMMARY
# ============================================================

lot_summary = (
    qualification_df
    .groupby("Lot")
    .agg(

        Mean_Thickness_nm=(
            "Film_Thickness_nm",
            "mean"
        ),

        Std_Thickness_nm=(
            "Film_Thickness_nm",
            "std"
        ),

        Mean_GPC_nm_per_cycle=(
            "GPC_nm_per_cycle",
            "mean"
        ),

        Mean_Uniformity_percent=(
            "Thickness_Uniformity_1sigma_%",
            "mean"
        ),

        Mean_Stress_MPa=(
            "Film_Stress_MPa",
            "mean"
        ),

        Mean_Density_g_cm3=(
            "Film_Density_g_cm3",
            "mean"
        ),

        Mean_Roughness_nm=(
            "Surface_Roughness_nm_RMS",
            "mean"
        ),

        Mean_Defects_per_cm2=(
            "Defect_Density_per_cm2",
            "mean"
        ),

        Accepted_Measurements=(
            "Qualification_OK",
            "sum"
        ),

        Total_Measurements=(
            "Qualification_OK",
            "count"
        )
    )
    .reset_index()
)


lot_summary[
    "Lot_Qualification_%"
] = (
    lot_summary[
        "Accepted_Measurements"
    ]
    /
    lot_summary[
        "Total_Measurements"
    ]
    *
    100
)


# ============================================================
# PRINT RESULTS
# ============================================================

print()
print("=" * 75)
print("REQUALIFICATION PRODUCTION SUMMARY")
print("=" * 75)

print()

print(
    f"Qualification lots       : "
    f"{NUMBER_OF_LOTS}"
)

print(
    f"Wafers per lot          : "
    f"{WAFERS_PER_LOT}"
)

print(
    f"Measurements per wafer  : "
    f"{MEASUREMENTS_PER_WAFER}"
)

print(
    f"Total measurements      : "
    f"{total_measurements}"
)

print()

print(
    f"Qualified measurements  : "
    f"{qualified_measurements}"
)

print(
    f"Rejected measurements   : "
    f"{rejected_measurements}"
)

print(
    f"Qualification yield     : "
    f"{qualification_yield:.2f}%"
)


# ============================================================
# FILM QUALITY RESULTS
# ============================================================

print()
print("=" * 75)
print("REQUALIFICATION FILM QUALITY")
print("=" * 75)

print()

print(
    f"Thickness mean         : "
    f"{thickness_mean:.6f} nm"
)

print(
    f"Thickness std          : "
    f"{thickness_std:.6f} nm"
)

print(
    f"GPC mean               : "
    f"{gpc_mean:.6f} nm/cycle"
)

print(
    f"GPC std                : "
    f"{gpc_std:.6f} nm/cycle"
)

print(
    f"Uniformity mean        : "
    f"{uniformity_mean:.6f}%"
)

print(
    f"Stress mean            : "
    f"{qualification_df['Film_Stress_MPa'].mean():.6f} MPa"
)

print(
    f"Density mean           : "
    f"{qualification_df['Film_Density_g_cm3'].mean():.6f} g/cm³"
)

print(
    f"Roughness mean         : "
    f"{qualification_df['Surface_Roughness_nm_RMS'].mean():.6f} nm"
)

print(
    f"Defect density mean    : "
    f"{defect_mean:.6f} defects/cm²"
)


# ============================================================
# CAPABILITY RESULTS
# ============================================================

print()
print("=" * 75)
print("REQUALIFICATION PROCESS CAPABILITY")
print("=" * 75)

print()

print(
    f"Film Thickness Cp      : "
    f"{thickness_cp:.4f}"
)

print(
    f"Film Thickness Cpk     : "
    f"{thickness_cpk:.4f}"
)

print()

print(
    f"GPC Cp                 : "
    f"{gpc_cp:.4f}"
)

print(
    f"GPC Cpk                : "
    f"{gpc_cpk:.4f}"
)

print()

print(
    f"Uniformity Cpk         : "
    f"{uniformity_cpk:.4f}"
)

print(
    f"Defect Density Cpk     : "
    f"{defect_cpk:.4f}"
)


# ============================================================
# QUALIFICATION DECISION
# ============================================================

minimum_cpk = min(
    thickness_cpk,
    gpc_cpk,
    uniformity_cpk,
    defect_cpk
)


print()
print("=" * 75)
print("PROCESS QUALIFICATION DECISION")
print("=" * 75)

print()

print(
    f"Minimum Cpk            : "
    f"{minimum_cpk:.4f}"
)

print(
    f"Qualification yield    : "
    f"{qualification_yield:.2f}%"
)

print()

if (
    minimum_cpk >= 1.33
    and
    qualification_yield >= 99.0
):

    qualification_status = (
        "PROCESS QUALIFIED"
    )

else:

    qualification_status = (
        "PROCESS NOT QUALIFIED"
    )


print(
    f"PROCESS STATUS         : "
    f"{qualification_status}"
)


# ============================================================
# BEFORE VS AFTER CORRECTIVE ACTION
# ============================================================

before_file = (
    "results/production_lot_data.csv"
)

before_df = pd.read_csv(
    before_file
)


before_thickness_mean = (
    before_df[
        "Film_Thickness_nm"
    ].mean()
)

before_thickness_std = (
    before_df[
        "Film_Thickness_nm"
    ].std()
)

before_gpc_mean = (
    before_df[
        "GPC_nm_per_cycle"
    ].mean()
)

before_gpc_std = (
    before_df[
        "GPC_nm_per_cycle"
    ].std()
)


before_gpc_cp = (
    (
        GPC_USL
        -
        GPC_LSL
    )
    /
    (
        6
        *
        before_gpc_std
    )
)


before_gpc_cpk = min(

    (
        GPC_USL
        -
        before_gpc_mean
    )
    /
    (
        3
        *
        before_gpc_std
    ),

    (
        before_gpc_mean
        -
        GPC_LSL
    )
    /
    (
        3
        *
        before_gpc_std
    )
)


before_thickness_cp = (
    (
        THICKNESS_USL
        -
        THICKNESS_LSL
    )
    /
    (
        6
        *
        before_thickness_std
    )
)


before_thickness_cpk = min(

    (
        THICKNESS_USL
        -
        before_thickness_mean
    )
    /
    (
        3
        *
        before_thickness_std
    ),

    (
        before_thickness_mean
        -
        THICKNESS_LSL
    )
    /
    (
        3
        *
        before_thickness_std
    )
)


before_yield = (
    before_df.get(
        "Measurement_OK",
        pd.Series(
            [True] * len(before_df)
        )
    ).mean()
    *
    100
)


comparison = pd.DataFrame({

    "Metric": [

        "Thickness Mean (nm)",
        "Thickness Std (nm)",
        "Thickness Cp",
        "Thickness Cpk",

        "GPC Mean (nm/cycle)",
        "GPC Std (nm/cycle)",
        "GPC Cp",
        "GPC Cpk",

        "Qualification / Yield (%)"
    ],

    "Before_Correction": [

        before_thickness_mean,
        before_thickness_std,
        before_thickness_cp,
        before_thickness_cpk,

        before_gpc_mean,
        before_gpc_std,
        before_gpc_cp,
        before_gpc_cpk,

        before_yield
    ],

    "After_Correction": [

        thickness_mean,
        thickness_std,
        thickness_cp,
        thickness_cpk,

        gpc_mean,
        gpc_std,
        gpc_cp,
        gpc_cpk,

        qualification_yield
    ]
})


# ============================================================
# SAVE FILES
# ============================================================

qualification_df.to_csv(
    QUALIFICATION_DATA_FILE,
    index=False
)

lot_summary.to_csv(
    "results/requalification_lot_summary.csv",
    index=False
)

comparison.to_csv(
    COMPARISON_FILE,
    index=False
)


summary = pd.DataFrame({

    "Metric": [

        "Total Measurements",
        "Qualified Measurements",
        "Rejected Measurements",
        "Qualification Yield (%)",

        "Thickness Mean (nm)",
        "Thickness Std (nm)",
        "Thickness Cp",
        "Thickness Cpk",

        "GPC Mean (nm/cycle)",
        "GPC Std (nm/cycle)",
        "GPC Cp",
        "GPC Cpk",

        "Uniformity Mean (%)",
        "Uniformity Cpk",

        "Defect Density Mean",
        "Defect Density Cpk",

        "Minimum Cpk",
        "Qualification Status"
    ],

    "Value": [

        total_measurements,
        qualified_measurements,
        rejected_measurements,
        qualification_yield,

        thickness_mean,
        thickness_std,
        thickness_cp,
        thickness_cpk,

        gpc_mean,
        gpc_std,
        gpc_cp,
        gpc_cpk,

        uniformity_mean,
        uniformity_cpk,

        defect_mean,
        defect_cpk,

        minimum_cpk,
        qualification_status
    ]
})


summary.to_csv(
    SUMMARY_FILE,
    index=False
)


# ============================================================
# BEFORE / AFTER PLOT
# ============================================================

metrics = [

    "Thickness Cpk",
    "GPC Cpk",
    "Qualification Yield (%)"
]

before_values = [

    before_thickness_cpk,
    before_gpc_cpk,
    before_yield
]

after_values = [

    thickness_cpk,
    gpc_cpk,
    qualification_yield
]


x = np.arange(
    len(metrics)
)

width = 0.35


plt.figure(
    figsize=(10, 6)
)

plt.bar(
    x - width / 2,
    before_values,
    width,
    label="Before Correction"
)

plt.bar(
    x + width / 2,
    after_values,
    width,
    label="After Correction"
)


plt.xticks(
    x,
    metrics
)

plt.ylabel(
    "Value"
)

plt.title(
    "ALD Process Requalification: Before vs After Correction"
)

plt.legend()

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    PLOT_FILE,
    dpi=300
)

plt.close()


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("PROCESS RE-QUALIFICATION COMPLETE")
print("=" * 75)

print()

print(
    "Generated files:"
)

print(
    "  results/requalification_data.csv"
)

print(
    "  results/requalification_lot_summary.csv"
)

print(
    "  results/requalification_summary.csv"
)

print(
    "  results/requalification_before_after.csv"
)

print(
    "  results/requalification_comparison.png"
)

print("=" * 75)
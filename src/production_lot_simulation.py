# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 12: PRODUCTION LOT SIMULATION
# ============================================================

import os
import numpy as np
import pandas as pd


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

INPUT_FILE = "results/optimum_ALD_process.csv"

OUTPUT_FILE = (
    "results/production_lot_data.csv"
)

# Production simulation settings
NUM_LOTS = 30
WAFERS_PER_LOT = 10
MEASUREMENTS_PER_WAFER = 5

# Target process values
TARGET_THICKNESS = 10.0
TARGET_GPC = 0.100


# ============================================================
# LOAD OPTIMIZED PROCESS
# ============================================================

optimized = pd.read_csv(
    INPUT_FILE
)

optimized = optimized.iloc[0]


temperature = optimized["Temperature_C"]
pressure = optimized["Pressure_Torr"]
tma_pulse = optimized["TMA_Pulse_s"]
h2o_pulse = optimized["H2O_Pulse_s"]
purge = optimized["Purge_s"]

nominal_gpc = optimized[
    "GPC_nm_per_cycle"
]

nominal_thickness = optimized[
    "Film_Thickness_nm"
]

nominal_uniformity = optimized[
    "Thickness_Uniformity_1sigma_%"
]

nominal_stress = optimized[
    "Film_Stress_MPa"
]

nominal_density = optimized[
    "Film_Density_g_cm3"
]

nominal_roughness = optimized[
    "Surface_Roughness_nm_RMS"
]

nominal_defects = optimized[
    "Defect_Density_per_cm2"
]

nominal_cycle_time = optimized[
    "Cycle_Time_s"
]

nominal_throughput = optimized[
    "Relative_Throughput_cycles_per_hour"
]


# ============================================================
# DISPLAY PROCESS
# ============================================================

print("=" * 75)
print("ALD PRODUCTION LOT SIMULATION")
print("=" * 75)

print()
print("OPTIMIZED PROCESS RECIPE")
print("-" * 75)

print(
    f"Temperature       : {temperature:.2f} °C"
)

print(
    f"Pressure          : {pressure:.2f} Torr"
)

print(
    f"TMA Pulse         : {tma_pulse:.2f} s"
)

print(
    f"H2O Pulse         : {h2o_pulse:.2f} s"
)

print(
    f"Purge             : {purge:.2f} s"
)

print(
    f"Nominal GPC       : {nominal_gpc:.4f} nm/cycle"
)

print(
    f"Nominal Thickness : {nominal_thickness:.3f} nm"
)


# ============================================================
# RANDOM NUMBER GENERATOR
# ============================================================

rng = np.random.default_rng(
    42
)


# ============================================================
# PRODUCTION DATA STORAGE
# ============================================================

production_data = []


# ============================================================
# SIMULATE PRODUCTION LOTS
# ============================================================

for lot in range(
    1,
    NUM_LOTS + 1
):

    # --------------------------------------------------------
    # Lot-to-lot process variation
    # --------------------------------------------------------

    lot_temperature = (
        temperature
        +
        rng.normal(
            0,
            1.5
        )
    )

    lot_pressure = (
        pressure
        +
        rng.normal(
            0,
            0.03
        )
    )

    lot_tma_pulse = (
        tma_pulse
        +
        rng.normal(
            0,
            0.015
        )
    )

    lot_h2o_pulse = (
        h2o_pulse
        +
        rng.normal(
            0,
            0.015
        )
    )

    lot_purge = (
        purge
        +
        rng.normal(
            0,
            0.10
        )
    )


    # --------------------------------------------------------
    # Lot-level GPC variation
    # --------------------------------------------------------

    lot_gpc = (
        nominal_gpc
        *
        (
            1
            +
            rng.normal(
                0,
                0.015
            )
        )
    )


    # --------------------------------------------------------
    # Lot-level film properties
    # --------------------------------------------------------

    lot_thickness = (
        nominal_thickness
        *
        (
            1
            +
            rng.normal(
                0,
                0.008
            )
        )
    )


    lot_uniformity = (
        nominal_uniformity
        +
        rng.normal(
            0,
            0.08
        )
    )

    lot_uniformity = max(
        lot_uniformity,
        0.5
    )


    lot_stress = (
        nominal_stress
        +
        rng.normal(
            0,
            3.0
        )
    )


    lot_density = (
        nominal_density
        +
        rng.normal(
            0,
            0.015
        )
    )


    lot_roughness = (
        nominal_roughness
        +
        rng.normal(
            0,
            0.01
        )
    )


    lot_roughness = max(
        lot_roughness,
        0.05
    )


    lot_defects = (
        nominal_defects
        *
        (
            1
            +
            rng.normal(
                0,
                0.10
            )
        )
    )

    lot_defects = max(
        lot_defects,
        0
    )


    # --------------------------------------------------------
    # Lot cycle time and throughput
    # --------------------------------------------------------

    lot_cycle_time = (
        lot_purge * 2
        +
        lot_tma_pulse
        +
        lot_h2o_pulse
    )


    lot_throughput = (
        3600
        /
        lot_cycle_time
    )


    # ========================================================
    # SIMULATE WAFERS
    # ========================================================

    for wafer in range(
        1,
        WAFERS_PER_LOT + 1
    ):

        wafer_thickness = (
            lot_thickness
            +
            rng.normal(
                0,
                lot_thickness
                *
                0.003
            )
        )


        wafer_gpc = (
            lot_gpc
            +
            rng.normal(
                0,
                0.0008
            )
        )


        wafer_uniformity = (
            lot_uniformity
            +
            rng.normal(
                0,
                0.03
            )
        )


        wafer_stress = (
            lot_stress
            +
            rng.normal(
                0,
                1.0
            )
        )


        wafer_density = (
            lot_density
            +
            rng.normal(
                0,
                0.005
            )
        )


        wafer_roughness = (
            lot_roughness
            +
            rng.normal(
                0,
                0.003
            )
        )


        wafer_defects = (
            lot_defects
            *
            (
                1
                +
                rng.normal(
                    0,
                    0.04
                )
            )
        )


        wafer_defects = max(
            wafer_defects,
            0
        )


        # ====================================================
        # SIMULATE WITHIN-WAFER MEASUREMENTS
        # ====================================================

        for measurement in range(
            1,
            MEASUREMENTS_PER_WAFER + 1
        ):

            measurement_thickness = (
                wafer_thickness
                +
                rng.normal(
                    0,
                    wafer_thickness
                    *
                    0.0015
                )
            )


            measurement_gpc = (
                wafer_gpc
                +
                rng.normal(
                    0,
                    0.0003
                )
            )


            production_data.append({

                "Lot": lot,

                "Wafer": wafer,

                "Measurement": measurement,

                "Temperature_C":
                    lot_temperature,

                "Pressure_Torr":
                    lot_pressure,

                "TMA_Pulse_s":
                    lot_tma_pulse,

                "H2O_Pulse_s":
                    lot_h2o_pulse,

                "Purge_s":
                    lot_purge,

                "GPC_nm_per_cycle":
                    measurement_gpc,

                "Film_Thickness_nm":
                    measurement_thickness,

                "Thickness_Uniformity_1sigma_%":
                    wafer_uniformity,

                "Film_Stress_MPa":
                    wafer_stress,

                "Film_Density_g_cm3":
                    wafer_density,

                "Surface_Roughness_nm_RMS":
                    wafer_roughness,

                "Defect_Density_per_cm2":
                    wafer_defects,

                "Cycle_Time_s":
                    lot_cycle_time,

                "Throughput_cycles_per_hour":
                    lot_throughput
            })


# ============================================================
# CREATE DATAFRAME
# ============================================================

production_df = pd.DataFrame(
    production_data
)


# ============================================================
# BASIC PROCESS FLAGS
# ============================================================

production_df[
    "Thickness_Deviation_%"
] = (
    (
        production_df[
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


production_df[
    "Thickness_OK"
] = (
    abs(
        production_df[
            "Thickness_Deviation_%"
        ]
    )
    <= 5.0
)


production_df[
    "Uniformity_OK"
] = (
    production_df[
        "Thickness_Uniformity_1sigma_%"
    ]
    <= 2.0
)


production_df[
    "Stress_OK"
] = (
    abs(
        production_df[
            "Film_Stress_MPa"
        ]
    )
    <= 80
)


production_df[
    "Density_OK"
] = (
    production_df[
        "Film_Density_g_cm3"
    ]
    >= 2.90
)


production_df[
    "Roughness_OK"
] = (
    production_df[
        "Surface_Roughness_nm_RMS"
    ]
    <= 0.30
)


production_df[
    "Defectivity_OK"
] = (
    production_df[
        "Defect_Density_per_cm2"
    ]
    <= 20
)


# ============================================================
# OVERALL MEASUREMENT ACCEPTANCE
# ============================================================

production_df[
    "Measurement_OK"
] = (
    production_df["Thickness_OK"]
    &
    production_df["Uniformity_OK"]
    &
    production_df["Stress_OK"]
    &
    production_df["Density_OK"]
    &
    production_df["Roughness_OK"]
    &
    production_df["Defectivity_OK"]
)


# ============================================================
# SAVE PRODUCTION DATA
# ============================================================

production_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# PRODUCTION SUMMARY
# ============================================================

print()
print("=" * 75)
print("PRODUCTION SIMULATION SUMMARY")
print("=" * 75)

print(
    f"Production lots       : {NUM_LOTS}"
)

print(
    f"Wafers per lot        : {WAFERS_PER_LOT}"
)

print(
    f"Measurements/wafer    : "
    f"{MEASUREMENTS_PER_WAFER}"
)

print(
    f"Total measurements    : "
    f"{len(production_df)}"
)


# ============================================================
# SUMMARY STATISTICS
# ============================================================

print()
print("-" * 75)
print("PROCESS MEASUREMENT STATISTICS")
print("-" * 75)

print(
    f"Thickness mean        : "
    f"{production_df['Film_Thickness_nm'].mean():.4f} nm"
)

print(
    f"Thickness std         : "
    f"{production_df['Film_Thickness_nm'].std():.4f} nm"
)

print(
    f"Thickness minimum     : "
    f"{production_df['Film_Thickness_nm'].min():.4f} nm"
)

print(
    f"Thickness maximum     : "
    f"{production_df['Film_Thickness_nm'].max():.4f} nm"
)

print()

print(
    f"GPC mean              : "
    f"{production_df['GPC_nm_per_cycle'].mean():.5f} nm/cycle"
)

print(
    f"GPC std               : "
    f"{production_df['GPC_nm_per_cycle'].std():.5f} nm/cycle"
)

print()

print(
    f"Uniformity mean       : "
    f"{production_df['Thickness_Uniformity_1sigma_%'].mean():.4f}%"
)

print(
    f"Stress mean           : "
    f"{production_df['Film_Stress_MPa'].mean():.3f} MPa"
)

print(
    f"Density mean          : "
    f"{production_df['Film_Density_g_cm3'].mean():.4f} g/cm³"
)

print(
    f"Roughness mean        : "
    f"{production_df['Surface_Roughness_nm_RMS'].mean():.4f} nm RMS"
)

print(
    f"Defect density mean   : "
    f"{production_df['Defect_Density_per_cm2'].mean():.3f}"
    f" defects/cm²"
)


# ============================================================
# ACCEPTANCE SUMMARY
# ============================================================

total_measurements = len(
    production_df
)

accepted_measurements = (
    production_df[
        "Measurement_OK"
    ].sum()
)


acceptance_rate = (
    accepted_measurements
    /
    total_measurements
    *
    100
)


print()
print("=" * 75)
print("PROCESS ACCEPTANCE")
print("=" * 75)

print(
    f"Accepted measurements : "
    f"{accepted_measurements}"
)

print(
    f"Rejected measurements : "
    f"{total_measurements - accepted_measurements}"
)

print(
    f"Acceptance rate       : "
    f"{acceptance_rate:.2f}%"
)


# ============================================================
# LOT-LEVEL SUMMARY
# ============================================================

lot_summary = (
    production_df
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

        Mean_Throughput=(
            "Throughput_cycles_per_hour",
            "mean"
        ),

        Accepted_Measurements=(
            "Measurement_OK",
            "sum"
        ),

        Total_Measurements=(
            "Measurement_OK",
            "count"
        )
    )
    .reset_index()
)


lot_summary[
    "Lot_Acceptance_%"
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
# SAVE LOT SUMMARY
# ============================================================

lot_summary.to_csv(
    "results/production_lot_summary.csv",
    index=False
)


# ============================================================
# DISPLAY FIRST 10 LOTS
# ============================================================

print()
print("=" * 75)
print("LOT-LEVEL SUMMARY")
print("=" * 75)

print(
    lot_summary.head(10).to_string(
        index=False
    )
)


# ============================================================
# DISPLAY PRODUCTION DATA SAMPLE
# ============================================================

print()
print("=" * 75)
print("PRODUCTION DATA SAMPLE")
print("=" * 75)

print(
    production_df.head(10).to_string(
        index=False
    )
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("PRODUCTION LOT SIMULATION COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/production_lot_data.csv"
)

print(
    "  results/production_lot_summary.csv"
)

print("=" * 75)
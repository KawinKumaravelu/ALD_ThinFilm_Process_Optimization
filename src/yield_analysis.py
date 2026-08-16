# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 15: MANUFACTURING YIELD ANALYSIS
# ============================================================

import os
import numpy as np
import pandas as pd


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

INPUT_FILE = "results/production_lot_data.csv"

TARGET_THICKNESS = 10.0

# Engineering specifications
THICKNESS_LSL = 9.5
THICKNESS_USL = 10.5

GPC_LSL = 0.095
GPC_USL = 0.105

UNIFORMITY_USL = 2.0

STRESS_USL = 80.0

DENSITY_LSL = 2.90

ROUGHNESS_USL = 0.30

DEFECT_DENSITY_USL = 20.0


# ============================================================
# LOAD PRODUCTION DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("ALD MANUFACTURING YIELD ANALYSIS")
print("=" * 75)

print()
print(
    f"Production measurements loaded : {len(df)}"
)


# ============================================================
# CALCULATE SPECIFICATION CHECKS
# ============================================================

df["Thickness_OK"] = (
    (df["Film_Thickness_nm"] >= THICKNESS_LSL)
    &
    (df["Film_Thickness_nm"] <= THICKNESS_USL)
)


df["GPC_OK"] = (
    (df["GPC_nm_per_cycle"] >= GPC_LSL)
    &
    (df["GPC_nm_per_cycle"] <= GPC_USL)
)


df["Uniformity_OK"] = (
    df["Thickness_Uniformity_1sigma_%"]
    <= UNIFORMITY_USL
)


df["Stress_OK"] = (
    abs(df["Film_Stress_MPa"])
    <= STRESS_USL
)


df["Density_OK"] = (
    df["Film_Density_g_cm3"]
    >= DENSITY_LSL
)


df["Roughness_OK"] = (
    df["Surface_Roughness_nm_RMS"]
    <= ROUGHNESS_USL
)


df["Defectivity_OK"] = (
    df["Defect_Density_per_cm2"]
    <= DEFECT_DENSITY_USL
)


# ============================================================
# OVERALL GOOD / DEFECTIVE CLASSIFICATION
# ============================================================

df["Good"] = (
    df["Thickness_OK"]
    &
    df["GPC_OK"]
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
)


df["Yield_Status"] = np.where(
    df["Good"],
    "GOOD",
    "DEFECTIVE"
)


# ============================================================
# TOTAL YIELD
# ============================================================

total_measurements = len(df)

good_measurements = (
    df["Good"].sum()
)

defective_measurements = (
    total_measurements
    -
    good_measurements
)

yield_percent = (
    good_measurements
    /
    total_measurements
    *
    100
)


# ============================================================
# DISPLAY OVERALL YIELD
# ============================================================

print()
print("=" * 75)
print("OVERALL MANUFACTURING YIELD")
print("=" * 75)

print(
    f"Total measurements     : "
    f"{total_measurements}"
)

print(
    f"Good measurements      : "
    f"{good_measurements}"
)

print(
    f"Defective measurements : "
    f"{defective_measurements}"
)

print(
    f"Manufacturing yield    : "
    f"{yield_percent:.2f}%"
)


# ============================================================
# PARAMETER-WISE YIELD
# ============================================================

print()
print("=" * 75)
print("PARAMETER-WISE YIELD")
print("=" * 75)


parameter_checks = {

    "Film Thickness":
        "Thickness_OK",

    "GPC":
        "GPC_OK",

    "Thickness Uniformity":
        "Uniformity_OK",

    "Film Stress":
        "Stress_OK",

    "Film Density":
        "Density_OK",

    "Surface Roughness":
        "Roughness_OK",

    "Defect Density":
        "Defectivity_OK"
}


parameter_results = []


for parameter, column in parameter_checks.items():

    good_count = (
        df[column].sum()
    )

    bad_count = (
        total_measurements
        -
        good_count
    )

    parameter_yield = (
        good_count
        /
        total_measurements
        *
        100
    )

    parameter_results.append({

        "Parameter":
            parameter,

        "Good_Count":
            good_count,

        "Defective_Count":
            bad_count,

        "Yield_%":
            parameter_yield
    })

    print()

    print(
        f"{parameter:<25}"
        f"Yield = "
        f"{parameter_yield:.2f}%"
        f" | Defects = "
        f"{bad_count}"
    )


# ============================================================
# SAVE PARAMETER YIELD
# ============================================================

parameter_yield_df = pd.DataFrame(
    parameter_results
)


parameter_yield_file = (
    "results/parameter_yield_summary.csv"
)


parameter_yield_df.to_csv(
    parameter_yield_file,
    index=False
)


# ============================================================
# DEFECT CONTRIBUTION ANALYSIS
# ============================================================
#
# Count how many measurements fail each specification.
#
# A measurement can fail more than one parameter.
#
# ============================================================

defect_counts = {

    "Film Thickness":
        (~df["Thickness_OK"]).sum(),

    "GPC":
        (~df["GPC_OK"]).sum(),

    "Thickness Uniformity":
        (~df["Uniformity_OK"]).sum(),

    "Film Stress":
        (~df["Stress_OK"]).sum(),

    "Film Density":
        (~df["Density_OK"]).sum(),

    "Surface Roughness":
        (~df["Roughness_OK"]).sum(),

    "Defect Density":
        (~df["Defectivity_OK"]).sum()
}


defect_results = []


for parameter, count in defect_counts.items():

    defect_results.append({

        "Parameter":
            parameter,

        "Defect_Count":
            int(count),

        "Defect_Rate_%":
            count
            /
            total_measurements
            *
            100
    })


defect_df = pd.DataFrame(
    defect_results
)


# ============================================================
# DISPLAY DEFECT CONTRIBUTION
# ============================================================

print()
print("=" * 75)
print("DEFECT CONTRIBUTION")
print("=" * 75)

for _, row in defect_df.iterrows():

    print(
        f"{row['Parameter']:<25}"
        f"Defects = "
        f"{int(row['Defect_Count']):<6}"
        f"Rate = "
        f"{row['Defect_Rate_%']:.2f}%"
    )


# ============================================================
# SAVE DEFECT ANALYSIS
# ============================================================

defect_file = (
    "results/defect_contribution.csv"
)

defect_df.to_csv(
    defect_file,
    index=False
)


# ============================================================
# LOT-LEVEL YIELD
# ============================================================

lot_yield = (
    df
    .groupby("Lot")
    .agg(

        Total_Measurements=(
            "Good",
            "count"
        ),

        Good_Measurements=(
            "Good",
            "sum"
        )
    )
    .reset_index()
)


lot_yield["Defective_Measurements"] = (
    lot_yield["Total_Measurements"]
    -
    lot_yield["Good_Measurements"]
)


lot_yield["Yield_%"] = (
    lot_yield["Good_Measurements"]
    /
    lot_yield["Total_Measurements"]
    *
    100
)


# ============================================================
# DISPLAY LOT YIELD
# ============================================================

print()
print("=" * 75)
print("LOT-LEVEL YIELD")
print("=" * 75)

print(
    lot_yield.to_string(
        index=False
    )
)


# ============================================================
# SAVE LOT YIELD
# ============================================================

lot_yield_file = (
    "results/lot_yield_summary.csv"
)

lot_yield.to_csv(
    lot_yield_file,
    index=False
)


# ============================================================
# FIRST PASS YIELD
# ============================================================
#
# First-pass yield is the percentage of measurements that
# pass all specifications without requiring rework.
#
# ============================================================

first_pass_yield = (
    good_measurements
    /
    total_measurements
    *
    100
)


print()
print("=" * 75)
print("FIRST-PASS YIELD")
print("=" * 75)

print(
    f"First-pass yield       : "
    f"{first_pass_yield:.2f}%"
)


# ============================================================
# SAVE FINAL PRODUCTION DATA
# ============================================================

output_file = (
    "results/production_yield_data.csv"
)

df.to_csv(
    output_file,
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print()
print("=" * 75)
print("YIELD ANALYSIS SUMMARY")
print("=" * 75)

print(
    f"Total production measurements : "
    f"{total_measurements}"
)

print(
    f"Good measurements              : "
    f"{good_measurements}"
)

print(
    f"Defective measurements         : "
    f"{defective_measurements}"
)

print(
    f"Manufacturing yield            : "
    f"{yield_percent:.2f}%"
)

print(
    f"First-pass yield               : "
    f"{first_pass_yield:.2f}%"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("YIELD ANALYSIS COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/production_yield_data.csv"
)

print(
    "  results/parameter_yield_summary.csv"
)

print(
    "  results/defect_contribution.csv"
)

print(
    "  results/lot_yield_summary.csv"
)

print("=" * 75)
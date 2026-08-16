# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 14: PROCESS CAPABILITY ANALYSIS
# Cp / Cpk
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

# Engineering specifications
TARGET_THICKNESS = 10.0

THICKNESS_LSL = 9.5
THICKNESS_USL = 10.5

# GPC specification
GPC_TARGET = 0.100

GPC_LSL = 0.095
GPC_USL = 0.105

# Uniformity specification
UNIFORMITY_LSL = 0.0
UNIFORMITY_USL = 2.0

# Defect density specification
DEFECT_LSL = 0.0
DEFECT_USL = 20.0


# ============================================================
# LOAD PRODUCTION DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("ALD PROCESS CAPABILITY ANALYSIS")
print("=" * 75)

print()
print(
    f"Production measurements loaded : {len(df)}"
)


# ============================================================
# CAPABILITY FUNCTION
# ============================================================

def calculate_capability(
    series,
    lsl,
    usl
):

    mean = series.mean()

    std = series.std(
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
        cpu,
        cpl,
        cpk
    )


# ============================================================
# INTERPRETATION FUNCTION
# ============================================================

def capability_status(cpk):

    if cpk >= 1.67:

        return "Excellent"

    elif cpk >= 1.33:

        return "Capable"

    elif cpk >= 1.00:

        return "Marginal"

    else:

        return "Not Capable"


# ============================================================
# PARAMETERS
# ============================================================

parameters = [

    {
        "column":
            "Film_Thickness_nm",

        "name":
            "Film Thickness",

        "unit":
            "nm",

        "lsl":
            THICKNESS_LSL,

        "usl":
            THICKNESS_USL
    },

    {
        "column":
            "GPC_nm_per_cycle",

        "name":
            "GPC",

        "unit":
            "nm/cycle",

        "lsl":
            GPC_LSL,

        "usl":
            GPC_USL
    },

    {
        "column":
            "Thickness_Uniformity_1sigma_%",

        "name":
            "Thickness Uniformity",

        "unit":
            "%",

        "lsl":
            UNIFORMITY_LSL,

        "usl":
            UNIFORMITY_USL
    },

    {
        "column":
            "Defect_Density_per_cm2",

        "name":
            "Defect Density",

        "unit":
            "defects/cm²",

        "lsl":
            DEFECT_LSL,

        "usl":
            DEFECT_USL
    }
]


# ============================================================
# RESULTS STORAGE
# ============================================================

results = []


# ============================================================
# CAPABILITY ANALYSIS
# ============================================================

for parameter in parameters:

    column = parameter["column"]

    name = parameter["name"]

    unit = parameter["unit"]

    lsl = parameter["lsl"]

    usl = parameter["usl"]


    (
        mean,
        std,
        cp,
        cpu,
        cpl,
        cpk
    ) = calculate_capability(
        df[column],
        lsl,
        usl
    )


    status = capability_status(
        cpk
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    results.append({

        "Parameter":
            name,

        "Unit":
            unit,

        "LSL":
            lsl,

        "USL":
            usl,

        "Mean":
            mean,

        "Std_Dev":
            std,

        "Cp":
            cp,

        "Cpu":
            cpu,

        "Cpl":
            cpl,

        "Cpk":
            cpk,

        "Capability_Status":
            status
    })


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print()
    print("=" * 75)

    print(
        f"PROCESS CAPABILITY: {name}"
    )

    print("=" * 75)

    print()

    print(
        f"Lower Specification Limit : "
        f"{lsl:.6f}"
    )

    print(
        f"Upper Specification Limit : "
        f"{usl:.6f}"
    )

    print(
        f"Process Mean              : "
        f"{mean:.6f}"
    )

    print(
        f"Standard Deviation        : "
        f"{std:.6f}"
    )

    print()

    print(
        f"Cp                        : "
        f"{cp:.4f}"
    )

    print(
        f"Cpu                       : "
        f"{cpu:.4f}"
    )

    print(
        f"Cpl                       : "
        f"{cpl:.4f}"
    )

    print(
        f"Cpk                       : "
        f"{cpk:.4f}"
    )

    print()

    print(
        f"Capability Status         : "
        f"{status}"
    )


    # ========================================================
    # CAPABILITY HISTOGRAM
    # ========================================================

    plt.figure(
        figsize=(10, 6)
    )

    plt.hist(
        df[column],
        bins=30,
        density=True
    )

    plt.axvline(
        lsl,
        linestyle="--",
        linewidth=2,
        label="LSL"
    )

    plt.axvline(
        usl,
        linestyle="--",
        linewidth=2,
        label="USL"
    )

    plt.axvline(
        mean,
        linestyle="-",
        linewidth=2,
        label="Process Mean"
    )

    plt.title(
        f"Process Capability - {name}"
    )

    plt.xlabel(
        f"{name} ({unit})"
    )

    plt.ylabel(
        "Probability Density"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()


    filename = (
        "results/"
        +
        column
        +
        "_capability.png"
    )

    plt.savefig(
        filename,
        dpi=300
    )

    plt.close()


# ============================================================
# CREATE CAPABILITY SUMMARY
# ============================================================

capability_df = pd.DataFrame(
    results
)


# ============================================================
# SAVE CAPABILITY RESULTS
# ============================================================

output_file = (
    "results/process_capability_summary.csv"
)

capability_df.to_csv(
    output_file,
    index=False
)


# ============================================================
# OVERALL PROCESS CAPABILITY
# ============================================================

print()
print("=" * 75)
print("OVERALL PROCESS CAPABILITY")
print("=" * 75)

print()

for _, row in capability_df.iterrows():

    print(
        f"{row['Parameter']:<25}"
        f"Cp = {row['Cp']:.3f}   "
        f"Cpk = {row['Cpk']:.3f}   "
        f"{row['Capability_Status']}"
    )


# ============================================================
# DETERMINE OVERALL STATUS
# ============================================================

minimum_cpk = capability_df[
    "Cpk"
].min()


if minimum_cpk >= 1.67:

    overall_status = (
        "HIGHLY CAPABLE"
    )

elif minimum_cpk >= 1.33:

    overall_status = (
        "CAPABLE"
    )

elif minimum_cpk >= 1.00:

    overall_status = (
        "MARGINALLY CAPABLE"
    )

else:

    overall_status = (
        "NOT CAPABLE"
    )


print()

print(
    f"Minimum Cpk              : "
    f"{minimum_cpk:.4f}"
)

print(
    f"Overall Process Status   : "
    f"{overall_status}"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("PROCESS CAPABILITY ANALYSIS COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/process_capability_summary.csv"
)

print(
    "  results/Film_Thickness_nm_capability.png"
)

print(
    "  results/GPC_nm_per_cycle_capability.png"
)

print(
    "  results/Thickness_Uniformity_1sigma_%_capability.png"
)

print(
    "  results/Defect_Density_per_cm2_capability.png"
)

print("=" * 75)
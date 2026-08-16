# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 13: STATISTICAL PROCESS CONTROL (SPC)
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

# Number of standard deviations for control limits
SIGMA_LEVEL = 3


# ============================================================
# LOAD PRODUCTION DATA
# ============================================================

df = pd.read_csv(INPUT_FILE)

print("=" * 75)
print("ALD STATISTICAL PROCESS CONTROL (SPC)")
print("=" * 75)

print()
print(
    f"Production measurements loaded : {len(df)}"
)


# ============================================================
# PARAMETERS TO MONITOR
# ============================================================

parameters = {

    "Film_Thickness_nm":
        "Film Thickness (nm)",

    "GPC_nm_per_cycle":
        "GPC (nm/cycle)",

    "Thickness_Uniformity_1sigma_%":
        "Thickness Uniformity (%)",

    "Defect_Density_per_cm2":
        "Defect Density (defects/cm²)"
}


# ============================================================
# SPC FUNCTION
# ============================================================

def calculate_control_limits(series):

    mean = series.mean()

    std = series.std(
        ddof=1
    )

    ucl = (
        mean
        +
        SIGMA_LEVEL * std
    )

    lcl = (
        mean
        -
        SIGMA_LEVEL * std
    )

    return mean, std, ucl, lcl


# ============================================================
# STORE SPC SUMMARY
# ============================================================

spc_results = []


# ============================================================
# PROCESS EACH PARAMETER
# ============================================================

for column, label in parameters.items():

    print()
    print("=" * 75)

    print(
        f"SPC ANALYSIS: {label}"
    )

    print("=" * 75)


    # --------------------------------------------------------
    # Calculate control limits
    # --------------------------------------------------------

    mean, std, ucl, lcl = (
        calculate_control_limits(
            df[column]
        )
    )


    # --------------------------------------------------------
    # Detect control-limit violations
    # --------------------------------------------------------

    out_of_control = (
        (df[column] > ucl)
        |
        (df[column] < lcl)
    )


    number_out_of_control = (
        out_of_control.sum()
    )


    percentage_out_of_control = (
        number_out_of_control
        /
        len(df)
        *
        100
    )


    # --------------------------------------------------------
    # Store results
    # --------------------------------------------------------

    spc_results.append({

        "Parameter":
            column,

        "Mean":
            mean,

        "Std_Dev":
            std,

        "LCL":
            lcl,

        "Center_Line":
            mean,

        "UCL":
            ucl,

        "Out_of_Control_Count":
            number_out_of_control,

        "Out_of_Control_Percent":
            percentage_out_of_control
    })


    # --------------------------------------------------------
    # Display
    # --------------------------------------------------------

    print()

    print(
        f"Mean / Center Line     : "
        f"{mean:.6f}"
    )

    print(
        f"Standard deviation     : "
        f"{std:.6f}"
    )

    print(
        f"Lower Control Limit    : "
        f"{lcl:.6f}"
    )

    print(
        f"Upper Control Limit    : "
        f"{ucl:.6f}"
    )

    print(
        f"Out-of-control points  : "
        f"{number_out_of_control}"
    )

    print(
        f"Out-of-control percent : "
        f"{percentage_out_of_control:.2f}%"
    )


    # ========================================================
    # CONTROL CHART
    # ========================================================

    plt.figure(
        figsize=(12, 6)
    )

    x = np.arange(
        1,
        len(df) + 1
    )

    plt.plot(
        x,
        df[column],
        linewidth=1
    )

    plt.axhline(
        mean,
        linestyle="--",
        label="Center Line"
    )

    plt.axhline(
        ucl,
        linestyle="--",
        label="UCL (+3σ)"
    )

    plt.axhline(
        lcl,
        linestyle="--",
        label="LCL (-3σ)"
    )


    # Highlight out-of-control points

    if number_out_of_control > 0:

        plt.scatter(
            x[out_of_control],
            df.loc[
                out_of_control,
                column
            ],
            s=30,
            label="Out of Control"
        )


    plt.title(
        f"SPC Control Chart - {label}"
    )

    plt.xlabel(
        "Production Measurement"
    )

    plt.ylabel(
        label
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.3
    )

    plt.tight_layout()


    # --------------------------------------------------------
    # Safe filename
    # --------------------------------------------------------

    safe_name = (
        column
        .replace(
            "/",
            "_"
        )
    )


    plot_file = (
        f"results/SPC_{safe_name}.png"
    )


    plt.savefig(
        plot_file,
        dpi=300
    )

    plt.close()


# ============================================================
# SPC SUMMARY DATAFRAME
# ============================================================

spc_summary = pd.DataFrame(
    spc_results
)


# ============================================================
# SAVE SPC SUMMARY
# ============================================================

summary_file = (
    "results/SPC_summary.csv"
)

spc_summary.to_csv(
    summary_file,
    index=False
)


# ============================================================
# ADD SPC STATUS TO ORIGINAL DATA
# ============================================================

for column, label in parameters.items():

    mean, std, ucl, lcl = (
        calculate_control_limits(
            df[column]
        )
    )


    df[
        f"{column}_SPC_Status"
    ] = np.where(

        (
            df[column] > ucl
        )
        |
        (
            df[column] < lcl
        ),

        "OUT_OF_CONTROL",

        "IN_CONTROL"
    )


# ============================================================
# SAVE DATA WITH SPC STATUS
# ============================================================

spc_data_file = (
    "results/production_lot_SPC_data.csv"
)

df.to_csv(
    spc_data_file,
    index=False
)


# ============================================================
# OVERALL SPC STATUS
# ============================================================

all_status_columns = [

    f"{column}_SPC_Status"

    for column in parameters
]


df["Overall_SPC_Status"] = np.where(

    df[
        all_status_columns
    ].eq(
        "OUT_OF_CONTROL"
    ).any(
        axis=1
    ),

    "OUT_OF_CONTROL",

    "IN_CONTROL"
)


# ============================================================
# OVERALL SUMMARY
# ============================================================

total_points = len(df)

total_ooc = (
    df[
        "Overall_SPC_Status"
    ]
    .eq(
        "OUT_OF_CONTROL"
    )
    .sum()
)


total_ic = (
    total_points
    -
    total_ooc
)


print()
print("=" * 75)
print("OVERALL SPC SUMMARY")
print("=" * 75)

print(
    f"Total measurements    : "
    f"{total_points}"
)

print(
    f"In-control points     : "
    f"{total_ic}"
)

print(
    f"Out-of-control points : "
    f"{total_ooc}"
)

print(
    f"Out-of-control rate   : "
    f"{total_ooc / total_points * 100:.2f}%"
)


# ============================================================
# FINAL STATUS
# ============================================================

if total_ooc == 0:

    print()
    print(
        "PROCESS STATUS        : IN CONTROL"
    )

else:

    print()
    print(
        "PROCESS STATUS        : "
        "OUT OF CONTROL"
    )


# ============================================================
# SAVE FINAL SPC DATA
# ============================================================

df.to_csv(
    spc_data_file,
    index=False
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("SPC ANALYSIS COMPLETE")
print("=" * 75)

print(
    "Generated files:"
)

print(
    "  results/SPC_summary.csv"
)

print(
    "  results/production_lot_SPC_data.csv"
)

print(
    "  results/SPC_Film_Thickness_nm.png"
)

print(
    "  results/SPC_GPC_nm_per_cycle.png"
)

print(
    "  results/SPC_Thickness_Uniformity_1sigma_%.png"
)

print(
    "  results/SPC_Defect_Density_per_cm2.png"
)

print("=" * 75)
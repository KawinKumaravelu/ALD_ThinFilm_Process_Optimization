# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 17: ROOT CAUSE ANALYSIS (RCA)
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

INPUT_FILE = "results/process_excursion_data.csv"

OUTPUT_FILE = (
    "results/root_cause_analysis.csv"
)

FIVE_WHY_FILE = (
    "results/five_why_analysis.csv"
)

RCA_PLOT = (
    "results/root_cause_analysis.png"
)


# ============================================================
# LOAD EXCURSION DATA
# ============================================================

df = pd.read_csv(
    INPUT_FILE
)

print("=" * 75)
print("ALD ROOT CAUSE ANALYSIS")
print("=" * 75)

print()

print(
    f"Production measurements loaded : "
    f"{len(df)}"
)


# ============================================================
# IDENTIFY EXCURSION
# ============================================================

excursion_df = df[
    df["Excursion_Status"]
    ==
    "EXCURSION"
].copy()


normal_df = df[
    df["Excursion_Status"]
    ==
    "NORMAL"
].copy()


print(
    f"Excursion measurements         : "
    f"{len(excursion_df)}"
)

print(
    f"Normal measurements            : "
    f"{len(normal_df)}"
)


# ============================================================
# COMPARE NORMAL VS EXCURSION
# ============================================================

comparison = []

parameters = [

    (
        "TMA_Pulse_s",
        "TMA Pulse",
        "s"
    ),

    (
        "H2O_Pulse_s",
        "H2O Pulse",
        "s"
    ),

    (
        "Pressure_Torr",
        "Chamber Pressure",
        "Torr"
    ),

    (
        "GPC_nm_per_cycle",
        "GPC",
        "nm/cycle"
    ),

    (
        "Film_Thickness_nm",
        "Film Thickness",
        "nm"
    ),

    (
        "Thickness_Uniformity_1sigma_%",
        "Thickness Uniformity",
        "%"
    ),

    (
        "Film_Stress_MPa",
        "Film Stress",
        "MPa"
    ),

    (
        "Film_Density_g_cm3",
        "Film Density",
        "g/cm3"
    ),

    (
        "Surface_Roughness_nm_RMS",
        "Surface Roughness",
        "nm RMS"
    ),

    (
        "Defect_Density_per_cm2",
        "Defect Density",
        "defects/cm2"
    )
]


for column, name, unit in parameters:

    normal_mean = (
        normal_df[column].mean()
    )

    excursion_mean = (
        excursion_df[column].mean()
    )

    absolute_change = (
        excursion_mean
        -
        normal_mean
    )

    if normal_mean != 0:

        percentage_change = (
            absolute_change
            /
            abs(normal_mean)
            *
            100
        )

    else:

        percentage_change = 0


    comparison.append({

        "Parameter":
            name,

        "Unit":
            unit,

        "Normal_Mean":
            normal_mean,

        "Excursion_Mean":
            excursion_mean,

        "Absolute_Change":
            absolute_change,

        "Percentage_Change":
            percentage_change
    })


comparison_df = pd.DataFrame(
    comparison
)


# ============================================================
# DISPLAY COMPARISON
# ============================================================

print()
print("=" * 75)
print("NORMAL VS EXCURSION COMPARISON")
print("=" * 75)

print()

print(
    comparison_df.to_string(
        index=False
    )
)


# ============================================================
# IDENTIFY PRIMARY EFFECT
# ============================================================

normal_gpc = normal_df[
    "GPC_nm_per_cycle"
].mean()

excursion_gpc = excursion_df[
    "GPC_nm_per_cycle"
].mean()


normal_tma = normal_df[
    "TMA_Pulse_s"
].mean()

excursion_tma = excursion_df[
    "TMA_Pulse_s"
].mean()


gpc_change_percent = (
    (
        excursion_gpc
        -
        normal_gpc
    )
    /
    normal_gpc
    *
    100
)


tma_change_percent = (
    (
        excursion_tma
        -
        normal_tma
    )
    /
    normal_tma
    *
    100
)


# ============================================================
# PRINT PRIMARY FINDING
# ============================================================

print()
print("=" * 75)
print("PRIMARY RCA FINDING")
print("=" * 75)

print()

print(
    f"Normal TMA pulse       : "
    f"{normal_tma:.6f} s"
)

print(
    f"Excursion TMA pulse    : "
    f"{excursion_tma:.6f} s"
)

print(
    f"TMA pulse change       : "
    f"{tma_change_percent:.2f}%"
)

print()

print(
    f"Normal GPC             : "
    f"{normal_gpc:.6f} nm/cycle"
)

print(
    f"Excursion GPC          : "
    f"{excursion_gpc:.6f} nm/cycle"
)

print(
    f"GPC change             : "
    f"{gpc_change_percent:.2f}%"
)


# ============================================================
# 5-WHY ANALYSIS
# ============================================================

five_why = [

    {
        "Why_Level": 1,
        "Question":
            "Why did the product fail?",
        "Finding":
            "GPC fell below the lower specification limit."
    },

    {
        "Why_Level": 2,
        "Question":
            "Why did GPC fall?",
        "Finding":
            "The effective TMA precursor dose decreased."
    },

    {
        "Why_Level": 3,
        "Question":
            "Why did the TMA precursor dose decrease?",
        "Finding":
            "The simulated TMA pulse delivery was reduced during Lot 17."
    },

    {
        "Why_Level": 4,
        "Question":
            "Why was the TMA pulse delivery reduced?",
        "Finding":
            "A precursor delivery / valve timing deviation is identified as the simulated process mechanism."
    },

    {
        "Why_Level": 5,
        "Question":
            "What is the underlying process-control issue?",
        "Finding":
            "Insufficient monitoring and control of precursor pulse delivery can allow a TMA dosing excursion to affect GPC."
    }
]


five_why_df = pd.DataFrame(
    five_why
)


# ============================================================
# DISPLAY 5-WHY
# ============================================================

print()
print("=" * 75)
print("5-WHY ROOT CAUSE ANALYSIS")
print("=" * 75)

for _, row in five_why_df.iterrows():

    print()

    print(
        f"Why {row['Why_Level']}: "
        f"{row['Question']}"
    )

    print(
        f"Finding: "
        f"{row['Finding']}"
    )


# ============================================================
# ROOT CAUSE CATEGORIES
# ============================================================

root_causes = [

    {
        "Category":
            "Equipment",

        "Potential_Cause":
            "Precursor valve timing or delivery instability",

        "Evidence":
            "TMA pulse decreased during excursion",

        "Likelihood":
            "High"
    },

    {
        "Category":
            "Process",

        "Potential_Cause":
            "Reduced effective precursor dose",

        "Evidence":
            "TMA pulse reduction accompanied GPC reduction",

        "Likelihood":
            "High"
    },

    {
        "Category":
            "Control",

        "Potential_Cause":
            "Insufficient real-time precursor delivery monitoring",

        "Evidence":
            "Excursion was detected through downstream GPC monitoring",

        "Likelihood":
            "Medium"
    },

    {
        "Category":
            "Material",

        "Potential_Cause":
            "Precursor depletion or delivery instability",

        "Evidence":
            "Not directly simulated",

        "Likelihood":
            "Low / Unconfirmed"
    },

    {
        "Category":
            "Recipe",

        "Potential_Cause":
            "Incorrect TMA pulse recipe value",

        "Evidence":
            "No recipe change was simulated",

        "Likelihood":
            "Low / Unconfirmed"
    }
]


root_cause_df = pd.DataFrame(
    root_causes
)


# ============================================================
# DISPLAY ROOT CAUSES
# ============================================================

print()
print("=" * 75)
print("ROOT CAUSE CATEGORIES")
print("=" * 75)

print()

print(
    root_cause_df.to_string(
        index=False
    )
)


# ============================================================
# ROOT CAUSE CONCLUSION
# ============================================================

print()
print("=" * 75)
print("RCA CONCLUSION")
print("=" * 75)

print()

print(
    "Primary suspected root cause:"
)

print(
    "TMA precursor delivery / pulse timing deviation."
)

print()

print(
    "Process effect:"
)

print(
    "Reduced TMA dose caused a reduction in GPC."
)

print()

print(
    "Detection method:"
)

print(
    "SPC monitoring detected the GPC excursion."
)

print()

print(
    "Confidence:"
)

print(
    "High within the simulated process model; "
    "physical equipment verification would be required "
    "for real manufacturing confirmation."
)


# ============================================================
# RECOMMENDED INVESTIGATION
# ============================================================

investigation = [

    {
        "Priority": 1,
        "Check":
            "Verify TMA valve timing",
        "Purpose":
            "Confirm actual precursor pulse duration"
    },

    {
        "Priority": 2,
        "Check":
            "Verify TMA delivery pressure / flow",
        "Purpose":
            "Confirm sufficient precursor delivery"
    },

    {
        "Priority": 3,
        "Check":
            "Check precursor source condition",
        "Purpose":
            "Identify depletion or supply instability"
    },

    {
        "Priority": 4,
        "Check":
            "Review recipe and equipment logs",
        "Purpose":
            "Identify control or recipe changes"
    },

    {
        "Priority": 5,
        "Check":
            "Run verification deposition",
        "Purpose":
            "Confirm recovery of GPC after correction"
    }
]


investigation_df = pd.DataFrame(
    investigation
)


# ============================================================
# DISPLAY INVESTIGATION
# ============================================================

print()
print("=" * 75)
print("RECOMMENDED RCA INVESTIGATION")
print("=" * 75)

print()

print(
    investigation_df.to_string(
        index=False
    )
)


# ============================================================
# CREATE RCA SUMMARY
# ============================================================

summary_rows = [

    {
        "Item":
            "Problem",

        "Result":
            "GPC below specification in Lot 17"
    },

    {
        "Item":
            "Affected Lot",

        "Result":
            "Lot 17"
    },

    {
        "Item":
            "Affected Measurements",

        "Result":
            len(excursion_df)
    },

    {
        "Item":
            "Primary Affected Parameter",

        "Result":
            "GPC"
    },

    {
        "Item":
            "Suspected Root Cause",

        "Result":
            "TMA precursor delivery / pulse timing deviation"
    },

    {
        "Item":
            "Process Effect",

        "Result":
            "Reduced precursor dose and reduced GPC"
    },

    {
        "Item":
            "Detection Method",

        "Result":
            "SPC GPC monitoring"
    },

    {
        "Item":
            "Detection Rate",

        "Result":
            "100%"
    }
]


summary_df = pd.DataFrame(
    summary_rows
)


# ============================================================
# SAVE RCA FILES
# ============================================================

comparison_df.to_csv(
    OUTPUT_FILE,
    index=False
)

five_why_df.to_csv(
    FIVE_WHY_FILE,
    index=False
)

root_cause_df.to_csv(
    "results/root_cause_categories.csv",
    index=False
)

investigation_df.to_csv(
    "results/rca_investigation_plan.csv",
    index=False
)

summary_df.to_csv(
    "results/root_cause_summary.csv",
    index=False
)


# ============================================================
# RCA BAR CHART
# ============================================================

plot_df = comparison_df[
    comparison_df["Parameter"].isin(
        [
            "TMA Pulse",
            "GPC",
            "Film Thickness"
        ]
    )
].copy()


plt.figure(
    figsize=(10, 6)
)


plt.bar(
    plot_df["Parameter"],
    plot_df["Percentage_Change"]
)


plt.axhline(
    0,
    linewidth=1
)


plt.title(
    "Process Parameter Change During Excursion"
)

plt.xlabel(
    "Process / Film Parameter"
)

plt.ylabel(
    "Change from Normal (%)"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()


plt.savefig(
    RCA_PLOT,
    dpi=300
)

plt.close()


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("ROOT CAUSE ANALYSIS COMPLETE")
print("=" * 75)

print()

print(
    "Generated files:"
)

print(
    "  results/root_cause_analysis.csv"
)

print(
    "  results/five_why_analysis.csv"
)

print(
    "  results/root_cause_categories.csv"
)

print(
    "  results/rca_investigation_plan.csv"
)

print(
    "  results/root_cause_summary.csv"
)

print(
    "  results/root_cause_analysis.png"
)

print("=" * 75)
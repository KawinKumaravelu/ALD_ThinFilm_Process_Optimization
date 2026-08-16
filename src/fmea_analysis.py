# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 18: FMEA ANALYSIS
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

OUTPUT_FILE = "results/FMEA_analysis.csv"
RISK_FILE = "results/FMEA_risk_priority.csv"
PLOT_FILE = "results/FMEA_RPN_chart.png"


# ============================================================
# FMEA SCORING
# ============================================================
#
# Severity (S)
# 1  = negligible effect
# 10 = critical effect
#
# Occurrence (O)
# 1  = very unlikely
# 10 = frequent
#
# Detection (D)
# 1  = almost certain detection
# 10 = very difficult to detect
#
# RPN = Severity × Occurrence × Detection
# ============================================================


fmea_data = [

    {
        "Process_Step":
            "TMA precursor pulse",

        "Failure_Mode":
            "TMA pulse duration too short",

        "Potential_Effect":
            "Reduced precursor dose and low GPC",

        "Potential_Cause":
            "Valve timing or precursor delivery instability",

        "Current_Control":
            "Recipe control and GPC monitoring",

        "Severity":
            8,

        "Occurrence":
            5,

        "Detection":
            4,

        "Recommended_Action":
            "Monitor TMA pulse delivery and verify valve timing"
    },

    {
        "Process_Step":
            "TMA precursor pulse",

        "Failure_Mode":
            "TMA pulse duration too long",

        "Potential_Effect":
            "Excess deposition and increased GPC",

        "Potential_Cause":
            "Valve timing or recipe error",

        "Current_Control":
            "Recipe verification and GPC monitoring",

        "Severity":
            7,

        "Occurrence":
            3,

        "Detection":
            4,

        "Recommended_Action":
            "Add pulse-duration verification and alarm limits"
    },

    {
        "Process_Step":
            "H2O reactant pulse",

        "Failure_Mode":
            "H2O pulse insufficient",

        "Potential_Effect":
            "Incomplete surface reaction and reduced film quality",

        "Potential_Cause":
            "Reactant delivery instability",

        "Current_Control":
            "Recipe control and film characterization",

        "Severity":
            7,

        "Occurrence":
            4,

        "Detection":
            5,

        "Recommended_Action":
            "Monitor H2O pulse delivery and verify reactant supply"
    },

    {
        "Process_Step":
            "H2O reactant pulse",

        "Failure_Mode":
            "H2O pulse excessive",

        "Potential_Effect":
            "Process time increase and possible process instability",

        "Potential_Cause":
            "Recipe or valve timing deviation",

        "Current_Control":
            "Recipe control",

        "Severity":
            5,

        "Occurrence":
            3,

        "Detection":
            5,

        "Recommended_Action":
            "Implement pulse timing verification"
    },

    {
        "Process_Step":
            "Purge",

        "Failure_Mode":
            "Insufficient purge time",

        "Potential_Effect":
            "Gas-phase reaction, contamination and non-ideal ALD growth",

        "Potential_Cause":
            "Incorrect purge recipe or valve timing",

        "Current_Control":
            "Recipe verification and film characterization",

        "Severity":
            8,

        "Occurrence":
            4,

        "Detection":
            6,

        "Recommended_Action":
            "Establish minimum validated purge time"
    },

    {
        "Process_Step":
            "Purge",

        "Failure_Mode":
            "Excessive purge time",

        "Potential_Effect":
            "Reduced process throughput",

        "Potential_Cause":
            "Over-conservative process recipe",

        "Current_Control":
            "Cycle-time monitoring",

        "Severity":
            5,

        "Occurrence":
            5,

        "Detection":
            2,

        "Recommended_Action":
            "Optimize purge time while maintaining film quality"
    },

    {
        "Process_Step":
            "Temperature control",

        "Failure_Mode":
            "Temperature below target",

        "Potential_Effect":
            "Reduced reaction rate and GPC variation",

        "Potential_Cause":
            "Heater or temperature-control instability",

        "Current_Control":
            "Temperature monitoring",

        "Severity":
            8,

        "Occurrence":
            3,

        "Detection":
            3,

        "Recommended_Action":
            "Use temperature alarms and calibration checks"
    },

    {
        "Process_Step":
            "Temperature control",

        "Failure_Mode":
            "Temperature above target",

        "Potential_Effect":
            "GPC variation and possible precursor decomposition",

        "Potential_Cause":
            "Heater-control deviation",

        "Current_Control":
            "Temperature monitoring",

        "Severity":
            8,

        "Occurrence":
            3,

        "Detection":
            3,

        "Recommended_Action":
            "Implement high-temperature alarm and heater verification"
    },

    {
        "Process_Step":
            "Chamber pressure",

        "Failure_Mode":
            "Pressure below target",

        "Potential_Effect":
            "Precursor transport and reaction variation",

        "Potential_Cause":
            "Pressure-control or pumping instability",

        "Current_Control":
            "Pressure monitoring",

        "Severity":
            7,

        "Occurrence":
            4,

        "Detection":
            3,

        "Recommended_Action":
            "Monitor pressure trend and verify pressure-control system"
    },

    {
        "Process_Step":
            "Chamber pressure",

        "Failure_Mode":
            "Pressure above target",

        "Potential_Effect":
            "Changed precursor transport and film non-uniformity",

        "Potential_Cause":
            "Throttle valve or pumping issue",

        "Current_Control":
            "Pressure monitoring",

        "Severity":
            7,

        "Occurrence":
            4,

        "Detection":
            3,

        "Recommended_Action":
            "Implement pressure alarm limits"
    },

    {
        "Process_Step":
            "Precursor supply",

        "Failure_Mode":
            "Precursor depletion",

        "Potential_Effect":
            "Reduced GPC and production yield",

        "Potential_Cause":
            "Low precursor inventory",

        "Current_Control":
            "Source-level monitoring",

        "Severity":
            8,

        "Occurrence":
            3,

        "Detection":
            6,

        "Recommended_Action":
            "Implement precursor inventory monitoring and replacement limits"
    },

    {
        "Process_Step":
            "Deposition",

        "Failure_Mode":
            "Film thickness outside specification",

        "Potential_Effect":
            "Device/process performance degradation",

        "Potential_Cause":
            "Combined process parameter variation",

        "Current_Control":
            "Thickness measurement and SPC",

        "Severity":
            9,

        "Occurrence":
            3,

        "Detection":
            2,

        "Recommended_Action":
            "Maintain SPC monitoring and process capability analysis"
    },

    {
        "Process_Step":
            "Deposition",

        "Failure_Mode":
            "Film non-uniformity",

        "Potential_Effect":
            "Wafer-to-wafer or within-wafer performance variation",

        "Potential_Cause":
            "Pressure, temperature or precursor distribution variation",

        "Current_Control":
            "Uniformity measurement",

        "Severity":
            8,

        "Occurrence":
            3,

        "Detection":
            4,

        "Recommended_Action":
            "Monitor wafer uniformity and optimize process window"
    },

    {
        "Process_Step":
            "Film characterization",

        "Failure_Mode":
            "High surface roughness",

        "Potential_Effect":
            "Degraded interface and device performance",

        "Potential_Cause":
            "Non-ideal growth conditions",

        "Current_Control":
            "Surface roughness characterization",

        "Severity":
            6,

        "Occurrence":
            3,

        "Detection":
            4,

        "Recommended_Action":
            "Track roughness during process qualification"
    },

    {
        "Process_Step":
            "Film characterization",

        "Failure_Mode":
            "High defect density",

        "Potential_Effect":
            "Reduced manufacturing yield",

        "Potential_Cause":
            "Particles, contamination or process instability",

        "Current_Control":
            "Defect inspection",

        "Severity":
            9,

        "Occurrence":
            3,

        "Detection":
            4,

        "Recommended_Action":
            "Monitor defect density and perform contamination control"
    }
]


# ============================================================
# CREATE DATAFRAME
# ============================================================

fmea_df = pd.DataFrame(
    fmea_data
)


# ============================================================
# CALCULATE RPN
# ============================================================

fmea_df["RPN"] = (
    fmea_df["Severity"]
    *
    fmea_df["Occurrence"]
    *
    fmea_df["Detection"]
)


# ============================================================
# RISK CLASSIFICATION
# ============================================================

def classify_risk(rpn):

    if rpn >= 200:
        return "HIGH"

    elif rpn >= 100:
        return "MEDIUM"

    else:
        return "LOW"


fmea_df["Risk_Level"] = (
    fmea_df["RPN"]
    .apply(
        classify_risk
    )
)


# ============================================================
# SORT BY RPN
# ============================================================

fmea_df = fmea_df.sort_values(
    "RPN",
    ascending=False
).reset_index(
    drop=True
)


fmea_df["Risk_Rank"] = (
    fmea_df.index + 1
)


# ============================================================
# DISPLAY FMEA
# ============================================================

print("=" * 75)
print("ALD PROCESS FMEA")
print("=" * 75)

print()

print(
    f"Failure modes analyzed : "
    f"{len(fmea_df)}"
)

print()

print("=" * 75)
print("FMEA RISK PRIORITY")
print("=" * 75)

print()

display_columns = [

    "Risk_Rank",

    "Process_Step",

    "Failure_Mode",

    "Severity",

    "Occurrence",

    "Detection",

    "RPN",

    "Risk_Level"
]


print(
    fmea_df[
        display_columns
    ].to_string(
        index=False
    )
)


# ============================================================
# HIGHEST-RISK FAILURE MODE
# ============================================================

highest_risk = fmea_df.iloc[0]


print()
print("=" * 75)
print("HIGHEST-RISK FAILURE MODE")
print("=" * 75)

print()

print(
    f"Failure Mode : "
    f"{highest_risk['Failure_Mode']}"
)

print(
    f"Process Step : "
    f"{highest_risk['Process_Step']}"
)

print(
    f"Severity     : "
    f"{highest_risk['Severity']}"
)

print(
    f"Occurrence   : "
    f"{highest_risk['Occurrence']}"
)

print(
    f"Detection    : "
    f"{highest_risk['Detection']}"
)

print(
    f"RPN          : "
    f"{highest_risk['RPN']}"
)

print(
    f"Risk Level   : "
    f"{highest_risk['Risk_Level']}"
)

print()

print(
    "Recommended Action:"
)

print(
    highest_risk[
        "Recommended_Action"
    ]
)


# ============================================================
# SAVE COMPLETE FMEA
# ============================================================

fmea_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SAVE TOP RISKS
# ============================================================

top_risks = fmea_df.head(
    10
)

top_risks.to_csv(
    RISK_FILE,
    index=False
)


# ============================================================
# RISK SUMMARY
# ============================================================

risk_summary = (
    fmea_df
    .groupby(
        "Risk_Level"
    )
    .size()
    .reset_index(
        name="Failure_Mode_Count"
    )
)


print()
print("=" * 75)
print("RISK LEVEL SUMMARY")
print("=" * 75)

print()

print(
    risk_summary.to_string(
        index=False
    )
)


# ============================================================
# CREATE RPN BAR CHART
# ============================================================

plot_df = fmea_df.head(
    10
).copy()


labels = plot_df[
    "Failure_Mode"
].str.slice(
    0,
    35
)


plt.figure(
    figsize=(12, 7)
)

plt.barh(
    labels,
    plot_df["RPN"]
)

plt.xlabel(
    "Risk Priority Number (RPN)"
)

plt.ylabel(
    "Failure Mode"
)

plt.title(
    "Top 10 ALD Process Failure Modes by RPN"
)

plt.gca().invert_yaxis()

plt.grid(
    axis="x",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    PLOT_FILE,
    dpi=300
)

plt.close()


# ============================================================
# FMEA CONCLUSION
# ============================================================

print()
print("=" * 75)
print("FMEA CONCLUSION")
print("=" * 75)

print()

print(
    "The FMEA identifies precursor delivery, "
    "pulse timing, purge control and film quality "
    "as important process risks."
)

print()

print(
    "The highest-RPN failure modes should receive "
    "priority for process controls and corrective actions."
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("FMEA ANALYSIS COMPLETE")
print("=" * 75)

print()

print(
    "Generated files:"
)

print(
    "  results/FMEA_analysis.csv"
)

print(
    "  results/FMEA_risk_priority.csv"
)

print(
    "  results/FMEA_RPN_chart.png"
)

print("=" * 75)
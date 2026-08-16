# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# STEP 21: PROCESS CONTROL PLAN
# ============================================================

import os
import pandas as pd


# ============================================================
# SETTINGS
# ============================================================

os.makedirs("results", exist_ok=True)

OUTPUT_FILE = (
    "results/ALD_process_control_plan.csv"
)

SUMMARY_FILE = (
    "results/ALD_control_plan_summary.csv"
)


# ============================================================
# CONTROL PLAN
# ============================================================

control_plan = [

    {
        "Control_ID": "CP-01",
        "Process_Stage": "ALD Reactor",
        "Parameter": "Temperature",
        "Target": 200.0,
        "Lower_Limit": 195.0,
        "Upper_Limit": 205.0,
        "Unit": "°C",
        "Measurement_Method": "Temperature sensor / thermocouple",
        "Monitoring_Frequency": "Continuous",
        "Control_Method": "Temperature controller",
        "Alarm_Action": "Stop deposition and investigate heater/control system",
        "Reaction_to_Out_of_Control": "Hold lot, verify temperature sensor and heater, re-qualify if required"
    },

    {
        "Control_ID": "CP-02",
        "Process_Stage": "ALD Reactor",
        "Parameter": "Chamber Pressure",
        "Target": 1.0,
        "Lower_Limit": 0.90,
        "Upper_Limit": 1.10,
        "Unit": "Torr",
        "Measurement_Method": "Pressure gauge / manometer",
        "Monitoring_Frequency": "Continuous",
        "Control_Method": "Pressure controller / throttle valve",
        "Alarm_Action": "Generate pressure alarm",
        "Reaction_to_Out_of_Control": "Hold lot and verify pumping / pressure-control system"
    },

    {
        "Control_ID": "CP-03",
        "Process_Stage": "Precursor Delivery",
        "Parameter": "TMA Pulse",
        "Target": 1.0,
        "Lower_Limit": 0.95,
        "Upper_Limit": 1.05,
        "Unit": "s",
        "Measurement_Method": "Valve timing / precursor delivery monitoring",
        "Monitoring_Frequency": "Every deposition cycle",
        "Control_Method": "Recipe-controlled pulse timing",
        "Alarm_Action": "TMA pulse deviation alarm",
        "Reaction_to_Out_of_Control": "Stop process, inspect TMA valve/delivery system and verify recipe"
    },

    {
        "Control_ID": "CP-04",
        "Process_Stage": "Reactant Delivery",
        "Parameter": "H2O Pulse",
        "Target": 1.0,
        "Lower_Limit": 0.95,
        "Upper_Limit": 1.05,
        "Unit": "s",
        "Measurement_Method": "Valve timing / reactant delivery monitoring",
        "Monitoring_Frequency": "Every deposition cycle",
        "Control_Method": "Recipe-controlled pulse timing",
        "Alarm_Action": "H2O pulse deviation alarm",
        "Reaction_to_Out_of_Control": "Stop process and verify H2O delivery system"
    },

    {
        "Control_ID": "CP-05",
        "Process_Stage": "Purge",
        "Parameter": "Purge Time",
        "Target": 5.0,
        "Lower_Limit": 5.0,
        "Upper_Limit": 10.0,
        "Unit": "s",
        "Measurement_Method": "Recipe timer / valve sequence",
        "Monitoring_Frequency": "Every deposition cycle",
        "Control_Method": "Recipe lock",
        "Alarm_Action": "Prevent cycle execution if purge is below minimum",
        "Reaction_to_Out_of_Control": "Stop process and verify purge sequence before restarting"
    },

    {
        "Control_ID": "CP-06",
        "Process_Stage": "Deposition",
        "Parameter": "Number of ALD Cycles",
        "Target": 100,
        "Lower_Limit": 100,
        "Upper_Limit": 100,
        "Unit": "cycles",
        "Measurement_Method": "Recipe / cycle counter",
        "Monitoring_Frequency": "Every lot",
        "Control_Method": "Recipe lock",
        "Alarm_Action": "Prevent lot completion if cycle count is incorrect",
        "Reaction_to_Out_of_Control": "Hold lot and investigate recipe execution"
    },

    {
        "Control_ID": "CP-07",
        "Process_Stage": "Film Characterization",
        "Parameter": "GPC",
        "Target": 0.100,
        "Lower_Limit": 0.095,
        "Upper_Limit": 0.105,
        "Unit": "nm/cycle",
        "Measurement_Method": "Thickness measurement / XRR",
        "Monitoring_Frequency": "Lot sampling",
        "Control_Method": "SPC control chart",
        "Alarm_Action": "Investigate if GPC crosses control limits",
        "Reaction_to_Out_of_Control": "Hold lot, perform RCA and verify precursor delivery"
    },

    {
        "Control_ID": "CP-08",
        "Process_Stage": "Film Characterization",
        "Parameter": "Film Thickness",
        "Target": 10.0,
        "Lower_Limit": 9.5,
        "Upper_Limit": 10.5,
        "Unit": "nm",
        "Measurement_Method": "XRR / thickness measurement",
        "Monitoring_Frequency": "Lot sampling",
        "Control_Method": "SPC + specification limits",
        "Alarm_Action": "Thickness out-of-control alarm",
        "Reaction_to_Out_of_Control": "Hold lot and investigate process parameters"
    },

    {
        "Control_ID": "CP-09",
        "Process_Stage": "Film Characterization",
        "Parameter": "Thickness Uniformity",
        "Target": 1.0,
        "Lower_Limit": 0.0,
        "Upper_Limit": 2.0,
        "Unit": "%",
        "Measurement_Method": "Multi-point wafer thickness measurement",
        "Monitoring_Frequency": "Lot sampling",
        "Control_Method": "Uniformity trend monitoring",
        "Alarm_Action": "Uniformity limit alarm",
        "Reaction_to_Out_of_Control": "Investigate temperature, pressure and precursor distribution"
    },

    {
        "Control_ID": "CP-10",
        "Process_Stage": "Film Characterization",
        "Parameter": "Film Stress",
        "Target": 50.0,
        "Lower_Limit": -80.0,
        "Upper_Limit": 80.0,
        "Unit": "MPa",
        "Measurement_Method": "Wafer curvature / stress measurement",
        "Monitoring_Frequency": "Lot sampling",
        "Control_Method": "Trend monitoring",
        "Alarm_Action": "Stress specification alarm",
        "Reaction_to_Out_of_Control": "Hold lot and investigate thermal/process conditions"
    },

    {
        "Control_ID": "CP-11",
        "Process_Stage": "Film Characterization",
        "Parameter": "Film Density",
        "Target": 3.0,
        "Lower_Limit": 2.90,
        "Upper_Limit": 3.10,
        "Unit": "g/cm³",
        "Measurement_Method": "XRR",
        "Monitoring_Frequency": "Lot qualification / periodic monitoring",
        "Control_Method": "Density trend monitoring",
        "Alarm_Action": "Density limit alarm",
        "Reaction_to_Out_of_Control": "Investigate precursor/reactant reaction conditions"
    },

    {
        "Control_ID": "CP-12",
        "Process_Stage": "Film Characterization",
        "Parameter": "Surface Roughness",
        "Target": 0.20,
        "Lower_Limit": 0.0,
        "Upper_Limit": 0.30,
        "Unit": "nm RMS",
        "Measurement_Method": "AFM / surface characterization",
        "Monitoring_Frequency": "Periodic qualification",
        "Control_Method": "Roughness trend monitoring",
        "Alarm_Action": "Roughness specification alarm",
        "Reaction_to_Out_of_Control": "Investigate growth conditions and contamination"
    },

    {
        "Control_ID": "CP-13",
        "Process_Stage": "Film Characterization",
        "Parameter": "Defect Density",
        "Target": 5.0,
        "Lower_Limit": 0.0,
        "Upper_Limit": 20.0,
        "Unit": "defects/cm²",
        "Measurement_Method": "Wafer defect inspection",
        "Monitoring_Frequency": "Lot sampling",
        "Control_Method": "Defect trend monitoring",
        "Alarm_Action": "Defectivity alarm",
        "Reaction_to_Out_of_Control": "Hold lot and perform contamination / equipment investigation"
    },

    {
        "Control_ID": "CP-14",
        "Process_Stage": "Film Composition",
        "Parameter": "O/Al Ratio",
        "Target": 1.50,
        "Lower_Limit": 1.35,
        "Upper_Limit": 1.65,
        "Unit": "ratio",
        "Measurement_Method": "XPS",
        "Monitoring_Frequency": "Periodic qualification",
        "Control_Method": "Composition trend monitoring",
        "Alarm_Action": "Composition deviation alarm",
        "Reaction_to_Out_of_Control": "Investigate precursor/reactant balance and surface contamination"
    },

    {
        "Control_ID": "CP-15",
        "Process_Stage": "Film Characterization",
        "Parameter": "Surface Carbon",
        "Target": 0.0,
        "Lower_Limit": 0.0,
        "Upper_Limit": 10.0,
        "Unit": "atomic %",
        "Measurement_Method": "XPS",
        "Monitoring_Frequency": "Periodic qualification",
        "Control_Method": "Contamination trend monitoring",
        "Alarm_Action": "Surface contamination alarm",
        "Reaction_to_Out_of_Control": "Investigate purge efficiency, chamber condition and contamination source"
    }
]


# ============================================================
# CREATE DATAFRAME
# ============================================================

control_df = pd.DataFrame(
    control_plan
)


# ============================================================
# CONTROL PRIORITY
# ============================================================

priority_map = {

    "Continuous": 1,

    "Every deposition cycle": 1,

    "Every lot": 2,

    "Lot sampling": 3,

    "Periodic qualification": 4
}


control_df[
    "Monitoring_Priority"
] = control_df[
    "Monitoring_Frequency"
].map(
    priority_map
)


# ============================================================
# CONTROL CATEGORY
# ============================================================

def classify_control(row):

    if row[
        "Parameter"
    ] in [
        "Temperature",
        "Chamber Pressure",
        "TMA Pulse",
        "H2O Pulse",
        "Purge Time",
        "Number of ALD Cycles"
    ]:

        return "Process Control"

    elif row[
        "Parameter"
    ] in [
        "GPC",
        "Film Thickness",
        "Thickness Uniformity",
        "Film Stress",
        "Film Density",
        "Surface Roughness",
        "Defect Density",
        "O/Al Ratio",
        "Surface Carbon"
    ]:

        return "Product / Film Control"

    else:

        return "Other"


control_df[
    "Control_Category"
] = control_df.apply(
    classify_control,
    axis=1
)


# ============================================================
# DISPLAY CONTROL PLAN
# ============================================================

print("=" * 75)
print("ALD PROCESS CONTROL PLAN")
print("=" * 75)

print()

print(
    f"Control points defined : "
    f"{len(control_df)}"
)

print()

print("=" * 75)
print("KEY PROCESS CONTROLS")
print("=" * 75)

print()

display_columns = [

    "Control_ID",
    "Parameter",
    "Target",
    "Lower_Limit",
    "Upper_Limit",
    "Unit",
    "Monitoring_Frequency",
    "Control_Category"
]

print(
    control_df[
        display_columns
    ].to_string(
        index=False
    )
)


# ============================================================
# CRITICAL CONTROLS
# ============================================================

critical_parameters = [

    "Temperature",
    "Chamber Pressure",
    "TMA Pulse",
    "H2O Pulse",
    "Purge Time",
    "GPC",
    "Film Thickness"
]


critical_df = control_df[
    control_df[
        "Parameter"
    ].isin(
        critical_parameters
    )
].copy()


critical_df[
    "Critical_Control"
] = "YES"


critical_df.to_csv(
    "results/critical_process_controls.csv",
    index=False
)


# ============================================================
# SAVE COMPLETE CONTROL PLAN
# ============================================================

control_df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# CONTROL PLAN SUMMARY
# ============================================================

process_controls = control_df[
    control_df[
        "Control_Category"
    ]
    ==
    "Process Control"
].shape[0]


film_controls = control_df[
    control_df[
        "Control_Category"
    ]
    ==
    "Product / Film Control"
].shape[0]


continuous_controls = control_df[
    control_df[
        "Monitoring_Frequency"
    ]
    ==
    "Continuous"
].shape[0]


cycle_controls = control_df[
    control_df[
        "Monitoring_Frequency"
    ]
    ==
    "Every deposition cycle"
].shape[0]


lot_controls = control_df[
    control_df[
        "Monitoring_Frequency"
    ]
    ==
    "Lot sampling"
].shape[0]


periodic_controls = control_df[
    control_df[
        "Monitoring_Frequency"
    ]
    ==
    "Periodic qualification"
].shape[0]


summary = pd.DataFrame({

    "Metric": [

        "Total Control Points",

        "Process Controls",

        "Product / Film Controls",

        "Continuous Controls",

        "Every Cycle Controls",

        "Lot Sampling Controls",

        "Periodic Qualification Controls"
    ],

    "Count": [

        len(control_df),

        process_controls,

        film_controls,

        continuous_controls,

        cycle_controls,

        lot_controls,

        periodic_controls
    ]
})


summary.to_csv(
    SUMMARY_FILE,
    index=False
)


# ============================================================
# DISPLAY CONTROL RESPONSE LOGIC
# ============================================================

print()
print("=" * 75)
print("CONTROL RESPONSE LOGIC")
print("=" * 75)

print()

print(
    "NORMAL"
)

print(
    "  ↓"
)

print(
    "Continue production"
)

print(
    "  ↓"
)

print(
    "SPC / Process Monitoring"
)

print(
    "  ↓"
)

print(
    "Control limit violation?"
)

print(
    "  ↓"
)

print(
    "YES"
)

print(
    "  ↓"
)

print(
    "Hold affected lot"
)

print(
    "  ↓"
)

print(
    "Verify equipment + recipe + process parameters"
)

print(
    "  ↓"
)

print(
    "Perform RCA"
)

print(
    "  ↓"
)

print(
    "Corrective Action"
)

print(
    "  ↓"
)

print(
    "Verification deposition"
)

print(
    "  ↓"
)

print(
    "Release / Re-qualify"
)


# ============================================================
# FINAL CONTROL PLAN STATUS
# ============================================================

print()
print("=" * 75)
print("CONTROL PLAN STATUS")
print("=" * 75)

print()

print(
    "Process status : QUALIFIED"
)

print(
    "Control strategy : SPC + recipe control + "
    "film characterization"
)

print(
    "Primary critical control : TMA precursor pulse"
)

print(
    "Primary product response : GPC / film thickness"
)

print(
    "Excursion response : Hold lot → RCA → "
    "Corrective Action → Verification"
)


# ============================================================
# FINAL OUTPUT
# ============================================================

print()
print("=" * 75)
print("PROCESS CONTROL PLAN COMPLETE")
print("=" * 75)

print()

print(
    "Generated files:"
)

print(
    "  results/ALD_process_control_plan.csv"
)

print(
    "  results/ALD_control_plan_summary.csv"
)

print(
    "  results/critical_process_controls.csv"
)

print("=" * 75)
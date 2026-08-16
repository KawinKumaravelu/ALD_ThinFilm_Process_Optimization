# ============================================================
# ALD THIN-FILM PROCESS OPTIMIZATION
# ANOVA ANALYSIS
# ============================================================

import os
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols


# ============================================================
# LOAD DOE DATASET
# ============================================================

input_file = "results/DOE_results.csv"

df = pd.read_csv(input_file)


print("=" * 75)
print("ALD PROCESS ANOVA ANALYSIS")
print("=" * 75)

print(
    f"DOE experiments loaded : {len(df)}"
)

print()


# ============================================================
# CREATE RESULTS DIRECTORY
# ============================================================

os.makedirs("results", exist_ok=True)


# ============================================================
# ANOVA FUNCTION
# ============================================================

def perform_anova(response, output_name):

    print("=" * 75)

    print(
        f"ANOVA FOR {response}"
    )

    print("-" * 75)


    # --------------------------------------------------------
    # Build statistical model
    # --------------------------------------------------------

    model = ols(
        f"{response} ~ "
        "C(Temperature_C) + "
        "C(Pressure_Torr) + "
        "C(TMA_Pulse_s) + "
        "C(H2O_Pulse_s) + "
        "C(Purge_s)",
        data=df
    ).fit()


    # --------------------------------------------------------
    # Generate ANOVA table
    # --------------------------------------------------------

    anova_table = sm.stats.anova_lm(
        model,
        typ=2
    )


    # --------------------------------------------------------
    # Calculate percentage contribution
    # --------------------------------------------------------

    ss_total = anova_table["sum_sq"].sum()

    anova_table["Contribution_%"] = (
        anova_table["sum_sq"]
        / ss_total
        * 100
    )


    # --------------------------------------------------------
    # Display ANOVA table
    # --------------------------------------------------------

    print(
        anova_table.to_string()
    )

    print()


    # --------------------------------------------------------
    # Save ANOVA table
    # --------------------------------------------------------

    output_file = (
        f"results/{output_name}.csv"
    )

    anova_table.to_csv(
        output_file
    )


    print(
        f"ANOVA results saved to: {output_file}"
    )

    print()


    # --------------------------------------------------------
    # Rank factors by contribution
    # --------------------------------------------------------

    factor_rows = anova_table[
        anova_table.index != "Residual"
    ].copy()


    factor_rows = factor_rows.sort_values(
        by="Contribution_%",
        ascending=False
    )


    print(
        "FACTOR IMPORTANCE"
    )

    print("-" * 75)


    for rank, (factor, row) in enumerate(
        factor_rows.iterrows(),
        start=1
    ):

        factor_name = (
            factor
            .replace("C(", "")
            .replace(")", "")
        )

        print(
            f"{rank}. "
            f"{factor_name:<20} "
            f"{row['Contribution_%']:.2f}%"
        )


    print()

    return model, anova_table


# ============================================================
# ANOVA FOR GPC
# ============================================================

gpc_model, gpc_anova = perform_anova(
    "GPC_nm_per_cycle",
    "ANOVA_GPC"
)


# ============================================================
# ANOVA FOR FILM THICKNESS
# ============================================================

thickness_model, thickness_anova = perform_anova(
    "Film_Thickness_nm",
    "ANOVA_Thickness"
)


# ============================================================
# ANOVA FOR CYCLE TIME
# ============================================================

cycle_model, cycle_anova = perform_anova(
    "Cycle_Time_s",
    "ANOVA_Cycle_Time"
)


# ============================================================
# ANOVA FOR THROUGHPUT
# ============================================================

throughput_model, throughput_anova = perform_anova(
    "Relative_Throughput_cycles_per_hour",
    "ANOVA_Throughput"
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("=" * 75)
print("ANOVA ANALYSIS COMPLETE")
print("=" * 75)

print()
print("Generated files:")
print()
print("  results/ANOVA_GPC.csv")
print("  results/ANOVA_Thickness.csv")
print("  results/ANOVA_Cycle_Time.csv")
print("  results/ANOVA_Throughput.csv")

print()
print("=" * 75)
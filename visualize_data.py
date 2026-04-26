#!/usr/bin/env python3
"""
Visualization script για τα preprocessing outputs.

Δημιουργεί charts για:
1. Time series για ordered_qty και ship_qty ανά μήνα (συνολικά)
2. Top 10 προϊόντα με το μεγαλύτερο volume
3. Correlation heatmap για rolling features
4. Train/Test split visualization
5. Distribution plots

Outputs: Αποθηκεύονται στο ./charts/ directory ως PNG files
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Ελληνικά fonts (optional, αλλιώς θα δείχνει τετραγωνάκια)
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial"]
plt.rcParams["axes.unicode_minus"] = False

# Style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)


def plot_monthly_totals(df: pd.DataFrame, outdir: Path) -> None:
    """Plot συνολικών ordered_qty και ship_qty ανά μήνα."""
    monthly = df.groupby("month")[["ordered_qty", "ship_qty"]].sum().reset_index()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(
        monthly["month"],
        monthly["ordered_qty"],
        marker="o",
        label="Ordered Quantity",
        linewidth=2,
    )
    ax.plot(
        monthly["month"],
        monthly["ship_qty"],
        marker="s",
        label="Shipped Quantity",
        linewidth=2,
        alpha=0.7,
    )

    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Quantity", fontsize=12)
    ax.set_title(
        "Monthly Totals: Ordered vs Shipped Quantity", fontsize=14, fontweight="bold"
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out_path = outdir / "01_monthly_totals.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out_path}")


def plot_top_products(df: pd.DataFrame, outdir: Path, top_n: int = 10) -> None:
    """Plot top N προϊόντων με το μεγαλύτερο συνολικό ordered_qty."""
    product_totals = (
        df.groupby("product_id")["ordered_qty"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette("viridis", len(product_totals))
    product_totals.plot(kind="barh", ax=ax, color=colors)

    ax.set_xlabel("Total Ordered Quantity", fontsize=12)
    ax.set_ylabel("Product ID", fontsize=12)
    ax.set_title(
        f"Top {top_n} Products by Total Ordered Quantity",
        fontsize=14,
        fontweight="bold",
    )
    ax.invert_yaxis()
    plt.tight_layout()

    out_path = outdir / f"02_top{top_n}_products.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out_path}")


def plot_correlation_heatmap(df: pd.DataFrame, outdir: Path) -> None:
    """Correlation heatmap για rolling features και target."""
    # Επιλογή numeric columns που σχετίζονται με rolling features
    cols_of_interest = [
        c
        for c in df.columns
        if "roll" in c or c in ["ordered_qty", "ordered_lag1", "ship_qty"]
    ]

    if len(cols_of_interest) < 2:
        print("⚠ Not enough rolling features for correlation heatmap. Skipping...")
        return

    corr = df[cols_of_interest].corr()

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )

    ax.set_title(
        "Correlation Heatmap: Rolling Features & Target", fontsize=14, fontweight="bold"
    )
    plt.tight_layout()

    out_path = outdir / "03_correlation_heatmap.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out_path}")


def plot_train_test_split(
    train: pd.DataFrame, test: pd.DataFrame, outdir: Path
) -> None:
    """Visualization του train/test split."""
    train_monthly = train.groupby("month")["ordered_qty"].sum().reset_index()
    test_monthly = test.groupby("month")["ordered_qty"].sum().reset_index()

    fig, ax = plt.subplots(figsize=(14, 6))
    ax.plot(
        train_monthly["month"],
        train_monthly["ordered_qty"],
        marker="o",
        label="Train Set",
        linewidth=2,
        color="#2E86AB",
    )
    ax.plot(
        test_monthly["month"],
        test_monthly["ordered_qty"],
        marker="s",
        label="Test Set",
        linewidth=2,
        color="#A23B72",
    )

    # Vertical line για split point
    if len(train_monthly) > 0 and len(test_monthly) > 0:
        split_point = train_monthly["month"].max()
        ax.axvline(
            x=split_point,
            color="red",
            linestyle="--",
            linewidth=2,
            alpha=0.7,
            label="Train/Test Split",
        )

    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Total Ordered Quantity", fontsize=12)
    ax.set_title("Train/Test Split Visualization", fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out_path = outdir / "04_train_test_split.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out_path}")


def plot_distribution(df: pd.DataFrame, outdir: Path) -> None:
    """Distribution plots για ordered_qty (log scale)."""
    # Remove zeros for log scale
    df_nonzero = df[df["ordered_qty"] > 0].copy()

    if len(df_nonzero) == 0:
        print("⚠ No non-zero ordered_qty values. Skipping distribution plot...")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Histogram
    axes[0].hist(
        df_nonzero["ordered_qty"],
        bins=50,
        color="skyblue",
        edgecolor="black",
        alpha=0.7,
    )
    axes[0].set_xlabel("Ordered Quantity", fontsize=11)
    axes[0].set_ylabel("Frequency", fontsize=11)
    axes[0].set_title(
        "Distribution of Ordered Quantity (Non-Zero)", fontsize=12, fontweight="bold"
    )
    axes[0].grid(True, alpha=0.3)

    # Log scale histogram
    axes[1].hist(
        df_nonzero["ordered_qty"], bins=50, color="coral", edgecolor="black", alpha=0.7
    )
    axes[1].set_xlabel("Ordered Quantity (Log Scale)", fontsize=11)
    axes[1].set_ylabel("Frequency", fontsize=11)
    axes[1].set_title(
        "Distribution of Ordered Quantity (Log Scale)", fontsize=12, fontweight="bold"
    )
    axes[1].set_yscale("log")
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    out_path = outdir / "05_distribution.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out_path}")


def plot_product_time_series(
    df: pd.DataFrame, outdir: Path, product_ids: list = None, max_products: int = 5
) -> None:
    """Time series για συγκεκριμένα προϊόντα."""
    if product_ids is None:
        # Επιλογή top products by total ordered_qty
        top_products = (
            df.groupby("product_id")["ordered_qty"]
            .sum()
            .nlargest(max_products)
            .index.tolist()
        )
    else:
        top_products = product_ids

    fig, ax = plt.subplots(figsize=(14, 6))

    for pid in top_products:
        prod_data = df[df["product_id"] == pid].sort_values("month")
        ax.plot(
            prod_data["month"],
            prod_data["ordered_qty"],
            marker="o",
            label=f"Product {pid}",
            linewidth=2,
        )

    ax.set_xlabel("Month", fontsize=12)
    ax.set_ylabel("Ordered Quantity", fontsize=12)
    ax.set_title(
        f"Time Series for Top {len(top_products)} Products",
        fontsize=14,
        fontweight="bold",
    )
    ax.legend(fontsize=10, loc="best")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    out_path = outdir / "06_product_time_series.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate visualization charts for preprocessing outputs"
    )
    parser.add_argument(
        "--train_csv",
        type=str,
        default="output/train_item_month_2017_2019_cutoff_2019-04_with_roll.csv",
    )
    parser.add_argument(
        "--test_csv",
        type=str,
        default="output/test_item_month_2017_2019_start_2019-05_with_roll.csv",
    )
    parser.add_argument(
        "--full_csv", type=str, default="output/item_month_agg_2017_2019_with_roll.csv"
    )
    parser.add_argument("--outdir", type=str, default="charts")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Sales Data Visualization Generator")
    print("=" * 60)

    # Load data
    print(f"\n📊 Loading data from {args.full_csv}...")
    full_df = pd.read_csv(args.full_csv, parse_dates=["month"])

    print(f"📊 Loading train data from {args.train_csv}...")
    train_df = pd.read_csv(args.train_csv, parse_dates=["month"])

    print(f"📊 Loading test data from {args.test_csv}...")
    test_df = pd.read_csv(args.test_csv, parse_dates=["month"])

    print(f"\n✓ Loaded {len(full_df):,} rows from full dataset")
    print(f"✓ Loaded {len(train_df):,} rows from train set")
    print(f"✓ Loaded {len(test_df):,} rows from test set")

    # Generate charts
    print(f"\n📈 Generating charts in {outdir.absolute()}...\n")

    plot_monthly_totals(full_df, outdir)
    plot_top_products(full_df, outdir, top_n=10)
    plot_correlation_heatmap(full_df, outdir)
    plot_train_test_split(train_df, test_df, outdir)
    plot_distribution(full_df, outdir)
    plot_product_time_series(full_df, outdir, max_products=5)

    print("\n" + "=" * 60)
    print(f"✅ All charts saved successfully in: {outdir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()

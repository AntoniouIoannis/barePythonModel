#!/usr/bin/env python3
"""
Wrapper script για εκτέλεση preprocessing με file picker.

Τρέξε αυτό το αρχείο και θα ανοίξουν file dialogs για να επιλέξεις:
1. Sales 2017.xlsx
2. Sales 2018.xlsx
3. Sales 2019.xlsx

Τα outputs θα αποθηκευτούν στο ./output directory.
Τα charts θα αποθηκευτούν στο ./charts directory.
"""

import subprocess
import sys
from pathlib import Path


def main():
    print("=" * 60)
    print("Sales Data Preprocessing - File Picker Mode")
    print("=" * 60)
    print("\nΘα ανοίξουν 3 file dialogs.")
    print("Επέλεξε τα αρχεία με τη σειρά:")
    print("  1. Sales 2017.xlsx")
    print("  2. Sales 2018.xlsx")
    print("  3. Sales 2019.xlsx")
    print("\nΠάτησε Enter για να ξεκινήσεις...")
    input()

    # Δημιουργία output directories
    output_dir = Path("./output")
    output_dir.mkdir(exist_ok=True)

    charts_dir = Path("./charts")
    charts_dir.mkdir(exist_ok=True)

    # Εκτέλεση του preprocess_sales.py χωρίς arguments (θα ζητήσει file picker)
    cmd_preprocess = [
        sys.executable,
        "preprocess_sales.py",
        "--outdir",
        str(output_dir),
        "--train_end",
        "2019-04-01",
        "--test_start",
        "2019-05-01",
    ]

    print("\n📊 ΒΗΜΑ 1/2: Preprocessing δεδομένων...")
    print(f"Εκτέλεση: {' '.join(cmd_preprocess)}\n")
    result = subprocess.run(cmd_preprocess)

    if result.returncode != 0:
        print("\n" + "=" * 60)
        print("✗ Preprocessing απέτυχε. Έλεγξε τα μηνύματα πιο πάνω.")
        print("=" * 60)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("✓ Preprocessing ολοκληρώθηκε επιτυχώς!")
    print(f"✓ Τα αρχεία αποθηκεύτηκαν στο: {output_dir.absolute()}")
    print("=" * 60)

    # Εκτέλεση του visualization script
    cmd_visualize = [
        sys.executable,
        "visualize_data.py",
        "--train_csv",
        str(output_dir / "train_item_month_2017_2019_cutoff_2019-04_with_roll.csv"),
        "--test_csv",
        str(output_dir / "test_item_month_2017_2019_start_2019-05_with_roll.csv"),
        "--full_csv",
        str(output_dir / "item_month_agg_2017_2019_with_roll.csv"),
        "--outdir",
        str(charts_dir),
    ]

    print("\n📈 ΒΗΜΑ 2/2: Δημιουργία visualizations...")
    print(f"Εκτέλεση: {' '.join(cmd_visualize)}\n")
    result = subprocess.run(cmd_visualize)

    if result.returncode != 0:
        print("\n" + "=" * 60)
        print("⚠ Visualization απέτυχε, αλλά τα δεδομένα έχουν επεξεργαστεί επιτυχώς.")
        print("=" * 60)
        sys.exit(0)

    print("\n" + "=" * 60)
    print("✅ Όλα ολοκληρώθηκαν επιτυχώς!")
    print(f"📊 Data outputs: {output_dir.absolute()}")
    print(f"📈 Charts: {charts_dir.absolute()}")
    print("=" * 60)


if __name__ == "__main__":
    main()

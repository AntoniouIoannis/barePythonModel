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

import shutil
import subprocess
import sys
from pathlib import Path


def cleanup_workspace():
    """Διαγράφει τα περιεχόμενα των output και charts φακέλων καθώς και τα csv αρχεία στο root."""
    print("\n🧹 Καθαρισμός φακέλου εργασίας...")

    # 1. Καθαρισμός φακέλων output και charts
    for folder_name in ["output", "charts"]:
        folder = Path(folder_name)
        if folder.exists() and folder.is_dir():
            print(f"   Διαγραφή περιεχομένων: {folder_name}/")
            for item in folder.iterdir():
                try:
                    if item.is_file():
                        item.unlink()
                    elif item.is_dir():
                        shutil.rmtree(item)
                except Exception as e:
                    print(f"   ⚠️ Σφάλμα στη διαγραφή {item}: {e}")
        else:
            folder.mkdir(exist_ok=True)

    # 2. Διαγραφή .csv αρχείων στο root (εκτός αν είναι σημαντικά αρχεία ρυθμίσεων)
    root_path = Path(".")
    for csv_file in root_path.glob("*.csv"):
        try:
            print(f"   Διαγραφή αρχείου: {csv_file.name}")
            csv_file.unlink()
        except Exception as e:
            print(f"   ⚠️ Σφάλμα στη διαγραφή {csv_file}: {e}")

    print("✨ Ο καθαρισμός ολοκληρώθηκε.\n")


def get_environment_info():
    """Επιστρέφει πληροφορίες για Python version και virtual environment."""
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )

    # Έλεγχος αν τρέχει σε virtual environment
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )

    venv_path = sys.prefix if in_venv else "None"
    venv_name = Path(venv_path).name if in_venv else "System Python"

    return {
        "version": python_version,
        "in_venv": in_venv,
        "venv_name": venv_name,
        "venv_path": venv_path,
    }


def main():
    env_info = get_environment_info()

    print("=" * 60)
    print("Sales Data Preprocessing - File Picker Mode")
    print("=" * 60)
    print(f"\n🐍 Python Version: {env_info['version']}")
    print(f"📦 Virtual Environment: {env_info['venv_name']}")
    if env_info["in_venv"]:
        print(f"   Path: {env_info['venv_path']}")
    print("=" * 60)

    # Καθαρισμός πριν την έναρξη
    cleanup_workspace()

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
    print("=" * 60)
    print(f"📊 Data outputs: {output_dir.absolute()}")
    print(f"📈 Charts: {charts_dir.absolute()}")
    print("-" * 60)
    print(f"🐍 Python: {env_info['version']} | Venv: {env_info['venv_name']}")
    print("=" * 60)


if __name__ == "__main__":
    main()

# 📊 Sales Data Preprocessing & Visualization

Αυτό το project επεξεργάζεται sales data από Excel files και δημιουργεί visualizations.

## 🚀 Γρήγορη Εκκίνηση

### 1️⃣ Εγκατάσταση Dependencies

```bash
pip install -r requirements.txt
```

**Τι εγκαθίσταται:**
- `pandas` - Επεξεργασία δεδομένων
- `numpy` - Αριθμητικοί υπολογισμοί
- `openpyxl` - Ανάγνωση Excel files
- `scikit-learn` - Machine learning models
- `matplotlib` - Δημιουργία charts
- `seaborn` - Advanced visualizations

### 2️⃣ Εκτέλεση με File Picker (Εύκολος Τρόπος)

```bash
python run_with_file_picker.py
```

**Τι κάνει:**
1. Ανοίγει file dialog για να επιλέξεις `sales 2017.xlsx`
2. Ανοίγει file dialog για να επιλέξεις `sales 2018.xlsx`
3. Ανοίγει file dialog για να επιλέξεις `sales 2019.xlsx`
4. Επεξεργάζεται τα δεδομένα
5. Δημιουργεί visualizations

**Outputs:**
- `./output/` - Επεξεργασμένα CSV files (με 3 δεκαδικά)
- `./charts/` - PNG charts για visualization

### 3️⃣ Εκτέλεση με Command Line Arguments (Προχωρημένοι)

```bash
python preprocess_sales.py \
  --sales2017 "C:\path\to\sales 2017.xlsx" \
  --sales2018 "C:\path\to\sales 2018.xlsx" \
  --sales2019 "C:\path\to\sales 2019.xlsx" \
  --outdir "./output"
```

Μετά δημιούργησε charts:

```bash
python visualize_data.py --outdir "./charts"
```

---

## 📁 Output Files

### Data Files (στο `./output/`)

1. **`sales_transactions_2017_2019.csv.gz`** 🗜️
   - **Τι είναι:** Συμπιεσμένο CSV με όλες τις transaction-level γραμμές
   - **Γιατί .gz:** Εξοικονομεί χώρο (compressed με gzip)
   - **Πώς να το ανοίξω:** `pd.read_csv('file.csv.gz')` ή 7-Zip/WinRAR

2. **`item_month_agg_2017_2019.csv`**
   - Aggregated δεδομένα ανά product-month (observed only)

3. **`item_month_agg_2017_2019_with_roll.csv`**
   - Full panel με rolling features (lag1, rolling means, std)

4. **`train_item_month_2017_2019_cutoff_2019-04_with_roll.csv`**
   - Training set (2017-01 έως 2019-04)

5. **`test_item_month_2017_2019_start_2019-05_with_roll.csv`**
   - Test set (2019-05 και μετά)

**Όλα τα numeric columns έχουν 3 δεκαδικά ψηφία** (π.χ. `123.456`)

### Chart Files (στο `./charts/`)

1. **`01_monthly_totals.png`**
   - Time series: Συνολικές ποσότητες ανά μήνα (Ordered vs Shipped)

2. **`02_top10_products.png`**
   - Bar chart: Top 10 προϊόντα με το μεγαλύτερο volume

3. **`03_correlation_heatmap.png`**
   - Heatmap: Correlations μεταξύ rolling features και target

4. **`04_train_test_split.png`**
   - Visualization του train/test split

5. **`05_distribution.png`**
   - Histograms: Distribution του ordered_qty (normal & log scale)

6. **`06_product_time_series.png`**
   - Time series: Top 5 προϊόντα μέσα στο χρόνο

---

## 🔧 Advanced Usage

### Τρέξε μόνο το Preprocessing (χωρίς charts)

```bash
python preprocess_sales.py
```

### Τρέξε μόνο τα Charts (αν έχεις ήδη data)

```bash
python visualize_data.py
```

### Άλλαξε το Train/Test Split

```bash
python preprocess_sales.py --train_end "2019-03-01" --test_start "2019-04-01"
```

### Άλλαξε Rolling Windows

```bash
python preprocess_sales.py --windows 6 12 24
```

---

## 📊 Data Pipeline

```
Excel Files (2017, 2018, 2019)
    ↓
[File Picker / CLI Args]
    ↓
Read & Standardize
    ↓
Transaction-level Data
    ↓
Aggregate to Product-Month
    ↓
Complete Panel (fill missing months)
    ↓
Rolling Features (no leakage)
    ↓
Train/Test Split
    ↓
Save to CSV (3 decimals) → ./output/
    ↓
Generate Charts → ./charts/
```

---

## ❓ FAQ

### Γιατί υπάρχει .gz αρχείο;

Το `sales_transactions_2017_2019.csv.gz` είναι **compressed** για να εξοικονομήσει χώρο. Τα transaction-level data είναι συνήθως πολύ μεγάλα. Μπορείς να το ανοίξεις κανονικά με pandas ή να το decompress με 7-Zip.

### Πώς μπορώ να δω τα .gz δεδομένα;

```python
import pandas as pd
df = pd.read_csv('sales_transactions_2017_2019.csv.gz')
print(df.head())
```

### Μπορώ να επιλέξω αρχεία από διαφορετικούς δίσκους;

**Ναι!** Το file picker σε αφήνει να πας οπουδήποτε - `C:\`, `D:\`, network drives, Downloads, όπου θέλεις.

### Πώς κάνω update τα requirements;

```bash
pip install -r requirements.txt --upgrade
```

---

## 📝 Notes

- **Python Version:** 3.10.11 (recommended)
- **Numeric Format:** Όλα τα outputs έχουν 3 δεκαδικά (`.3f`)
- **Leakage Control:** Rolling features χρησιμοποιούν lag1 (no future data)
- **Train/Test:** Chronological split (default: train έως 2019-04, test από 2019-05)

---

**Καλή επιτυχία! 🚀**

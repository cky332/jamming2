"""
Build the SQLite DB from the real CSV files, bypassing Git LFS.

The checked-in mimic_iii.db / eicu.db are Git LFS objects; if `git lfs pull` is
unavailable (e.g. the code was copied without a .git dir, or the LFS object
isn't hosted), SQLInterpreter/Calendar fail with "file is not a database".
The CSVs are plain files and are always present, so we reconstruct the DB.

    python build_db_from_csv.py                  # mimic_iii (default)
    python build_db_from_csv.py --dataset eicu   # eICU

Each CSV becomes a table named after the file (lowercased), matching the
table names used by the agent's tools and example queries.
"""

import os
import glob
import time
import sqlite3
import argparse
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))

# dataset -> (csv subdir, db filename)
DATASETS = {
    "mimic_iii": ("mimic_iii", "mimic_iii.db"),
    "eicu": ("eicu", "eicu.db"),
}


def build(dataset):
    subdir, db_name = DATASETS[dataset]
    csv_dir = os.path.join(HERE, subdir)
    db_path = os.path.join(csv_dir, db_name)
    csvs = sorted(glob.glob(os.path.join(csv_dir, "*.csv")))
    if not csvs:
        raise SystemExit(f"No CSV files found in {csv_dir}")

    if os.path.exists(db_path):
        os.remove(db_path)

    con = sqlite3.connect(db_path)
    t0 = time.time()
    for path in csvs:
        table = os.path.splitext(os.path.basename(path))[0].lower()
        df = pd.read_csv(path)
        df.to_sql(table, con, if_exists="replace", index=False)
        print(f"  {table:24s} <- {os.path.basename(path)} ({len(df)} rows)")
    con.commit()
    con.close()
    print(f"\nBuilt {db_path} ({os.path.getsize(db_path) // 1024 // 1024} MB) in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--dataset", choices=list(DATASETS), default="mimic_iii")
    args = p.parse_args()
    build(args.dataset)


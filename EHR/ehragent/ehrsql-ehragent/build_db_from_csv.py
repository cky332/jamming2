"""
Build mimic_iii.db from the real CSV files, bypassing Git LFS.

The checked-in mimic_iii.db is a Git LFS object; if `git lfs pull` is
unavailable (e.g. the code was copied without a .git dir, or the LFS object
isn't hosted), SQLInterpreter/Calendar fail with "file is not a database".
The CSVs in mimic_iii/ are plain files and are always present, so we can
reconstruct the SQLite DB from them.

    python build_db_from_csv.py

Each CSV becomes a table named after the file (lowercased), matching the
table names used by the agent's tools and example queries (patients,
admissions, diagnoses_icd, ...).
"""

import os
import glob
import sqlite3
import time
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CSV_DIR = os.path.join(HERE, "mimic_iii")
DB_PATH = os.path.join(CSV_DIR, "mimic_iii.db")


def looks_like_lfs_pointer(path):
    if not os.path.exists(path) or os.path.getsize(path) > 1000:
        return False
    with open(path, "rb") as f:
        return f.read(40).startswith(b"version https://git-lfs")


def build():
    csvs = sorted(glob.glob(os.path.join(CSV_DIR, "*.csv")))
    if not csvs:
        raise SystemExit(f"No CSV files found in {CSV_DIR}")

    if os.path.exists(DB_PATH):
        # Only the LFS stub or a previously-built DB should live here; remove it.
        os.remove(DB_PATH)

    con = sqlite3.connect(DB_PATH)
    t0 = time.time()
    for path in csvs:
        table = os.path.splitext(os.path.basename(path))[0].lower()
        df = pd.read_csv(path)
        df.to_sql(table, con, if_exists="replace", index=False)
        print(f"  {table:24s} <- {os.path.basename(path)} ({len(df)} rows)")
    con.commit()
    con.close()
    print(f"\nBuilt {DB_PATH} ({os.path.getsize(DB_PATH) // 1024 // 1024} MB) in {time.time()-t0:.1f}s")


if __name__ == "__main__":
    build()

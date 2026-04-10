"""
Run this file first to check if your DB is connected and working.
    python test_db.py
"""
import sys

# ── 1. Check mariadb is installed ────────────────────────────
try:
    import mariadb
except ImportError:
    print("ERROR: mariadb library not installed.")
    print("  Run:  pip install mariadb")
    sys.exit(1)

# ── 2. Try connecting ────────────────────────────────────────
from config import DB_CONFIG, get_conn

print("Connecting to MariaDB...")
try:
    conn = get_conn()
    print("  Connected!")
except mariadb.Error as e:
    print(f"  FAILED: {e}")
    print("\nCheck:")
    print("  • MariaDB is running (open XAMPP or HeidiSQL)")
    print("  • config.py has the right user/password")
    sys.exit(1)

# ── 3. Check database exists ─────────────────────────────────
cur = conn.cursor()
cur.execute("SELECT DATABASE()")
db = cur.fetchone()[0]
print(f"  Database: {db}")

# ── 4. Check all tables exist ────────────────────────────────
required = ["students","team","team_member","advisers","panelists",
            "projects","project_adviser","project_panelist","project_files"]

cur.execute("SHOW TABLES")
existing = [r[0] for r in cur.fetchall()]

print("\nChecking tables:")
all_ok = True
for tbl in required:
    ok = tbl in existing
    print(f"  {'OK' if ok else 'MISSING'}  {tbl}")
    if not ok: all_ok = False

# ── 5. Check row counts ──────────────────────────────────────
if all_ok:
    print("\nRow counts:")
    for tbl in ["students","advisers","projects","team"]:
        cur.execute(f"SELECT COUNT(*) FROM {tbl}")
        print(f"  {tbl}: {cur.fetchone()[0]} rows")

conn.close()

if all_ok:
    print("\nAll good! You can now run:  python main.py")
else:
    print("\nSome tables are missing. Run setup_db.sql first (see README).")

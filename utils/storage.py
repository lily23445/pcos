
import json, os, pandas as pd
from pathlib import Path

DATA_DIR = Path("user_data")          # ← turn it into a Path object
DATA_DIR.mkdir(exist_ok=True)
# ── helper --------------------------------------------------------------
def _user_dir(email: str) -> Path:
    user_dir = DATA_DIR / email       # now Path / str works
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir

# ── PROFILE CRUD --------------------------------------------------------
def save_profile(email, data):
    """Save user profile into user_data/{email}/profile.json"""
    user_dir = _user_dir(email)
    filepath = user_dir / "profile.json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)


def load_profile(email: str) -> dict:
    """Load the profile dict; return empty dict if missing or invalid."""
    p = _user_dir(email) / "profile.json"

    # Ensure user folder exists
    p.parent.mkdir(parents=True, exist_ok=True)

    if not p.exists():
        return {}

    try:
        return json.loads(p.read_text())
    except json.JSONDecodeError:
        # If file exists but is empty or broken
        return {}
    except Exception as e:
        print(f"Error reading profile for {email}: {e}")
        return {}

# ---------- daily log ----------
import pandas as pd
from pathlib import Path

def append_weekly(entry, email):
    print("DEBUG:", type(entry), type(email))
    # 1.  Build user-specific folder path
    user_dir = Path("user_data") / email
    user_dir.mkdir(parents=True, exist_ok=True)

    # 2.  CSV file that stores the weekly log
    csv_file = user_dir / "weekly_log.csv"

    # 3.  Load existing data or start fresh
    if csv_file.exists():
        df = pd.read_csv(csv_file)
    else:
        df = pd.DataFrame()

    # 4.  Ensure we’re working with a DataFrame row
    week_col = "WeekOf"  # must be in entry dict
    new_row = pd.DataFrame([entry])

    if week_col in df.columns and entry[week_col] in df[week_col].values:
        # Update existing row safely
        idx = df.index[df[week_col] == entry[week_col]][0]
        for col in new_row.columns:
            df.at[idx, col] = entry[col]
    else:
        # Append as new row
        df = pd.concat([df, new_row], ignore_index=True)

    # 5.  Save back to CSV
    df.to_csv(csv_file, index=False)



def read_weekly(email):
    user_dir = Path("user_data") / email
    csv_file = user_dir / "weekly_log.csv"

    if csv_file.exists():
        return pd.read_csv(csv_file)
    else:
        return pd.DataFrame() 


def reset_user(email: str) -> None:
    """Delete profile.json and daily_log.csv for a single user."""
    for f in (_user_dir(email) / "profile.json", _user_dir(email) / "daily_log.csv"):
        if f.exists():
            f.unlink()

def reset_all() -> None:
    """Delete every file under user_data/ (use with care!)."""
    for p in DATA_DIR.rglob("*"):
        if p.is_file():
            p.unlink()

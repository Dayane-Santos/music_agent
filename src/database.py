import sqlite3
import pandas as pd
import glob
import os

def get_db_connection():
    """Loads the CSVs into memory."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    csv_files = glob.glob("data/*.csv")
    
    for file_path in csv_files:
        base_name = os.path.basename(file_path).replace(".csv", "")
        table_name = base_name.replace("desafio_tecnico_ai_eng - ", "").strip()
        
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]
        df.to_sql(table_name, conn, index=False, if_exists="replace")
        
    return conn
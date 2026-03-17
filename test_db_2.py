import traceback
from sqlalchemy import create_engine

# The new URL includes hostaddr to bypass DNS while preserving the exact SNI host for Neon
url = "postgresql+psycopg2://neondb_owner:npg_28qVFELvsNlX@ep-weathered-cell-ai1016n1-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require&hostaddr=98.91.36.187"

try:
    engine = create_engine(url)
    conn = engine.connect()
    print("DB connected OK to Neon via hostaddr!")
    conn.close()
except Exception as e:
    traceback.print_exc()

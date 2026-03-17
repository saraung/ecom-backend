import traceback
try:
    from app.core.database import engine
    conn = engine.connect()
    print("DB connected OK")
    conn.close()
except Exception as e:
    traceback.print_exc()

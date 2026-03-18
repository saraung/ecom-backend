import sys
try:
    from app.core.database import engine
    conn = engine.connect()
    print("DB connected OK")
    conn.close()
except Exception as e:
    with open("err.txt", "w") as f:
        f.write(str(getattr(e, 'orig', e)))

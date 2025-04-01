import psycopg

try:
    conn = psycopg.connect("postgresql://aria_user:aria_password@localhost:6024/aria_db")
    print("✅ Connected using localhost!")
    conn.close()
except Exception as e:
    print("❌ Localhost failed:")
    print(e)

try:
    conn = psycopg.connect("postgresql://aria_user:aria_password@127.0.0.1:6024/aria_db")
    print("✅ Connected using 127.0.0.1!")
    conn.close()
except Exception as e:
    print("❌ 127.0.0.1 failed:")
    print(e)


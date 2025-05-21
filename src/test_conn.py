import psycopg2

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="K@siet,bakyt123",
    host="db.homjbtgwrphodegiswaf.supabase.co",
    port="5432",
    sslmode="require"
)

cur = conn.cursor()
cur.execute("SELECT 1;")
print(cur.fetchone())
cur.close()
conn.close()

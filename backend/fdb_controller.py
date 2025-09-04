import fdb

db_path = "./firebird-data/test.fdb"
con = fdb.connect(database=db_path, user="SYSDBA", password="MySecretPassword")
cur = con.cursor()

with open("./data/source_scripts/firebird_source_schema.sql") as f:
    statements = f.read().split(";")

for stmt in statements:
    stmt = stmt.strip()
    if stmt:
        # Skip CREATE TABLE if it exists
        if stmt.upper().startswith("CREATE TABLE"):
            table_name = stmt.split()[2].upper()
            exists = cur.execute(
                f"SELECT COUNT(*) FROM RDB$RELATIONS WHERE RDB$RELATION_NAME='{table_name}'"
            ).fetchone()[0]
            if exists:
                continue  # skip table creation
        cur.execute(stmt)
        # Commit immediately after DDL
        if stmt.upper().startswith("CREATE TABLE"):
            con.commit()

con.commit()
con.close()

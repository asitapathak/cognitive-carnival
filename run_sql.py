import duckdb

con = duckdb.connect()
for query in open("queries.sql").read().split(";"):
    if query.strip():
        result = con.sql(query)
        if result is not None:
            print(result.df(), "\n")
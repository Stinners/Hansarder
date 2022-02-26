from psycopg_pool import ConnectionPool

import os
import sys

def get_connection_info() -> str:
    env = os.getenv("ENV")
    if env == "PROD":
        dbmate_connection_string = os.getenv("PROD_DATABASE_URL")
    elif env == "TEST":
        dbmate_connection_string = os.getenv("TEST_DATABASE_URL")
    else:
        dbmate_connection_string = os.getenv("DATABASE_URL")

    if dbmate_connection_string == None:
        print("Please set the \"DATABASE_URL\" environment variable")
        sys.exit(1)

    # Split of the connection parameters which are just useful for bdmate

    regular_connection_string = dbmate_connection_string.split("?")[0]
    return regular_connection_string


# Get a connetion pool
# We should really create a single connection pool and only use that 
def get_db() -> ConnectionPool:
    conninfo = get_connection_info()
    return ConnectionPool(conninfo)

from psycopg_pool import ConnectionPool
import os


connection_url = os.getenv("CONNECTION_URL")
self.pool = ConnectionPool(connection_url)
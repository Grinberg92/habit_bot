from psycopg_pool import ConnectionPool

from config.config import settings


pool = ConnectionPool(
        f"host={settings.POSTGRES_HOST} "
        f"port={settings.POSTGRES_PORT} "
        f"dbname={settings.POSTGRES_DB} "
        f"user={settings.POSTGRES_USER} "
        f"password={settings.POSTGRES_PASSWORD} ",
        max_size=10,
        min_size=1
                )


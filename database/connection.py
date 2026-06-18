from psycopg_pool import AsyncConnectionPool

from config.config import db_settings


pool = AsyncConnectionPool(
        conninfo=
        f"host={db_settings.POSTGRES_HOST} "
        f"port={db_settings.POSTGRES_PORT} "
        f"dbname={db_settings.POSTGRES_DB} "
        f"user={db_settings.POSTGRES_USER} "
        f"password={db_settings.POSTGRES_PASSWORD} ",
        max_size=10,
        min_size=1,
        open=False
                )



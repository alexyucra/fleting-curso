
DEFAULT_EXCLUDED_TABLES = {
    "_fleting_migrations",
    "migrations",
    "schema_migrations",
    "alembic_version",
    "sqlite_sequence",
    "flyway_schema_history",
}

def is_internal_table(table_name: str) -> bool:

    return (
        table_name.startswith("_")
        or table_name.startswith("sys_")
        or table_name.startswith("tmp_")
    )

def should_generate_model(table_name: str, config_excludes=None) -> bool:

    config_excludes = set(config_excludes or [])

    if table_name in DEFAULT_EXCLUDED_TABLES:
        return False

    if table_name in config_excludes:
        return False

    if is_internal_table(table_name):
        return False

    return True
 

# core/orm.py
class ForeignKey:
    def __init__(self, table: str, local: str, remote: str = "id"):
        self.table = table
        self.local = local
        self.remote = remote

    def resolve(self, cursor, value):
        cursor.execute(
            f"SELECT * FROM {self.table} WHERE {self.remote} = ?",
            (value,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None

    def __repr__(self):
        return f"<ForeignKey {self.local} → {self.table}.{self.remote}>"

class HasMany:
    def __init__(self, table: str, foreign_key: str):
        self.table = table
        self.foreign_key = foreign_key

    def resolve(self, cursor, value):
        cursor.execute(
            f"SELECT * FROM {self.table} WHERE {self.foreign_key} = ?",
            (value,)
        )
        return [dict(r) for r in cursor.fetchall()]

    def __repr__(self):
        return f"<HasMany {self.table} via {self.foreign_key}>"

 
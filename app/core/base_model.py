
# core/base_model.py
from core.database import get_connection
from core.orm import ForeignKey, HasMany
from typing import Any

class QuerySet:

    def __init__(self, model, relations=None):
        self.model = model
        self.relations = relations or []
    
    def _cursor(self):
        conn = get_connection()
        conn.row_factory = lambda c, r: dict(
            zip([col[0] for col in c.description], r)
        )
        return conn, conn.cursor()

    def all(self):
        conn, cursor = self._cursor()

        cursor.execute(
            f"SELECT * FROM {self.model.table_name}"
        )
        rows = cursor.fetchall()

        return self._attach_relations(cursor, rows)
    
    def first(self):
        conn, cursor = self._cursor()
        cursor.execute(
            f"SELECT * FROM {self.model.table_name} LIMIT 1"
        )
        row = cursor.fetchone()
        if not row:
            return None
        return self._attach_relations(cursor, [row])[0]

    def find(self, id):
        conn, cursor = self._cursor()

        cursor.execute(
            f"SELECT * FROM {self.model.table_name} WHERE id = ?",
            (id,)
        )
        row = cursor.fetchone()

        if not row:
            return None

        return self._attach_relations(cursor, [row])[0]

    def where(self, **filters):
        conn, cursor = self._cursor()

        keys = filters.keys()
        values = tuple(filters.values())
        cond = " AND ".join(f"{k}=?" for k in keys)

        cursor.execute(
            f"SELECT * FROM {self.model.table_name} WHERE {cond}",
            values
        )

        rows = cursor.fetchall()
        return self._attach_relations(cursor, rows)
    
    def count(self):
        conn, cursor = self._cursor()
        cursor.execute(
            f"SELECT COUNT(*) as total FROM {self.model.table_name}"
        )
        return cursor.fetchone()["total"]
    
    def exists(self, **filters):
        return len(self.where(**filters)) > 0
    
    # =========================
    # Relations
    # =========================

    def _attach_relations(self, cursor, rows):
        if not self.relations:
            return rows

        for row in rows:
            for rel_name in self.relations:
                rel = getattr(self.model, rel_name, None)

                if isinstance(rel, ForeignKey):
                    value = row.get(rel.local)
                    row[rel_name] = rel.resolve(cursor, value)

                elif isinstance(rel, HasMany):
                    value = row.get("id")
                    row[rel_name] = rel.resolve(cursor, value)

        return rows

class BaseModel:
    table_name: str
    # ---------- Query ----------
    @classmethod
    def with_(cls, *relations):
        return QuerySet(cls, relations)

    @classmethod
    def all(cls):
        return cls.with_().all()
    
    @classmethod
    def first(cls):
        return cls.with_().first()

    @classmethod
    def find(cls, id):
        return cls.with_().find(id)

    @classmethod
    def where(cls, **filters):
        return cls.with_().where(**filters)
    
    @classmethod
    def count(cls):
        return cls.with_().count()
    
    @classmethod
    def exists(cls, **filters):
        return cls.with_().exists(**filters)

    # ---------- Write ----------
    @classmethod
    def create(cls, **data):
        conn = get_connection()
        cursor = conn.cursor()

        keys = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        values = tuple(data.values())

        cursor.execute(
            f"INSERT INTO {cls.table_name} ({keys}) VALUES ({placeholders})",
            values
        )
        conn.commit()

        return cls.find(cursor.lastrowid)

    def to_dict(self):
        return {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_")
        }

    def save(self):
        data = self.__dict__.copy()

        if "id" in data and data["id"]:
            self.update(**data)
        else:
            obj = self.__class__.create(**data)
            self.id = obj["id"]

        return self

    def update(self, **data):
        conn = get_connection()
        cursor = conn.cursor()

        if "id" not in data:
            raise ValueError("Update requires id")

        id = data.pop("id")
        assigns = ", ".join(f"{k}=?" for k in data)
        values = tuple(data.values()) + (id,)

        cursor.execute(
            f"UPDATE {self.table_name} SET {assigns} WHERE id = ?",
            values
        )
        conn.commit()
        return self

    def delete(self):
        if not getattr(self, "id", None):
            raise ValueError("Delete requires id")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"DELETE FROM {self.table_name} WHERE id = ?",
            (self.id,)
        )
        conn.commit()
 
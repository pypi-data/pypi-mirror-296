from tinydb import TinyDB, Query
from uuid import uuid4


def default_key_gen() -> str:
    return str(uuid4())


class Table:
    def __init__(
        self, db: TinyDB, table: str, primary_key: str = None, key_gen: callable = None
    ) -> None:
        self.table = db.table(table)
        self.primary_key = f"{table}_id" if primary_key is None else primary_key
        self.key_gen = default_key_gen if key_gen is None else key_gen
        self.search = Query()

    def all(self) -> dict:
        return self.table.all()

    def insert(self, item: dict, id: str = None) -> str:
        id = self.key_gen() if id is None else id
        item[self.primary_key] = id
        self.table.insert(item)
        return id

    def update(self, id: str, item: dict) -> str:
        found = self.find(id)
        self.table.update(item, doc_ids=[found.doc_id])
        return id

    def delete(self, id: str) -> str:
        found = self.find(id)
        self.table.remove(doc_ids=[found.doc_id])
        return id

    def find(self, id: str) -> str:
        return self.table.get(self.search[self.primary_key] == id)

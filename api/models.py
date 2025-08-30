from google.cloud import firestore
from pydantic import BaseModel
from typing import List

class Item(BaseModel):
    item_type: str
    description: str

class Meal(BaseModel):
    id: str
    campus: str
    supplier: str
    meal_type: str
    date: str
    items: List[Item]

    @classmethod
    def from_firestore(cls, doc: firestore.DocumentSnapshot) -> "Meal | None":
        if not doc.exists:
            return None
        data = doc.to_dict() or {}
        if 'id' in data:
            del data['id']
        return cls(id=doc.id, **data)
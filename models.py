from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Book:
    book_id : str
    title : str
    author : str
    year : str
    book_lend_member_id : Optional[str] = None # Optional property, not necessary to create an object

    def is_available(self) -> bool:
        return self.book_lend_member_id is None # Returning True/False if book_lend_member_id exists

@dataclass
class Member:
    member_id : str
    name : str

@dataclass
class Loan:
    loan_id : str
    member_id : str
    book_id : str
    borrowed_at : datetime
    returned_at : Optional[datetime] = None

    def is_active(self) -> bool:
        return self.returned_at is None

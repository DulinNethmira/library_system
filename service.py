from dataclasses import dataclass
from datetime import datetime
from repositories import BookRepository, MemberRepository, LoanRepository
from models import Book, Member, Loan

class LibraryError(Exception):
    pass

@dataclass
class LibraryService:
    book: BookRepository
    member: MemberRepository  #Instance Variables
    loan: LoanRepository

    def add_books(self, book_id: str, title:str, author:str, year:str) -> Book:
        if self.book.get_by_id(book_id) is not None:
            raise LibraryError(f"Book already exists with book ID : {book_id}") # Exception message

        book = Book(book_id=book_id, title=title, author=author, year=year) # Book Object creation
        self.book.add(book)
        return book

    def register_member(self, member_id: str, name: str) -> Member:
        if self.member.get_member_by_id(member_id) is not None:
            raise LibraryError(f"Member already exists with member ID : {member_id}")

        member = Member(member_id, name)
        self.member.add(member)
        return member

    def list_all_books(self):
        return self.book.list_all_books()

    def list_all_members(self):
        return self.member.list_all_members()

    def borrow_books(self, loan_id: str, member_id: str, book_id:str):
        if self.book.get_by_id(book_id) is None:
            raise LibraryError("Book not found")

        if self.member.get_member_by_id(member_id) is None:
            raise LibraryError("Member not found")

        if not self.book.get_by_id(book_id).is_available():
            raise LibraryError("Book not available!")

        loan = Loan(loan_id, member_id, book_id, datetime.now())
        book = self.book.get_by_id(book_id)
        book.book_lend_member_id = member_id
        self.book.update(book)

        self.loan.add(loan)
        return loan

    def return_book(self, loan_id: str) -> Loan:
        loan = self.loan.get_by_id(loan_id)

        if loan is None:
            raise LibraryError("Loan doesn't exists")

        if loan.is_active():
            raise LibraryError("Loan not available!")

        book = self.book.get_by_id(loan.book_id)
        book.book_lend_member_id = None
        self.book.update(book)

        loan.returned_at = datetime.now()
        self.loan.update(loan)
        return loan

    def list_all_loans(self):
        return [loan for loan in self.loan.list_all_loans() if loan.is_active()]

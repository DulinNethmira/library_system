from abc import ABC, abstractmethod
from typing import List, Dict
from models import Book, Member, Loan
from datetime import datetime


class BookRepository(ABC):
    @abstractmethod
    def add(self, book: Book) -> None:
       pass

    @abstractmethod
    def get_by_id(self, book_id:str) -> Book:
        pass

    @abstractmethod
    def update(self, book:Book) -> None:
        pass

    @abstractmethod
    def list_all_books(self) -> List[Book]:
        pass


class MemberRepository(ABC):
    @abstractmethod
    def add(self, member: Member) -> None:
        pass

    @abstractmethod
    def get_member_by_id(self, member_id:str) -> Member:
        pass

    @abstractmethod
    def list_all_members(self) -> List[Member]:
        pass


class LoanRepository(ABC):
    @abstractmethod
    def add(self, loan: Loan) -> None:
       pass

    @abstractmethod
    def get_by_id(self, loan_id:str) -> Loan:
        pass

    @abstractmethod
    def update(self, loan:Loan) -> None:
        pass

    @abstractmethod
    def list_all_loans(self) -> List[Loan]:
        pass


class InMemoryBookRepository(BookRepository):
    def __init__(self):
        self.__book: Dict[str, Book] = {}

    def add(self, book: Book) -> None:
       self.__book[book.book_id] = book

    def get_by_id(self, book_id:str) -> Book:
        return self.__book.get(book_id)

    def update(self, book:Book) -> None:
        self.__book[book.book_id] = book

    def list_all_books(self) -> List[Book]:
        return list(self.__book.values())


class InMemoryMemberRepository(MemberRepository):
    def __init__(self):
        self.__member: Dict[str, Member] = {}

    def add(self, member: Member) -> None:
        self.__member[member.member_id] = member

    def get_member_by_id(self, member_id:str) -> Member:
        return self.__member.get(member_id)

    def list_all_members(self) -> List[Member]:
        return list(self.__member.values())


class InMemoryLoanRepository(LoanRepository):
    def __init__(self):
        self.__loan: Dict[str, Loan] = {}

    def add(self, loan: Loan) -> None:
       self.__loan[loan.loan_id] = loan

    def get_by_id(self, loan_id:str) -> Loan:
        return self.__loan.get(loan_id)

    def update(self, loan:Loan) -> None:
        self.__loan[loan.loan_id] = loan

    def list_all_loans(self) -> List[Loan]:
        return list(self.__loan.values())


class TextFileBookRepository(BookRepository):

    def __init__(self, filename: str = "books_data.txt"):
        self.filename = filename

    def save_books(self, books: Dict[str, Book]):
        with open(self.filename, "w") as f:
            for book in books.values():
                f.write(f"{book.book_id}|{book.title}|{book.author}|{book.year}|{book.book_lend_member_id}\n")
            # 001 | Sevens | Dulin | 2025 | None

    def load_books(self) -> Dict[str, Book]:
        books = {}
        with open(self.filename, "r") as f:
            for book_line in f:
                # book_id, title, author, year, book_lend_id = book_line.split("|")
                book_line = book_line.strip()
                data = book_line.split("|")
                if len(data) == 5:
                    book_id, title, author, year, book_lend_id = data #Value unpacking
                    books[book_id] = Book(book_id,
                                          title,
                                          author,
                                          year,
                                          book_lend_id if "None" not in book_lend_id else None)
        return books


    def add(self, book: Book) -> None:
        books = self.load_books()
        books[book.book_id] = book
        self.save_books(books)

    def get_by_id(self, book_id: str) -> Book:
        books = self.load_books()
        return books.get(book_id)

    def update(self, book: Book) -> None:
        books = self.load_books()
        books[book.book_id] = book
        self.save_books(books)

    def list_all_books(self) -> List[Book]:
        books = self.load_books()
        return list(books.values())

class TextFileMemberRepository(MemberRepository):

    def __init__(self, filename: str = "members_data.txt"):
        self.filename = filename

    def save_members(self, members: Dict[str, Member]):
        with open(self.filename, "w") as f:
            for member in members.values():
                f.write(f"{member.member_id}|{member.name}\n")

    def load_members(self) -> Dict[str, Member]:
        members = {}
        with open(self.filename, "r") as f:
            for member_line in f:
                member_line = member_line.strip()
                data = member_line.split("|")
                if len(data) == 2:
                    member_id, name = data
                    members[member_id] = Member(member_id,
                                                name)
        return members

    def add(self, member: Member) -> None:
        members = self.load_members()
        members[member.member_id] = member
        self.save_members(members)

    def get_member_by_id(self, member_id: str) -> Member:
        members = self.load_members()
        return members.get(member_id)

    def list_all_members(self) -> List[Member]:
        members = self.load_members()
        return list(members.values())

class TextFileLoanRepository(LoanRepository):

    def __init__(self, filename: str = "loans_data.txt"):
        self.filename = filename

    def save_loans(self, loans: Dict[str, Loan]):
        with open(self.filename, "w") as f:
            for loan in loans.values():
                f.write(f"{loan.loan_id}|{loan.member_id}|{loan.book_id}|{loan.borrowed_at}|{loan.returned_at}\n")
    def load_loans(self) -> Dict[str, Loan]:
        loans = {}
        with open(self.filename, "r") as f:
            for loan_lines in f:
                loan_lines = loan_lines.strip()
                data = loan_lines.split("|")
                if len(data) == 5:
                    loan_id, member_id, book_id, borrowed_at, returned_at = data
                    borrowed_at = datetime.fromisoformat(borrowed_at)
                    if "None" in returned_at:
                        returned_at = None
                    else:
                        returned_at = datetime.fromisoformat(returned_at)
                    loans[loan_id] = Loan(loan_id,
                                          member_id,
                                          book_id,
                                          borrowed_at,
                                          returned_at
                                          )
        return loans

    def add(self, loan: Loan) -> None:
        loans = self.load_loans()
        loans[loan.loan_id] = loan
        self.save_loans(loans)

    def get_by_id(self, loan_id: str) -> Loan:
        loans = self.load_loans()
        return loans.get(loan_id)

    def update(self, loan: Loan) -> None:
        loans = self.load_loans()
        loans[loan.loan_id] = loan
        self.save_loans(loans)

    def list_all_loans(self) -> List[Loan]:
        loans = self.load_loans()
        return list(loans.values())


if __name__ == '__main__':
    text_book_repository = TextFileBookRepository()

    books = {"001" : Book("001" , "Sevens" , "Dulin" , "2025"),
             "002" : Book("002" , "Madolduwa" , "Martin W." , "1950"),
             "003" : Book("003" , "blablaba" , "dasdaa" , "1950")}

    text_book_repository.save_books(books)
    text_book_repository.load_books()


    text_member_repository = TextFileMemberRepository()

    members = {"001" : Member("001" , "Dulin Nethmira"),
               "002" : Member("002" , "Sanjana Isuranga"),
               "003" : Member("003" , "Inoka Thushari")}

    text_member_repository.save_members(members)
    text_member_repository.load_members()


    text_loan_repository = TextFileLoanRepository()

    loans = {"001" : Loan("001" , "001" , "001" , datetime.now()),
             "002" : Loan("002" , "002" , "002" , datetime.now() , datetime.now()),
             "003" : Loan("003" , "003" , "003" , datetime.now())}

    text_loan_repository.save_loans(loans)
    text_loan_repository.load_loans()
import time
from repositories import InMemoryLoanRepository, InMemoryMemberRepository, TextFileBookRepository
from service import LibraryService, LibraryError

library_service = LibraryService(book=TextFileBookRepository(),
                                 member=InMemoryMemberRepository(),
                                 loan=InMemoryLoanRepository()
                                 )

def add_book():
    book_id = input("Enter book ID : ")
    book_title = input("Enter book title : ")
    book_author = input("Enter book author : ")
    book_year = input("Enter book's year : ")

    try:
        library_service.add_books(book_id, book_title, book_author, book_year)
        print("Book successfully added!")
    except LibraryError as e:
        print("Error : ", e)

    time.sleep(2)

def register_member():
    member_id = input("Enter member ID : ")
    name = input("Enter member name : ")

    try:
        library_service.register_member(member_id, name)
        print("Member successfully registered!")
    except LibraryError as e:
        print("Error : ",e)

    time.sleep(2)

def list_books():
    books = library_service.list_all_books()

    for book in books:
        status = "Available" if book.is_available() else f"Out by: {book.book_lend_member_id}"
        print("Please wait...")
        time.sleep(2)
        print(f"\nBook ID - {book.book_id}\n"
              f"Title - {book.title}\n"
              f"Author - {book.author}\n"
              f"Year - {book.year}\n"
              f"Status - {status}")
    time.sleep(2)

def list_members():
    members = library_service.list_all_members()

    for member in members:
        print(f"\nMembers ID - {member.member_id}\n"
              f"Name - {member.name}")
    time.sleep(2)

def borrow_book():
    loan_id = input("Enter loan ID - ")
    member_id = input("Enter member ID - ")
    book_id = input("Enter book ID - ")

    try:
        library_service.borrow_books(loan_id, member_id, book_id)
        print("Book successfully borrowed!")
    except LibraryError as e:
        print("Error : ",e)

    time.sleep(2)

def return_book():
    loan_id = input("Enter loan ID - ")

    try:
        library_service.return_book(loan_id)
        print("Book successfully returned.\nThank you & Come again!!")
    except LibraryError as e:
        print("Error : ",e)

    time.sleep(3)

def list_loans():
    loans = library_service.list_all_loans()

    for loan in loans:
        print(f"Loan ID - {loan.member_id}"
              f"Borrowed by - {loan.member_id}")
    time.sleep(2)

while True:
    print("\n<---------- Library System ---------->")
    print(
        """
        1) Press 1 to Add Books
        2) Press 2 to Register Members
        3) Press 3 to list all books
        4) Press 4 to list all members
        5) Press 5 to borrow books
        6) Press 6 to return books
        7) Press 7 to list all loans
        8) Press 0 to exit
        """
    )
    print("<------------------------------------>")
    choice = int(input("Enter your choice : "))

    if choice == 1:
        add_book()

    if choice == 2:
        register_member()

    if choice == 3:
        list_books()

    if choice == 4:
        list_members()

    if choice == 5:
        borrow_book()

    if choice == 6:
        return_book()

    if choice == 7:
        list_loans()

    if choice == 0:
        print("Please come again!!!")
        quit()
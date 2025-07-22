# Create a program using multiple functions to solve a larger problem — for example, a simple library management system with functions to add books, search for a book, and display the inventory. Ensure each functionality is handled by a separate function and is called from a main program.

books = []

def add_book():
    book_name = input("Enter the book details (name, author, year) separated by commas: ")
    books.append(book_name)

def search_book():
    book_name = input("Enter the book name: ")
    for book in books:
        if book_name in book:
            print(book)


input_book_name = input("add or search book: ")
while input_book_name != "done":
    if input_book_name == "add":
        add_book()
    elif input_book_name == "search":
        search_book()
    else:
        print("Invalid input")
    input_book_name = input("add or search book: ")









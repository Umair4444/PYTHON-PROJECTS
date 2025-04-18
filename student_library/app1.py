import json
import streamlit as st

class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "books.json"
        self.read_from_file()
    
    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []
    
    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)
    
    def add_book(self, title, author, year, genre, read):
        new_book = {"title": title, "author": author, "year": year, "genre": genre, "read": read}
        self.book_list.append(new_book)
        self.save_to_file()
    
    def delete_book(self, title):
        self.book_list = [book for book in self.book_list if book["title"].lower() != title.lower()]
        self.save_to_file()
    
    def find_books(self, search_text):
        return [book for book in self.book_list if search_text.lower() in book["title"].lower() or search_text.lower() in book["author"].lower()]
    
    def update_book(self, title, new_data):
        for book in self.book_list:
            if book["title"].lower() == title.lower():
                book.update(new_data)
                self.save_to_file()
                return True
        return False
    
    def get_all_books(self):
        return self.book_list
    
    def get_reading_progress(self):
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        return total_books, (completed_books / total_books * 100) if total_books > 0 else 0

book_manager = BookCollection()

st.title("📚 Book Collection Manager")

menu = ["Add Book", "View Books", "Search Book", "Update Book", "Delete Book", "Reading Progress"]
choice = st.sidebar.selectbox("Select an action", menu)

if choice == "Add Book":
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.text_input("Publication Year")
    genre = st.text_input("Genre")
    read = st.checkbox("Have you read this book?")
    if st.button("Add Book"):
        book_manager.add_book(title, author, year, genre, read)
        st.success("Book added successfully!")

elif choice == "View Books":
    st.subheader("All Books")
    books = book_manager.get_all_books()
    if books:
        for book in books:
            st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        st.info("No books found.")

elif choice == "Search Book":
    st.subheader("Search for a Book")
    search_text = st.text_input("Enter title or author name")
    if st.button("Search"):
        results = book_manager.find_books(search_text)
        if results:
            for book in results:
                st.write(f"**{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
        else:
            st.warning("No matching books found.")

elif choice == "Update Book":
    st.subheader("Update a Book")
    title = st.text_input("Enter the title of the book to update")
    new_title = st.text_input("New Title", "")
    new_author = st.text_input("New Author", "")
    new_year = st.text_input("New Year", "")
    new_genre = st.text_input("New Genre", "")
    new_read = st.checkbox("Mark as Read")
    if st.button("Update Book"):
        updated = book_manager.update_book(title, {
            "title": new_title or title,
            "author": new_author or None,
            "year": new_year or None,
            "genre": new_genre or None,
            "read": new_read
        })
        if updated:
            st.success("Book updated successfully!")
        else:
            st.warning("Book not found!")

elif choice == "Delete Book":
    st.subheader("Delete a Book")
    title = st.text_input("Enter the title of the book to delete")
    if st.button("Delete Book"):
        book_manager.delete_book(title)
        st.success("Book deleted successfully!")

elif choice == "Reading Progress":
    st.subheader("Reading Progress")
    total, progress = book_manager.get_reading_progress()
    st.write(f"Total books: {total}")
    st.write(f"Reading Progress: {progress:.2f}%")

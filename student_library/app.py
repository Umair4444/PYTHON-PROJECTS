import streamlit as st
import json
import os

# Define the JSON file for persistent storage
BOOKS_DATA = "books.json"

# Function to load books from the JSON file
def load_books():
    if os.path.exists(BOOKS_DATA):
        with open(BOOKS_DATA, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    else:
        return []

# Function to save books to the JSON file
def save_books(books):
    with open(BOOKS_DATA, "w") as file:
        json.dump(books, file, indent=4)

# Initialize session state for books if not already done
if "books" not in st.session_state:
    st.session_state.books = load_books()

# Function to view all books
def view_books():
    st.subheader("Books Collection")
    books = st.session_state.books
    if not books:
        st.info("Your library is empty.")
    else:
        for index, book in enumerate(books, 1):
            status = "Read" if book.get("read", False) else "Unread"
            st.write(f"**{index}. {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")

# Function to add a new book
def add_book():
    st.subheader("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author", value="Unknown")
    year = st.text_input("Publication Year", value="Not Specific")
    genre = st.text_input("Genre", value="Other")
    read_input = st.selectbox("Have you read the book?", ["No", "Yes"])
    
    if st.button("Add Book"):
        new_book = {
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read": True if read_input.lower() in ["yes", "y"] else False,
        }
        st.session_state.books.append(new_book)
        save_books(st.session_state.books)
        st.success("Book added successfully!")

# Function to delete a book
def delete_book():
    st.subheader("Delete a Book")
    books = st.session_state.books
    if not books:
        st.info("No books to delete.")
        return
    
    # Let the user choose a book by title
    titles = [book["title"] for book in books]
    selected_title = st.selectbox("Select book to delete", titles)
    if st.button("Delete Book"):
        st.session_state.books = [book for book in books if book["title"] != selected_title]
        save_books(st.session_state.books)
        st.success(f"Book '{selected_title}' deleted successfully!")

# Function to update a book
def update_book():
    st.subheader("Update Book Details")
    books = st.session_state.books
    if not books:
        st.info("No books available to update.")
        return

    titles = [book["title"] for book in books]
    selected_title = st.selectbox("Select book to update", titles)
    book = next((b for b in books if b["title"] == selected_title), None)
    if book:
        st.write("Leave field blank to keep the existing value.")
        new_title = st.text_input(f"New title (current: {book['title']})", value=book["title"])
        new_author = st.text_input(f"New author (current: {book['author']})", value=book["author"])
        new_year = st.text_input(f"New publication year (current: {book['year']})", value=book["year"])
        new_genre = st.text_input(f"New genre (current: {book['genre']})", value=book["genre"])
        new_read = st.selectbox("Have you read the book?", ["No", "Yes"], index=1 if book.get("read", False) else 0)
        
        if st.button("Update Book"):
            # Update the fields (if user input is provided, otherwise keep the existing value)
            book["title"] = new_title or book["title"]
            book["author"] = new_author or book["author"]
            book["year"] = new_year or book["year"]
            book["genre"] = new_genre or book["genre"]
            book["read"] = True if new_read.lower() in ["yes", "y"] else False
            save_books(st.session_state.books)
            st.success("Book updated successfully!")
    else:
        st.error("Selected book not found.")

# Function to search for books
def search_books():
    st.subheader("Search Books")
    search_type = st.radio("Search by", ("Title", "Author"))
    search_term = st.text_input("Enter search term").lower()
    if st.button("Search"):
        if not search_term:
            st.error("Please enter a search term.")
            return
        results = [
            book for book in st.session_state.books 
            if (search_term in book["title"].lower() if search_type == "Title" else search_term in book["author"].lower())
        ]
        if results:
            st.write("Matching Books:")
            for index, book in enumerate(results, 1):
                status = "Read" if book.get("read", False) else "Unread"
                st.write(f"**{index}. {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
        else:
            st.info("No matching books found.")

# Function to show reading progress
def show_reading_progress():
    st.subheader("Reading Progress")
    total_books = len(st.session_state.books)
    completed_books = sum(1 for book in st.session_state.books if book.get("read", False))
    completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0

    st.write(f"**Total books in collection:** {total_books}")
    st.write(f"**Books read:** {completed_books}")
    st.write(f"**Reading progress:** {completion_rate:.2f}%")
    
    if total_books > 0:
        unread_books = [book["title"] for book in st.session_state.books if not book.get("read", False)]
        if unread_books:
            st.write("**Books to Read:**")
            for title in unread_books:
                st.write(f"- {title}")

# Sidebar menu for navigation
menu = st.sidebar.radio("Select an Option", 
                          ["View Books", "Add Book", "Delete Book", "Update Book", "Search Books", "Reading Progress"])

if menu == "View Books":
    view_books()
elif menu == "Add Book":
    add_book()
elif menu == "Delete Book":
    delete_book()
elif menu == "Update Book":
    update_book()
elif menu == "Search Books":
    search_books()
elif menu == "Reading Progress":
    show_reading_progress()

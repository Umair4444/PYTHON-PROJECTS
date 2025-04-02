# import streamlit as st
# import json

# # student file in a variable for storage
# BOOKS_DATA = "books.json"


# #function to load books

# def load_books():
#     try:
#         with open(BOOKS_DATA, "r") as file:
#             return json.load(file)
#     # error handling 
#     except (FileNotFoundError, json.JSONDecodeError):
#         return []
    
# # Function to save books

# def save_books(books_list):
#     with open(BOOKS_DATA,"w") as file:
#         json.dump(books_list,file,indent=4)

# # Initialize session state for books
# if "books_list" not in st.session_state:
#     st.session_state.books_list = load_books()

# st.title("Student Library Manager")
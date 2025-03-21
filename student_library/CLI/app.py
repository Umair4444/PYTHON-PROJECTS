import json

class StudentLibrary:
    def __init__(self):
        self.books_list = []
        self.books_data = "books.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.books_data,"r") as file:
                self.books_list = json.load(file)
        except:
            self.books_list = []

    def save_to_file(self):
        with open(self.books_data,"w") as file:
            json.dump(self.books_list,file,indent=4)
        
    def create_new_book(self):
        book_title = input("Enter book title: ")
        book_author = input("Enter author: ") or "Unknown"
        publication_year = input("Enter publication year: ") or "Not Specific"
        book_genre = input("Enter genre: ") or "Other"
        # have_read = input("Have you read the book : (yes/no)").strip().lower() == ["yes","y"]
        have_read = input("Have you read the book : (yes/no) ").strip().lower() in ["yes","y"]

        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": have_read,
        }

        self.books_list.append(new_book)
        self.save_to_file()
        print("Book added successfully!\n")

    def delete_book(self):
        book_title = input("Enter the title of the book to remove: ")

        for book in self.books_list:
            if book["title"].lower() == book_title.lower():
                self.books_list.remove(book)
                self.save_to_file()
                print("Book removed successfully!\n")
                return
        print("Book not found!\n")

    # 5
    def show_all_books(self):
        if not self.books_list:
            print("Book not found\n") 
            return

        print("Books Collection")
        for index,book in enumerate(self.books_list,1):
            reading_status = "Read" if book["read"] else "Unread"
            print(
                f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
            )
        print()

    def find_book(self):
        search_type = input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
        search_text = input("Enter search term: ").lower()

        found_books = [book for book in self.books_list if search_text in book["title"].lower() or search_text in book["author"].lower()]
        # found_books =  for books in self.books_list:
        #             if search_text in book["title"].lower():
        #                 book
        #             elif search_text in book["author"].lower():
        #               book 
        
        if found_books:
            print("Matching Books:")
            for index, book in enumerate(found_books, 1):
                reading_status = "Read" if book["read"] else "Unread"
                print(
                    f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
                )
        else:
            print("No matching books found.\n")

    def update_book(self):
        book_title = input("Enter the title of the book you want to edit: ")
        for book in self.books_list:
            if book["title"].lower() == book_title.lower():
                print("Leave blank to keep existing value.")
                book["title"] = input(f"New title ({book['title']}): ") or book["title"]
                book["author"] = (
                    input(f"New author ({book['author']}): ") or book["author"]
                )
                book["year"] = input(f"New year ({book['year']}): ") or book["year"]
                book["genre"] = input(f"New genre ({book['genre']}): ") or book["genre"]
                book["read"] = (
                    input("Have you read this book? (yes/no): ").strip().lower()
                    in ["yes","y"]
                )
                self.save_to_file()
                print("Book updated successfully!\n")
                return
        print("Book not found!\n")

    def show_reading_progress(self):
        total_books = len(self.books_list)
        completed_books = sum(1 for book in self.books_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0
        # (if total_books > 0:
        #     (completed_books / total_books * 100)  
        # else:
        #     0)
        
        print(f"Total books in collection: {total_books} and I you have read {completed_books}")
        print(f"Reading progress: {completion_rate:.2f}%\n")


    def start_application(self):
        """Run the main application loop with a user-friendly menu interface."""
        while True:
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Remove a book")
            print("3. Search for books")
            print("4. Update book details")
            print("5. View all books")
            print("6. View reading progress")
            print("7. Exit")
            user_choice = input("Please choose an option (1-7): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.save_to_file()
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    book_manager = StudentLibrary()
    book_manager.start_application()
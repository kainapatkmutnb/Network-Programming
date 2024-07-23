import json

# Initial list of books
books = ['book1', 'book2', 'book3']

# Convert list to JSON string
json_books = json.dumps(books)
print(json_books)  # This will print the JSON string

# Check the type of the JSON string
print(type(json_books))  # This should print <class 'str'>

# JSON string
books_string = '["book1", "book2", "book3"]'

# Convert JSON string back to list
book_list = json.loads(books_string)
print(book_list)  # This will print the list
print(type(book_list))  # This should print <class 'list'>

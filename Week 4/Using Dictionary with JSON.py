import json

books = {'A':'Book1', 'B': 'Book2', 'C': 'Book3'}
print(type(books))

print(books['A'])
print(books['B'])
print(books['C'])
#print(books['D'])

print(json.dumps(books))

books_json = json.dumps(books)
print(books_json)
json.loads(books_json)
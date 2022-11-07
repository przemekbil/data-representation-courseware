import consume_api as books_api

books = books_api.getAllBooks()

total = 0
count = 0

for book in books:
    total += book["Price"]
    count += 1

print("Average of {} books is {}".format(count, total/count))
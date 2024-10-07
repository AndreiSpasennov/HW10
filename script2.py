import Library
my_books = []
my_books.append(Book("Tree", "Bob", 1990, 150, True))
my_books.append(Book("House", "Ann", 2000, 500, True))
my_books.append(Book("Orange", "Mike", 1800, 100, False))
for i in my_books:
    print(i.title, i.author, i.year, i.price, i.stoplist)

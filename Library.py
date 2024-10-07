class Book:
    def __init__(self, t, a, y, p, s):
        self.title = t
        self.author = a
        self.year = y
        self.price = p
        self.stoplist = s
    def get_info(self):
        print(self.author, self.title, self.year, self.list, self.stoplist)
    def get_pr(self):
        return (self.price)
    def most_exp_book(book_list):
        exp_book = book_list[0]
        max_pr = book_list[0].get_pr
        for book in book_list:
            price = book.get_pr
            if price > max_pr:
                max_pr = price
                exp_book = book
        return exp_book
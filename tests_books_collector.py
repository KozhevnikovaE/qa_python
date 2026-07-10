import pytest

from main import BooksCollector

class TestBooksCollector:

    @pytest.mark.parametrize("book_names, expected_count", [
        (['Гордость и предубеждение и зомби', 'Что делать, если ваш кот хочет вас убить'], 2),
        (['Война и мир'], 1),
        ([], 0),
        (['1984', '1984'], 1),
        (['Мастер и Маргарита', 'Мастер и Маргарита', 'Преступление и наказание'], 2)
    ])
    def test_add_new_book_multiple_books(self, book_names, expected_count):
        collector = BooksCollector()
        for book in book_names:
            collector.add_new_book(book)

        books = collector.get_books_genre()

        assert len(books) == expected_count
        assert len(set(book_names)) == expected_count

        for book_name in books:
            assert book_name in books
            assert books[book_name] == ""  
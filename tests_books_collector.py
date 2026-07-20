import pytest

from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()
    

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

        for book_name in books:
            assert book_name in books
            assert books[book_name] == "" 


    @pytest.mark.parametrize("books_data, expected_children_books", [
        ({'Книга 1': 'Фантастика', 'Книга 2': 'Мультфильмы'}, ['Книга 1', 'Книга 2']),
        ({'Книга ужасов': 'Ужасы', 'Детектив': 'Детективы'},[]),
        ({'Мультфильм': 'Мультфильмы',
           'Ужастик': 'Ужасы',
           'Комедия': 'Комедии',
           'Детектив': 'Детективы'},['Мультфильм', 'Комедия']),
        ({},[]),
        ({'Научная книга': 'Наука', 'Историческая': 'История'},[]),
        ({'Мультфильм': 'Мультфильмы',
          'Ужастик': 'Ужасы',
          'Учебник': 'Наука'},['Мультфильм'])
    ])
    def test_get_books_for_children(self, books_data, expected_children_books):
        collector = BooksCollector()

        for book_name, genre in books_data.items():
            collector.books_genre[book_name] = genre

        result = collector.get_books_for_children()

        assert result == expected_children_books


    
    
    @pytest.mark.parametrize("book_name,genre,expected_genre", [
        ('1984', 'Фантастика', 'Фантастика'),
        ('Война и мир', 'Ужасы', 'Ужасы'),
        ('Гарри Поттер', 'Детективы', 'Детективы'),
        ('Том и Джерри', 'Мультфильмы', 'Мультфильмы'),
        ('Один дома', 'Комедии', 'Комедии'),
    ])
    def test_add_genre_to_existing_book_with_empty_genre(self, collector, book_name, genre, expected_genre):
    
        collector.add_new_book(book_name)

        collector.set_book_genre(book_name, genre)

        assert collector.books_genre[book_name] == expected_genre


    @pytest.mark.parametrize("book_title, expected_genre", [
    ("Мастер и Маргарита", "Фантастика"),
    ("Гарри Поттер и философский камень", "Комедии"),
    ("Преступление и наказание", "Ужасы"),
    ("Маленький принц", "Мультфильмы"),
    ("Шерлок Холмс", "Детективы")
    ])
    def test_get_genre_by_book_title(self, collector, book_title, expected_genre):
        
        collector.add_new_book(book_title)
        collector.set_book_genre(book_title, expected_genre)
        
        assert book_title in collector.books_genre
        assert collector.books_genre[book_title] == expected_genre
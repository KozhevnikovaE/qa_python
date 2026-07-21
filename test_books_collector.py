import pytest
from main import BooksCollector
 

class TestBooksCollector:

    @pytest.mark.parametrize("book_names, expected_count", [
        (['Война и мир'], 1),
        (['Гордость и предубеждение и зомби', 'Что делать, если ваш кот хочет вас убить'], 2),
        ([], 0),
        (['1984', '1984'], 1),
        (['А'], 1),
        (['Очень длинное название книги, которое превышает обычные пределы и может вызвать проблемы'], 0),
        
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
        ({'Мадагаскар': 'Мультфильмы', 'История игрушек': 'Мультфильмы'}, ['Мадагаскар', 'История игрушек']),
        ({'Оно': 'Ужасы', 'Шерлок Холмс': 'Детективы'},[]),
        ({'Мадагаскар': 'Мультфильмы', 'Оно': 'Ужасы', 'Король Лев': 'Мультфильмы'}, ['Мадагаскар', 'Король Лев']),
        ({},[])
        ])
        
    def test_get_books_for_children(self, books_data, expected_children_books):
        collector = BooksCollector()

        for book_name, genre in books_data.items():
            collector.books_genre[book_name] = genre

        result = collector.get_books_for_children()

        assert result == expected_children_books


    
    
    @pytest.mark.parametrize("book_name, genre, expected_genre",[
        ('А', 'Фантастика', 'Фантастика'),

        ('A' * 40, 'Ужасы', 'Ужасы'),
        ('Гарри Поттер', 'Детективы', 'Детективы')
    ])
    
    def test_add_genre_to_valid_book_name(self, collector, book_name, genre, expected_genre):
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.books_genre[book_name] == expected_genre 


    @pytest.mark.parametrize("invalid_book_name",[           
        '',            
        'A' * 41 
    ])
    def test_add_invalid_book_name(self, collector, invalid_book_name):
        collector.add_new_book(invalid_book_name)
   
        assert invalid_book_name not in collector.books_genre   


    @pytest.mark.parametrize("book_title, expected_genre", [
    ("Мастер и Маргарита", "Фантастика"),
    ("Гарри Поттер и философский камень", "Комедии"),
    ("Преступление и наказание", "Ужасы"),
    ("Маленький принц", "Мультфильмы"),
    ("Шерлок Холмс", "Детективы")
    ])
    def test_get_genre_by_book_title(self, collector, book_title, expected_genre): # Проверка метода get_book_genre - получаем жанр книги по её имени 
        
        collector.add_new_book(book_title)
        collector.set_book_genre(book_title, expected_genre)

        result = collector.get_book_genre(book_title)
        
        assert result == expected_genre 


    @pytest.mark.parametrize("test_books, expected_result", [
        ({}, {}),                                                                            
        ({"Война и мир": "", "Преступление и наказание": ""},
         {"Война и мир": "", "Преступление и наказание": ""}),                                          
        ({"Мастер и Маргарита": "Фантастика", "1984": "Ужасы"},
         {"Мастер и Маргарита": "Фантастика", "1984": "Ужасы"}),        
        ({"Гарри Поттер": "Фэнтези", "Анна Каренина": ""},
         {"Гарри Поттер": "Фэнтези", "Анна Каренина": ""})
         ])
    def test_get_books_genre(self, collector, test_books, expected_result):
        collector.books_genre = test_books

        result = collector.get_books_genre()

        assert isinstance(result, dict)
        assert result == expected_result
        assert len(result) == len(expected_result)



    @pytest.mark.parametrize("book_name, genre",[
        ("Война и мир", "Ужасы"),
        ("Мастер и Маргарита", "Фантастика"),
        ("Гарри Поттер", "Фэнтези")
    ])
    def test_add_book_in_favorites_valid(self, collector, book_name, genre):

        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)

        result = collector.add_book_in_favorites(book_name)

        assert result is None 
        assert book_name in collector.favorites  
        assert len(collector.favorites) == 1 


    @pytest.mark.parametrize("book_name",[
        "1984",           
        "",              
        None             
    ])
    def test_add_book_in_favorites_invalid(self, collector, book_name):
    
        result = collector.add_book_in_favorites(book_name)

    
        assert result is None  
        assert book_name not in collector.favorites 
        assert len(collector.favorites) == 0   


    def test_delete_book_from_favorites_simple(self, collector):
    
        collector.favorites = ["Война и мир", "Мастер и Маргарита"]

        collector.delete_book_from_favorites("Война и мир")

        assert collector.favorites == ["Мастер и Маргарита"] 


    @pytest.mark.parametrize("books_in_favorites, expected_result",
     [([], []), 
     (["Книга 1"], ["Книга 1"]),
     (["Книга А", "Книга Б", "Книга В"], ["Книга А", "Книга Б", "Книга В"]),
     ])
    def test_get_list_of_favorites_books_parametrized(self, books_in_favorites, expected_result):
        collector = BooksCollector()

        collector.favorites = books_in_favorites

        result = collector.get_list_of_favorites_books()

        assert result == expected_result 
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json
import os

@dataclass
class Book:
    """Класс для представления книги"""
    id: int
    title: str
    author: str
    year: int
    isbn: str = ""
    
    def to_dict(self) -> Dict:
        """Преобразование книги в словарь для сериализации"""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "isbn": self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Book':
        """Создание книги из словаря"""
        return cls(**data)

class BookLibrary:
    """Основной класс библиотеки книг"""
    
    def __init__(self, filename: str = "library.json"):
        self.books: List[Book] = []
        self.next_id = 1
        self.filename = filename
        self.load_from_file()
    
    def add_book(self, title: str, author: str, year: int, isbn: str = "") -> Book:
        """Добавить новую книгу в библиотеку"""
        book = Book(self.next_id, title, author, year, isbn)
        self.books.append(book)
        self.next_id += 1
        self.save_to_file()
        return book
    
    def remove_book(self, book_id: int) -> bool:
        """Удалить книгу по ID"""
        for i, book in enumerate(self.books):
            if book.id == book_id:
                self.books.pop(i)
                self.save_to_file()
                return True
        return False
    
    def find_by_title(self, title: str, case_sensitive: bool = False) -> List[Book]:
        """Поиск книг по названию"""
        if case_sensitive:
            return [book for book in self.books if title in book.title]
        else:
            return [book for book in self.books if title.lower() in book.title.lower()]
    
    def find_by_author(self, author: str, case_sensitive: bool = False) -> List[Book]:
        """Поиск книг по автору"""
        if case_sensitive:
            return [book for book in self.books if author in book.author]
        else:
            return [book for book in self.books if author.lower() in book.author.lower()]
    
    def find_by_year(self, year: int, exact: bool = False) -> List[Book]:
        """Поиск книг по году издания"""
        if exact:
            return [book for book in self.books if book.year == year]
        else:
            return [book for book in self.books if book.year >= year]
    
    def find_by_year_range(self, start_year: int, end_year: int) -> List[Book]:
        """Поиск книг в диапазоне годов"""
        return [book for book in self.books if start_year <= book.year <= end_year]
    
    def search(self, title: str = "", author: str = "", year: int = 0) -> List[Book]:
        """Универсальный поиск по всем критериям"""
        results = self.books
        
        if title:
            results = [book for book in results if title.lower() in book.title.lower()]
        if author:
            results = [book for book in results if author.lower() in book.author.lower()]
        if year:
            results = [book for book in results if book.year == year]
        
        return results
    
    def sort_by_title(self, reverse: bool = False) -> List[Book]:
        """Сортировка по названию"""
        return sorted(self.books, key=lambda x: x.title.lower(), reverse=reverse)
    
    def sort_by_author(self, reverse: bool = False) -> List[Book]:
        """Сортировка по автору"""
        return sorted(self.books, key=lambda x: x.author.lower(), reverse=reverse)
    
    def sort_by_year(self, reverse: bool = False) -> List[Book]:
        """Сортировка по году"""
        return sorted(self.books, key=lambda x: x.year, reverse=reverse)
    
    def get_all_books(self) -> List[Book]:
        """Получить все книги"""
        return self.books.copy()
    
    def get_book_by_id(self, book_id: int) -> Optional[Book]:
        """Получить книгу по ID"""
        for book in self.books:
            if book.id == book_id:
                return book
        return None
    
    def get_stats(self) -> Dict:
        """Получить статистику библиотеки"""
        total_books = len(self.books)
        years = [book.year for book in self.books]
        authors = {}
        for book in self.books:
            authors[book.author] = authors.get(book.author, 0) + 1
        
        return {
            "total_books": total_books,
            "min_year": min(years) if years else 0,
            "max_year": max(years) if years else 0,
            "avg_year": sum(years) / len(years) if years else 0,
            "authors_count": len(authors),
            "top_authors": dict(sorted(authors.items(), key=lambda x: x[1], reverse=True)[:3])
        }
    
    def save_to_file(self):
        """Сохранить библиотеку в файл"""
        data = [{"next_id": self.next_id}] + [book.to_dict() for book in self.books]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self):
        """Загрузить библиотеку из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.next_id = data[0]["next_id"]
                    self.books = [Book.from_dict(book_data) for book_data in data[1:]]
            except (json.JSONDecodeError, IndexError, KeyError):
                self.books = []
                self.next_id = 1
    
    def clear_library(self):
        """Очистить библиотеку"""
        self.books = []
        self.next_id = 1
        self.save_to_file()


def print_books(books: List[Book], limit: int = None):
    """Вывести список книг в красивом формате"""
    if not books:
        print("Книги не найдены.")
        return
    
    books = books[:limit] if limit else books
    print(f"\n{'='*80}")
    print(f"{'ID':<4} {'Название':<35} {'Автор':<25} {'Год':<6} {'ISBN'}")
    print('='*80)
    
    for book in books:
        print(f"{book.id:<4} {book.title[:34]:<35} {book.author[:24]:<25} {book.year:<6} {book.isbn}")
    print(f"{'='*80}\n")
    print(f"Всего найдено: {len(books)} книг")


# Пример использования
if __name__ == "__main__":
    # Создаем библиотеку
    library = BookLibrary()
    
    # Добавляем тестовые книги
    library.add_book("Война и мир", "Лев Толстой", 1869, "978-5-17-001160-9")
    library.add_book("Преступление и наказание", "Фёдор Достоевский", 1866)
    library.add_book("1984", "Джордж Оруэлл", 1949, "978-0-452-28423-4")
    library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1967)
    library.add_book("Гарри Поттер и философский камень", "Дж. К. Роулинг", 1997)
    
    print("=== Демонстрация работы библиотеки ===\n")
    
    # Поиск
    print("1. Поиск по автору 'Толстой':")
    tolstoy_books = library.find_by_author("Толстой")
    print_books(tolstoy_books)
    
    print("2. Поиск по названию 'Гарри':")
    harry_books = library.find_by_title("Гарри")
    print_books(harry_books)
    
    print("3. Книги после 1950 года:")
    modern_books = library.find_by_year(1950)
    print_books(modern_books)
    
    print("4. Универсальный поиск (Достоевский, после 1860):")
    search_results = library.search(author="Достоевский", year=1866)
    print_books(search_results)
    
    # Сортировка
    print("5. Сортировка по году (убывание):")
    sorted_by_year = library.sort_by_year(reverse=True)
    print_books(sorted_by_year, limit=5)
    
    print("6. Статистика библиотеки:")
    stats = library.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    
    print("\nБиблиотека сохранена в файл library.json")
# Простая библиотека на Python с использованием только массивов

# Создаем библиотеку как список книг
# Каждая книга - это словарь с полями: название, автор, жанр, год
library = [
    {"title": "Война и мир", "author": "Лев Толстой", "genre": "Роман", "year": 1869},
    {"title": "Преступление и наказание", "author": "Федор Достоевский", "genre": "Роман", "year": 1866},
    {"title": "Мастер и Маргарита", "author": "Михаил Булгаков", "genre": "Фантастика", "year": 1967},
    {"title": "Евгений Онегин", "author": "Александр Пушкин", "genre": "Поэма", "year": 1833},
    {"title": "1984", "author": "Джордж Оруэлл", "genre": "Антиутопия", "year": 1949},
    {"title": "Собачье сердце", "author": "Михаил Булгаков", "genre": "Фантастика", "year": 1925},
    {"title": "Анна Каренина", "author": "Лев Толстой", "genre": "Роман", "year": 1877},
    {"title": "Мертвые души", "author": "Николай Гоголь", "genre": "Поэма", "year": 1842},
]


def show_books(books):
    """Показать все книги"""
    if not books:
        print("📚 Библиотека пуста")
        return
    
    print("\n" + "="*60)
    print("СПИСОК КНИГ")
    print("="*60)
    for i, book in enumerate(books, 1):
        print(f"{i}. {book['title']}")
        print(f"   Автор: {book['author']}")
        print(f"   Жанр: {book['genre']}")
        print(f"   Год: {book['year']}")
        print("-"*40)


def sort_by_title(books, reverse=False):
    """Сортировка по названию"""
    return sorted(books, key=lambda x: x['title'].lower(), reverse=reverse)


def sort_by_author(books, reverse=False):
    """Сортировка по автору"""
    return sorted(books, key=lambda x: x['author'].lower(), reverse=reverse)


def sort_by_genre(books):
    """Сортировка по жанру"""
    return sorted(books, key=lambda x: (x['genre'].lower(), x['author'].lower()))


def sort_by_year(books, reverse=False):
    """Сортировка по году"""
    return sorted(books, key=lambda x: x['year'], reverse=reverse)


def add_book(books):
    """Добавить новую книгу"""
    print("\n📖 ДОБАВЛЕНИЕ КНИГИ")
    print("-"*30)
    
    title = input("Название книги: ").strip()
    if not title:
        print("❌ Название не может быть пустым!")
        return books
    
    author = input("Автор: ").strip()
    if not author:
        print("❌ Автор не может быть пустым!")
        return books
    
    genre = input("Жанр: ").strip()
    if not genre:
        print("❌ Жанр не может быть пустым!")
        return books
    
    try:
        year = int(input("Год издания: "))
    except:
        print("❌ Год должен быть числом!")
        return books
    
    # Создаем новую книгу
    new_book = {
        "title": title,
        "author": author,
        "genre": genre,
        "year": year
    }
    
    # Добавляем в библиотеку
    books.append(new_book)
    print(f"✅ Книга '{title}' добавлена!")
    
    return books


def search_books(books):
    """Поиск книг"""
    print("\n🔍 ПОИСК КНИГ")
    print("-"*30)
    print("1. Поиск по названию")
    print("2. Поиск по автору")
    print("3. Поиск по жанру")
    
    choice = input("Выберите вариант (1-3): ").strip()
    
    if choice == '1':
        query = input("Введите название: ").strip().lower()
        results = [b for b in books if query in b['title'].lower()]
        print(f"\nНайдено книг: {len(results)}")
        
    elif choice == '2':
        query = input("Введите автора: ").strip().lower()
        results = [b for b in books if query in b['author'].lower()]
        print(f"\nНайдено книг: {len(results)}")
        
    elif choice == '3':
        query = input("Введите жанр: ").strip().lower()
        results = [b for b in books if query in b['genre'].lower()]
        print(f"\nНайдено книг: {len(results)}")
        
    else:
        print("❌ Неверный выбор")
        return
    
    if results:
        show_books(results)
    else:
        print("❌ Ничего не найдено")
    
    input("\nНажмите Enter для продолжения...")


def main_menu():
    """Главное меню"""
    global library
    
    while True:
        print("\n" + "="*50)
        print("📚 МОЯ БИБЛИОТЕКА")
        print("="*50)
        print("1. Показать все книги")
        print("2. Сортировать по названию")
        print("3. Сортировать по автору")
        print("4. Сортировать по жанру")
        print("5. Сортировать по году")
        print("6. Добавить книгу")
        print("7. Поиск книг")
        print("0. Выход")
        print("="*50)
        
        choice = input("Выберите действие (0-7): ").strip()
        
        if choice == '0':
            print("\n👋 До свидания!")
            break
            
        elif choice == '1':
            show_books(library)
            input("\nНажмите Enter для продолжения...")
            
        elif choice == '2':
            print("\n1. А-Я (возрастание)")
            print("2. Я-А (убывание)")
            sub = input("Выберите (1-2): ").strip()
            
            if sub == '1':
                sorted_books = sort_by_title(library)
                show_books(sorted_books)
            elif sub == '2':
                sorted_books = sort_by_title(library, reverse=True)
                show_books(sorted_books)
            else:
                print("❌ Неверный выбор")
            
            input("\nНажмите Enter для продолжения...")
            
        elif choice == '3':
            print("\n1. А-Я (возрастание)")
            print("2. Я-А (убывание)")
            sub = input("Выберите (1-2): ").strip()
            
            if sub == '1':
                sorted_books = sort_by_author(library)
                show_books(sorted_books)
            elif sub == '2':
                sorted_books = sort_by_author(library, reverse=True)
                show_books(sorted_books)
            else:
                print("❌ Неверный выбор")
            
            input("\nНажмите Enter для продолжения...")
            
        elif choice == '4':
            sorted_books = sort_by_genre(library)
            show_books(sorted_books)
            input("\nНажмите Enter для продолжения...")
            
        elif choice == '5':
            print("\n1. От старых к новым")
            print("2. От новых к старым")
            sub = input("Выберите (1-2): ").strip()
            
            if sub == '1':
                sorted_books = sort_by_year(library)
                show_books(sorted_books)
            elif sub == '2':
                sorted_books = sort_by_year(library, reverse=True)
                show_books(sorted_books)
            else:
                print("❌ Неверный выбор")
            
            input("\nНажмите Enter для продолжения...")
            
        elif choice == '6':
            library = add_book(library)
            input("\nНажмите Enter для продолжения...")
            
        elif choice == '7':
            search_books(library)
            
        else:
            print("❌ Неверный выбор. Попробуйте снова.")
            input("\nНажмите Enter для продолжения...")


# Запуск программы
if __name__ == "__main__":
    print("Добро пожаловать в библиотеку!")
    main_menu()
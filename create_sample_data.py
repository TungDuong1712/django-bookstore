#!/usr/bin/env python
import os
import django
from datetime import date

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')
django.setup()

from books.models import Category, Author, Book, Review
from users.models import CustomUser

def create_sample_data():
    """Tạo dữ liệu mẫu cho project"""
    
    print("Creating sample data...")
    
    # Tạo categories
    categories_data = [
        {
            'name': 'Tiểu thuyết',
            'description': 'Các tác phẩm tiểu thuyết văn học'
        },
        {
            'name': 'Khoa học',
            'description': 'Sách về khoa học và công nghệ'
        },
        {
            'name': 'Kinh doanh',
            'description': 'Sách về kinh doanh và quản lý'
        },
        {
            'name': 'Lập trình',
            'description': 'Sách về lập trình và công nghệ thông tin'
        },
        {
            'name': 'Tâm lý học',
            'description': 'Sách về tâm lý học và phát triển bản thân'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    # Tạo authors
    authors_data = [
        {
            'name': 'Nguyễn Nhật Ánh',
            'bio': 'Nhà văn nổi tiếng Việt Nam với nhiều tác phẩm văn học được yêu thích',
            'email': 'nguyennhatanh@example.com'
        },
        {
            'name': 'Dale Carnegie',
            'bio': 'Tác giả nổi tiếng với các sách về kỹ năng giao tiếp và phát triển bản thân',
            'email': 'dalecarnegie@example.com'
        },
        {
            'name': 'Robert C. Martin',
            'bio': 'Tác giả nổi tiếng về lập trình và kiến trúc phần mềm',
            'email': 'robertmartin@example.com'
        },
        {
            'name': 'Stephen Hawking',
            'bio': 'Nhà vật lý lý thuyết nổi tiếng với các nghiên cứu về vũ trụ học',
            'email': 'stephenhawking@example.com'
        },
        {
            'name': 'Paulo Coelho',
            'bio': 'Nhà văn Brazil nổi tiếng với tác phẩm "Nhà giả kim"',
            'email': 'paulocoelho@example.com'
        }
    ]
    
    authors = []
    for auth_data in authors_data:
        author, created = Author.objects.get_or_create(
            name=auth_data['name'],
            defaults=auth_data
        )
        authors.append(author)
        if created:
            print(f"Created author: {author.name}")
    
    # Tạo books
    books_data = [
        {
            'title': 'Tôi Thấy Hoa Vàng Trên Cỏ Xanh',
            'author': authors[0],  # Nguyễn Nhật Ánh
            'category': categories[0],  # Tiểu thuyết
            'description': 'Một tác phẩm văn học đặc sắc về tuổi thơ và tình bạn',
            'isbn': '9786043234567',
            'publication_date': date(2010, 1, 1),
            'publisher': 'NXB Trẻ',
            'language': 'vi',
            'pages': 400,
            'price': 120000,
            'status': 'available',
            'stock_quantity': 50
        },
        {
            'title': 'Đắc Nhân Tâm',
            'author': authors[1],  # Dale Carnegie
            'category': categories[4],  # Tâm lý học
            'description': 'Nghệ thuật đắc nhân tâm - cách ứng xử và giao tiếp hiệu quả',
            'isbn': '9786043234568',
            'publication_date': date(1936, 1, 1),
            'publisher': 'NXB Tổng hợp',
            'language': 'vi',
            'pages': 320,
            'price': 89000,
            'status': 'available',
            'stock_quantity': 30
        },
        {
            'title': 'Clean Code',
            'author': authors[2],  # Robert C. Martin
            'category': categories[3],  # Lập trình
            'description': 'Hướng dẫn viết code sạch và dễ bảo trì',
            'isbn': '9786043234569',
            'publication_date': date(2008, 1, 1),
            'publisher': 'Prentice Hall',
            'language': 'en',
            'pages': 464,
            'price': 250000,
            'status': 'available',
            'stock_quantity': 25
        },
        {
            'title': 'A Brief History of Time',
            'author': authors[3],  # Stephen Hawking
            'category': categories[1],  # Khoa học
            'description': 'Lược sử thời gian - khám phá vũ trụ và thuyết tương đối',
            'isbn': '9786043234570',
            'publication_date': date(1988, 1, 1),
            'publisher': 'Bantam Books',
            'language': 'en',
            'pages': 256,
            'price': 180000,
            'status': 'available',
            'stock_quantity': 20
        },
        {
            'title': 'Nhà Giả Kim',
            'author': authors[4],  # Paulo Coelho
            'category': categories[0],  # Tiểu thuyết
            'description': 'Câu chuyện về hành trình tìm kiếm kho báu và ý nghĩa cuộc sống',
            'isbn': '9786043234571',
            'publication_date': date(1988, 1, 1),
            'publisher': 'NXB Văn học',
            'language': 'vi',
            'pages': 208,
            'price': 75000,
            'status': 'available',
            'stock_quantity': 40
        },
        {
            'title': 'The Lean Startup',
            'author': authors[2],  # Robert C. Martin (thay thế)
            'category': categories[2],  # Kinh doanh
            'description': 'Phương pháp khởi nghiệp tinh gọn và hiệu quả',
            'isbn': '9786043234572',
            'publication_date': date(2011, 1, 1),
            'publisher': 'Crown Business',
            'language': 'en',
            'pages': 336,
            'price': 200000,
            'status': 'available',
            'stock_quantity': 15
        }
    ]
    
    books = []
    for book_data in books_data:
        book, created = Book.objects.get_or_create(
            isbn=book_data['isbn'],
            defaults=book_data
        )
        books.append(book)
        if created:
            print(f"Created book: {book.title}")
    
    # Tạo users
    users_data = [
        {
            'username': 'user1',
            'email': 'user1@example.com',
            'first_name': 'Nguyễn',
            'last_name': 'Văn A',
            'password': 'user123'
        },
        {
            'username': 'user2',
            'email': 'user2@example.com',
            'first_name': 'Trần',
            'last_name': 'Thị B',
            'password': 'user123'
        }
    ]
    
    users = []
    for user_data in users_data:
        user, created = CustomUser.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name']
            }
        )
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"Created user: {user.username}")
        users.append(user)
    
    # Tạo reviews
    reviews_data = [
        {
            'book': books[0],
            'user': users[0],
            'rating': 5,
            'comment': 'Một tác phẩm tuyệt vời về tuổi thơ!'
        },
        {
            'book': books[0],
            'user': users[1],
            'rating': 4,
            'comment': 'Sách hay, đáng đọc!'
        },
        {
            'book': books[1],
            'user': users[0],
            'rating': 5,
            'comment': 'Sách rất hữu ích cho việc phát triển kỹ năng giao tiếp'
        },
        {
            'book': books[2],
            'user': users[1],
            'rating': 5,
            'comment': 'Một cuốn sách kinh điển về lập trình!'
        },
        {
            'book': books[3],
            'user': users[0],
            'rating': 4,
            'comment': 'Sách khoa học rất thú vị và dễ hiểu'
        }
    ]
    
    for review_data in reviews_data:
        review, created = Review.objects.get_or_create(
            book=review_data['book'],
            user=review_data['user'],
            defaults={
                'rating': review_data['rating'],
                'comment': review_data['comment']
            }
        )
        if created:
            print(f"Created review: {review.user.username} - {review.book.title}")
    
    print("\nSample data created successfully!")
    print(f"Created {len(categories)} categories")
    print(f"Created {len(authors)} authors")
    print(f"Created {len(books)} books")
    print(f"Created {len(users)} users")
    print(f"Created {Review.objects.count()} reviews")

if __name__ == '__main__':
    create_sample_data() 
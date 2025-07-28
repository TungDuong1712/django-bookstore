# Django REST Framework Project - Bookstore

Đây là một project Django cơ bản sử dụng Django REST Framework để học và hiểu đầy đủ các tính năng của Django.

## Cấu trúc Project

```
django_DRF/
├── bookstore/          # Project chính
│   ├── __init__.py
│   ├── settings.py     # Cấu hình project
│   ├── urls.py         # URL routing chính
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── books/              # App quản lý sách
│   ├── models.py       # Models cho Book, Author, Category
│   ├── serializers.py  # DRF Serializers
│   ├── views.py        # API Views
│   ├── urls.py         # URL routing cho books
│   └── admin.py        # Django Admin
├── users/              # App quản lý người dùng
│   ├── models.py       # Custom User Model
│   ├── serializers.py  # User Serializers
│   ├── views.py        # User API Views
│   └── urls.py         # URL routing cho users
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
└── README.md          # Hướng dẫn này
```

## Tính năng chính

### 1. Models (Django ORM)
- **Book Model**: Quản lý thông tin sách
- **Author Model**: Quản lý tác giả
- **Category Model**: Phân loại sách
- **Custom User Model**: Quản lý người dùng

### 2. Django REST Framework
- **Serializers**: Chuyển đổi dữ liệu giữa JSON và Python objects
- **ViewSets**: API views với CRUD operations
- **Routers**: Tự động tạo URL patterns
- **Permissions**: Kiểm soát quyền truy cập
- **Authentication**: Xác thực người dùng

### 3. Django Admin
- Giao diện quản trị tích hợp
- Quản lý dữ liệu trực quan

### 4. API Endpoints
- `/api/books/` - CRUD operations cho sách
- `/api/authors/` - CRUD operations cho tác giả
- `/api/categories/` - CRUD operations cho danh mục
- `/api/users/` - Quản lý người dùng
- `/admin/` - Django Admin interface

## Cài đặt và Chạy

### 1. Tạo virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Tạo superuser
```bash
python manage.py createsuperuser
```

### 5. Chạy development server
```bash
python manage.py runserver
```

## Truy cập

- **Django Admin**: http://localhost:8000/admin/
- **API Root**: http://localhost:8000/api/
- **Books API**: http://localhost:8000/api/books/
- **Authors API**: http://localhost:8000/api/authors/
- **Categories API**: http://localhost:8000/api/categories/

## Học tập

### Django Core Concepts
1. **Models**: Định nghĩa cấu trúc dữ liệu
2. **Views**: Xử lý logic nghiệp vụ
3. **URLs**: Định tuyến request
4. **Templates**: Hiển thị giao diện
5. **Forms**: Xử lý dữ liệu từ user
6. **Admin**: Giao diện quản trị

### Django REST Framework
1. **Serializers**: Chuyển đổi dữ liệu
2. **ViewSets**: API views với CRUD
3. **Routers**: Tự động tạo URLs
4. **Permissions**: Kiểm soát quyền
5. **Authentication**: Xác thực
6. **Pagination**: Phân trang
7. **Filtering**: Lọc dữ liệu

### Best Practices
1. **Project Structure**: Tổ chức code rõ ràng
2. **App Separation**: Tách biệt chức năng
3. **Model Relationships**: Quan hệ giữa models
4. **API Design**: Thiết kế API RESTful
5. **Security**: Bảo mật ứng dụng 
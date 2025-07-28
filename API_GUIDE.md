# Hướng dẫn sử dụng Bookstore API

## Tổng quan

Bookstore API là một RESTful API được xây dựng bằng Django REST Framework, cung cấp các endpoint để quản lý sách, tác giả, danh mục, người dùng và đánh giá.

## Base URL

```
http://localhost:8000/api/
```

## Authentication

API sử dụng Session Authentication và Basic Authentication. Một số endpoint yêu cầu đăng nhập.

### Đăng nhập
```bash
POST /api/auth/login/
Content-Type: application/json

{
    "username": "admin",
    "password": "admin123"
}
```

### Đăng ký
```bash
POST /api/auth/register/
Content-Type: application/json

{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "password123",
    "password_confirm": "password123",
    "first_name": "Nguyễn",
    "last_name": "Văn A"
}
```

## API Endpoints

### 1. Books API

#### Lấy danh sách sách
```bash
GET /api/books/
```

**Query Parameters:**
- `search`: Tìm kiếm theo tên sách, tác giả, mô tả
- `category`: Lọc theo danh mục
- `author`: Lọc theo tác giả
- `language`: Lọc theo ngôn ngữ
- `status`: Lọc theo trạng thái
- `ordering`: Sắp xếp (title, price, publication_date, created_at)

**Ví dụ:**
```bash
GET /api/books/?search=clean&language=en&ordering=-created_at
```

#### Lấy chi tiết sách
```bash
GET /api/books/{slug}/
```

#### Tạo sách mới (cần đăng nhập)
```bash
POST /api/books/
Content-Type: application/json

{
    "title": "Tên sách",
    "author": 1,
    "category": 1,
    "description": "Mô tả sách",
    "isbn": "9786043234567",
    "publication_date": "2023-01-01",
    "publisher": "NXB Trẻ",
    "language": "vi",
    "pages": 300,
    "price": "150000.00",
    "status": "available",
    "stock_quantity": 10
}
```

#### Cập nhật sách (cần đăng nhập)
```bash
PUT /api/books/{slug}/
PATCH /api/books/{slug}/
```

#### Xóa sách (cần đăng nhập)
```bash
DELETE /api/books/{slug}/
```

#### Các endpoint đặc biệt cho sách

**Sách có sẵn:**
```bash
GET /api/books/available/
```

**Sách bán chạy:**
```bash
GET /api/books/best_sellers/
```

**Sách mới xuất bản:**
```bash
GET /api/books/new_releases/
```

**Đánh giá của sách:**
```bash
GET /api/books/{slug}/reviews/
```

**Thêm đánh giá (cần đăng nhập):**
```bash
POST /api/books/{slug}/add_review/
Content-Type: application/json

{
    "rating": 5,
    "comment": "Sách rất hay!"
}
```

### 2. Authors API

#### Lấy danh sách tác giả
```bash
GET /api/authors/
```

**Query Parameters:**
- `search`: Tìm kiếm theo tên, bio, email
- `ordering`: Sắp xếp

#### Lấy chi tiết tác giả
```bash
GET /api/authors/{slug}/
```

#### Sách của tác giả
```bash
GET /api/authors/{slug}/books/
```

### 3. Categories API

#### Lấy danh sách danh mục
```bash
GET /api/categories/
```

#### Lấy chi tiết danh mục
```bash
GET /api/categories/{slug}/
```

#### Sách trong danh mục
```bash
GET /api/categories/{slug}/books/
```

### 4. Users API

#### Lấy thông tin user hiện tại
```bash
GET /api/users/me/
```

#### Cập nhật profile
```bash
PUT /api/users/update_profile/
PATCH /api/users/update_profile/
```

#### Đổi mật khẩu
```bash
POST /api/users/change_password/
Content-Type: application/json

{
    "old_password": "oldpass",
    "new_password": "newpass",
    "new_password_confirm": "newpass"
}
```

#### Profile công khai của user
```bash
GET /api/profile/{username}/
```

#### Đánh giá của user
```bash
GET /api/profile/{username}/reviews/
```

### 5. Reviews API

#### Lấy danh sách đánh giá
```bash
GET /api/reviews/
```

**Query Parameters:**
- `book`: Lọc theo sách
- `user`: Lọc theo user
- `rating`: Lọc theo điểm đánh giá

#### Tạo đánh giá mới (cần đăng nhập)
```bash
POST /api/reviews/
Content-Type: application/json

{
    "book": 1,
    "rating": 5,
    "comment": "Sách rất hay!"
}
```

### 6. Search API

#### Tìm kiếm sách nâng cao
```bash
GET /api/search/
```

**Query Parameters:**
- `q`: Từ khóa tìm kiếm
- `min_price`: Giá tối thiểu
- `max_price`: Giá tối đa
- `language`: Ngôn ngữ
- `ordering`: Sắp xếp

### 7. Statistics API

#### Thống kê tổng quan
```bash
GET /api/statistics/
```

Trả về:
- Tổng số sách
- Số sách có sẵn
- Tổng số tác giả
- Tổng số danh mục
- Thống kê theo danh mục
- Thống kê theo ngôn ngữ
- Sách có đánh giá cao nhất

## Response Format

### Success Response
```json
{
    "count": 10,
    "next": "http://localhost:8000/api/books/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "title": "Tên sách",
            "author_name": "Tên tác giả",
            "category_name": "Tên danh mục",
            "price": "150000.00",
            "is_available": true
        }
    ]
}
```

### Error Response
```json
{
    "error": "Mô tả lỗi",
    "detail": "Chi tiết lỗi"
}
```

## Pagination

API sử dụng pagination với 10 items mỗi trang. Response bao gồm:
- `count`: Tổng số items
- `next`: URL trang tiếp theo
- `previous`: URL trang trước
- `results`: Dữ liệu của trang hiện tại

## Filtering

### Text Search
```bash
GET /api/books/?search=python
```

### Range Filtering
```bash
GET /api/books/?min_price=100000&max_price=200000
```

### Exact Filtering
```bash
GET /api/books/?language=vi&status=available
```

## Ordering

```bash
GET /api/books/?ordering=title          # Tăng dần
GET /api/books/?ordering=-price         # Giảm dần
GET /api/books/?ordering=author__name   # Theo tên tác giả
```

## File Upload

Để upload ảnh (avatar, cover_image, photo), sử dụng `multipart/form-data`:

```bash
POST /api/books/
Content-Type: multipart/form-data

{
    "title": "Tên sách",
    "cover_image": [file],
    ...
}
```

## Status Codes

- `200 OK`: Thành công
- `201 Created`: Tạo mới thành công
- `400 Bad Request`: Dữ liệu không hợp lệ
- `401 Unauthorized`: Chưa đăng nhập
- `403 Forbidden`: Không có quyền
- `404 Not Found`: Không tìm thấy
- `500 Internal Server Error`: Lỗi server

## Testing với curl

### Lấy danh sách sách
```bash
curl -X GET http://localhost:8000/api/books/
```

### Đăng nhập
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### Tạo sách mới (với session)
```bash
curl -X POST http://localhost:8000/api/books/ \
  -H "Content-Type: application/json" \
  -b sessionid=your_session_id \
  -d '{"title": "Sách mới", "author": 1, "category": 1, ...}'
```

## Testing với Postman

1. Import collection từ file `Bookstore_API.postman_collection.json`
2. Set base URL: `http://localhost:8000/api/`
3. Đăng nhập để lấy session
4. Test các endpoint

## Documentation

Truy cập API documentation tại:
```
http://localhost:8000/docs/
```

## Admin Interface

Truy cập Django Admin tại:
```
http://localhost:8000/admin/
```

**Credentials:**
- Username: `admin`
- Password: `admin123` 
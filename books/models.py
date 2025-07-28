from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
    """Model cho danh mục sách"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})


class Author(models.Model):
    """Model cho tác giả"""
    name = models.CharField(max_length=200, verbose_name="Tên tác giả")
    bio = models.TextField(blank=True, verbose_name="Tiểu sử")
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Website")
    photo = models.ImageField(upload_to='authors/', blank=True, verbose_name="Ảnh")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Tác giả"
        verbose_name_plural = "Tác giả"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'slug': self.slug})


class Book(models.Model):
    """Model cho sách"""
    LANGUAGE_CHOICES = [
        ('vi', 'Tiếng Việt'),
        ('en', 'English'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('ja', '日本語'),
        ('ko', '한국어'),
        ('zh', '中文'),
    ]

    STATUS_CHOICES = [
        ('available', 'Có sẵn'),
        ('borrowed', 'Đã mượn'),
        ('reserved', 'Đã đặt trước'),
        ('maintenance', 'Bảo trì'),
    ]

    title = models.CharField(max_length=200, verbose_name="Tên sách")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='books',
        verbose_name="Tác giả"
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='books',
        verbose_name="Danh mục"
    )
    description = models.TextField(verbose_name="Mô tả")
    isbn = models.CharField(max_length=13, unique=True, verbose_name="ISBN")
    publication_date = models.DateField(verbose_name="Ngày xuất bản")
    publisher = models.CharField(max_length=200, verbose_name="Nhà xuất bản")
    language = models.CharField(
        max_length=2, 
        choices=LANGUAGE_CHOICES, 
        default='vi',
        verbose_name="Ngôn ngữ"
    )
    pages = models.PositiveIntegerField(verbose_name="Số trang")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Giá"
    )
    cover_image = models.ImageField(
        upload_to='books/covers/', 
        blank=True, 
        verbose_name="Ảnh bìa"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='available',
        verbose_name="Trạng thái"
    )
    stock_quantity = models.PositiveIntegerField(
        default=1, 
        verbose_name="Số lượng tồn kho"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Sách"
        verbose_name_plural = "Sách"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug': self.slug})

    @property
    def is_available(self):
        """Kiểm tra sách có sẵn không"""
        return self.status == 'available' and self.stock_quantity > 0

    @property
    def average_rating(self):
        """Tính điểm đánh giá trung bình"""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class Review(models.Model):
    """Model cho đánh giá sách"""
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='reviews',
        verbose_name="Sách"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        verbose_name="Người dùng"
    )
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)],
        verbose_name="Điểm đánh giá"
    )
    comment = models.TextField(verbose_name="Nhận xét")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    class Meta:
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
        unique_together = ['book', 'user']  # Mỗi user chỉ đánh giá 1 lần
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating}/5"

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Author, Book, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration cho Category model"""
    list_display = ['name', 'books_count', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def books_count(self, obj):
        """Hiển thị số lượng sách trong danh mục"""
        count = obj.books.count()
        return format_html(
            '<a href="{}?category__id__exact={}">{}</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )
    books_count.short_description = 'Số sách'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """Admin configuration cho Author model"""
    list_display = ['name', 'email', 'books_count', 'photo_preview', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', 'bio', 'email']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'photo_preview']
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'slug', 'bio', 'email', 'website')
        }),
        ('Ảnh', {
            'fields': ('photo', 'photo_preview')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def books_count(self, obj):
        """Hiển thị số lượng sách của tác giả"""
        count = obj.books.count()
        return format_html(
            '<a href="{}?author__id__exact={}">{}</a>',
            reverse('admin:books_book_changelist'),
            obj.id,
            count
        )
    books_count.short_description = 'Số sách'
    
    def photo_preview(self, obj):
        """Hiển thị preview ảnh tác giả"""
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.photo.url
            )
        return "Không có ảnh"
    photo_preview.short_description = 'Ảnh'


class ReviewInline(admin.TabularInline):
    """Inline admin cho Review trong Book"""
    model = Review
    extra = 0
    readonly_fields = ['user', 'created_at']
    fields = ['user', 'rating', 'comment', 'created_at']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration cho Book model"""
    list_display = [
        'title', 'author', 'category', 'isbn', 'price', 
        'status', 'stock_quantity', 'is_available', 'cover_preview'
    ]
    list_filter = [
        'category', 'author', 'language', 'status', 
        'publication_date', 'created_at'
    ]
    search_fields = ['title', 'isbn', 'author__name', 'category__name', 'description']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'cover_preview', 'is_available']
    list_editable = ['status', 'stock_quantity']
    inlines = [ReviewInline]
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('title', 'slug', 'author', 'category', 'description')
        }),
        ('Thông tin xuất bản', {
            'fields': ('isbn', 'publication_date', 'publisher', 'language', 'pages')
        }),
        ('Thông tin kinh doanh', {
            'fields': ('price', 'status', 'stock_quantity', 'is_available')
        }),
        ('Ảnh bìa', {
            'fields': ('cover_image', 'cover_preview')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_available(self, obj):
        """Hiển thị trạng thái có sẵn"""
        if obj.is_available:
            return format_html(
                '<span style="color: green;">✓ Có sẵn</span>'
            )
        return format_html(
            '<span style="color: red;">✗ Hết hàng</span>'
        )
    is_available.short_description = 'Trạng thái'
    
    def cover_preview(self, obj):
        """Hiển thị preview ảnh bìa"""
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.cover_image.url
            )
        return "Không có ảnh"
    cover_preview.short_description = 'Ảnh bìa'
    
    def get_queryset(self, request):
        """Tối ưu queryset với select_related"""
        return super().get_queryset(request).select_related('author', 'category')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration cho Review model"""
    list_display = ['book', 'user', 'rating', 'comment_preview', 'created_at']
    list_filter = ['rating', 'created_at', 'book__category']
    search_fields = ['book__title', 'user__username', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    
    def comment_preview(self, obj):
        """Hiển thị preview comment"""
        if len(obj.comment) > 50:
            return obj.comment[:50] + "..."
        return obj.comment
    comment_preview.short_description = 'Nhận xét'
    
    def get_queryset(self, request):
        """Tối ưu queryset với select_related"""
        return super().get_queryset(request).select_related('book', 'user')


# Customize admin site
admin.site.site_header = "Bookstore Admin"
admin.site.site_title = "Bookstore Admin Portal"
admin.site.index_title = "Chào mừng đến với Bookstore Admin Portal"

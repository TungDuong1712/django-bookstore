from rest_framework import serializers
from .models import Category, Author, Book, Review


class CategorySerializer(serializers.ModelSerializer):
    """Serializer cho Category model"""
    books_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'description', 'slug', 
            'created_at', 'updated_at', 'books_count'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_books_count(self, obj):
        """Đếm số sách trong danh mục"""
        return obj.books.count()


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer cho Author model"""
    books_count = serializers.SerializerMethodField()
    photo_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = [
            'id', 'name', 'bio', 'email', 'website', 'photo', 'photo_url',
            'slug', 'created_at', 'updated_at', 'books_count'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_books_count(self, obj):
        """Đếm số sách của tác giả"""
        return obj.books.count()
    
    def get_photo_url(self, obj):
        """Lấy URL của ảnh tác giả"""
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class BookListSerializer(serializers.ModelSerializer):
    """Serializer cho danh sách sách (tối ưu cho performance)"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    cover_url = serializers.SerializerMethodField()
    is_available = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author_name', 'category_name',
            'isbn', 'publication_date', 'publisher', 'language',
            'price', 'cover_url', 'status', 'stock_quantity',
            'is_available', 'created_at'
        ]
        read_only_fields = ['slug', 'created_at']
    
    def get_cover_url(self, obj):
        """Lấy URL của ảnh bìa sách"""
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None


class BookDetailSerializer(serializers.ModelSerializer):
    """Serializer chi tiết cho sách"""
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    cover_url = serializers.SerializerMethodField()
    is_available = serializers.BooleanField(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Book
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'description',
            'isbn', 'publication_date', 'publisher', 'language', 'pages',
            'price', 'cover_image', 'cover_url', 'status', 'stock_quantity',
            'is_available', 'average_rating', 'reviews_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_cover_url(self, obj):
        """Lấy URL của ảnh bìa sách"""
        if obj.cover_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.cover_image.url)
            return obj.cover_image.url
        return None
    
    def get_reviews_count(self, obj):
        """Đếm số đánh giá của sách"""
        return obj.reviews.count()


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer cho Review model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'book', 'book_title', 'user', 'user_username',
            'rating', 'comment', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        """Tự động gán user hiện tại khi tạo review"""
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def validate_rating(self, value):
        """Validate rating phải từ 1-5"""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating phải từ 1 đến 5")
        return value


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer cho việc tạo và cập nhật sách"""
    
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'category', 'description', 'isbn',
            'publication_date', 'publisher', 'language', 'pages',
            'price', 'cover_image', 'status', 'stock_quantity'
        ]
    
    def validate_isbn(self, value):
        """Validate ISBN format"""
        if len(value) != 13 or not value.isdigit():
            raise serializers.ValidationError("ISBN phải có 13 chữ số")
        return value
    
    def validate_price(self, value):
        """Validate giá sách"""
        if value <= 0:
            raise serializers.ValidationError("Giá sách phải lớn hơn 0")
        return value
    
    def validate_stock_quantity(self, value):
        """Validate số lượng tồn kho"""
        if value < 0:
            raise serializers.ValidationError("Số lượng tồn kho không được âm")
        return value 
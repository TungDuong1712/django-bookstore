from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404

from .models import Category, Author, Book, Review
from .serializers import (
    CategorySerializer, AuthorSerializer, BookListSerializer,
    BookDetailSerializer, BookCreateUpdateSerializer, ReviewSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet cho Category model"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def books(self, request, slug=None):
        """Lấy danh sách sách trong danh mục"""
        category = self.get_object()
        books = category.books.all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    """ViewSet cho Author model"""
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'bio', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    lookup_field = 'slug'

    @action(detail=True, methods=['get'])
    def books(self, request, slug=None):
        """Lấy danh sách sách của tác giả"""
        author = self.get_object()
        books = author.books.all()
        serializer = BookListSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)


class BookViewSet(viewsets.ModelViewSet):
    """ViewSet cho Book model"""
    queryset = Book.objects.select_related('author', 'category').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'language', 'status', 'publisher']
    search_fields = ['title', 'description', 'isbn', 'author__name', 'category__name']
    ordering_fields = ['title', 'price', 'publication_date', 'created_at', 'average_rating']
    ordering = ['-created_at']
    lookup_field = 'slug'

    def get_serializer_class(self):
        """Chọn serializer phù hợp dựa trên action"""
        if self.action == 'list':
            return BookListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        return BookDetailSerializer

    def get_queryset(self):
        """Tối ưu queryset với prefetch_related cho reviews"""
        return super().get_queryset().prefetch_related('reviews')

    @action(detail=False, methods=['get'])
    def available(self, request):
        """Lấy danh sách sách có sẵn"""
        books = self.get_queryset().filter(status='available', stock_quantity__gt=0)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def best_sellers(self, request):
        """Lấy danh sách sách bán chạy (dựa trên số lượng tồn kho thấp)"""
        books = self.get_queryset().filter(status='available').order_by('stock_quantity')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def new_releases(self, request):
        """Lấy danh sách sách mới xuất bản"""
        from datetime import datetime, timedelta
        thirty_days_ago = datetime.now().date() - timedelta(days=30)
        books = self.get_queryset().filter(
            publication_date__gte=thirty_days_ago
        ).order_by('-publication_date')[:10]
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, slug=None):
        """Lấy danh sách đánh giá của sách"""
        book = self.get_object()
        reviews = book.reviews.select_related('user').all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_review(self, request, slug=None):
        """Thêm đánh giá cho sách"""
        book = self.get_object()
        serializer = ReviewSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # Kiểm tra xem user đã đánh giá sách này chưa
            existing_review = Review.objects.filter(book=book, user=request.user).first()
            if existing_review:
                return Response(
                    {'error': 'Bạn đã đánh giá sách này rồi'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save(book=book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet cho Review model"""
    queryset = Review.objects.select_related('book', 'user').all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['book', 'user', 'rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter reviews theo user nếu không phải admin"""
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Tự động gán user khi tạo review"""
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        """Chỉ cho phép user sở hữu review cập nhật"""
        if serializer.instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Bạn không có quyền cập nhật đánh giá này")
        serializer.save()

    def perform_destroy(self, instance):
        """Chỉ cho phép user sở hữu review hoặc admin xóa"""
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise PermissionError("Bạn không có quyền xóa đánh giá này")
        instance.delete()


# Custom API Views
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


class BookSearchView(ListAPIView):
    """API view cho tìm kiếm sách nâng cao"""
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.select_related('author', 'category').all()
        
        # Tìm kiếm theo từ khóa
        q = self.request.query_params.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(author__name__icontains=q) |
                Q(category__name__icontains=q) |
                Q(isbn__icontains=q)
            )
        
        # Lọc theo giá
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Lọc theo ngôn ngữ
        language = self.request.query_params.get('language', None)
        if language:
            queryset = queryset.filter(language=language)
        
        # Sắp xếp
        ordering = self.request.query_params.get('ordering', '-created_at')
        if ordering:
            queryset = queryset.order_by(ordering)
        
        return queryset


class BookStatisticsView(APIView):
    """API view cho thống kê sách"""
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        """Lấy thống kê tổng quan về sách"""
        total_books = Book.objects.count()
        available_books = Book.objects.filter(status='available', stock_quantity__gt=0).count()
        total_authors = Author.objects.count()
        total_categories = Category.objects.count()
        
        # Thống kê theo danh mục
        category_stats = Category.objects.annotate(
            book_count=Count('books')
        ).values('name', 'book_count')
        
        # Thống kê theo ngôn ngữ
        language_stats = Book.objects.values('language').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Sách có đánh giá cao nhất
        top_rated_books = Book.objects.annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]
        
        top_rated_data = BookListSerializer(
            top_rated_books, many=True, context={'request': request}
        ).data
        
        return Response({
            'total_books': total_books,
            'available_books': available_books,
            'total_authors': total_authors,
            'total_categories': total_categories,
            'category_stats': list(category_stats),
            'language_stats': list(language_stats),
            'top_rated_books': top_rated_data
        })

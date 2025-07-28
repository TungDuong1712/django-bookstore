from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, AuthorViewSet, BookViewSet, ReviewViewSet,
    BookSearchView, BookStatisticsView
)

# Tạo router cho ViewSets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'reviews', ReviewViewSet)

app_name = 'books'

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Custom API endpoints
    path('search/', BookSearchView.as_view(), name='book-search'),
    path('statistics/', BookStatisticsView.as_view(), name='book-statistics'),
] 
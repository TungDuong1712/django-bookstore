from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Admin configuration cho CustomUser model"""
    list_display = [
        'username', 'email', 'full_name', 'user_type', 'is_verified',
        'is_active', 'avatar_preview', 'date_joined'
    ]
    list_filter = [
        'user_type', 'is_verified', 'email_verified', 'is_active',
        'is_staff', 'is_superuser', 'date_joined'
    ]
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering = ['-date_joined']
    
    # Fieldsets cho form edit
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Thông tin cá nhân', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'address')
        }),
        ('Thông tin bổ sung', {
            'fields': ('date_of_birth', 'avatar', 'bio', 'user_type')
        }),
        ('Quyền hạn', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Trạng thái', {
            'fields': ('is_verified', 'email_verified'),
        }),
        ('Thời gian', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    # Fieldsets cho form add
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ['last_login', 'date_joined', 'avatar_preview']
    
    def full_name(self, obj):
        """Hiển thị tên đầy đủ"""
        return obj.full_name
    full_name.short_description = 'Họ và tên'
    
    def avatar_preview(self, obj):
        """Hiển thị preview avatar"""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px;" />',
                obj.avatar.url
            )
        return "Không có ảnh"
    avatar_preview.short_description = 'Ảnh đại diện'
    
    def get_queryset(self, request):
        """Tối ưu queryset"""
        return super().get_queryset(request).select_related()

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Custom User model mở rộng từ AbstractUser"""
    
    # Thêm các trường mới
    phone_number = models.CharField(
        max_length=15, 
        blank=True, 
        verbose_name="Số điện thoại"
    )
    address = models.TextField(
        blank=True, 
        verbose_name="Địa chỉ"
    )
    date_of_birth = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Ngày sinh"
    )
    avatar = models.ImageField(
        upload_to='users/avatars/', 
        blank=True, 
        verbose_name="Ảnh đại diện"
    )
    bio = models.TextField(
        blank=True, 
        verbose_name="Tiểu sử"
    )
    
    # Các choices cho user type
    USER_TYPE_CHOICES = [
        ('customer', 'Khách hàng'),
        ('staff', 'Nhân viên'),
        ('admin', 'Quản trị viên'),
    ]
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='customer',
        verbose_name="Loại người dùng"
    )
    
    # Các trường cho thông tin bổ sung
    is_verified = models.BooleanField(
        default=False, 
        verbose_name="Đã xác thực"
    )
    email_verified = models.BooleanField(
        default=False, 
        verbose_name="Email đã xác thực"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Ngày cập nhật"
    )

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        """Lấy tên đầy đủ của user"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def is_staff_member(self):
        """Kiểm tra có phải nhân viên không"""
        return self.user_type in ['staff', 'admin']

    def get_avatar_url(self):
        """Lấy URL avatar"""
        if self.avatar:
            return self.avatar.url
        return None

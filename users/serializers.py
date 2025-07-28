from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer cho User model"""
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.CharField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone_number', 'address', 'date_of_birth', 'avatar', 'avatar_url',
            'bio', 'user_type', 'is_verified', 'email_verified',
            'date_joined', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'date_joined', 'created_at', 'updated_at',
            'is_verified', 'email_verified'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def get_avatar_url(self, obj):
        """Lấy URL avatar"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer cho việc tạo user mới"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'phone_number', 'address',
            'date_of_birth', 'bio'
        ]
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Mật khẩu không khớp")
        return attrs
    
    def create(self, validated_data):
        """Tạo user mới"""
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer cho việc cập nhật thông tin user"""
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone_number', 'address',
            'date_of_birth', 'avatar', 'bio'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer cho việc đổi mật khẩu"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate(self, attrs):
        """Validate password confirmation"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError("Mật khẩu mới không khớp")
        return attrs
    
    def validate_old_password(self, value):
        """Validate mật khẩu cũ"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Mật khẩu cũ không đúng")
        return value


class LoginSerializer(serializers.Serializer):
    """Serializer cho đăng nhập"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        """Validate thông tin đăng nhập"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Thông tin đăng nhập không đúng")
            if not user.is_active:
                raise serializers.ValidationError("Tài khoản đã bị khóa")
            attrs['user'] = user
        else:
            raise serializers.ValidationError("Vui lòng nhập đầy đủ thông tin")
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer cho profile user (thông tin công khai)"""
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.CharField(read_only=True)
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'first_name', 'last_name', 'full_name',
            'avatar_url', 'bio', 'user_type', 'is_verified',
            'date_joined', 'reviews_count'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'is_verified']
    
    def get_avatar_url(self, obj):
        """Lấy URL avatar"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None
    
    def get_reviews_count(self, obj):
        """Đếm số đánh giá của user"""
        return obj.review_set.count() 
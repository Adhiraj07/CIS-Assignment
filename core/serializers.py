from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Task
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        validators=[validate_password]
    )
    email = serializers.EmailField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        try:
            validate_password(attrs['password'])
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
        return attrs
    
    def create(self, validated_data):
        # Default to USER role unless specified by admin
        if 'role' not in validated_data:
            validated_data['role'] = 'USER'
            
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'is_active': {'read_only': True}
        }
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user': {
                'id': self.user.id,
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role,
                'is_active': self.user.is_active
            }
        })
        return data

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    assigned_to = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
    )
    assigned_by_username = serializers.CharField(source='assigned_by.username', read_only=True)
    assigned_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    
    def validate(self, attrs):
        if 'assigned_by' in attrs:
            raise serializers.ValidationError(
                {"assigned_by": "This field cannot be set manually"}
            )
        return attrs
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'deadline', 
                 'assigned_to', 'assigned_to_username', 'assigned_by_username', 'assigned_by',
                 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'assigned_by_username']

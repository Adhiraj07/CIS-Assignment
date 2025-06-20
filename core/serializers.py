from django.contrib.auth.password_validation import validate_password
from .models import Task
from django.core import exceptions
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Q

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls,user):
        token = super().get_token(user)
        token['role'] = user.role
        return token
    def validate(self,attrs):
        import logging
        logger = logging.getLogger(__name__)
        try:
            logger.info(f"Attempting login for user: {attrs.get('username')}")
            user = User.objects.get(username=attrs.get('username'))
            logger.info(f"User status - is_active: {user.is_active}, last_login: {user.last_login}")
            validated_data = super().validate(attrs)
            logger.info("Login validation succeeded")
            validated_data["user"]={
                "id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
                "role": self.user.role,
                "is_active": self.user.is_active
            }
            return validated_data
        except Exception as e:
            logger.error(f"Login validation failed: {str(e)}")
            raise

class UserSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True,required=True,style={'input_type': 'password'},validators=[validate_password])
    email=serializers.EmailField(required=False,allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'role': {'read_only': True},
            'is_active': {'read_only': True}
        }
        
    def create(self,validated_data):
        #By default we will give USER role
        validated_data['role'] = validated_data.get('role', 'USER')
        user=User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', 'none'),
            password=validated_data['password'],
            role=validated_data['role']
        )
        return user

class TaskSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username')
        
    assigned_by_user = serializers.CharField(source='assigned_by.username', read_only=True)
    assigned_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(Q(role='MANAGER')|Q(role='ADMIN')),
        required=False
    )
    deadline = serializers.DateField(format="%Y-%m-%d")
        
    class Meta:
        model = Task
        fields = ['id','title','description','status','deadline','assigned_to',
        'assigned_by_user','assigned_by','created_at','updated_at']
        read_only_fields = ['created_at','updated_at','assigned_by_user']
    
    def validate(self, attrs):
        if 'assigned_by' not in attrs:
            attrs['assigned_by'] = self.context['request'].user
        elif self.context['request'].user.role not in ['MANAGER', 'ADMIN']:
            raise serializers.ValidationError(
                {"assigned_by": "Only managers or admins can set this field"}
            )
        return attrs

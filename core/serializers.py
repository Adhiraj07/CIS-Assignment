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
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self,field):
        try:
            user = User.objects.get(username=field.get('username'))
            validated_data = super().validate(field)
            validated_data["user"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active
            }
            return validated_data
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "User does not exist"})
        except Exception as e:
            raise serializers.ValidationError({"detail": "Login failed"})

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,style={'input_type': 'password'},validators=[validate_password])
    email = serializers.EmailField(required=False, allow_blank=True)


    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role', 'is_active']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True}
        }
        
    def create(self, validated_data):
        allowed_roles = ['USER', 'MANAGER', 'ADMIN']
        role = validated_data.get('role', 'USER')
        
        if role not in allowed_roles:
            role = 'USER'  #By default


        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=role
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
        request = self.context['request']
    
        # Skip all validation if only updating status
        if set(attrs.keys()) == {'status'}:
            return attrs
            
        # Auto-set assigned_by if not provided
        if 'assigned_by' not in attrs:
            attrs['assigned_by'] = request.user
        
        # Only check assigner for other updates
        if (request.user == self.instance.assigned_to and 
            'assigned_by' in attrs and 
            attrs['assigned_by'] != self.instance.assigned_by):
            raise serializers.ValidationError("Cannot change task assigner")
        
        return attrs

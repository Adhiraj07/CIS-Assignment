from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from .models import User, Task
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, TaskSerializer
from .permissions import IsAdminOrManager, IsAdmin
from rest_framework.exceptions import PermissionDenied

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]
    
    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'MANAGER']:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)
    
    def perform_create(self, serializer):
        if 'assigned_by' in serializer.validated_data:
            raise serializers.ValidationError({"assigned_by": "This field is automatically set"})
        serializer.save(
            assigned_to=serializer.validated_data.get('assigned_to'),
            assigned_by=self.request.user
        )

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [IsAdminOrManager()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'MANAGER']:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        if (self.request.user.role == 'USER' and 
            'assigned_to' in serializer.validated_data):
            raise PermissionDenied("Cannot reassign tasks")
        serializer.save()

class ReactivateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_active = True
        user.save()
        return Response({'status': 'user reactivated'}, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import status
from .models import User,Task
from .serializers import UserSerializer,MyTokenObtainPairSerializer,TaskSerializer
from .permissions import IsAdminOrmanager,IsAdmin
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    GenericAPIView,
    ListCreateAPIView,
    UpdateAPIView
)
import logging

class MyTokenObtainPairView(TokenObtainPairView):
    #for login this will give the accesss and refresh token
    serializer_class=MyTokenObtainPairSerializer

class UserRegisterView(CreateAPIView):
    # Only admin can create new users
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAdmin]

class UserListView(ListAPIView):
    #userlist in this view only admin and manager can see all users
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated,IsAdminOrmanager]

class UserDetailView(RetrieveUpdateDestroyAPIView):
    #userdetailview in this view only admin and manager can see all users and user can see only his own details
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[IsAuthenticated,IsAdminOrmanager]

    def destroy(self,request,*args,**kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        
        return Response({'detail':'User deleted'},status=status.HTTP_200_OK)

class TaskCreateListView(ListCreateAPIView):
    #tasklistview in this view only admin and manager can see all tasks
    serializer_class=TaskSerializer
    permission_classes=[IsAuthenticated,IsAdminOrmanager]
    def get_queryset(self):
        if self.request.user.role in ['ADMIN','MANAGER']:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)

class TaskDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            # Get task ID without fetching object
            task_id = self.kwargs.get('pk')
            task = Task.objects.filter(id=task_id).first()
            if task and task.assigned_to != self.request.user and self.request.user.role not in ['ADMIN', 'MANAGER']:
                raise PermissionDenied("You do not have permission to view this...")
                
        elif self.request.method == 'DELETE':
            if self.request.user.role != 'ADMIN':
                raise PermissionDenied("admins can deleteonly")
                
        elif self.request.method in ['PUT', 'PATCH']:
            task_id = self.kwargs.get('pk')
            task = Task.objects.filter(id=task_id).first()
            if task and task.assigned_to != self.request.user and self.request.user.role not in ['ADMIN', 'MANAGER']:
                raise PermissionDenied("You do not have permission to modify this...")
                
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role in ['ADMIN', 'MANAGER']:
            return Task.objects.all()
        return Task.objects.filter(assigned_to=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.role == 'USER' and 'assigned_to' in serializer.validated_data:
            raise PermissionDenied("You cannot reassign tasks")
        serializer.save()

class LogoutView(GenericAPIView):   
    permission_classes=[IsAuthenticated]
    

    def post(self,request,*args,**kwargs):
        if "refresh_token" not in request.data:
            return Response({"error":"refresh_token is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail":"Sucessfully logout"},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)

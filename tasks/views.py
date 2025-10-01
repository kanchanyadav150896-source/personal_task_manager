from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.shortcuts import get_object_or_404

from .models import Task
from .serializers import TaskSerializer
from .permissions import IsAssignedUser

from rest_framework.views import APIView
from django.contrib.auth import authenticate

from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Welcome to Personal Tasks API"})

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        # Only return tasks for the current user
        return Task.objects.filter(assigned_to=self.request.user).order_by('-created_at')


    def perform_create(self, serializer):
        serializer.save(assigned_to=self.request.user)


    def get_permissions(self):
        # For update/delete detail
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsAssignedUser]
        else:
            self.permission_classes = [IsAuthenticated]
            return super().get_permissions()


class ObtainTokenView(APIView):
    permission_classes = []
    authentication_classes = []


    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
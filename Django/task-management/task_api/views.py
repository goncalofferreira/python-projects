from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class TaskViewSet(viewsets.ModelViewSet):    
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Apenas tarefas do utilizador autenticado        
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Define o dono como o utilizador autenticado
        serializer.save(owner=self.request.user)

    @method_decorator(cache_page(60*2))  # cache por 2 minutos
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def completed(self, request):
        # Endpoint personalizado: /tasks/completed/
        tasks = self.get_queryset().filter(completed=True)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

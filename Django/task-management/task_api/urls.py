from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

# automatiza a criação de URLs para as views baseadas em ViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
]

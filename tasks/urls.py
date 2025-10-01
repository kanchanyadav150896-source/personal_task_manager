from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ObtainTokenView, home


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')


urlpatterns = [
    path('', home),
    path('api/token/', ObtainTokenView.as_view(), name='api-token'),
    path('api/', include(router.urls)),
    
]
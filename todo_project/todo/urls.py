from django.urls import path, include
from rest_framework.routers import DefaultRouter
from todo.views import Registration, Login, ToDoViewSet


router = DefaultRouter()
router.register('todos', ToDoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', Registration.as_view({'post': 'create'})),
    path('login/', Login.as_view({'post': 'create', 'delete': 'destroy'})),
]

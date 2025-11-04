from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.habits.views import HabitViewSet, PublicHabitListAPIView
from apps.habits.views import index

app_name = 'habits'

router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

urlpatterns = [
    path('', index, name='index'),
    path('public/', PublicHabitListAPIView.as_view(), name='habit-public-list'),
    path('', include(router.urls)),
]

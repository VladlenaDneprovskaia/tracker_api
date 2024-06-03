from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from habits.viewsets import HabitViewSet, CheckInViewSet

app_name = 'habits'

habit_router = SimpleRouter()
habit_router.register(r'habits', HabitViewSet, basename='habit')

checkins_router = NestedSimpleRouter(habit_router, r'habits', lookup='habit')
checkins_router.register(r'checkins', CheckInViewSet, basename='checkin')

urlpatterns = [
    path(r'', include(habit_router.urls)),
    path(r'', include(checkins_router.urls)),
]

from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter

from coaches.viewsets import MenteeViewSet, CoachViewSet, RecommendationViewSet

app_name = 'coaches'

coaches_router = SimpleRouter()
coaches_router.register(r'coaches', CoachViewSet, basename='coach')

mentees_router = NestedSimpleRouter(coaches_router, r'coaches', lookup='coach')
mentees_router.register('mentees', MenteeViewSet, basename='mentee')

recommendation_router = NestedSimpleRouter(mentees_router, r'mentees', lookup='mentee')
recommendation_router.register('recommendations', RecommendationViewSet, basename='recommendation')

urlpatterns = [
    path(r'', include(coaches_router.urls)),
    path(r'', include(mentees_router.urls)),
    path(r'', include(recommendation_router.urls)),
]

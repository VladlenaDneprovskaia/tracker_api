from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView, SpectacularAPIView

from tracker.views import RegistrationView, RefreshTokenView, AccessTokenView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include('habits.urls', 'habits'), name='habits'),
    path('api/', include('coaches.urls', 'coaches'), name='coaches'),

    path('api/auth/registration/', RegistrationView.as_view(), name='registration'),
    path('api/auth/token/', AccessTokenView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

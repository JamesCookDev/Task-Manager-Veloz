from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )
from app.views import SignUpView


def root_redirect(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


urlpatterns = [
    path('', root_redirect, name='root'),
    path('admin/', admin.site.urls),
    path('', include('app.urls')),

    # API routes
    path('api/v1/', include('app.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

     # Authentication (Django default auth views)
    path('accounts/', include('django.contrib.auth.urls')), 
]


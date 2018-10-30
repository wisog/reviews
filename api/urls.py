from django.urls import path
from django.conf.urls import include

from rest_framework_swagger.views import get_swagger_view

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import ReviewViewSet, UserListView

schema_view = get_swagger_view(title='Reviews API')

urlpatterns = [
    path('', UserListView.as_view()),
    path(r'docs/', schema_view),
    path(r'token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(r'token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(r'auth/', include('rest_auth.urls')),
    path(r'reviews/', ReviewViewSet.as_view({ 'get': 'list', 'post': 'create' }), name='reviews'),
    path(r'reviews/<int:review_id>/', ReviewViewSet.as_view({'get': 'retrieve'}), name='review'),
]
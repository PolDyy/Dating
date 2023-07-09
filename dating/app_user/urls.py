from django.urls import path, include
from .views import UserViewSet

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path("clients/create",
         UserViewSet.as_view(
             {
                 "post": "create",

             }
         ), ),
    path("list",
         UserViewSet.as_view(
             {
                 "get": "list",

             }
         ), ),
]

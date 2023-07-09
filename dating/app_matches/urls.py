from django.urls import path, include
from .views import MatchAPIView

urlpatterns = [
    path("clients/<int:id>/match",
         MatchAPIView.as_view(), ),
]

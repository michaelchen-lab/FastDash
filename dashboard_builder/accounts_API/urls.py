from django.urls import path
from .views import UserList, CustomTokenObtainPairView

urlpatterns = [
    path('users/', UserList.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
]
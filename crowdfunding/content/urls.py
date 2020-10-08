from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('content/<int:pk>/upload', views.OwnerImageLibrary.as_view()),
    path('content/<int:pk>/', views.ProjectDetail.as_view()),
    path('content/', views.ProjectList.as_view()),
    path('pledges/', views.PledgeList.as_view())
]
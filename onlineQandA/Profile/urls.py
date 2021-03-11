from django.urls import path
from . import views

urlpatterns = [
    # path('',views.home),
    path('profile/edit', views.editprofile, name="edit-profile"),
    path('profile', views.profile, name="profile")
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Root URL pattern
    path('signup/', views.signup, name='signup'),
    # Other URL patterns
]

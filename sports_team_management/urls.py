
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path('auth/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', accounts_views.index, name='index'),  # Add this line
]


from django.contrib import admin
from django.urls import path, include

import user, dashboard

urlpatterns = [
    path('', include('dashboard.urls'), name='dashboard'),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls'), name='user'),
]

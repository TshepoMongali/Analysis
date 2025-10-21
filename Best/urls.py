from django.urls import path, include
from django.contrib import admin
from analysis import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('analysis.urls')),
    path('', views.index, name='home'),  # this handles the root URL
]



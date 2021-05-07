from django.contrib import admin
from django.urls import path, include

#from user.views import RequestCountView, RequestCountResetView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('movie_collection.urls')),
    
]

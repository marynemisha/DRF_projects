"""
URL configuration for NoteManagement project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from notes import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view()),
    path('users/',views.UserView.as_view()), 
    path('login/',obtain_auth_token),
    path('notes/',views.NoteListCreateView.as_view()),
    path('notes/<int:pk>/',views.Notesview.as_view()),
    path('jwt_login/',TokenObtainPairView.as_view()),
    path('refresh/',TokenRefreshView.as_view()),
    path('tasks/',views.TaskView.as_view()),
    path('tasks/<int:id>/',views.TaskRetrieveUpdateDeleteView.as_view()),
    path('jwt_logout/',views.JWT_Logout.as_view())
]

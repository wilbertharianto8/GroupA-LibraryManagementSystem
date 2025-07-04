"""
URL configuration for online_library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name='users'),
    path('book-management/', include('book_management.urls'), name='book_management'),
    path('books/', include('books.urls'), name='books'),
    path('search/', views.search_books, name='search_books'),
    path('borrow/', include('borrow.urls'), name='borrow'),
    path('borrow_history/', include('borrow_history.urls'), name='borrow_history'),
    path('return/', include('return.urls'), name='return'),
    path('aboutus/', views.about, name='about'),
    path('contactus/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('',views.home,name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

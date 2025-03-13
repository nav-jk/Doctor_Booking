from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import get_superuser_details


urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('book-token/', views.book_token, name='book_token'),  # Patient token booking
    path('view-tokens/', views.view_tokens, name='view_tokens'),  # View tokens page
    path('doctor-dashboard/', views.doctor_dashboard, name='doctor_dashboard'),  # Doctor's dashboard
    path('doctor-login/', auth_views.LoginView.as_view(template_name='doctor_login.html'), name='doctor_login'),
    path('doctor-logout/', auth_views.LogoutView.as_view(next_page='home'), name='doctor_logout'),
    path('delete-date/<int:date_id>/', views.delete_date, name='delete_date'),
    path('delete-token/<int:token_id>/', views.delete_token, name='delete_token'),
     path("superuser-details/", get_superuser_details, name="superuser_details"),

]




    

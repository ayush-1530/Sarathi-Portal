from django.urls import path
from .import views
from django.views.generic import TemplateView

urlpatterns = [
    path ('', views.search_user, name='search_user'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path("error/", TemplateView.as_view(template_name="error.html"), name="error"),
    path("success/", TemplateView.as_view(template_name="success.html"), name="success")
]
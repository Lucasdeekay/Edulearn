from django.urls import path, include

from School import views

app_name = "School"

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("faq", views.faq, name="faq"),
    path("contact", views.contact, name="contact"),
]
from django.urls import path
from .views import Scrape

urlpatterns = [
    path("scrape/", Scrape.as_view()),
]
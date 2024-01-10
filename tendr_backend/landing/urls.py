from django.urls import path
from .views import Scrape, Search

urlpatterns = [
    path("scrape/", Scrape.as_view()),
    path("search/", Search.as_view()),
]
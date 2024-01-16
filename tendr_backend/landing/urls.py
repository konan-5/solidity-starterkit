from django.urls import path
from .views import Scrape, Search, ViewMore

urlpatterns = [
    path("scrape/", Scrape.as_view()),
    path("search/", Search.as_view()),
    path("view-more/", ViewMore.as_view()),
]
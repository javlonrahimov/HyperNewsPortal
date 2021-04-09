from django.urls import path
from .views import MainMenu, NewsFromJSON, CreateNews, ComingSoon

urlpatterns = [
    path('', ComingSoon.as_view(), name='home'),
    path('news/', MainMenu.as_view(), name='home_news'),
    path('news', MainMenu.as_view(), name='home_news'),
    path('news/create', CreateNews.as_view(), name='create'),
    path('news/create/', CreateNews.as_view()),
    path('news/<int:news_id>/', NewsFromJSON.as_view(), name='detail')
]

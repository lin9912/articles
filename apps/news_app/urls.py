from django.urls import path
from . import views

app_name = 'news_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('article_detail/<article_id>', views.article_detail, name='article_detail'),
    path('write_article/', views.write_article, name='write_article'),
    path('article_management/<username>', views.article_management, name='article_management'),
    path('delete/<article_id>', views.delete_article, name='delete'),
    path('edit/<article_id>', views.edit_article, name='edit'),
    path('search/', views.search, name='search'),
    path('category/<category_name>', views.category_page, name='category'),
]
from django.urls import path
# Импортируем созданное нами представление
from .views import *
from django.views.decorators.cache import cache_page
import logging


# Начало теста логгирования
logger_dr = logging.getLogger('django.request')
logger_cn = logging.getLogger('django')

logger_dr.error("Hello! I'm error in your app. Enjoy:)")
logger_cn.error("Hello! I'm error in your app. Enjoy:)")
# Конец теста логгирования

urlpatterns = [
   path('', cache_page(60*1)(PostsList.as_view()), name = 'posts_list'),
   path('search/', PostsSearch.as_view()),
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения
   path('<int:pk>', cache_page(60*5)(PostDetail.as_view()), name = 'post_detail'),# добавим кэширование на детали поста. Раз в 5 минут пост будет записываться в кэш для экономии ресурсов.
   path('create/', ArticlesCreate.as_view(), name='articles_create'),
   path('<int:pk>/edit/', ArticlesEdit.as_view(), name='articles_edit'),
   path('<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('test/', index_test, name='index_test'),
]
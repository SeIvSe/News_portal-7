from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from django.shortcuts import render, reverse, redirect
from .models import *
from django.core.mail import send_mail
from .filters import PostFilter
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver, Signal
from django.http import HttpResponse

# включаем логирование
import logging
# ниже  можно в качестве параметра подставлять все описанные loggers
# если есть необходимость отлавливать сообщения из разных модулей
# тогда можно в качестве параметра использовать __name__
# но при этом в settings.py.LOGGING нужно описать иерархию логеров
# и использовать propagate для исключения двойной обработки сообщений
# разными логерами находящимися в одной иерархии
# logger = logging.getLogger('file_general')
logger = logging.getLogger('django')


def index_test(request):
    # отправим сообщение разного уровня
    logger.debug("Hello! --------DEBUG--------Enjoy:)")
    logger.info("Hello! --------INFO--------Enjoy:)")
    logger.warning("Hello! --------WARNING--------Enjoy:)")
    logger.error("Hello! --------ERROR--------Enjoy:)")
    logger.critical("Hello! --------CRITICAL--------Enjoy:)")
    return HttpResponse("<p> Сообщение для тестирования </p>")

class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-dateCreation'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10 # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = Post
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'post'


class PostsSearch(ListView):
    form_class = SearchForm
    model = Post
    template_name = 'post_list.html'
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context

addpost = Signal()

class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = CreateForm
    model = Post
    template_name = 'news_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)

# Добавляем представление для изменения новости.
class NewsEdit(PermissionRequiredMixin, UpdateView):
    form_class = CreateForm
    model = Post
    template_name = 'news_edit.html'
    permission_required = ('news.edit_post',)

# Представление удаляющее товар.
class NewsDelete(DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('posts_list')


class ArticlesCreate(PermissionRequiredMixin, CreateView):
    form_class = CreateForm
    model = Post
    template_name = 'articles_create.html'
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        return super().form_valid(form)

# Добавляем представление для изменения новости.
class ArticlesEdit(PermissionRequiredMixin, UpdateView):
    form_class = CreateForm
    model = Post
    template_name = 'articles_edit.html'
    permission_required = ('news.edit_post',)

# Представление удаляющее товар.
class ArticlesDelete(DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('posts_list')


@login_required
def add_subscribe(request, pk):
    pk = id #новости (например 46)
    user = request.user
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    category = Category.objects.get(name=category_object_name)

    # Делаем запись в поле subscribe модели Category
    add_subscribe = Category.objects.get(name=category_object_name)
    add_subscribe.subscribers = user
    add_subscribe.save()
    user.category_set.add(add_subscribe)

    # # Вариант 2. Используем для хранения списка подписавшихся пользователей встроенные в auth.models группы
    # Group.objects.get_or_create(name=category_object_name)
    # category_group = Group.objects.get(name=category_object_name)
    # if not request.user.groups.filter(name=category_object_name).exists():
    #     category_group.user_set.add(user)

    send_mail(
        subject=f'News Portal: {category_object_name}',
        message=f'Доброго дня, {request.user}! Вы подписались на уведомления о выходе новых статей в категории {category_object_name}',
        from_email='andreitestivanov@yandex.ru',
        recipient_list=[user.email, ],
    )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def del_subscribe(request, pk):
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    del_subscribe = Category.objects.get(name=category_object_name)
    del_subscribe.subscribers = None
    del_subscribe.save()
    user = request.user

    # # Вариант 2. Используем для хранения списка подписавшихся пользователей встроенные в auth.models группы
    # category_group = Group.objects.get(name=category_object_name)
    # category_group.user_set.remove(user)

    send_mail(
        subject=f'News Portal: {category_object_name}',
        message=f'Доброго дня, {request.user}! Вы отменили уведомления о выходе новых статей в категории {category_object_name}. Нам очень жаль, что данная категория Вам не понравилась, ждем Вас снова на нашем портале!',
        from_email='andreitestivanov@yandex.ru',
        recipient_list=[user.email, ],
    )
    return redirect(request.META.get('HTTP_REFERER'))
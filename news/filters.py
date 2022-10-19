from django_filters import FilterSet, DateFilter
from django.forms import DateInput
from .models import Post

# Создаем свой набор фильтров для модели Post.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    added_after = DateFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateInput(
            format='%Y-%m-%d',
            attrs={'type': 'date'}
        ),
    )
    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       fields = {
           # поиск по названию
           'title': ['icontains'],
           # поиск по категории
           'categoryType': ['exact'],
       }
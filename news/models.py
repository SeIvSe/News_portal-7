import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models import  Sum
from django.urls import reverse
from django.core.cache import cache

# Create your models here.
class Author (models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category (models.Model):
    name = models.CharField(max_length=64, unique=True)
    subscribers = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.name}'


class Post (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )
    categoryType = models.CharField(max_length=2, choices= CATEGORY_CHOICES)
    dateCreation = models.DateField(auto_now_add=True)
    postCategory = models.ManyToManyField (Category, through='PostCategory', default = 'History')
    title = models.CharField(max_length=128, unique=True)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.title.title()} ({self.dateCreation.strftime("%d.%m.%y")}): {self.text[:20]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def category(self):
        category_object = PostCategory.objects.get(postThrough=self.id)
        category_object_name = category_object.categoryThrough
        category = Category.objects.get(name=category_object_name)
        return category

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его



class PostCategory (models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.categoryThrough} | {self.postThrough}'


class CategorySubscribers(models.Model):
    subscriber_thru = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,)
    category_thru = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,)


class Comment (models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
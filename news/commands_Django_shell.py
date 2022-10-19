############### Команды для исполнения в Django shell ####################
# 1.
# >>> u1 = User.objects.create_user(username='Sergey')
# >>> u2 = User.objects.create_user(username='Andrei')
#
# 2.
# >>> Author.objects.create(authorUser=u1)
# <Author: Author object (1)>
# >>> Author.objects.create(authorUser=u2)
# <Author: Author object (2)>
#
# 3.
# >>> Category.objects.create(name='IT')
# <Category: Category object (1)>
# >>> Category.objects.create(name='Crime')
# <Category: Category object (2)>
# >>> Category.objects.create(name='City')
# <Category: Category object (3)>
# >>> Category.objects.create(name='Auto')
# <Category: Category object (4)>
#
# 4.
# >>> author = Author.objects.get(id=1)
# >>> Post.objects.create(author=author, categoryType='NW', title='sometitle', text='VERYB
# IGTEXT')
# >>> Post.objects.create(author=author, categoryType='AR', title='Article1', text='textAr
# ticle1')
# <Post: Post object (2)>
# >>> Post.objects.create(author=author, categoryType='AR', title='Article2', text='textAr
# ticle2')
# <Post: Post object (3)>
#
# 5.
# >>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=1))
# >>> Post.objects.get(id=1).postCategory.add(Category.objects.get(id=2))
#
# 6.
# >>> Comment.objects.create(commentPost=Post.objects.get(id=1), commentUser=Author.object
# s.get(id=1).authorUser, text='bigtextauthor')
# <Comment: Comment object (1)>
# >>> Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.object
# s.get(id=1).authorUser, text='bigdata its cool')
# <Comment: Comment object (2)>
# >>> Comment.objects.create(commentPost=Post.objects.get(id=2), commentUser=Author.object
# s.get(id=2).authorUser, text='ooo yaaah')
# <Comment: Comment object (3)>
# >>> Comment.objects.create(commentPost=Post.objects.get(id=3), commentUser=Author.object
# s.get(id=1).authorUser, text='Iam byba')
# <Comment: Comment object (4)>
#
# 7.
# >>> Comment.objects.get(id=1).like()
# >>> Comment.objects.get(id=1).like()
# >>> Comment.objects.get(id=1).like()
# >>> Comment.objects.get(id=1).like()
# >>> Comment.objects.get(id=1).rating
# 4
# >>> Comment.objects.get(id=2).like()
# >>> Comment.objects.get(id=2).like()
# >>> Comment.objects.get(id=2).like()
# >>> Comment.objects.get(id=2).dislike()
# >>> Comment.objects.get(id=2).rating
# 2
# >>> Comment.objects.get(id=3).dislike()
# >>> Comment.objects.get(id=3).dislike()
# >>> Comment.objects.get(id=3).dislike()
# >>> Comment.objects.get(id=3).dislike()
# >>> Comment.objects.get(id=3).rating
# -4
# >>> Post.objects.get(id=3).like()
# >>> Post.objects.get(id=3).rating
# 1
# >>> Post.objects.get(id=3).like()
# >>> Post.objects.get(id=3).like()
# >>> Post.objects.get(id=3).rating
# 2
#
# 8.
# >>> a=Author.objects.get(id=1)
# >>> a.update_rating()
# >>> a.ratingAuthor
# 6
# >>> Post.objects.get(id=1).like()
# >>> a.update_rating()
# >>> a.ratingAuthor
# 9
# >>> a = Author.objects.order_by('-ratingAuthor')
# >>> a
# <QuerySet [<Author: Author object (1)>, <Author: Author object (2)>]>
#
# 9.
# >>> for i in a:
# ...    i.ratingAuthor
# ...    i.authorUser.username
# ...
# 9
# 'Sergey'
# 0
# 'Andrei'
#
# 10.
# >>> w = Post.objects.order_by('-rating')
# >>> for i in w:
# ...     i.dateCreation
# ...     i.author
# ...     i.rating
# ...     i.title
# ...     i.text[0:4]+'...'
# ...
# datetime.datetime(2022, 7, 29, 18, 2, 46, 199143, tzinfo=datetime.timezone.utc)
# <Author: Author object (1)>
# 2
# 'Article2'
# 'text...'
# datetime.datetime(2022, 7, 29, 17, 56, 11, 113842, tzinfo=datetime.timezone.utc)
# <Author: Author object (1)>
# 1
# 'sometitle'
# 'VERY...'
# datetime.datetime(2022, 7, 29, 18, 2, 32, 385441, tzinfo=datetime.timezone.utc)
# <Author: Author object (1)>
# 0
# 'Article1'
# 'text...'
#
# 11.
# # Выводим все комментарии
# >>> q = Comment.objects.order_by()
# >>> for i in q:
# ...     i.dateCreation
# ...     i.commentUser
# ...     i.rating
# ...     i.text
# ...
# datetime.datetime(2022, 7, 29, 18, 19, 12, 821179, tzinfo=datetime.timezone.utc)
# <User: Sergey>
# 4
# 'bigtextauthor'
# datetime.datetime(2022, 7, 29, 18, 21, 22, 804637, tzinfo=datetime.timezone.utc)
# <User: Sergey>
# 2
# 'bigdata its cool'
# datetime.datetime(2022, 7, 29, 18, 21, 46, 484568, tzinfo=datetime.timezone.utc)
# <User: Andrei>
# -4
# 'ooo yaaah'
# datetime.datetime(2022, 7, 29, 18, 22, 37, 21642, tzinfo=datetime.timezone.utc)
# <User: Sergey>
# 0
# 'Iam byba'
#
#
# #Либо выводим комментарии (как в моем примере) к посту с id=2 (так как именно ко 2
#  посту добавил 2 комментария)
# >>> q = Comment.objects.order_by()
# >>> a = Post.objects.get(id=2)
# >>> for i in q:
# ...     if i.commentPost == a:
# ...             i.dateCreation
# ...             i.commentUser
# ...             i.rating
# ...             i.text
# ...
# datetime.datetime(2022, 7, 29, 18, 21, 22, 804637, tzinfo=datetime.timezone.utc)
# <User: Sergey>
# 2
# 'bigdata its cool'
# datetime.datetime(2022, 7, 29, 18, 21, 46, 484568, tzinfo=datetime.timezone.utc)
# <User: Andrei>
# -4
# 'ooo yaaah'
#
# Таким же образом можно проверить каждый пост на наличие комментариев.

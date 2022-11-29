from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    rating_author = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        self.rating_author = 0
        self.rating_post = 0
        self.rating_author_comm = 0
        self.rating_comm = 0
        for post in Post.objects.filter(author_rel_id=self.id):
            self.rating_post += post.rating_post * 3
            for comment in Comment.objects.filter(comm_post=post):
                self.rating_author_comm += comment.rating_comment
        for comment in Comment.objects.filter(comm_us=self.author):
            self.rating_comm += comment.rating_comment

        self.rating_author = self.rating_post + self.rating_author_comm + self.rating_comm

        self.save()

class Category(models.Model):
    topic = models.CharField(max_length=255, unique=True)

class Content_type(models.TextChoices):
    ARTICLE = 'ART', 'Статья'
    NEWS = "NEWS", 'Новости'


class Post(models.Model):
    type_content = models.CharField(max_length=4,
                                    choices=Content_type.choices,
                                    default=Content_type.ARTICLE)
    article = models.CharField(max_length=255,
                               default="Тут может быть ваш заголовок")
    text_post = models.TextField()
    datetime_post = models.DateTimeField(auto_now_add=True)
    rating_post = models.IntegerField(default=0)
    author_rel = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_rel = models.ManyToManyField(Category, through='PostCategory')

    def like_post(self):
        self.rating_post += 1
        self.save()

    def dislike_post(self):
        self.rating_post -= 1
        self.save()

    def preview_post(self):
        self.text_post = self.text_post[0:124] + '...'
        self.save()


class Comment(models.Model):
    text_comment = models.TextField()
    datetime_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    comm_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comm_us = models.ForeignKey(User, on_delete=models.CASCADE)


    def like_com(self):
        self.rating_comment += 1
        self.save()

    def dislike_com(self):
        self.rating_comment -= 1
        self.save()



class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)




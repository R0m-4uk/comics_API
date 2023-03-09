from django.contrib.auth.models import User
from django.db import models


# --{ Комикс }--
class Format(models.Model):
    title = models.CharField(max_length=16, null=False, blank=False, unique=True)

    def __str__(self):
        return self.title


class AgeLimit(models.Model):
    title = models.IntegerField(null=False, blank=False, unique=True)

    def __str__(self):
        return f"{self.title}+"


class Available(models.Model):
    title = models.CharField(max_length=16, null=False, blank=False, unique=True)

    def __str__(self):
        return self.title


class Comics(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False)
    image = models.ImageField()
    description = models.TextField()
    price = models.FloatField()
    format = models.ForeignKey(Format, on_delete=models.SET_NULL, null=True)
    page_count = models.IntegerField()
    weight = models.FloatField()
    age_limit = models.ForeignKey(AgeLimit, on_delete=models.SET_NULL, null=True)
    available = models.ForeignKey(Available, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


# --{ АВТОР }--
class Post(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    username = models.CharField(max_length=64, null=False, blank=False)
    image = models.ImageField()
    description = models.TextField()
    post = models.OneToOneField(Post, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'"{self.username}" - "{self.post.title}"'


class ComicsAuthor(models.Model):
    comics = models.ForeignKey(Comics, on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'"{self.comics.title}" - "{self.author.username}"'


# --{ Доставка }--
class Delivery(models.Model):
    title = models.CharField(max_length=32, null=False, blank=False, unique=True)

    def __str__(self):
        return self.title


class ComicsDelivery(models.Model):
    comics = models.ForeignKey(Comics, on_delete=models.SET_NULL, null=True)
    delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'"{self.comics.title}" - "{self.delivery.title}"'


# --{ Корзина }--
class Cart(models.Model):
    comics = models.ForeignKey(Comics, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return f'"{self.comics.title}" - "{self.user.username}"'

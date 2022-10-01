
from pyexpat import model
from unicodedata import category
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    premium = models.BooleanField(default=False)
    coins = models.IntegerField(default=0)
    shared_fact_counts = models.IntegerField(default=0)
    last_seen = models.DateTimeField(auto_now_add=True)
    streak = models.IntegerField(default=0)
    premium_start_date = models.DateField(null=True)
    premium_end_date = models.DateField(null=True)


class Category(models.Model):
    name = models.CharField(max_length=20)
    imgURL = models.URLField(null=True)
    isPremium = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Fact(models.Model):
    fact = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    imgURL = models.URLField(null=True)
    imgURL2 = models.URLField(null=True, blank=True)
    ref = models.URLField(null=True, blank=True)
    desc = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.fact[:20]


class DailyFact(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now_add=True)


class BookMark(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fact', 'user',)


class Like(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fact', 'user',)


class Reward(models.Model):
    title = models.CharField(max_length=30)
    discount = models.CharField(max_length=30)
    preCoin = models.IntegerField()
    newCoin = models.IntegerField()
    imgURL = models.URLField()

    def __str__(self) -> str:
        return self.title


class Subscription(models.Model):
    cost = models.IntegerField()
    type = models.CharField(max_length=20)
    duration = models.IntegerField()
    description = models.CharField(max_length=50, null=True)


class UserTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_number = models.IntegerField()


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
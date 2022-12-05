
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    premium = models.BooleanField(default=False)
    coins = models.IntegerField(default=0)
    shared_fact_counts = models.IntegerField(default=0)
    last_seen = models.DateTimeField(auto_now=True)
    streak = models.IntegerField(default=0)
    premium_start_date = models.DateField(null=True)
    premium_end_date = models.DateField(null=True)
    avtar = models.IntegerField(default=0, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=20)
    description: models.CharField(max_length=50,blank=True,null=True)
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
    isAd = models.BooleanField(default=False, null=True)

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
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    duration = models.IntegerField()
    cost = models.IntegerField()
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


class CategoryRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    # Status 0 Waiting, Status 1 Accepted, Status 2 Rejected
    status = models.IntegerField(default=0)


class ReportFact(models.Model):
    fact = models.ForeignKey(Fact, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    reason = models.TextField()
    description = models.TextField()

    class Meta:
        unique_together = ('fact', 'email',)

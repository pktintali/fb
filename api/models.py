
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to="profile_pics/", blank=True)
    premium = models.BooleanField(default=False)
    redeemedPremium = models.BooleanField(default=False,verbose_name='Redeemed')
    coins = models.IntegerField(default=50)
    shared_fact_counts = models.IntegerField(default=0,verbose_name='Shared')
    last_seen = models.DateTimeField(auto_now=True)
    streak = models.IntegerField(default=0)
    premium_start_date = models.DateField(null=True)
    premium_end_date = models.DateField(null=True)
    avtar = models.IntegerField(default=0, blank=True, null=True)
    
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

# Using Custom AuthModel to Allow user login with either username or password
class AuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            try:
                user = UserModel.objects.get(email=username)
            except UserModel.DoesNotExist:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a nonexistent user (#20760).
                UserModel().set_password(password)
            else:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user


class Category(models.Model):
    name = models.CharField(max_length=20)
    language = models.CharField(max_length=20,default='english')
    desc= models.CharField(max_length=50, null=True)
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
        # return self.fact[:20]
        return self.fact[:150]


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

    class Meta:
        verbose_name = "Coupon"
        verbose_name_plural = "Coupons"


#! Not in use in production
class Subscription(models.Model):
    cost = models.IntegerField()
    type = models.CharField(max_length=20)
    duration = models.IntegerField()
    description = models.CharField(max_length=50, null=True)


class UserTasks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_number = models.IntegerField()
    
    class Meta:
        unique_together = ('user', 'task_number',)


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'category',)


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

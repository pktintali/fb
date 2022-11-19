from django.contrib import admin

from api.models import *

# Register your models here.
admin.site.register([User, Category, Fact, BookMark,
                    Like, Reward, Subscription, UserTasks, DailyFact, CategoryRequest, ReportFact, UserInterest])

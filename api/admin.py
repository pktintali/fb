from django.contrib import admin
from django.utils.html import format_html

from api.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'first_name', 'last_name', 'email', 'last_seen',
                    'coins', 'avtar', 'streak', 'shared_fact_counts', 'premium', 'redeemedPremium', 'premium_end_date']
    list_filter = ['premium', 'redeemedPremium',
                   'last_seen', 'premium_end_date']
    search_fields = ['username', 'first_name', 'last_name']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'desc',
                    '_language', 'image_url', 'isPremium']
    list_display_links = ['image_url']
    list_filter = ['isPremium', 'language']
    search_fields = ['desc', 'name']

    def image_url(self, obj):
        return obj.imgURL[:50] + '...' if len(obj.imgURL) > 50 else obj.imgURL

    def _language(self, obj):
        if obj.language == 'hindi':
            return format_html('<span style="color:yellow;">Hindi</span>')
        else:
            return format_html('<span style="color:green;">English</span>')
    _language.allow_tags = True


class FactAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact_', 'category', 'premium', 'timestamp', 'isAd']
    list_display_links = ['fact_']
    list_filter = ['isAd', 'category__isPremium']
    search_fields = ['fact', 'desc']
    list_select_related = True

    def fact_(self, obj):
        return obj.fact[:100] + '...' if len(obj.fact) > 100 else obj.fact

    def premium(self, obj):
        if obj.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium.allow_tags = True


class DailyFactAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact', 'premium_cat', 'date']
    list_editable = ['fact']

    def premium_cat(self, obj):
        if obj.fact.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium_cat.allow_tags = True


class BookMarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact', 'category', 'pc', 'user',
                    'pu',  'timestamp']
    list_filter = ['timestamp', 'user__premium',
                   'fact__category__isPremium']
    search_fields = ['user__username', 'fact__category__name']
    search_help_text = 'Search in [username] [category]'

    def category(self, obj):
        return obj.fact.category

    def pu(self, obj):
        if (obj.user.premium or obj.user.redeemedPremium):
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    pu.allow_tags = True

    def pc(self, obj):
        if obj.fact.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    pc.allow_tags = True


class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact', 'category', 'pc', 'user',
                    'pu',  'timestamp']
    list_filter = ['timestamp', 'user__premium',
                   'fact__category__isPremium']
    search_fields = ['user__username', 'fact__category__name']
    search_help_text = 'Search in [username] [category]'

    def category(self, obj):
        return obj.fact.category

    def pu(self, obj):
        if (obj.user.premium or obj.user.redeemedPremium):
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    pu.allow_tags = True

    def pc(self, obj):
        if obj.fact.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    pc.allow_tags = True


class CouponAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'cost', 'image_url']
    list_display_links = ['image_url']
    list_filter = ['cost']
    search_fields = ['title', 'description', 'cost']
    search_help_text = 'Search in [title] [description] [cost]'

    def image_url(self, obj):
        return obj.imgURL[:50] + '...' if len(obj.imgURL) > 50 else obj.imgURL


class UserTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'premium_user', 'task_number']
    # list_display_links = []
    list_filter = ['user__premium', 'task_number']
    search_fields = ['user']
    search_help_text = 'Search in [user]'

    def premium_user(self, obj):
        if (obj.user.premium or obj.user.redeemedPremium):
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')


class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'premium_user',
                    'category', 'premium_category', 'timestamp']
    # list_display_links = []
    list_filter = ['user__premium', 'category__isPremium', 'timestamp']
    search_fields = ['user', 'category']
    search_help_text = 'Search in [user] [category]'

    def premium_user(self, obj):
        if (obj.user.premium or obj.user.redeemedPremium):
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')

    def premium_category(self, obj):
        if obj.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium_category.allow_tags = True


class CategoryRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'user',
                    'premium_user', 'status', 'timestamp']
    # list_display_links = []
    list_filter = ['user__premium', 'timestamp', 'status']
    search_fields = ['user', 'description']
    search_help_text = 'Search in [user] [description]'

    def premium_user(self, obj):
        if (obj.user.premium or obj.user.redeemedPremium):
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium_user.allow_tags = True


class ReportFactAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact_', 'category', 'premium_category', 'email',
                    'reason', 'description', 'timestamp']
    list_filter = ['timestamp','fact__category__isPremium']
    search_fields = ['fact__fact', 'reason', 'description']
    search_help_text = 'Search in [fact] [reason] [description]'

    def fact_(self, obj):
        return obj.fact.fact[:100] + '...' if len(obj.fact.fact) > 100 else obj.fact.fact

    def category(self, obj):
        return obj.fact.category

    def premium_category(self, obj):
        if obj.fact.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium_category.allow_tags = True

# Register your models here.
# admin.site.register(
#     [
#         User,
#         Category,
#         Fact,
#         BookMark,
#         Like,
#         Reward,
#         Subscription,
#         UserTasks,
#         DailyFact,
#         CategoryRequest,
#         ReportFact,
#         UserInterest,
#     ]
# )


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Fact, FactAdmin)
admin.site.register(DailyFact, DailyFactAdmin)
admin.site.register(BookMark, BookMarkAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Reward, CouponAdmin)
admin.site.register(UserTasks, UserTaskAdmin)
admin.site.register(UserInterest, UserInterestAdmin)
admin.site.register(CategoryRequest, CategoryRequestAdmin)
admin.site.register(ReportFact, ReportFactAdmin)

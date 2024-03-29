import datetime
from django.utils import formats
from django.contrib import admin
from django.utils.html import format_html

from api.models import *


def formatted_timestamp(utc_time):
    # Get the 'Asia/Kolkata' time zone offset
    asia_kolkata_offset = datetime.timedelta(hours=5, minutes=30)

    # Convert the timestamp to 'Asia/Kolkata' time zone
    local_time = utc_time + asia_kolkata_offset

    # Format the local time as desired
    formatted_time = formats.date_format(local_time, format='P j F Y')

    return formatted_time


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', '_last_seen_xxxxxxxxxxxxx', '_date_joined_xxxxxxxxxxxxx',
                    'coins', 'avtar', 'lang', 'streak', 'shared_fact_counts', 'premium', 'redeemedPremium', 'premium_end_date', 'is_staff', '_last_login_xxxxxxxxxxxxx', 'email']
    list_filter = ['last_seen', 'date_joined', 'lang',
                   'premium', 'redeemedPremium', 'last_login', 'premium_end_date', 'is_staff']
    search_fields = ['username', 'first_name', 'last_name']
    search_help_text = 'Search in [username] [first_name] [last_name]'
    list_per_page = 50

    def _last_seen_xxxxxxxxxxxxx(self, obj):
        if obj.last_seen:
            return formatted_timestamp(obj.last_seen)
        return '-'

    def _last_login_xxxxxxxxxxxxx(self, obj):
        if obj.last_login:
            return formatted_timestamp(obj.last_login)
        return '-'

    def _date_joined_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.date_joined)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'desc', 'isActive', 'isSpecial',
                    '_language', 'image_url', 'isPremium']
    list_display_links = ['image_url']
    list_filter = ['isPremium', 'language', 'isActive']
    search_fields = ['desc', 'name']
    list_per_page = 50

    def image_url(self, obj):
        return obj.imgURL[:50] + '...' if len(obj.imgURL) > 50 else obj.imgURL

    def _language(self, obj):
        if obj.language == 'hindi':
            return format_html('<span style="color:yellow;">Hindi</span>')
        else:
            return format_html('<span style="color:green;">English</span>')
    _language.allow_tags = True


class FactAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact_', 'category',
                    'premium', '_timestamp_xxxxxxxxxxxxx', 'isAd']
    list_display_links = ['fact_']
    list_filter = ['isAd', 'category__isPremium']
    search_fields = ['fact', 'desc']
    list_select_related = True
    list_per_page = 50

    def fact_(self, obj):
        return obj.fact[:100] + '...' if len(obj.fact) > 100 else obj.fact

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)

    def premium(self, obj):
        if obj.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium.allow_tags = True


class DailyFactAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact', 'premium_cat', 'date']
    list_editable = ['fact']
    list_per_page = 50

    def premium_cat(self, obj):
        if obj.fact.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium_cat.allow_tags = True


class BookMarkAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact', 'category', 'pc', 'bkm_user',
                    'pu',  '_timestamp_xxxxxxxxxxxxx']
    list_filter = ['timestamp', 'user__premium',
                   'fact__category__isPremium']
    search_fields = ['user__username', 'fact__category__name']
    search_help_text = 'Search in [username] [category]'
    list_per_page = 50

    def category(self, obj):
        return obj.fact.category

    def bkm_user(self, obj):
        return obj.user.username[:15]+'...'

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)

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
    list_display = ['id', 'fact', 'category', 'pc', 'like_user',
                    'pu',  '_timestamp_xxxxxxxxxxxxx']
    list_filter = ['timestamp', 'user__premium',
                   'fact__category__isPremium']
    search_fields = ['user__username', 'fact__category__name']
    search_help_text = 'Search in [username] [category]'
    list_per_page = 50

    def category(self, obj):
        return obj.fact.category

    def like_user(self, obj):
        return obj.user.username[:15]+'...'

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)

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
    list_per_page = 50

    def image_url(self, obj):
        return obj.imgURL[:50] + '...' if len(obj.imgURL) > 50 else obj.imgURL


class UserTaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'premium_user', 'task_number']
    # list_display_links = []
    list_filter = ['user__premium', 'task_number']
    search_fields = ['user']
    search_help_text = 'Search in [user]'
    list_per_page = 50

    def premium_user(self, obj):
        if (obj.user.premium or obj.user.redeemedPremium):
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')


class UserInterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',
                    'category', '_timestamp_xxxxxxxxxxxxx', 'premium_user', 'premium_category', ]
    # list_display_links = []
    list_filter = ['user__premium', 'category__isPremium', 'timestamp']
    search_fields = ['user__username', 'category__name']
    search_help_text = 'Search in [user] [category]'
    list_per_page = 50

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)

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
                    'premium_user', 'status', '_timestamp_xxxxxxxxxxxxx']
    # list_display_links = []
    list_filter = ['user__premium', 'timestamp', 'status']
    search_fields = ['user', 'description']
    search_help_text = 'Search in [user] [description]'
    list_per_page = 50

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)

    def premium_user(self, obj):
        if (obj.user.premium or obj.user.redeemedPremium):
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium_user.allow_tags = True


class ReportFactAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact_', 'category', 'premium_category', 'email',
                    'reason', 'description', '_timestamp_xxxxxxxxxxxxx']
    list_filter = ['timestamp', 'fact__category__isPremium']
    search_fields = ['fact__fact', 'reason', 'description']
    search_help_text = 'Search in [fact] [reason] [description]'
    list_per_page = 50

    def fact_(self, obj):
        return obj.fact.fact[:100] + '...' if len(obj.fact.fact) > 100 else obj.fact.fact

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)

    def category(self, obj):
        return obj.fact.category

    def premium_category(self, obj):
        if obj.fact.category.isPremium:
            return format_html('<span style="color:green;">&#10004;</span>')
        else:
            return format_html('<span style="color:red;">&#10008;</span>')
    premium_category.allow_tags = True


def make_expire(modeladmin, request, queryset):
    queryset.update(expiry_date=timezone.now())


def set_expiry_date_by_2_month(modeladmin, request, queryset):
    for view in queryset:
        view.expiry_date += timezone.timedelta(days=60)
        view.save()


class ViewsAdmin(admin.ModelAdmin):
    list_display = ['id', 'fact_', 'user',
                    '_timestamp_xxxxxxxxxxxxx', '_expiry_date_xxxxxxxxxxx']
    list_filter = ['timestamp', 'expiry_date']
    search_fields = ['user__username']
    search_help_text = 'Search in [user]'
    list_per_page = 50
    actions = [make_expire, set_expiry_date_by_2_month]

    def fact_(self, obj):
        return obj.fact.fact[:100] + '...' if len(obj.fact.fact) > 100 else obj.fact.fact

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)

    def _expiry_date_xxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.expiry_date)


class AnalyticsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'activity', '_timestamp_xxxxxxxxxxxxx']
    list_filter = ['timestamp', 'activity']
    search_fields = ['user__username', 'activity']
    search_help_text = 'Search in [user] [activity]'
    list_per_page = 50

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)


class AppNotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type', 'title','targetPage','isBtnOkLink',
                    'read', '_timestamp_xxxxxxxxxxxxx']
    list_filter = ['type','read', 'timestamp']
    search_fields = ['user__username', 'title','desc']
    search_help_text = 'Search in [user] [title] [desc]'
    list_per_page = 50

    def _timestamp_xxxxxxxxxxxxx(self, obj):
        return formatted_timestamp(obj.timestamp)


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
admin.site.register(Views, ViewsAdmin)
admin.site.register(Analytics, AnalyticsAdmin)
admin.site.register(AppNotification, AppNotificationAdmin)

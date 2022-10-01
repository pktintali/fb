from api.models import *
import django_filters


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['contains'],
            'isPremium': ['exact']
        }


class FactFilter(django_filters.FilterSet):
    class Meta:
        model = Fact
        fields = {
            'fact': ['contains'],
            'category': ['exact']
        }


class BookMarkFilter(django_filters.FilterSet):
    class Meta:
        model = BookMark
        fields = {
            'fact': ['exact'],
            'user': ['exact']
        }


class LikeFilter(django_filters.FilterSet):
    class Meta:
        model = Like
        fields = {
            'fact': ['exact'],
            'user': ['exact']
        }


class UserTaskFilter(django_filters.FilterSet):
    class Meta:
        model = UserTasks
        fields = {
            'user': ['exact']
        }


class UserInterestFilter(django_filters.FilterSet):
    class Meta:
        model = UserInterest
        fields = {
            'category': ['exact'],
            'user': ['exact']
        }

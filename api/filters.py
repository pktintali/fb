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
            'category': ['exact'],
            'isAd': ['exact']
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


class CategoryRequestFilter(django_filters.FilterSet):
    class Meta:
        model = CategoryRequest
        fields = {
            'user__premium': ['exact'],
            'user': ['exact'],
            'description': ['contains'],
            'status': ['exact']
        }


class ReportFactFilter(django_filters.FilterSet):
    class Meta:
        model = ReportFact
        fields = {
            'fact': ['exact'],
            'description': ['contains'],
            'reason': ['contains']
        }

from api.models import *
from django_filters import FilterSet

class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'name': ['contains'],
            'desc':['contains'],
            'language':['exact'],
            'isPremium': ['exact']
        }


class FactFilter(FilterSet):
    class Meta:
        model = Fact
        fields = {
            'fact': ['icontains'],
            'category': ['exact'],
            'isAd': ['exact'],
            'category__language': ['exact']
        }
        

class BookMarkFilter(FilterSet):
    class Meta:
        model = BookMark
        fields = {
            'fact': ['exact'],
            'user': ['exact']
        }


class LikeFilter(FilterSet):
    class Meta:
        model = Like
        fields = {
            'fact': ['exact'],
            'user': ['exact']
        }


class UserTaskFilter(FilterSet):
    class Meta:
        model = UserTasks
        fields = {
            'user': ['exact']
        }


class UserInterestFilter(FilterSet):
    class Meta:
        model = UserInterest
        fields = {
            'category': ['exact'],
            'user': ['exact']
        }


class CategoryRequestFilter(FilterSet):
    class Meta:
        model = CategoryRequest
        fields = {
            'user__premium': ['exact'],
            'user': ['exact'],
            'description': ['contains'],
            'status': ['exact']
        }


class ReportFactFilter(FilterSet):
    class Meta:
        model = ReportFact
        fields = {
            'fact': ['exact'],
            'description': ['contains'],
            'reason': ['contains']
        }

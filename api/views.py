from code import interact
from datetime import datetime
from multiprocessing.dummy import Array
from unicodedata import category
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from api.models import *
from api.serializers import *
from api.filters import *
from api.paginations import *
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('id').all()
    serializer_class = UserSerializer


class CategoryViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryFilter
    ordering_fields = ['name']
    queryset = Category.objects.order_by('name').all()
    serializer_class = CategorySerializer


class FactViewSet(ModelViewSet):
    queryset = Fact.objects.order_by('?').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    pagination_class = FactPagination
    ordering_fields = ['timestamp']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FactSerializer
        return FactAddSerializer


class CustomizedFactViewSet(ModelViewSet):
    
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    pagination_class = FactPagination
    ordering_fields = ['timestamp']

    def get_queryset(self):
        user = self.kwargs['user']
        use_interests = UserInterest.objects.filter(user__pk=user)
        interests = []
        for i in use_interests:
            interests.append(i.category)
        queryset = Fact.objects.order_by('?').filter(
        category__in=interests).all()
        print(user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FactSerializer
        return FactAddSerializer


class BookMarkViewSet(ModelViewSet):

    queryset = BookMark.objects.order_by('id').all()
    # serializer_class = BookMarkSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookMarkFilter
    ordering_fields = ['timestamp']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookMarkSerializer
        return BookMarkAddSerializer


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.order_by('id').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LikeFilter
    ordering_fields = ['timestamp']
    # serializer_class = LikeSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LikeSerializer
        return LikeAddSerializer


class RewardViewSet(ModelViewSet):
    queryset = Reward.objects.order_by('id').all()
    serializer_class = RewardSerializer
    
class UserInterestViewSet(ModelViewSet):
    queryset = UserInterest.objects.order_by('id').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserInterestFilter
    ordering_fields = ['timestamp']
    serializer_class = UserInterestSerializer


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.order_by('id').all()
    serializer_class = SubscriptionSerializer


class UserTasksViewSet(ModelViewSet):
    queryset = UserTasks.objects.order_by('id').all()
    serializer_class = UserTasksSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserTaskFilter
    ordering_fields = ['task_number']


class DailyFactViewSet(ModelViewSet):
    print('AAAAAAA')
    queryset = DailyFact.objects.order_by('id').all()

    def updateDailyFact(self):
        queryset = DailyFact.objects.order_by('id').all()

        def create():
            newFact: DailyFact = Fact.objects.order_by('?').first()
            DailyFact.objects.create(fact=newFact)
            print('Created')
            self.queryset = DailyFact.objects.order_by('id').all()

        if(len(queryset) == 0):
            print('Empty')
            create()
        else:
            df: DailyFact = queryset[0]
            factDay = df.date.day
            nowDay = datetime.now().day
            if factDay != nowDay:
                DailyFact.objects.all().delete()
                create()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            self.updateDailyFact()
            return DailyFactSerializer
        return DailyFactAddSerializer

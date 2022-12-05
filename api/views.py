from datetime import datetime
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models.aggregates import Count
from api.models import *
from api.serializers import *
from api.filters import *
from api.paginations import *
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('id').all()
    # serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserAddSerializer


class CategoryViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryFilter
    ordering_fields = ['name']
    queryset = Category.objects.order_by('name').all()
    serializer_class = CategorySerializer


class AdViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    ordering_fields = ['name']
    queryset = Fact.objects.filter(isAd=True).all()
    serializer_class = AdSerializer


class FactViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    pagination_class = FactPagination
    ordering_fields = ['timestamp', 'likes_count', 'bookmarks_count']
    queryset = Fact.objects.select_related('category').annotate(
        likes_count=Count('like'), bookmarks_count=Count('bookmark')).order_by('?').all()
    def list(self, request, *args, **kwargs):
        response = super(FactViewSet, self).list(request, args, kwargs)
        if self.request.user.is_authenticated:
            fact_list = response.data['results']
            for f in fact_list:
                liked  = Like.objects.filter(fact_id=f['id'], user=request.user).exists()
                bookmarked  = BookMark.objects.filter(fact_id=f['id'], user=request.user).exists()
                f[ 'isLiked' ] = liked
                f['isBookmarked'] = bookmarked
        return response
    

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FactSerializer
        return FactAddSerializer


class CustomizedFactViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    pagination_class = FactPagination
    ordering_fields = ['timestamp', 'likes_count', 'bookmarks_count']

    def get_queryset(self):
        user = self.kwargs['user']
        use_interests = UserInterest.objects.filter(user__pk=user)
        interests = []
        for i in use_interests:
            interests.append(i.category)
        queryset = Fact.objects.select_related('category').annotate(
            likes_count=Count('like'), bookmarks_count=Count('bookmark')).order_by('?').filter(
            category__in=interests).all()
        print(user)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FactSerializer
        return FactAddSerializer


class BookMarkViewSet(ModelViewSet):

    queryset = BookMark.objects.select_related('fact').annotate(
        likes_count=Count('fact__like')).order_by('id').all()
    # serializer_class = BookMarkSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookMarkFilter
    ordering_fields = ['timestamp']
    pagination_class = BookmarkAndLikePagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookMarkSerializer
        return BookMarkAddSerializer


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.order_by('id').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LikeFilter
    ordering_fields = ['timestamp']
    pagination_class = BookmarkAndLikePagination
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


class CategoryRequestViewSet(ModelViewSet):
    queryset = CategoryRequest.objects.order_by('id').all()
    serializer_class = CategoryRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryRequestFilter
    ordering_fields = ['timestamp']


class ReportFactViewSet(ModelViewSet):
    queryset = ReportFact.objects.order_by('id').all()
    serializer_class = ReportFactSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReportFactFilter
    ordering_fields = ['timestamp']


class DailyFactViewSet(ModelViewSet):
    print('Checking Daily Fact...')
    queryset = DailyFact.objects.order_by('id').all()

    def updateDailyFact(self):
        queryset = DailyFact.objects.order_by('id').all()

        def create():
            newFact: DailyFact = Fact.objects.order_by('?').first()
            DailyFact.objects.create(fact=newFact)
            print('Created')
            self.queryset = DailyFact.objects.order_by('id').all()

        if (len(queryset) == 0):
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

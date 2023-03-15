from datetime import datetime

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from django.db.models.aggregates import Count
from api.models import *
from api.serializers import *
from api.filters import *
from api.paginations import *
from accounts.permissions import IsAdminOrReadOnly, IsAdminOrNoAccess, IsAuthenticatedOrNoAccessEditAdminOnly
# Create your views here.


class UserViewSet(ModelViewSet):
    queryset = User.objects.order_by('id').all()
    # serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return UserAddSerializer


class CategoryViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryFilter
    ordering_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.order_by('name').all()
    serializer_class = CategorySerializer


class AdViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    ordering_fields = ['name']
    permission_classes = [IsAdminOrReadOnly]
    queryset = Fact.objects.filter(isAd=True).all()
    serializer_class = AdSerializer


class FactViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    pagination_class = FactPagination
    ordering_fields = ['timestamp', 'likes_count']
    permission_classes = [IsAdminOrReadOnly]
    queryset = Fact.objects.select_related('category').annotate(
        likes_count=Count('like')).order_by('?').all()

    def list(self, request, *args, **kwargs):
        response = super(FactViewSet, self).list(request, args, kwargs)
        if self.request.user.is_authenticated:
            fact_list = response.data['results']
            for f in fact_list:
                liked = Like.objects.filter(
                    fact_id=f['id'], user=request.user).exists()
                bookmarked = BookMark.objects.filter(
                    fact_id=f['id'], user=request.user).exists()
                f['isLiked'] = liked
                f['isBookmarked'] = bookmarked
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FactSerializer
        return FactAddSerializer


class FactLikeViewSet(viewsets.ViewSet):
    def create(self, request, pk=None):
        fact = get_object_or_404(Fact, pk=pk)
        like = Like.objects.create(user=request.user, fact=fact)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        fact = get_object_or_404(Fact, pk=pk)
        like = Like.objects.filter(user=request.user, fact=fact).first()
        if like:
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={"Not Fond"}, status=status.HTTP_404_NOT_FOUND)


class FactBookmarkViewSet(viewsets.ViewSet):
    def create(self, request, pk=None):
        fact = get_object_or_404(Fact, pk=pk)
        bookmark = BookMark.objects.create(user=request.user, fact=fact)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        fact = get_object_or_404(Fact, pk=pk)
        bookmark = BookMark.objects.filter(
            user=request.user, fact=fact).first()
        if bookmark:
            bookmark.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data={"Not Fond"}, status=status.HTTP_404_NOT_FOUND)


class CustomizedFactViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    pagination_class = FactPagination
    ordering_fields = ['timestamp', 'likes_count']
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_authenticated:
            use_interests = UserInterest.objects.filter(user=user)
            interests = []
            for i in use_interests:
                interests.append(i.category)
            queryset = Fact.objects.select_related('category').annotate(
                likes_count=Count('like')).order_by('?').filter(
                category__in=interests).all()
            user_lang = 'english'
            if use_interests.exists():
                user_lang = use_interests.first().category.language

            if len(interests) > 15:
                other_facts = Fact.objects.filter(category__language=user_lang).exclude(
                    category__in=interests
                ).order_by('?').all()
                if len(other_facts) > 10:
                    other_facts = other_facts[:10]
                queryset = queryset | other_facts

            if len(interests) <= 15 and len(interests) > 3:
                other_facts = Fact.objects.filter(category__language=user_lang).exclude(
                    category__in=interests
                ).order_by('?').all()
                if len(other_facts) > 15:
                    other_facts = other_facts[:15]
                queryset = queryset | other_facts

            if len(interests) <= 3:
                other_facts = Fact.objects.filter(category__language=user_lang).exclude(
                    category__in=interests
                ).order_by('?').all()
                if len(other_facts) > 25:
                    other_facts = other_facts[:25]
                queryset = queryset | other_facts
            return queryset
        return Fact.objects.none()

    def list(self, request, *args, **kwargs):
        response = super(CustomizedFactViewSet, self).list(
            request, args, kwargs)
        if self.request.user.is_authenticated:
            fact_list = response.data['results']
            for f in fact_list:
                liked = Like.objects.filter(
                    fact_id=f['id'], user=request.user).exists()
                bookmarked = BookMark.objects.filter(
                    fact_id=f['id'], user=request.user).exists()
                f['isLiked'] = liked
                f['isBookmarked'] = bookmarked
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FactSerializer
        return FactAddSerializer


class BookMarkViewSet(ModelViewSet):
    queryset = BookMark.objects.select_related('fact').annotate(
        likes_count=Count('fact__like')).order_by('-timestamp').all()
    # serializer_class = BookMarkSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookMarkFilter
    ordering_fields = ['timestamp']
    permission_classes = [permissions.IsAdminUser]
    pagination_class = BookmarkAndLikePagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookMarkSerializer
        return BookMarkAddSerializer


class MyBookMarkViewSet(ModelViewSet):
    # queryset = BookMark.objects.select_related('fact').annotate(
    #     likes_count=Count('fact__like')).order_by('id').all()
    # serializer_class = BookMarkSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = BookMarkFilter
    ordering_fields = ['timestamp']
    pagination_class = BookmarkAndLikePagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = BookMark.objects.filter(user=user).select_related('fact').annotate(
            likes_count=Count('fact__like')).order_by('-timestamp').all()
        return queryset

    def list(self, request, *args, **kwargs):
        response = super(MyBookMarkViewSet, self).list(
            request, args, kwargs)
        if self.request.user.is_authenticated:
            bookmark_list = response.data['results']
            for l in bookmark_list:
                liked = BookMark.objects.filter(
                    fact_id=l['fact']['id'], user=request.user).exists()
                bookmarked = BookMark.objects.filter(
                    fact_id=l['fact']['id'], user=request.user).exists()
                l['fact']['isLiked'] = liked
                l['fact']['isBookmarked'] = bookmarked
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookMarkSerializer
        return BookMarkAddSerializer


class LikeViewSet(ModelViewSet):
    queryset = Like.objects.select_related('fact').annotate(
        likes_count=Count('fact__like')).order_by('-timestamp').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LikeFilter
    ordering_fields = ['timestamp']
    pagination_class = BookmarkAndLikePagination
    permission_classes = [permissions.IsAdminUser]
    # serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LikeSerializer
        return LikeAddSerializer


class MyLikeViewSet(ModelViewSet):
    # queryset = Like.objects.select_related('fact').annotate(
    #     likes_count=Count('fact__like')).order_by('id').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = LikeFilter
    ordering_fields = ['timestamp']
    pagination_class = BookmarkAndLikePagination
    # serializer_class = LikeSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = Like.objects.filter(user=user).select_related('fact').annotate(
            likes_count=Count('fact__like')).order_by('-timestamp').all()
        return queryset

    def list(self, request, *args, **kwargs):
        response = super(MyLikeViewSet, self).list(
            request, args, kwargs)
        if self.request.user.is_authenticated:
            like_list = response.data['results']
            for l in like_list:
                liked = Like.objects.filter(
                    fact_id=l['fact']['id'], user=request.user).exists()
                bookmarked = BookMark.objects.filter(
                    fact_id=l['fact']['id'], user=request.user).exists()
                l['fact']['isLiked'] = liked
                l['fact']['isBookmarked'] = bookmarked
        return response

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LikeSerializer
        return LikeAddSerializer


class RewardViewSet(ModelViewSet):
    queryset = Reward.objects.order_by('id').all()
    serializer_class = RewardSerializer
    permission_classes = [IsAuthenticatedOrNoAccessEditAdminOnly]


class UserInterestViewSet(ModelViewSet):
    queryset = UserInterest.objects.order_by('id').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserInterestFilter
    ordering_fields = ['timestamp']
    permission_classes = [permissions.IsAdminUser]
    serializer_class = UserInterestSerializer


class MyInterestViewSet(ModelViewSet):
    # queryset = UserInterest.objects.order_by('id').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserInterestFilter
    ordering_fields = ['timestamp']
    serializer_class = UserInterestSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = UserInterest.objects.filter(user=user).order_by('id').all()
        return queryset


class SubscriptionViewSet(ModelViewSet):
    queryset = Subscription.objects.order_by('id').all()
    permission_classes = [IsAuthenticatedOrNoAccessEditAdminOnly]
    serializer_class = SubscriptionSerializer


class UserTasksViewSet(ModelViewSet):
    queryset = UserTasks.objects.order_by('id').all()
    serializer_class = UserTasksSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserTaskFilter
    ordering_fields = ['task_number']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyTasksViewSet(ModelViewSet):
    # queryset = UserTasks.objects.order_by('id').all()
    serializer_class = UserTasksSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = UserTaskFilter
    ordering_fields = ['task_number']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = UserTasks.objects.filter(user=user).order_by('id').all()
        return queryset


class CategoryRequestViewSet(ModelViewSet):
    queryset = CategoryRequest.objects.order_by('id').all()
    serializer_class = CategoryRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryRequestFilter
    permission_classes = [IsAdminOrNoAccess]
    ordering_fields = ['timestamp']


class MyCategoryRequestViewSet(ModelViewSet):
    # queryset = CategoryRequest.objects.order_by('id').all()
    # serializer_class = CategoryRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = CategoryRequestFilter
    ordering_fields = ['timestamp']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        queryset = CategoryRequest.objects.filter(
            user=user).order_by('id').all()
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CategoryRequestSerializer
        return CategoryRequestAddSerializer


class ReportFactViewSet(ModelViewSet):
    queryset = ReportFact.objects.order_by('id').all()
    serializer_class = ReportFactSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReportFactFilter
    ordering_fields = ['timestamp']


class DailyFactViewSet(ModelViewSet):
    print('Checking Daily Fact...')
    queryset = DailyFact.objects.order_by('id').all()
    permission_classes = [IsAdminOrReadOnly]

    def updateDailyFact(self):
        queryset = DailyFact.objects.order_by('id').all()

        def create():
            newFactEnglish: DailyFact = Fact.objects.filter(
                category__language='english').order_by('?').first()
            newFactHindi: DailyFact = Fact.objects.filter(
                category__language='hindi').order_by('?').first()
            DailyFact.objects.create(fact=newFactEnglish)
            DailyFact.objects.create(fact=newFactHindi)
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

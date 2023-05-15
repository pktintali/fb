from datetime import datetime
from django.db.models import Prefetch

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.decorators import action
from django.db.models.aggregates import Count
from api.models import *
from api.serializers import *
from api.filters import *
from api.paginations import *
from accounts.permissions import IsAdminOrReadOnly, IsAdminOrNoAccess, IsAuthenticatedOrNoAccessEditAdminOnly, FullAccessWithoutAuthentication, IsAuthenticatedOrNoAccess
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
    # pagination_class = FactPagination
    ordering_fields = ['timestamp', 'likes_count']
    permission_classes = [IsAdminOrReadOnly]
    queryset = Fact.objects.select_related('category').annotate(
        likes_count=Count('like'), views_count=Count('views')).order_by('?').all()

    def get_queryset(self):
        # Get the base queryset
        queryset = super().get_queryset()

        # Apply your custom filters, ordering or any other modifications
        if self.request.query_params.get('admin_order'):
            queryset = queryset.order_by('-id')

        return queryset

    def list(self, request, *args, **kwargs):
        if self.request.query_params.get('category'):
            self.pagination_class = FactPaginationWithFilter
        else:
            self.pagination_class = FactPagination
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
        elif self.request.method == 'PATCH':
            return FactPatchSerializer
        return FactAddSerializer

    @action(detail=False, methods=['post'], url_path='remove-duplicate')
    def remove_duplicate_facts(self, request):
        # Step 1: Group Fact instances by their fact field and filter for duplicates
        duplicate_facts = (
            Fact.objects
            .values('fact')
            .annotate(fact_count=Count('fact'))
            .filter(fact_count__gt=1)
            .values_list('fact', flat=True)
        )
        print(duplicate_facts)
        # Step 2-4: For each duplicate Fact instance, delete all but the first instance
        count = 0
        deleted_facts = []
        for fact in duplicate_facts:
            duplicates = Fact.objects.filter(fact=fact).exclude(
                id=Fact.objects.filter(fact=fact).order_by('id').first().id)
            print(duplicates)
            deleted_facts.append({'fact': fact, 'count': duplicates.count()})
            count += duplicates.count()
            duplicates.delete()

        return Response({'message': f'{count} duplicate facts removed', 'deleted_facts': deleted_facts}, status=status.HTTP_200_OK)

    def compute_similarity(self, fact1, fact2):
        words1 = set(fact1.split())
        words2 = set(fact2.split())
        intersection_size = len(words1.intersection(words2))
        union_size = len(words1.union(words2))
        similarity = intersection_size / union_size
        return similarity

    @action(detail=False, methods=['post'], url_path='remove-similar')
    def remove_similar_facts_by_category_ids(self, request):
        threshold = request.query_params.get('p', '80')
        try:
            threshold = int(threshold)
            if threshold < 55:
                return Response({'message': 'Threshold must be greater than or equal to 55'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'message': 'Invalid threshold value'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Fetch all the unique facts belonging to the selected categories
        cat_ids = request.query_params.get('cat_ids', '')
        cat_ids_list = cat_ids.split(',')
        facts = Fact.objects.filter(
            category__in=cat_ids_list).values_list('id', 'fact')
        n = len(facts)

        # Step 2-3: Fetch all the similar facts and delete them
        count = 0
        deleted_facts = []
        deleted_ids = []
        for i in range(n):
            if facts[i][0] in deleted_ids:  # Skip if this fact has already been deleted
                continue
            for j in range(i+1, n):
                if facts[j][0] in deleted_ids:  # Skip if this fact has already been deleted
                    continue
                if i != j:
                    similarity = self.compute_similarity(
                        facts[i][1], facts[j][1])
                    if similarity >= threshold/100:
                        deleted_fact = Fact.objects.get(id=facts[j][0])
                        deleted_fact_similarity = similarity * 100
                        deleted_facts.append(
                            {'fact': facts[i][1], 'deleted_fact': deleted_fact.fact, 'similarity': deleted_fact_similarity})
                        deleted_fact.delete()
                        deleted_ids.append(facts[j][0])
                        count += 1

        return Response({'message': f'{count} similar facts removed', 'deleted_facts': deleted_facts}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='auto_update')
    def auto_update_fact_by_id(self, request):
        #! Note this is a very long process
        fact_id = ''
        try:
            fact_id = request.query_params.get('id', '')
        except:
            return Response({'message': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)
        fact = Fact.objects.filter(id=fact_id).first()
        # Update the images of the fact
        imgURL1, imgURL2, ref, desc = getFactData(fact.fact)
        if not (imgURL1 and imgURL2):
            fact.imgURL = fact.category.imgURL
        else:
            if imgURL1:
                fact.imgURL = imgURL1
            else:
                fact.imgURL = imgURL2
        fact.imgURL2 = imgURL2
        if ref != None:
            fact.ref = ref
        if desc != None:
            fact.desc = desc
        fact.save()
        return Response({'message': 'Fact updated successfully'})


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
                # print(i.category)
            queryset = Fact.objects.select_related('category').annotate(
                likes_count=Count('like')).order_by('?').filter(
                category__in=interests).all()

            user_lang = 'english'
            if use_interests.exists():
                user_lang = random.choice(use_interests).category.language
            else:
                user_lang = user.lang

            if len(interests) > 15:
                other_facts = Fact.objects.filter(category__language=user_lang).exclude(
                    category__in=interests
                ).exclude(category__isActive=False).exclude(category__name='Ad').order_by('?').all()[:20]

            if len(interests) <= 15 and len(interests) > 3:
                other_facts = Fact.objects.filter(category__language=user_lang).exclude(
                    category__in=interests
                ).exclude(category__name='Ad').order_by('?').all()[:25]

            if len(interests) <= 3:
                other_facts = Fact.objects.filter(category__language=user_lang).exclude(
                    category__in=interests
                ).exclude(category__name='Ad').order_by('?').all()[:35]
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


class CustomizedUniqueFactViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = FactFilter
    pagination_class = FactPagination
    ordering_fields = ['timestamp', 'likes_count']
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            use_interests = UserInterest.objects.filter(user=user)
            interests = use_interests.values_list('category', flat=True)
            viewed_facts = Views.objects.filter(
                user=user).values_list('fact', flat=True)

            categories_prefetch = Prefetch(
                'category', queryset=Category.objects.filter(id__in=interests))

            queryset = Fact.objects.select_related('category').annotate(
                likes_count=Count('like')).filter(category__in=interests).exclude(
                id__in=viewed_facts).order_by('?').prefetch_related(categories_prefetch)

            user_lang = 'english'
            if use_interests.exists():
                user_lang = random.choice(use_interests).category.language
            else:
                user_lang = user.lang

            other_facts = Fact.objects.filter(category__language=user_lang).exclude(
                category__in=interests).exclude(category__name='Ad').exclude(category__isActive=False).exclude(
                id__in=viewed_facts).order_by('?').all()

            if len(interests) > 15:
                other_facts = other_facts[:20]

            if len(interests) <= 15 and len(interests) > 3:
                other_facts = other_facts[:25]

            if len(interests) <= 3:
                other_facts = other_facts[:35]

            queryset |= other_facts

            return queryset

        return Fact.objects.none()

    def list(self, request, *args, **kwargs):
        response = super(CustomizedUniqueFactViewSet, self).list(
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


class ViewsViewSet(ModelViewSet):
    queryset = Views.objects.select_related('fact').annotate(
        views=Count('fact__views')).all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ViewsFilter
    ordering_fields = ['timestamp']
    pagination_class = BookmarkAndLikePagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ViewsSerializer

    def create(self, request, *args, **kwargs):
        print(request.data.get('fact', []))
        fact_ids = request.data.get('fact_ids', [])
        if len(fact_ids) == 0:
            fact_ids = [request.data.get('fact')]

        user_id = request.user.id
        views = []
        for fact_id in fact_ids:
            view = Views(fact_id=fact_id, expiry_date=timezone.now(
            ) + timezone.timedelta(days=60), user_id=user_id)
            views.append(view)
        Views.objects.bulk_create(views)
        serializer = self.get_serializer(views, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ViewsSerializer
        return ViewsAddSerializer

    @action(detail=False, methods=['delete'])
    def delete_expired(self, request):
        expired_views = Views.objects.filter(expiry_date__lte=timezone.now())
        count = expired_views.count()
        expired_views.delete()
        message = f"{count} expired views deleted." if count > 0 else "No expired likes found."
        return Response({'message': message, 'count': count})


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

    @action(detail=False, methods=['delete'], url_path='delete_premium_interests')
    def delete_premium_categories(self, request):
        user_interests = UserInterest.objects.filter(
            user=request.user, category__isPremium=True)
        user_interests.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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

    @action(detail=False, methods=['delete'], url_path='delete_tasks')
    def delete_tasks(self, request):
        user_tasks = UserTasks.objects.filter(
            user=request.user).exclude(task_number__in=[1, 2])
        user_tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class AnalyticsViewSet(ModelViewSet):
    queryset = Analytics.objects.order_by('id').all()
    serializer_class = AnalyticsSerializer
    pagination_class = FactPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = AnalyticsFilter
    permission_classes = [FullAccessWithoutAuthentication]


def create_notification_for_user(user_id, data):
    title = data.get('title', None)
    description = data.get('description', None)
    type = data.get('type', None)
    closeButton = data.get('closeButton', False)
    btnOkText = data.get('btnOkText', None)
    btnCancelText = data.get('btnCancelText', None)
    isBtnOkLink = data.get('isBtnOkLink', False)
    btnOkLink = data.get('btnOkLink', None)
    targetPage = data.get('targetPage', None)
    isUriLaunch = data.get('isUriLaunch', False)
    user = User.objects.get(id=user_id)
    notification = AppNotification.objects.create(
        user=user,
        title=title,
        description=description,
        type=type,
        closeButton=closeButton,
        btnOkText=btnOkText,
        btnCancelText=btnCancelText,
        isBtnOkLink=isBtnOkLink,
        btnOkLink=btnOkLink,
        targetPage=targetPage,
        isUriLaunch=isUriLaunch,
    )


class NotificationViewSet(ModelViewSet):
    permission_classes = [IsAdminOrNoAccess]
    serializer_class = NotificationAdminSerializer
    pagination_class = FactPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    queryset = AppNotification.objects.all()

    @action(detail=False, methods=['POST'])
    def create_notification_for_all_users(self, request):
        if request.data:
            for user in User.objects.all():
                create_notification_for_user(user.id, request.data)
            return Response({'message': 'Notifications are being created for all users.'}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message': 'Message field is required.'}, status=status.HTTP_400_BAD_REQUEST)


class MyNotificationViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrNoAccess]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    serializer_class = NotificationSerializer
    queryset = AppNotification.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user, read=False)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.read = True
        notification.save()
        return Response({'detail': 'Notification marked as read.'}, status=status.HTTP_200_OK)


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

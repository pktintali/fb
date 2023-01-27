from rest_framework import routers
from django.urls import path
from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('facts', FactViewSet)
router.register('customized-facts', CustomizedFactViewSet,
                basename='customized-facts')
router.register('bookmarks', BookMarkViewSet)
router.register('my-bookmarks', MyBookMarkViewSet, basename="my-bookmarks")
router.register('likes', LikeViewSet)
router.register('my-likes', MyLikeViewSet, basename='my-likes')
router.register('rewards', RewardViewSet)
router.register('subscriptions', SubscriptionViewSet)
router.register('user-tasks', UserTasksViewSet)
router.register('my-tasks', MyTasksViewSet, basename='my-tasks')
router.register('fact-of-the-day', DailyFactViewSet)
router.register('users-interest', UserInterestViewSet)
router.register('my-interest', MyInterestViewSet, basename='my-interest')
router.register('category-requests', CategoryRequestViewSet)
router.register('my-category-requests', MyCategoryRequestViewSet,
                basename='my-category-request')
router.register('fact-reports', ReportFactViewSet)
router.register('ads', AdViewSet, basename='ads')

urlpatterns = [
    path('facts/<int:pk>/like/', FactLikeViewSet.as_view({'post': 'create'})),
    path('facts/<int:pk>/unlike/',
         FactLikeViewSet.as_view({'delete': 'destroy'})),
    path('facts/<int:pk>/bookmark/',
         FactBookmarkViewSet.as_view({'post': 'create'})),
    path('facts/<int:pk>/delbookmark/',
         FactBookmarkViewSet.as_view({'delete': 'destroy'})),
]+router.urls

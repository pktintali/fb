from django.urls import path, re_path
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet)
router.register('facts', FactViewSet)
router.register('bookmarks', BookMarkViewSet)
router.register('likes', LikeViewSet)
router.register('rewards', RewardViewSet)
router.register('subscriptions', SubscriptionViewSet)
router.register('user-tasks', UserTasksViewSet)
router.register('fact-of-the-day', DailyFactViewSet)
router.register('users-interest', UserInterestViewSet)
router.register('category-requests', CategoryRequestViewSet)
router.register('fact-reports', ReportFactViewSet)
router.register('ads', AdViewSet, basename='ads')

# router.register('customized-facts', CustomizedFactViewSet,
#                 basename='customized-fact')

urlpatterns = [
    re_path('^customized-facts/(?P<user>.+)/$',
            CustomizedFactViewSet.as_view({'get': 'list'})),
    # path('register/', RegisterView.as_view()),
]+router.urls

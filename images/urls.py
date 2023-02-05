from django.urls import path
from rest_framework import routers

from . import views

from images.views import ImageViewSet,BGImageViewSet

router = routers.DefaultRouter()
router.register('list', ImageViewSet)
router.register('bg-image', BGImageViewSet)

urlpatterns = [
    path('', views.index_view, name='images-index'),
    path('upload/', views.upload_view, name='images-upload'),
]+router.urls
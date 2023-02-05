import logging
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

from images.forms import UploadForm
from images.models import Image,BGImage
from images.tables import ImageTable
from images.serializer import ImageSerializer,BGImageSerializer

from accounts.permissions import FullAccessWithoutAuthentication


logger = logging.getLogger(__name__)


def index_view(request):
    images = Image.objects.all()
    image_table = ImageTable(images)
    upload_form = UploadForm()

    return render(request, 'images/index.html', {
        'images': images,
        'image_table': image_table,
        'upload_form': upload_form,
    })


@require_http_methods(["POST"])
def upload_view(request):
    upload_form = UploadForm(data=request.POST, files=request.FILES)

    if upload_form.is_valid():
        upload_form.save(commit=True)
    else:
        logger.warning("Something went wrong with uploading the file.")
        logger.warning(request.POST)
        logger.warning(request.FILES)

    return redirect('images-index')


class ImageViewSet(ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [FullAccessWithoutAuthentication]
    queryset = Image.objects.all()

class BGImageViewSet(ModelViewSet):
    serializer_class = BGImageSerializer
    permission_classes = [FullAccessWithoutAuthentication]
    queryset = BGImage.objects.all()
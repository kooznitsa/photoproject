from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import ImageUploadForm
from .services import UploadImageService


def upload(request: HttpRequest) -> HttpResponse:
    image_uri, predicted_label = None, None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_uri, predicted_label = UploadImageService.upload(form.cleaned_data['image'])
    else:
        form = ImageUploadForm()

    context = {
        'form': form,
        'image_uri': image_uri,
        'predicted_label': predicted_label,
        'title': 'Загрузка изображения',
    }

    return render(request, 'tags/index.html', context)

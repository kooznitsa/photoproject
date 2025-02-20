from django.shortcuts import render

from .forms import ImageUploadForm
from .services import UploadImageService


def index(request):
    image_uri, predicted_labels = None, None

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_uri, predicted_labels = UploadImageService.upload(form.cleaned_data['image'])
    else:
        form = ImageUploadForm()

    context = {
        'form': form,
        'image_uri': image_uri,
        'predicted_labels': ', '.join(predicted_labels) if predicted_labels else None,
        'title': 'Загрузка изображения',
    }

    return render(request, 'tags/index.html', context)

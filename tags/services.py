import asyncio
import base64
import io
import json
import logging
import os
from typing import Optional

from django.core.files.uploadedfile import TemporaryUploadedFile

from googletrans import Translator
from PIL import Image
import torch
from torchvision import models, transforms

from core import settings

info_logger = logging.getLogger('info_logger')
error_logger = logging.getLogger('error_logger')

# Load as global variable here to avoid expensive reloads with each request
model = models.efficientnet_v2_s(weights=models.EfficientNet_V2_S_Weights)
model.eval()

# https://pytorch.org/vision/main/models/generated/torchvision.models.efficientnet_v2_s.html
EFFICIENTNET_V2_S_PARAMS = {
    'resize': 384,
    'crop': 384,
    'mean': [0.485, 0.456, 0.406],
    'std': [0.229, 0.224, 0.225],
}

json_path = os.path.join(settings.base.STATICFILES_DIRS[0], 'imagenet_class_index.json')
imagenet_mapping = json.load(open(json_path))


class UploadImageService:
    @staticmethod
    def upload(image: TemporaryUploadedFile) -> tuple[str, Optional[list]]:
        """
        Upload an image.
        Return image URI and predicted tags.
        """
        predicted_labels = None
        image_bytes = image.file.read()
        encoded_img = base64.b64encode(image_bytes).decode('ascii')
        image_uri = 'data:%s;base64,%s' % ('image/jpeg', encoded_img)

        info_logger.info(f'Image type: {type(image)}')

        try:
            predicted_labels = TagsGeneratorService().get_prediction(image_bytes)
        except RuntimeError as e:
            error_logger.error(e)

        return image_uri, predicted_labels


class TagsGeneratorService:
    def get_prediction(self, image_bytes: bytes) -> list[str]:
        """For given image bytes, predict the label using a model."""
        tensor = self._transform_image(image_bytes)
        outputs = model.forward(tensor)
        _, y_hat = outputs.max(1)
        predicted_idx = str(y_hat.item())
        class_name, human_label = imagenet_mapping[predicted_idx]
        return asyncio.run(TranslatorService.translate_to_russian(human_label))

    @staticmethod
    def _transform_image(image_bytes: bytes) -> torch.Tensor:
        """
        Transform image into required format with 3 RGB channels and normalized.
        Return the corresponding tensor.
        """
        my_transforms = transforms.Compose([
            transforms.Resize(EFFICIENTNET_V2_S_PARAMS['resize']),
            transforms.CenterCrop(EFFICIENTNET_V2_S_PARAMS['crop']),
            transforms.ToTensor(),
            transforms.Normalize(
                EFFICIENTNET_V2_S_PARAMS['mean'],
                EFFICIENTNET_V2_S_PARAMS['std'],
            ),
        ])
        image = Image.open(io.BytesIO(image_bytes))
        return my_transforms(image).unsqueeze(0)


class TranslatorService:
    @staticmethod
    async def translate_to_russian(terms: str) -> list[str]:
        """Translate terms from English to Russian."""
        async with Translator() as translator:
            translated_terms = []
            for term in terms.split('_'):
                translated_term = await translator.translate(term, dest='ru')
                translated_terms.append(translated_term.text)
            return translated_terms

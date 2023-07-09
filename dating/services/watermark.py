from django.conf import settings
from PIL import Image


def set_water_mark(some_image):
    """Устанавливает водный знак на изображение """

    watermark_image = Image.open(settings.MEDIA_ROOT / "watermark.png")

    watermark_width = int(some_image.width * 0.5)
    watermark_height = int(watermark_image.height * (watermark_width / watermark_image.width))
    watermark_image = watermark_image.resize((watermark_width, watermark_height))

    some_image.paste(watermark_image, (0, 0), watermark_image)
    return some_image

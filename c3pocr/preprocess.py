from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


def prepare_image(image: str | Path | Image.Image, scale: int = 2) -> Image.Image:
    """Prepara uma imagem para OCR sem alterar o arquivo original."""
    prepared = image.copy() if isinstance(image, Image.Image) else Image.open(image).copy()
    prepared = prepared.convert("L")
    prepared = prepared.resize(
        (prepared.width * scale, prepared.height * scale), Image.Resampling.LANCZOS
    )
    prepared = ImageEnhance.Contrast(prepared).enhance(1.5)
    return prepared.filter(ImageFilter.SHARPEN)

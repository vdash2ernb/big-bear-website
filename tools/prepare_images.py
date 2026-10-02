"""Make responsive WebP copies of the approved source photography (Pillow)."""
from pathlib import Path
from PIL import Image, ImageOps
root=Path(__file__).resolve().parents[1]
sources={'entrance':root/'dist/assets/gate.jpeg'}
sources.update({p.stem:p for p in (root/'source-assets').glob('*') if p.stem in ('detail','custom','operator','driveway','access')})
for name,source in sources.items():
    image=ImageOps.exif_transpose(Image.open(source)).convert('RGB')
    for width in (640,960,1600):
        copy=image.copy()
        copy.thumbnail((width,10000))
        copy.save(root/f'dist/images/{name}-{width}.webp','WEBP',quality=82,method=6)
print(f'Prepared {len(sources)} photographs at three responsive sizes.')

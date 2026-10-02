import os
import sys
from PIL import Image, ImageEnhance

def generate_sharp_monochrome_image(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input image not found: {input_path}")

    print(f"Opening source image: {input_path}")
    img = Image.open(input_path)
    orig_w, orig_h = img.size
    print(f"Source image dimensions: {orig_w} x {orig_h}")

    # 1. Convert to pure high-fidelity Grayscale
    # Preserves full original detail, midtones, textures, objects, people, edges
    gray = img.convert('L')

    # 2. Subtle contrast enhancement (1.08x) - deep blacks and crisp highlights, NO crushed midtones
    contrasted = ImageEnhance.Contrast(gray).enhance(1.08)

    # Convert to RGB to ensure standard 3-channel layout for web canvas
    rgb_monochrome = contrasted.convert('RGB')

    # 3. Save at exact 1:1 original resolution with maximum quality and no subsampling
    # ZERO downscaling, ZERO nearest-neighbor pixelation, ZERO blur
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    rgb_monochrome.save(output_path, quality=98, subsampling=0)
    print(f"Successfully saved sharp monochrome scene to: {output_path} ({orig_w}x{orig_h})")

if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scene_path = os.path.join(base_dir, 'assets', 'scene.jpg')
    corrupted_path = os.path.join(base_dir, 'assets', 'scene-corrupted.jpg')
    generate_sharp_monochrome_image(scene_path, corrupted_path)

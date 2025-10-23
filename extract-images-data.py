import os
import json
import math
from PIL import Image


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def color_distance(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def find_closest_color_index(pixel, color_palette):
    distances = [color_distance(pixel, color) for color in color_palette]
    return distances.index(min(distances))


def image_to_indexed_array(image_path, color_palette):
    img = Image.open(image_path).convert('RGB')
    width, height = img.size
    indexed_array = []

    for x in range(width):
        column = []
        for y in range(height):
            pixel = img.getpixel((x, y))
            idx = find_closest_color_index(pixel, color_palette)
            column.append(idx)
        indexed_array.append(column)

    return indexed_array


def find_images(base_dir):
    found_images = []

    for root, dirs, files in os.walk(base_dir):
        for f in files:
            if f.lower().endswith(".png"):
                found_images.append(os.path.join(root, f))
    return found_images


def extract_images_data(base_dir, output_file):

    color_palette_hex = [
        "#000000",  # preto
        "#ffffff",  # branco
        "#ffaa24",  # amarelo
    ]

    color_palette = [hex_to_rgb(c) for c in color_palette_hex]

    images = find_images(base_dir)
    if not images:
        return

    data = {}

    for img_path in images:
        relative_path = os.path.relpath(img_path, base_dir)
        folder_name = os.path.dirname(relative_path).split(os.sep)[0]
        image_name = os.path.splitext(os.path.basename(img_path))[0]

        print(f"> Processando: {img_path}")
        try:
            array = image_to_indexed_array(img_path, color_palette)

            if folder_name not in data:
                data[folder_name] = []

            data[folder_name].append({
                "name": image_name,
                "data": array
            })

        except Exception as e:
            print(f"> Erro: '{img_path}', {e}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(',', ':'))

    print("\n> O arquivo \"data.json\" foi gerado.")


if __name__ == "__main__":
    base_dir = "images"
    output_file = "./src/lib/data.json"

    extract_images_data(base_dir, output_file)

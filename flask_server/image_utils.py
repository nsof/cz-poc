import io
import urllib.request
import matplotlib.pyplot as plt
import math

from PIL import Image
from PIL import ImageColor
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps


class ImageUtils:

    @staticmethod
    def get_image(url):
        response = urllib.request.urlopen(url)
        image_bytes = response.read()
        image_bytes_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(image_bytes_stream)
        return pil_image

    @staticmethod
    def _resize_image_while_maintaining_proportion(image, width, height, add_background = False):
        if width == None or height == None:
            return image

        resized_image = image.copy()
        resized_image.thumbnail((width, height), Image.LANCZOS)
        # filename = image.filename
        # resized_image.save(f"{filename}.resized.jpg")

        if add_background == True:
            background = Image.new("RGB", (width, height), "white")
            offset = (round((width - resized_image.width) / 2), round((height - resized_image.height) / 2))
            background.paste(resized_image, offset)
            # background.save(f"{filename}.background.jpg")
            return background
        else:
            return resized_image

    @staticmethod
    def prepare_image(pil_image, new_width=None, new_height=None):
        resized_image = ImageUtils._resize_image_while_maintaining_proportion(pil_image, new_width, new_height)

        if resized_image.mode != "RGB":
            resized_image_rgb = resized_image.convert("RGB")
        else:
            resized_image_rgb = resized_image

        image_bytes_stream = io.BytesIO()
        resized_image_rgb.save(image_bytes_stream, format='JPEG')
        image_bytes = image_bytes_stream.getvalue()
        return image_bytes

    @staticmethod
    def _get_font_based_on_image_size(image):
        try:
            factor = 30
            size = int(min(max(image.width/factor, image.height/factor), 50))
            font = ImageFont.truetype("arial.ttf", size)
        except IOError:
            print("Font not found, using default font.")
            font = ImageFont.load_default()
        return font

    @staticmethod
    def draw_boxes(image, results):
        """Overlay labeled boxes on an image with formatted scores and label names."""
        colors = list(ImageColor.colormap.values())
        font = ImageUtils._get_font_based_on_image_size(image)

        draw = ImageDraw.Draw(image)
        im_width, im_height = image.size
        thickness = 4

        for result in results:
            class_, score, box = result["class"], result["score"], result["box"]
            ymin, xmin, ymax, xmax = tuple(box)
            display_str = "{}: {}%".format(class_, int(100 * score))
            display_str_list = [display_str]
            color = colors[hash(class_) % len(colors)]
            (left, right, top, bottom) = (xmin * im_width, xmax * im_width, ymin * im_height, ymax * im_height)

            draw.line([(left, top), (left, bottom), (right, bottom), (right, top), (left, top)], width=thickness, fill=color)

            display_str_heights = [font.getsize(ds)[1] for ds in display_str_list]
            # Each display_str has a top and bottom margin of 0.05x.
            total_display_str_height = (1 + 2 * 0.05) * sum(display_str_heights)

            if top > total_display_str_height:
                text_bottom = top
            else:
                text_bottom = bottom + total_display_str_height
            # Reverse list and print from bottom to top.
            for display_str in display_str_list[::-1]:
                text_width, text_height = font.getsize(display_str)
                margin = math.ceil(0.05 * text_height)
                draw.rectangle([(left, text_bottom - text_height - 2 * margin), (left + text_width, text_bottom)], fill=color)
                draw.text((left + margin, text_bottom - text_height - margin), display_str, fill="black", font=font)
                text_bottom -= text_height - 2 * margin

        return image

    @staticmethod
    def display_image(image):
        #pylint: disable=unused-argument
        fig = plt.figure(figsize=(20, 15))
        plt.grid(False)
        plt.imshow(image)

import pathlib

def test_utils():
    image_url = pathlib.Path(pathlib.Path(__file__).parent, "data/yard.jpg").as_uri()
    if isinstance(image_url, ("".__class__, u"".__class__)):
        image = ImageUtils.get_image(image_url)

    ImageUtils.display_image(image)

    image_bytes = ImageUtils.prepare_image(image, 640, 480)
    resized_image = Image.open(io.BytesIO(image_bytes))
    ImageUtils.display_image(resized_image)

    results = [{"class": "TEST_CLASS", "score": 0.88, "box": [0.2, 0.2, 0.8, 0.8]}]

    image_with_boxes = ImageUtils.draw_boxes(resized_image, results)
    ImageUtils.display_image(image_with_boxes)
    
    plt.show(block=True)
    return "OK"

if __name__ == "__main__":
    test_utils()
    plt.show(block=True)

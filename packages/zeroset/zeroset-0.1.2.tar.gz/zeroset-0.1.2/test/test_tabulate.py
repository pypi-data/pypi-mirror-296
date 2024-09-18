from tabulate import tabulate
import sys
import cv2
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def from_pil(img_pil):
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def center_pad(img: np.ndarray, width: int, height: int, value=33):
    """
    Places an image at the size you specify, centered and keep ratio.
    :param img: opencv image
    :param width: width
    :param height: height
    :param value: pad value(int or tuple)
    :return: opencv image
    """
    channel = 1 if len(img.shape) == 2 else img.shape[2]
    if isinstance(value, int):
        value = tuple([value] * channel)
    dst = np.zeros((height, width, channel), dtype=np.uint8) + np.array(value, dtype=np.uint8)
    dx = (dst.shape[1] - img.shape[1]) // 2
    dy = (dst.shape[0] - img.shape[0]) // 2
    dst[dy:dy + img.shape[0], dx:dx + img.shape[1]] = img
    return dst


def create_text_image(text, font_path, font_size=20, line_spacing=5, color='black', title=None):
    # 모노스페이스 폰트 로드
    font = ImageFont.truetype(font_path, font_size)

    # 텍스트를 줄바꿈하여 리스트로 변환
    lines = text.split('\n')

    if title is not None:
        lines = [title, ""] + lines

    # 이미지 크기 추정
    max_line_width = max([font.getsize(line)[0] for line in lines])
    total_height = (font_size + line_spacing) * len(lines)

    # 흰색 배경 이미지 생성
    image = Image.new('RGB', (max_line_width, total_height), color='white')
    draw = ImageDraw.Draw(image)

    # 각 줄의 텍스트를 이미지에 추가
    y_text = 0
    for idx, line in enumerate(lines):
        if title is not None and idx == 0:
            draw.text((0, y_text), line, font=font, fill="blue")
        else:
            draw.text((0, y_text), line, font=font, fill=color)
        y_text += font_size + line_spacing

    return image


table = [["Sun", 696000, 1989100000], ["Earth", 6371, 5973.6], ["Moon", 1737, 73.5], ["Mars", 3390, 641.85]]
headers = ["Planet", "R (km)", "mass (x 10^29 kg)"]

table_formats = ["plain", "simple", "github", "grid", "simple_grid",
                 "rounded_grid", "heavy_grid", "mixed_grid", "double_grid",
                 "fancy_grid", "outline", "simple_outline", "rounded_outline",
                 "heavy_outline", "mixed_outline", "double_outline", "fancy_outline",
                 "pipe", "orgtbl", "asciidoc", "jira", "presto", "pretty", "psql",
                 "rst", "youtrack",
                 "latex", "latex_raw", "latex_booktabs", "latex_longtable", "textile", "tsv"]
["moinmoin", "html", "unsafehtml", "mediawiki", ]
# table = []
# for i in range(0, len(table_formats), 3):
#     row = table_formats[i:i + 3]
#     table.append(row)
#
# print(tabulate(table, headers=["-","-","-","-","-"],tablefmt="github"))

imgs = []
for table_format in table_formats:
    print(f'## {table_format}')

    text = tabulate(table, headers=headers, tablefmt=table_format)
    print(text)
    img = create_text_image(text, "CascadiaMono.ttf", title=f'table_format: {table_format}')
    img = from_pil(img)
    img = center_pad(img, img.shape[1] + 50, img.shape[0] + 50, 255)
    imgs.append(img)

MAX_WIDTH = max(img.shape[1] for img in imgs)
palettes = []
for img in imgs:
    palette = np.zeros((img.shape[0], MAX_WIDTH, 3), dtype=np.uint8)
    palette.fill(255)
    palette[0:img.shape[0], 0:img.shape[1]] = img.copy()
    palettes.append(palette.copy())
    # cv2.imshow("palette", palette)
    # cv2.waitKey(0)

sss = cv2.vconcat(palettes)
cv2.imwrite("tablefmt.png", sss)

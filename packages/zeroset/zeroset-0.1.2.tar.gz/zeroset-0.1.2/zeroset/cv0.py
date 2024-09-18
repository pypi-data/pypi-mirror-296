# 2024.07.14
import os
import cv2
import numpy as np
import re
from typing import *
import base64
import io
from PIL import Image, ImageFont, ImageDraw
from dataclasses import dataclass
import urllib.request
import sys


def glob(pathstr: str, ext: str = None, recursive: bool = False, _natsort: bool = False):
    import glob
    pathstr = re.sub('([\[\]])', '[\\1]', pathstr)
    if ext is not None:
        if ext.startswith("**"):
            recursive = True
        pathstr = os.path.join(pathstr, ext)
    files = glob.glob(pathstr, recursive=recursive)
    if _natsort:
        import natsort
        # files = natsort.natsorted(files)
        files = natsort.humansorted(files)
    return files


def from_blank(width: int, height: int, BGR: Tuple[int, int, int] = (0, 0, 0)) -> np.ndarray:
    return np.zeros((height, width, 3), dtype=np.uint8) + np.array(BGR, dtype=np.uint8)


########## from ? image ##########

# def from_plt(plt, fig):
#     plt.gcf().canvas.get_renderer()
#     img_pil = Image.frombytes('RGB', fig.canvas.get_width_height(), fig.canvas.tostring_rgb())
#     return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def from_url(url: str):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        image_data = response.read()
        image_array = np.asarray(bytearray(image_data), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:  # gif일 경우
            gif = Image.open(io.BytesIO(image_data))
            gif.seek(0)
            image = np.array(gif.convert('RGB'))
        return image
    except Exception as e:
        print(e)
        return None


def from_pil(img_pil):
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)


def from_base64(b64str: str):
    img = Image.open(io.BytesIO(base64.b64decode(b64str)))
    return cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)


def from_bytes(img_bytes):
    return cv2.cvtColor(np.array(Image.open(io.BytesIO(img_bytes))), cv2.COLOR_RGB2BGR)


########## to ? image ##########
def to_base64(img: np.ndarray, ext: str = ".png", params=None):
    return base64.b64encode(cv2.imencode(ext, img, params)[1]).decode("utf-8")


def to_pil(img):
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))


def to_bytes(img: np.ndarray, ext: str = ".png"):
    return cv2.imencode(ext, img)[1].tobytes()


def to_color(img: np.ndarray):
    if len(img.shape) == 2 or img.shape[2] == 1:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def imread(filename: str, flags=cv2.IMREAD_COLOR):
    """
    This imread method supports korean path
    :param filename: image file paths
    :param flags: image open mode flags
    :return: np.ndarray image
    """
    return cv2.imdecode(np.fromfile(filename, np.uint8), flags)


def imwrite(filename: str, img: np.ndarray, params=None):
    """
    This imread method supports korean path
    :param filename: image file path
    :param img: np.ndarray image
    :param params: cv2.imwrite flags
    :return: True if success else False
    """
    r, eimg = cv2.imencode(os.path.splitext(filename)[1], img, params)
    if r:
        with open(filename, mode="wb") as f:
            eimg.tofile(f)
    return r


def imreads(filepaths: str, flags=cv2.IMREAD_COLOR) -> List[np.ndarray]:
    """
    :param filepaths: image file paths
    :param flags:image open mode flags
    :return: images
    """
    return [imread(filepath, flags) for filepath in filepaths]


def waitKey(delay=0):
    return cv2.waitKey(delay)


def waitESC(delay=1):
    return cv2.waitKey(delay) == 27


def exit():
    sys.exit()


@dataclass
class _wndwait:
    waitKey = waitKey
    waitESC = waitESC


IMSHOW_DEFAULT = 0
IMSHOW_BEST = 1
IMSHOW_AUTOSIZE = 2
IMSHOW_FULLSCREEN = 3
IMSHOW_CV2 = 4


def imshow(arg1: Any, arg2: Any = None, mode: int = IMSHOW_BEST):
    """
    :param arg1: window name or image
    :param arg2: image if arg1 is window name else ignored
    :param mode: Just use IMSHOW_BEST
    :return: opencv image window utility class
    """

    if isinstance(arg1, str):
        winname, img = arg1, arg2
    else:
        import inspect
        winnames = [k for k, v in inspect.currentframe().f_back.f_locals.items() if v is arg1]
        winname = winnames[-1] if len(winnames) > 0 else "default"
        img = arg1
    if mode == IMSHOW_BEST:
        import screeninfo
        monitor = [m for m in screeninfo.get_monitors() if m.is_primary == True][0]
        if not cv2.getWindowProperty(winname, cv2.WND_PROP_VISIBLE):
            cv2.namedWindow(winname, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
            nw, nh = resize(img, width=monitor.width, height=monitor.height, return_size=True)
            cv2.resizeWindow(winname, nw, nh)
            cv2.moveWindow(winname, (monitor.width - nw) // 2, (monitor.height - nh) // 2)
        else:
            _, _, cw, ch = cv2.getWindowImageRect(winname)
            window_ratio = cv2.getWindowProperty(winname, cv2.WND_PROP_ASPECT_RATIO)
            image_ratio = img.shape[1] / img.shape[0]
            if abs(image_ratio - window_ratio) > 0.1:
                nw, nh = resize(img, width=cw, return_size=True)
                cv2.resizeWindow(winname, nw, nh)
    elif mode == IMSHOW_AUTOSIZE:
        cv2.namedWindow(winname, cv2.WINDOW_AUTOSIZE)
    elif mode == IMSHOW_FULLSCREEN:
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        _, _, cw, ch = cv2.getWindowImageRect(winname)
        img = resize(img, width=cw, height=ch, return_size=False)
        img = center_pad(img, cw, ch, 33)
    elif mode == IMSHOW_CV2:
        pass

    cv2.imshow(winname, img)
    return _wndwait


def resize(img: np.ndarray, width=None, height=None, interpolation=cv2.INTER_AREA, return_size=False):
    """
    Given both width and height, choose the smaller of the resulting sizes.
    :param img: opencv image
    :param width: width to change
    :param height: height to change
    :param interpolation: interpolation
    :return: opencv image
    """
    h, w = img.shape[:2]
    dims = []
    if height is not None:
        ratio = height / h
        dims.append((int(w * ratio), height))
    if width is not None:
        ratio = width / w
        dims.append((width, int(h * ratio)))
    if len(dims) == 2 and dims[0] > dims[1]:
        dims = dims[1:]
    if len(dims) == 0:
        return img if not return_size else (w, h)

    return cv2.resize(img, dims[0], interpolation=interpolation) if not return_size else dims[0]


def overlay(bgimg3c: np.ndarray, fgimg4c: np.ndarray, coord=(0, 0), inplace=True):
    """
    Overlay a 4-channel image on a 3-channel image
    :param bgimg3c: background 3c image
    :param fgimg4c: foreground 4c image
    :param coord: Coordinates of the bgimg3c  to overlay
    :param inplace: If true, bgimg3c is changed
    :return: Overlaid image
    """
    # if bgimg3c.shape[:2] != fgimg4c.shape[:2]:
    #     raise ValueError(bgimg3c.shape[:2], fgimg4c.shape[:2])
    h, w = fgimg4c.shape[:2]
    crop = bgimg3c[coord[0]:coord[0] + h, coord[1]:coord[1] + w]
    b, g, r, a = cv2.split(fgimg4c)
    mask = cv2.merge([a, a, a])
    fgimg3c = cv2.merge([b, g, r])
    mask = mask / 255.0
    mask_inv = 1.0 - mask
    ret = (crop * mask_inv + fgimg3c * mask).clip(0, 255).astype(np.uint8)
    if inplace:
        bgimg3c[coord[0]:coord[0] + h, coord[1]:coord[1] + w] = ret
    return ret


def center_pad(img: np.ndarray, width: int, height: int, value: Any = 33):
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


def letterbox(img: np.ndarray, value: Any):
    """
    Put a pad value on the image to change it to a 1:1 aspect ratio.
    :param img: opencv image
    :param value: pad value(int or tuple)
    :return: opencv image
    """
    channel = 1 if len(img.shape) == 2 else img.shape[2]
    if isinstance(value, int):
        value = tuple([value] * channel)
    N = max(img.shape[:2])
    dst = np.zeros((N, N, img.shape[2]), dtype=np.uint8) + np.array(value, dtype=np.uint8)
    dx = (N - img.shape[1]) // 2
    dy = (N - img.shape[0]) // 2
    dst[dy:dy + img.shape[0], dx:dx + img.shape[1]] = img
    return dst


def _to_image_list(args):
    imgs = []
    for arg in args:
        if isinstance(arg, list):
            imgs += arg
        elif isinstance(arg, np.ndarray):
            imgs.append(arg)
        else:
            pass
    return imgs


def hconcat(*args):
    """
    Return the input images horizontally.
    :param args: opencv image list OR comma seperated images
    :return: opencv image
    """
    imgs = _to_image_list(args)
    max_height = max(img.shape[0] for img in imgs)
    rimgs = [to_color(resize(img, height=max_height)) for img in imgs]
    return cv2.hconcat(rimgs)


def vconcat(*args):
    """
    Return the input images vertically.
    :param args: opencv image list OR comma seperated images
    :return: opencv image
    """
    imgs = _to_image_list(args)
    max_width = max(img.shape[1] for img in imgs)
    rimgs = [to_color(resize(img, width=max_width)) for img in imgs]
    return cv2.vconcat(rimgs)


def canny(img: np.ndarray):
    if len(img.shape) == 3:
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    high_th, _ = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    low_th = high_th / 2
    return cv2.Canny(img, low_th, high_th)


def write_fit_text(width: int, height: int, text: str, lr_pad=0, tb_pad=0, bg_color=(255, 255, 255), fg_color=(0, 0, 0),
                   align: str = "center", font_file: str = "NanumGothic.ttf"):
    image_size = {
        "width" : width - lr_pad * 2,
        "height": height - tb_pad * 2
    }

    dummy_img = Image.new("RGB", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    font_sizes = []
    for direction in ["width", "height"]:
        font_small, font_large = 1, 1000
        while font_small <= font_large:
            font_size = (font_small + font_large) // 2
            font = ImageFont.truetype(font_file, font_size)
            bbox = dummy_draw.textbbox((0, 0), text=text, font=font, font_size=font_size)
            text_size = {"width": bbox[2] - bbox[0], "height": bbox[3] - bbox[1]}
            if text_size["width"] <= image_size["width"] and text_size["height"] <= image_size["height"]:
                font_sizes.append(font_size)
            if text_size[direction] > image_size[direction]:
                font_large = font_size - 1
            else:
                font_small = font_size + 1
    max_font_size = max(font_sizes)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font_file, max_font_size)
    bbox = draw.textbbox((0, 0), text, font=font, font_size=max_font_size)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (image_size["width"] - text_width) / 2 - bbox[0]
    text_y = (image_size["height"] - text_height) / 2 - bbox[1]
    if align == "center":
        text_x += lr_pad
        text_y += tb_pad
    if align == "left":
        text_y += tb_pad
    draw.text((text_x, text_y), text, font=font, font_size=max_font_size, fill=fg_color)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return img_cv

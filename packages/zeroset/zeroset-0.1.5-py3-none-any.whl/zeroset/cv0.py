# 2024.09.18
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
import platform
from image_similarity_measures import quality_metrics
import imagehash
from dataclasses import dataclass
from enum import Enum, auto
import imageio


class similarity:
    @staticmethod
    def _quality_metrics(img1: np.ndarray, img2: np.ndarray, func: Callable[[np.ndarray, np.ndarray], float], size: Optional[Union[int, Tuple[int, ...]]] = None):
        """
        Compares two images using a function
        :param img1: opencv image(np.ndarray)
        :param img2: opencv image(np.ndarray)
        :param func: Functions in image_similarity_measures.quality_metrics
        :param size: Automatically resize the image if size is None.
                     If size is int, resize both width and height to the same size.
                     If size is a tuple, resize width,height to the specified value.
        :return: The return of the specified function(float)
        """
        if size is None:
            h1, w1 = img1.shape[:2]
            h2, w2 = img2.shape[:2]
            w, h = min(w1, w2), min(h1, h2)
        elif isinstance(size, int):
            w, h = size, size
        elif isinstance(size, tuple):
            w, h = size[0], size[1]
        else:
            raise TypeError("")
        img1r = cv2.resize(img1, (w, h))
        img2r = cv2.resize(img2, (w, h))
        return func(img1r, img2r)

    @staticmethod
    def rmse(img1: np.ndarray, img2: np.ndarray, size: Optional[Union[int, Tuple[int, ...]]] = None):
        # Root mean square error (RMSE)
        return similarity._quality_metrics(img1, img2, quality_metrics.rmse, size)

    @staticmethod
    def psnr(img1: np.ndarray, img2: np.ndarray, size: Optional[Union[int, Tuple[int, ...]]] = None):
        # Peak signal-to-noise ratio (PSNR)
        return similarity._quality_metrics(img1, img2, quality_metrics.psnr, size)

    @staticmethod
    def ssim(img1: np.ndarray, img2: np.ndarray, size: Optional[Union[int, Tuple[int, ...]]] = None):
        # Structural Similarity Index (SSIM)
        return similarity._quality_metrics(img1, img2, quality_metrics.ssim, size)

    @staticmethod
    def fsim(img1: np.ndarray, img2: np.ndarray, size: Optional[Union[int, Tuple[int, ...]]] = None):
        # Feature-based similarity index (FSIM)
        return similarity._quality_metrics(img1, img2, quality_metrics.fsim, size)

    @staticmethod
    def sre(img1: np.ndarray, img2: np.ndarray, size: Optional[Union[int, Tuple[int, ...]]] = None):
        # Signal to reconstruction error ratio (SRE)
        return similarity._quality_metrics(img1, img2, quality_metrics.sre, size)


class hash:
    @staticmethod
    def _get_image_hash(img1: np.ndarray, func: Callable[[np.ndarray], float]):
        ret = func(to_pil(img1))
        return ret

    @staticmethod
    def average_hash(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.average_hash)

    @staticmethod
    def colorhash(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.colorhash)

    @staticmethod
    def phash(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.phash)

    @staticmethod
    def phash_simple(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.phash_simple)

    @staticmethod
    def whash(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.whash)

    @staticmethod
    def dhash(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.dhash)

    @staticmethod
    def dhash_vertical(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.dhash_vertical)

    @staticmethod
    def crop_resistant_hash(img1: np.ndarray):
        return hash._get_image_hash(img1, imagehash.crop_resistant_hash)


@dataclass(frozen=True)
class GLOB(Enum):
    SORT_DEFAULT = auto()
    SORT_NAT = auto()
    SORT_SIZE = auto()


def glob(pathstr: str, ext: str = None, recursive: bool = False, sort_method: int = GLOB.SORT_DEFAULT):
    import glob
    pathstr = re.sub('([\[\]])', '[\\1]', pathstr)
    if ext is not None:
        if ext.startswith("**"):
            recursive = True
        pathstr = os.path.join(pathstr, ext)
    files = glob.glob(pathstr, recursive=recursive)
    if sort_method == GLOB.SORT_NAT:
        import natsort
        # files = natsort.natsorted(files)
        files = natsort.humansorted(files)
    elif sort_method == GLOB.SORT_SIZE:
        files.sort(key=lambda x: os.path.getsize(x))
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


def imwrite(filename: str, img: Union[np.ndarray, list[np.ndarray]], params: Optional[int] = None):
    """
    This imread method supports korean path
    :param filename: image file path
    :param img: np.ndarray image
    :param params: cv2.imwrite flags, Use duration if saving the file as a gif
    :return: True if success else False
    """

    if os.path.splitext(filename)[1] == ".gif":
        duration = 1000 if params is None else params
        frames = [to_pil(frame) for frame in img]
        frames[0].save(filename, format='GIF',
                       append_images=frames[1:],
                       save_all=True,
                       duration=duration, loop=0)
        return True
    else:
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


@dataclass(frozen=True)
class IMSHOW(Enum):
    DEFAULT = auto()
    BEST = auto()
    AUTOSIZE = auto()
    FULLSCREEN = auto()
    CV2 = auto()


def imshow(arg1: Any, arg2: Any = None, mode: int = IMSHOW.BEST):
    """
    :param arg1: window name or image
    :param arg2: image if arg1 is window name else ignored
    :param mode: Just use IMSHOW_BEST
    :return: opencv image window utility class
    """
    if not platform.platform().startswith('Windows'):
        mode = IMSHOW.DEFAULT
    if isinstance(arg1, str):
        winname, img = arg1, arg2
    else:
        import inspect
        winnames = [k for k, v in inspect.currentframe().f_back.f_locals.items() if v is arg1]
        winname = winnames[-1] if len(winnames) > 0 else "default"
        img = arg1
    if mode == IMSHOW.BEST:
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
    elif mode == IMSHOW.AUTOSIZE:
        cv2.namedWindow(winname, cv2.WINDOW_AUTOSIZE)
    elif mode == IMSHOW.FULLSCREEN:
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(winname, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        _, _, cw, ch = cv2.getWindowImageRect(winname)
        img = resize(img, width=cw, height=ch, return_size=False)
        img = center_pad(img, cw, ch, 33)
    elif mode == IMSHOW.CV2:
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


if __name__ == '__main__':
    # files = glob("W:/Dropbox/DesignAsset/PANEL/*.*")
    # imgs = imreads(files)
    # imgs = [resize(img, height=400) for img in imgs]
    #
    # imwrite("test.gif", imgs)
    # exit()

    img1 = imread("../data/computer01.jpg")
    img2 = imread("../data/computer02.jpg")
    r = similarity.rmse(img1, img2)
    print(r)

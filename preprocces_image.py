from pathlib import Path
from typing import Optional

import cv2
import numpy as np
from typer import Argument
from typer import Option
from typer import Typer

app = Typer(add_completion=False)

IMAGE_W = 800
IMAGE_H = 600
IMAGE_R = IMAGE_W / IMAGE_H

THUMBNAIL_W = 240
THUMBNAIL_H = 240


def downsize_image(src: np.ndarray) -> np.ndarray:
    """resize image to a manageable size"""
    shape_orig = src.shape
    ORIG_W = shape_orig[1]
    ORIG_H = shape_orig[0]
    ORIG_R = ORIG_W / ORIG_H
    if ORIG_R > IMAGE_R:
        # image is wider than target
        f = IMAGE_W / ORIG_W * 2
    else:
        # image is higher than target
        f = IMAGE_W / ORIG_W * 2

    return cv2.resize(src, dsize=None, fx=f, fy=f)


Roi = tuple[int, int, int, int]


@app.command()
def main(
        file: Path = Argument(..., exists=True, file_okay=True, readable=True),
        select_roi: Optional[bool] = Option(False, "--roi"),
        out: Optional[Path] = Option(..., exists=True, dir_okay=True, writable=True),
):
    img = cv2.imread(str(file))

    img = downsize_image(img)
    if select_roi:
        roi = cv2.selectROI("roi", img, False, False)
        if roi == (0, 0, 0, 0):
            print("no ROI selected, exiting")
            return
        print(f"selected ROI: {roi}")
        img = img[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]

    image = cut_image(img, IMAGE_W, IMAGE_H, "image")
    cv2.imshow("image", image)

    thumbnail = cut_image(img, THUMBNAIL_W, THUMBNAIL_H, "thumbnail")
    cv2.imshow("thumbnail", thumbnail)

    if out:
        file = out / "image.jpg"
        cv2.imwrite(str(file), image)
        print(f"saved image: {file}")

        file = out / "thumbnail.jpg"
        cv2.imwrite(str(file), thumbnail)
        print(f"saved thumbnail: {file}")

    cv2.waitKey(60 * 1000)


def cut_image(src: np.ndarray, w: int, h: int, what: str) -> np.ndarray:
    src_w = src.shape[1]
    src_h = src.shape[0]

    dst_w = w
    dst_h = h

    center_x = int(src_w / 2)
    center_y = int(src_h / 2)

    src_ratio = src_w / src_h
    dst_ratio = dst_w / dst_h

    if src_ratio > dst_ratio:
        # image is wider than target
        new_w = int(src_h * dst_ratio)
        new_h = src_h
    else:
        # image is higher than target
        new_w = src_w
        new_h = int(src_w / dst_ratio)

    roi = (center_x - int(new_w / 2), center_y - int(new_h / 2), new_w, new_h)

    img_selection = src.copy()
    cv2.rectangle(img_selection, (roi[0], roi[1]), (roi[0] + roi[2], roi[1] + roi[3]), (0, 0, 255), 3)
    cv2.imshow(f"selection of {what}", img_selection)

    img_cut = src[roi[1]:roi[1] + roi[3], roi[0]:roi[0] + roi[2]]
    img_out = cv2.resize(img_cut, (dst_w, dst_h))

    return img_out


def save_image(img: np.ndarray, path: Path):
    cv2.imwrite(str(path), img)
    print(f"saved image: {path}")


if __name__ == '__main__':
    app()

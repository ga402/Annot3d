import numpy as np
import functools
from joblib import delayed, Parallel
from libs.utils import *


@apply3D
def addChannel(img):
    x, y, _ = img.shape
    layer = np.zeros((x, y), dtype="uint8")
    return np.dstack([img, layer])


def readNdArray(file):
    arr = np.load(file)
    arr = arr.astype("uint8")
    assert len(arr.shape) == 4, "loaded array wrong dimensions"
    z, x, y, c = arr.shape
    if c < 3:
        img = arr
        while True:
            img = addChannel(img)
            if img.shape[3] == 3:
                break
    elif c > 3:
        img = arr[:, :, :, 0:3]
    elif c == 3:
        img = arr
    return img

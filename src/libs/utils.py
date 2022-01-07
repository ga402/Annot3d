import numpy as np
import cv2 as cv
import functools
import pandas as pd
import cv2 as cv
from joblib import delayed, Parallel

# from numba import jit
import multiprocessing


def dfuncapply(func, img):
    return np.array([func(img[i, ...]) for i in np.arange(0, img.shape[0])])


def apply3D(func):
    """[summary]

    Args:
        func ([type]): [description]

    Returns:
        [nd.array]: array
    """

    @functools.wraps(func)
    def wrapper_apply3D(*args, **kwargs):
        return dfuncapply(func, *args)

    return wrapper_apply3D


def sfuncapply(func, img):
    return [func(img[i, ...]) for i in np.arange(0, img.shape[0])]


def sapply3D(func):
    """[summary]

    Args:
        func ([type]): [description]

    Returns:
        [type]: list
    """

    @functools.wraps(func)
    def wrapper_sapply3D(*args, **kwargs):
        return sfuncapply(func, *args)

    return wrapper_sapply3D


def dfuncapply2Arr(func, img, img2):
    return np.array(
        [func(img[i, ...], img2[i, ...]) for i in np.arange(0, img.shape[0])]
    )


def applyTwoArr3D(func):
    """Wrapper function to apply a function to two arrays and return a single array

    Args:
        func ([type]): [description]

    Returns:
        [nd.array]: single nd.array
    """

    @functools.wraps(func)
    def wrapper_applyTwoArr3D(*args, **kwargs):
        return dfuncapply2Arr(func, *args)

    return wrapper_applyTwoArr3D


def dfuncapplyVec2Arr(func, img, vec):
    assert img.shape[0] == len(vec), "array and vector dimensions do not match"
    return np.array([func(img[i, ...], vec[i]) for i in np.arange(0, img.shape[0])])


def applyVec2Arr3D(func):
    """[summary]

    Args:
        func ([type]): [description]

    Returns:
        [nd.array]: 3d nd.array
    """

    @functools.wraps(func)
    def wrapper_apply3DVec2Arr(*args, **kwargs):
        return dfuncapplyVec2Arr(func, *args)

    return wrapper_apply3DVec2Arr


def getCPUs():
    """get the number of CPUs available

    Returns:
        [int]: number of CPUs on machine
    """
    try:
        cpus = multiprocessing.cpu_count()
        cpus = int(cpus / 2)
    except NotImplementedError:
        cpus = 2  # arbitrary default
    finally:
        return cpus


def parallelfuncapply(func, img):
    """apply function in parallel

    Args:
        func ([type]): [description]
        img ([type]): [description]

    Returns:
        [type]: [description]
    """
    cpu_count = getCPUs()
    values = Parallel(n_jobs=cpu_count)(
        delayed(func)(img[i, ...]) for i in np.arange(0, img.shape[0])
    )
    return np.array(values)


def sparallelfuncapply(func, img):
    """apply function in parallel

    Args:
        func ([type]): [description]
        img ([type]): [description]

    Returns:
        [type]: [description]
    """
    cpu_count = getCPUs()
    values = Parallel(n_jobs=cpu_count)(
        delayed(func)(img[i, ...]) for i in np.arange(0, img.shape[0])
    )
    return values


def papply3D(func):
    """decorator of parallelfuncapply

    Args:
        func ([type]): [description]

    Returns:
        [type]: [description]
    """

    @functools.wraps(func)
    def wrapper_papply3D(*args, **kwargs):
        return parallelfuncapply(func, *args)

    return wrapper_papply3D


def spapply3D(func):
    """decorator of parallelfuncapply

    Args:
        func ([type]): [description]

    Returns:
        [type]: [description]
    """

    @functools.wraps(func)
    def wrapper_spapply3D(*args, **kwargs):
        return sparallelfuncapply(func, *args)


def parallelTwoArrfuncapply(func, img, img2):
    """apply function in parallel

    Args:
        func ([type]): [description]
        img ([type]): [description]

    Returns:
        [type]: [description]
    """
    cpu_count = getCPUs()
    values = Parallel(n_jobs=cpu_count)(
        delayed(func)(img[i, ...], img2[i, ...]) for i in np.arange(0, img.shape[0])
    )
    return np.array(values)


def papply3DTwoArr(func):
    """decorator of parallelfuncapply to two arrays

    Args:
        func ([type]): [description]

    Returns:
        [type]: nd.array
    """

    @functools.wraps(func)
    def wrapper_papply3DTwoArr(*args, **kwargs):
        return parallelTwoArrfuncapply(func, *args)

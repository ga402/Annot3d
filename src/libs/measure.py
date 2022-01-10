
from math import sqrt
import hashlib
import re
import sys


def distance(p):
    return sqrt(p.x() * p.x() + p.y() * p.y())
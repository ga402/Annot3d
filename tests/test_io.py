import os
import sys
import unittest
import numpy as np


class testNumpyRead(unittest.TestCase):
    def test_addChannel(self):
        dir_name = os.path.abspath(os.path.dirname(__file__))
        libs_path = os.path.join(dir_name, "..", "src/libs")
        sys.path.insert(0, libs_path)

        from imagefuncs import addChannel

        img = np.zeros((2, 416, 416, 2), dtype="uint8")
        img = addChannel(img)
        self.assertEqual(img.shape[3], 3)

    def test_readNdArray(self):

        for i in range(1, 5):
            img = np.zeros((2, 416, 416, i), dtype="uint8")
            np.save(f"test{i}.npy", img)

        from imagefuncs import readNdArray

        for i in range(1, 5):
            img = readNdArray(f"test{i}.npy")
            self.assertEqual(img.shape[3], 3)
            self.assertEqual(img.shape[0], 2)
            self.assertEqual(img.shape[1], 416)
            self.assertEqual(img.shape[2], 416)


if __name__ == "__main__":
    unittest.main()

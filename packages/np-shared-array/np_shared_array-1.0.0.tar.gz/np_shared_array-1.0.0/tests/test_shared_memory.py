from multiprocessing import Process
from unittest import TestCase
import gc

from src.np_shared_array.shared_array import SharedNumpyArray, create_shared_array


def worker(shared_array: SharedNumpyArray):
    array = shared_array.to_numpy()
    array[0][0] = 1


class TestSharedMemory(TestCase):
    def test_process_modifies_array(self):
        shared_array_struct = create_shared_array([10, 10])
        shared_array = shared_array_struct.to_numpy()
        p = Process(target=worker, args=(shared_array_struct,))
        p.start()
        p.join()
        assert shared_array[0][0] == 1
        assert shared_array[0][1] == 0

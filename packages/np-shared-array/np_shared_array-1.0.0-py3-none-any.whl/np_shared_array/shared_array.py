from __future__ import annotations

from dataclasses import dataclass
from multiprocessing import RLock
from multiprocessing.managers import SharedMemoryManager
from multiprocessing.shared_memory import SharedMemory
from typing import Sequence, SupportsIndex, Tuple

import numpy as np
import numpy.typing as npt

_np_shared_array_smm: SharedMemoryManager | None = None


def create_shared_array(shape: Sequence[SupportsIndex], dtype: np.dtype = float) -> SharedNumpyArray:
    tmp = np.zeros(shape=shape, dtype=dtype)
    return SharedNumpyArray.from_numpy(tmp)


@dataclass
class SharedNumpyArray:
    memory: SharedMemory
    dtype: np.dtype
    shape: Tuple[int, ...]
    lock: RLock

    def to_numpy(self) -> npt.NDArray:
        arr = np.ndarray((np.prod(self.shape),), dtype=self.dtype, buffer=self.memory.buf)
        arr = arr[: np.prod(self.shape)].reshape(self.shape)
        return arr

    @classmethod
    def from_numpy(cls, array: npt.NDArray) -> SharedNumpyArray:
        manager = _get_memory_manager()
        memory = manager.SharedMemory(size=array.nbytes)
        return SharedNumpyArray(memory=memory, dtype=array.dtype, shape=array.shape, lock=RLock())


def _get_memory_manager() -> SharedMemoryManager:
    global _np_shared_array_smm
    if _np_shared_array_smm is None:
        _np_shared_array_smm = SharedMemoryManager()
        _np_shared_array_smm.start()
    return _np_shared_array_smm

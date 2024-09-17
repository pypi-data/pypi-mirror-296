# np-shared-array
Utility for sharing numpy arrays between processes. This can be useful if you have a background process
performing a calculation and main process on an API which can query the array.

Usage:

```python
from np_shared_array import create_shared_array, SharedNumpyArray
from multiprocessing import Process


def worker(shared_array: SharedNumpyArray):
    array = shared_array.to_numpy()
    with shared_array.lock:
        array[0][0] = 1


def main():
    shape = [10, 10]
    shared_array = create_shared_array(shape)
    array = shared_array.to_numpy()
    p = Process(
        target=worker,
        args=(shared_array,)
    )
    p.start()
    p.join()
    with shared_array.lock:
        print(array[0][0])


if __name__ == "__main__":
    main()
```

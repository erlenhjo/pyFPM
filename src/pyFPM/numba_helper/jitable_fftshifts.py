import numpy as np
from numba import njit, prange
import timeit

@njit(cache=True)
def fftshift(x: np.ndarray):
    shift_y = x.shape[0]//2
    shift_x = x.shape[1]//2
    return roll_forward(a=x, shift_x=shift_x, shift_y=shift_y)

@njit(cache=True)
def ifftshift(x: np.ndarray):
    shift_y = x.shape[0]//2
    shift_x = x.shape[1]//2
    return roll_backwards(a=x, shift_x=shift_x, shift_y=shift_y)

@njit(cache=True)
def roll_forward(a: np.ndarray, shift_x, shift_y):
    b = np.empty_like(a)
    c = np.empty_like(a)
    rows_num = a.shape[0]
    cols_num = a.shape[1]

    #shift x
    b[:, shift_x:] = a[:, :cols_num - shift_x]
    b[:, :shift_x] = a[:, cols_num - shift_x:]
    #shift y
    c[shift_y:, :] = b[:rows_num - shift_y, :]
    c[:shift_y, :] = b[rows_num - shift_y:, :]

    return c

@njit(cache=True)
def roll_backwards(a: np.ndarray, shift_x, shift_y):
    b = np.empty_like(a)
    c = np.empty_like(a)
    rows_num = a.shape[0]
    cols_num = a.shape[1]

    #reverse shift x
    b[:, cols_num-shift_x:] = a[:, :shift_x]
    b[:, :cols_num-shift_x] = a[:, shift_x:]
    #reverse shift y
    c[rows_num-shift_y:, :] = b[:shift_y, :]
    c[:rows_num-shift_y, :] = b[shift_y:, :]
    return c




def test_fftshift_speed():
    print(timeit.timeit("test_1", setup="from __main__ import test_1", number=10000))
    print(timeit.timeit("test_2", setup="from __main__ import test_2", number=10000))
    print(timeit.timeit("test_3", setup="from __main__ import test_3", number=10000))
    print(timeit.timeit("test_4", setup="from __main__ import test_4", number=10000))

def test_ifftshift_speed():
    print(timeit.timeit("test_i1", setup="from __main__ import test_i1", number=10000))
    print(timeit.timeit("test_i2", setup="from __main__ import test_i2", number=10000))
    print(timeit.timeit("test_i3", setup="from __main__ import test_i3", number=10000))
    print(timeit.timeit("test_i4", setup="from __main__ import test_i4", number=10000))


def test_results():
    assert np.array_equal(test_1(),test_2())
    assert np.array_equal(test_3(),test_4())
    assert np.array_equal(test_i1(),test_i2())
    assert np.array_equal(test_i3(),test_i4())
    
a1 = np.reshape(np.linspace(start=0, stop=100000, num=10000*20000),(10000,20000))
a2 = np.reshape(np.linspace(start=0, stop=100000, num=10001**2),(10001,10001))

def test_1():
    return fftshift(a1)
def test_2():
    return np.fft.fftshift(a1)
def test_3():
    return fftshift(a2)
def test_4():
    return np.fft.fftshift(a2)

def test_i1():
    return ifftshift(a1)
def test_i2():
    return np.fft.ifftshift(a1)
def test_i3():
    return ifftshift(a2)
def test_i4():
    return np.fft.ifftshift(a2)


if __name__ == "__main__":
    test_fftshift_speed()
    test_ifftshift_speed()
    test_results()



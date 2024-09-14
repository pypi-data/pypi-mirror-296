import numpy as np
from numba import njit


@njit(inline="always")
def nbamin(a: np.ndarray) -> float:
    return np.amin(a)


@njit(inline="always")
def nbamax(a: np.ndarray) -> float:
    return np.amax(a)


@njit(inline="always")
def nbmedian(a: np.ndarray) -> float:
    return np.median(a)


@njit(inline="always")
def nbnancumprod(a: np.ndarray) -> np.ndarray:
    return np.nancumprod(a)


@njit(inline="always")
def nbnancumsum(a: np.ndarray) -> np.ndarray:
    return np.nancumsum(a)


@njit(inline="always")
def nbnanmax(a: np.ndarray) -> float:
    return np.nanmax(a)


@njit(inline="always")
def nbnanmean(a: np.ndarray) -> float:
    return np.nanmean(a)


@njit(inline="always")
def nbnanmedian(a: np.ndarray) -> float:
    return np.nanmedian(a)


@njit(inline="always")
def nbnanmin(a: np.ndarray) -> float:
    return np.nanmin(a)


@njit(inline="always")
def nbnanpercentile(a: np.ndarray, q: float) -> float:
    return np.nanpercentile(a, q)


@njit(inline="always")
def nbnanquartile(a: np.ndarray, q: float) -> float:
    return np.nanquantile(a, q)


@njit(inline="always")
def nbnanprod(a: np.ndarray) -> float:
    return np.nanprod(a)


@njit(inline="always")
def nbnanstd(a: np.ndarray) -> float:
    return np.nanstd(a)


@njit(inline="always")
def nbnansum(a: np.ndarray) -> float:
    return np.nansum(a)


@njit(inline="always")
def nbnanvar(a: np.ndarray) -> float:
    return np.nanvar(a)


@njit(inline="always")
def nbpercentile(a: np.ndarray, q: float) -> float:
    return np.percentile(a, q)


@njit(inline="always")
def nbquantile(a: np.ndarray, q: float) -> float:
    return np.quantile(a, q)


@njit(inline="always")
def nbprod(a: np.ndarray) -> float:
    return np.prod(a)


@njit(inline="always")
def nbstdev(a: np.ndarray) -> float:
    return np.std(a)


@njit(inline="always")
def nbsum(a: np.ndarray) -> float:
    return np.sum(a)


@njit(inline="always")
def nbvar(a: np.ndarray) -> float:
    return np.var(a)


@njit(inline="always")
def nbdiff(a: np.ndarray, n: int = 1) -> np.ndarray:
    """
    Constraints:
    * 'a': dim=1, dtype='any numba supported'
    * 'n': dim=1, dtype=int, value='>=0'.
    """
    assert n >= 0 and a.ndim == 1

    if n == 0:
        return a.copy()

    a_size = a.size
    out_size = max(a_size - n, 0)
    out = np.empty(out_size, dtype=a.dtype)

    if out_size == 0:
        return out

    work = np.empty_like(a)

    # First iteration: diff a into work
    for i in range(a_size - 1):
        work[i] = a[i + 1] - a[i]

    # Other iterations: diff work into itself
    for niter in range(1, n):
        for i in range(a_size - niter - 1):
            work[i] = work[i + 1] - work[i]

    # Copy final diff into out
    out[:] = work[:out_size]

    return out

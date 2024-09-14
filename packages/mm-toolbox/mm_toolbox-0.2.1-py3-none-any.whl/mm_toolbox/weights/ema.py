import numpy as np
from numba import njit
from numba.types import float64
from typing import Optional


@njit(error_model="numpy", fastmath=True)
def ema_weights(window: int, alpha: Optional[float] = None) -> np.ndarray[float]:
    """
    Calculate EMA (Exponential Moving Average)-like weights for a given window size.

    Parameters
    ----------
    window : int
        The number of periods to use for the EMA calculation.

    alpha : float, optional
        The decay factor for the EMA calculation. If not provided, it is calculated as 3 / (window + 1).

    Returns
    -------
    np.ndarray
        An array of normalized EMA-like weights from lowest -> highest.
    """
    assert window > 1, "Number of weights generated cannot be <1."
    alpha = alpha if alpha is not None else 3.0 / float(window + 1)
    weights = np.array(
        [alpha * (1.0 - alpha) ** i for i in range(window - 1, -1, -1)], dtype=float64
    )
    return weights

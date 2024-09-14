import numpy as np
from numba import njit
from numba.types import int64, float64, bool_
from numba.experimental import jitclass


@njit(["void(float64[:, :], int64)"], inline="always")
def roll_2d_axis0_inplace(arr: np.ndarray, shift: int) -> None:
    """
    Roll a 2D array along axis 0 (rows) by a specified shift.

    Parameters
    ----------
    arr : np.ndarray
        The input 2D array to be rolled.

    shift : int
        The number of rows by which to roll the array.

    Returns
    -------
    None
        The operation is performed in-place, modifying the input array.
    """
    num_rows = arr.shape[0]
    assert arr.ndim == 2 and num_rows > 0

    arr[:] = arr[::-1]
    arr[:shift] = arr[:shift][::-1]
    arr[shift:] = arr[shift:][::-1]


@njit(["int64(float64[:, :], float64)"], inline="always")
def exp_search_closest_2d_axis0_bids(bids: np.ndarray, price: float) -> int:
    """
    Performs exponential search to find the index of the closest price in a 2D array along axis 0.
    If `isBid` is True, returns the index of the closest price that is <= the target price.
    If `isBid` is False (for asks), returns the index of the closest price that is >= the target price.

    Parameters
    ----------
    book_side : np.ndarray
        The 2D array containing bid or ask price levels, where the first column holds the prices.

    price : float
        The target price to find or approximate in the array.

    Returns
    -------
    int
        Index of the closest price that satisfies the condition (<= for bids, >= for asks).
    """
    # Find range for binary search by repeated doubling.
    index = 1
    n = bids.shape[0]

    while index < n and bids[index, 0] <= price:
        index = index * 2

    # Binary search for the found range.
    left = index // 2
    right = min(index, n - 1)

    while left <= right:
        mid = left + (right - left) // 2
        if bids[mid, 0] == price:
            return mid
        elif bids[mid, 0] < price:
            left = mid + 1
        else:
            right = mid - 1

    # Return the closest index for rolling.
    return left if bids[left, 0] >= price else left + 1


@njit(["int64(float64[:, :], float64)"], inline="always")
def exp_search_closest_2d_axis0_asks(asks: np.ndarray, price: float) -> int:
    """
    Performs exponential search to find the index of the closest price in a 2D array along axis 0.
    If `isBid` is True, returns the index of the closest price that is <= the target price.
    If `isBid` is False (for asks), returns the index of the closest price that is >= the target price.

    Parameters
    ----------
    book_side : np.ndarray
        The 2D array containing bid or ask price levels, where the first column holds the prices.

    price : float
        The target price to find or approximate in the array.

    Returns
    -------
    int
        Index of the closest price that satisfies the condition (<= for asks, >= for asks).
    """
    # Find range for binary search by repeated doubling.
    index = 1
    n = asks.shape[0]

    while index < n and asks[index, 0] <= price:
        index = index * 2

    # Binary search for the found range.
    left = index // 2
    right = min(index, n - 1)

    while left <= right:
        mid = left + (right - left) // 2
        if asks[mid, 0] == price:
            return mid
        elif asks[mid, 0] < price:
            left = mid + 1
        else:
            right = mid - 1

    # Return the closest index for rolling.
    return left if asks[left, 0] >= price else left + 1


@njit(["void(float64[:, :], float64, float64, bool_)"], inline="always")
def roll_and_insert(arr, price, size, isBid):
    """
    Rolls the 2D array along axis 0, inserts the price and size at the closest index to maintain sorted order.

    Parameters
    ----------
    arr : np.ndarray
        2D array representing bid or ask levels where the first column holds the prices and the second column holds sizes.

    price : float
        Price level to insert or update.

    size : float
        The size to insert or update at the given price.

    isBid : bool
        If True, this is for bids (closest price <= price). If False, this is for asks (closest price >= price).
    """
    # For bids, we want the closest price that is less than or equal to the price.
    if isBid:
        index = exp_search_closest_2d_axis0_bids(arr, price)

        if arr[index, 0] == price:
            arr[index, 1] = size
            return

        # Shift left and insert new price and size.
        arr[index + 1 :] = arr[index:-1]
        arr[index, 0] = price
        arr[index, 1] = size

    # For asks, we want the closest price that is greater than or equal to the price.
    else:
        index = exp_search_closest_2d_axis0_asks(arr, price)

        if arr[index, 0] == price:
            arr[index, 1] = size
            return

        # Shift right and insert new price and size.
        arr[index + 1 :] = arr[index:-1]
        arr[index, 0] = price
        arr[index, 1] = size


@jitclass
class HFTOrderbook:
    tick_size: float64
    lot_size: float64
    size: int64

    _asks: float64[:, :]
    _bids: float64[:, :]
    _seq_id: int64
    _warmed_up: bool_

    def __init__(self, tick_size: float, lot_size: float, size: int = 500) -> None:
        self.tick_size = tick_size
        self.lot_size = lot_size
        self.size = size

        self._asks = np.zeros((self.size, 2), dtype=float64)
        self._bids = np.zeros((self.size, 2), dtype=float64)
        self._seq_id = 0
        self._warmed_up = False

    def _reset(self) -> None:
        """
        Resets the order book by clearing the bids and asks and setting warmed_up to False.
        """
        self._asks.fill(0.0)
        self._bids.fill(0.0)
        self._seq_id = 0
        self._warmed_up = False

    def refresh(self, asks: np.ndarray, bids: np.ndarray, new_seq_id: int) -> None:
        """
        Refresh the order book with new bid and ask levels, as well as setting
        a new seq id for future updates.

        Parameters
        ----------
        asks : np.ndarray
            Array of ask prices and sizes, where each row is [price, size].

        bids : np.ndarray
            Array of bid prices and sizes, where each row is [price, size].

        new_seq_id : int
            The sequence ID associated with this update.

        Raises
        ------
        AssertionError
            If input arrays are not 2-dimensional or do not match the order book size.
        """
        assert (
            asks.ndim == 2
            and bids.ndim == 2
            and bids.shape[0] == self.size
            and asks.shape[0] == self.size
        ), "Input arrays must be 2-dimensional and match the order book size."

        self._reset()
        self._bids[:, :] = bids.sort()
        self._asks[:, :] = asks.sort()
        self._seq_id = new_seq_id
        self._warmed_up = True

    def update_bbo(
        self,
        bid_price: float,
        bid_size: float,
        ask_price: float,
        ask_size: float,
        new_seq_id: int,
    ) -> None:
        """
        Processes a BBO (Best Bid and Offer) update.

        Steps
        -----
        1. Process the incoming bid update:
        a. If the incoming bid price matches the best bid price:
            - If the size is zero, remove the level and shift the order book.
            - Otherwise, update the size at the best bid level.
        b. If the incoming bid price is higher than the worst bid price, ignore the update.
        c. If the incoming bid price is between the worst and the best prices, find the exact level to update the size.
        d. If the incoming bid price is better than the best price, adjust the order book to accommodate new price levels.

        2. Process the incoming ask update:
        a. If the incoming ask price matches the best ask price:
            - If the size is zero, remove the level and shift the order book.
            - Otherwise, update the size at the best ask level.
        b. If the incoming ask price is lower than the worst ask price, ignore the update.
        c. If the incoming ask price is between the worst and the best prices, find the exact level to update the size.
        d. If the incoming ask price is better than the best price, adjust the order book to accommodate new price levels.

        Parameters
        ----------
        bids : np.ndarray
            The bids array where each row represents a price level.

        asks : np.ndarray
            The asks array where each row represents a price level.

        updated_bid_price : float
            The updated price for the bid.

        updated_bid_size : float
            The updated size for the bid.

        updated_ask_price : float
            The updated price for the ask.

        updated_ask_size : float
            The updated size for the ask.
        """
        assert self._warmed_up, "Orderbook is not warmed up."

        if new_seq_id <= self._seq_id:
            return

        self.seq_id = new_seq_id

        c_best_bid = self._bids[-1]
        c_best_ask = self._asks[0]
        bbo_same_price_count = 0

        # Same bid price, update size.
        if c_best_bid[0] == bid_price:
            bbo_same_price_count += 1

            if bid_size == 0.0:
                roll_2d_axis0_inplace(self._bids, 1)
                self._bids[0, 0] = self._bids[1, 0] - self.tick_size
                self._bids[0, 1] = 0.0
            else:
                self._bids[-1, 1] = bid_size

        # Same bid price, update size.
        if c_best_ask[0] == ask_price:
            bbo_same_price_count += 1

            if ask_size == 0.0:
                roll_2d_axis0_inplace(self._asks, -1)
                self._asks[-1, 0] = self._asks[-2, 0] + self.tick_size
                self._asks[-1, 1] = 0.0
            else:
                self._asks[0, 1] = ask_size

        # If both prices were the same, early return.
        if bbo_same_price_count == 2:
            return

        # New best bid price, roll bids left, insert new bid and fix sizes.
        if bid_price > c_best_bid[0]:
            roll_2d_axis0_inplace(self._bids, -1)
            self._bids[-1, 0] = bid_price
            self._bids[-1, 1] = bid_size
            c_best_bid = self._bids[-1]

            # Overlapping bid price, roll asks right and fix sizes.
            if bid_price > c_best_ask[0]:
                stale_levels = self._asks[self._asks[:, 0] <= bid_price].shape[0]
                roll_2d_axis0_inplace(self._asks, -stale_levels)
                self._asks[-stale_levels:].fill(0.0)
                c_best_ask = self._asks[0]

        # New best ask price, roll asks right, insert new ask and fix sizes.
        if ask_price < c_best_ask[0]:
            roll_2d_axis0_inplace(self._asks, 1)
            self._asks[0, 0] = ask_price
            self._asks[0, 1] = ask_size
            c_best_ask = self._asks[0]

            # Overlapping ask price, roll bids right and fix sizes.
            if ask_price < c_best_bid[0]:
                stale_levels = self._bids[self._bids[:, 0] >= ask_price].shape[0]
                roll_2d_axis0_inplace(self._bids, stale_levels)
                self._asks[:stale_levels].fill(0.0)
                c_best_bid = self._bids[-1]

    def update_asks(self, updated_asks: np.ndarray, new_seq_id: int) -> None:
        """
        Processes a full level 2 update for asks.

        Steps:
        1. Identify the best and worst price levels in the current asks.
        2. For each update in the updates array:
            a. If the incoming price matches the best ask price, update or remove the level if the size is zero.
            b. If the incoming price is greater than the worst ask price, ignore the update.
            c. If the incoming price is between the worst and the best prices, find the exact level to update the size.
            d. If the incoming price is better than the best price, adjust the order book to accommodate new price levels.
        3. Update the best and worst prices after each iteration.

        Parameters
        ----------
        updated_asks : np.ndarray
            The updates array where each row represents a [price, size] pair for the update.
        """
        assert self._warmed_up, "Orderbook is not warmed up."
        assert (
            updated_asks.ndim == 2 and updated_asks.shape[0] > 0
        ), "Input array is empty or not 2-dimensional."

        if new_seq_id > self._seq_id:
            self._seq_id = new_seq_id

            c_best_ask = self._asks[0]
            c_worst_ask = self._asks[-1]

            for update_ask_level in updated_asks:
                price, size = update_ask_level

                # New best ask price, roll asks right, insert new ask and fix sizes.
                if price < c_best_ask[0]:
                    roll_2d_axis0_inplace(self._asks, 1)
                    self._asks[0, 0] = price
                    self._asks[0, 1] = size
                    c_best_ask = self._asks[0]

                    # Overlapping ask price, roll bids right and fix sizes.
                    if price < c_best_bid[0]:
                        stale_levels = self._bids[self._bids[:, 0] >= price].shape[0]
                        roll_2d_axis0_inplace(self._bids, stale_levels)
                        self._asks[:stale_levels].fill(0.0)
                        self._bids[-1]

                # If price is less than the worst price, update size accordingly.
                if price <= c_worst_ask[0]:
                    index = exp_search_closest_2d_axis0(self._asks, price, isBid=False)

                    # If same price is found, update size and continue.
                    if self._asks[index - 1, 0] == price:
                        if size > 0.0:
                            self._asks[index - 1, 1] = size
                        else:
                            # Roll left between index <-> end, and modify worst price.
                            self._asks[index + 1 :] = self._asks[index:-1]
                            self._asks[-1, 0] = self.c_worst_ask[0] + self.tick_size
                            self._asks[-1, 1] = 0.0
                            self.c_worst_ask = self._asks[-1]

                        continue

                    # Price level is new, roll right between index <-> end and modify index price/size.
                    else:
                        self._asks[index + 1 :] = self._asks[index:-1]
                        self._asks[-1, 0] = self.c_worst_ask[0] + self.tick_size
                        self._asks[-1, 1] = 0.0

                    # Price level not found, shift right and insert price.
                    if self._asks[price_idx, 0] != price:
                        self._asks[-1, 0] = self._asks[-2, 0] + self.tick_size
                        self._asks[-1, 1] = 0.0

    def update_bids(self, updated_bids: np.ndarray, new_seq_id: int) -> None:
        assert self._warmed_up, "Orderbook is not warmed up."
        assert (
            updated_bids.ndim == 2 and updated_bids.shape[0] > 0
        ), "Input array is empty or not 2-dimensional."

    def update_full(self, updated_asks: np.ndarray, new_seq_id: int) -> None:
        assert self._warmed_up, "Orderbook is not warmed up."
        assert (
            updated_asks.ndim == 2 and updated_asks.shape[0] > 0
        ), "Input array is empty or not 2-dimensional."

    def get_vamp(self, depth: float) -> float:
        """
        Calculates the volume-weighted average market price (VAMP) up to a specified depth for both bids and asks.

        Parameters
        ----------
        depth : float
            The depth (in terms of volume) up to which the VAMP is calculated.

        Returns
        -------
        float
            The VAMP, representing an average price weighted by order sizes up to the specified depth.
        """
        if self._warmed_up:
            # Avoid div 0 error by ensuring orderbook is warm.
            bid_size_weighted_sum = 0.0
            ask_size_weighted_sum = 0.0
            bid_cum_size = 0.0
            ask_cum_size = 0.0

            # Calculate size-weighted sum for bids
            for price, size in self._bids[::-1]:
                if bid_cum_size + size > depth:
                    remaining_size = depth - bid_cum_size
                    bid_size_weighted_sum += price * remaining_size
                    bid_cum_size += remaining_size
                    break

                bid_size_weighted_sum += price * size
                bid_cum_size += size

                if bid_cum_size >= depth:
                    break

            # Calculate size-weighted sum for asks
            for price, size in self._asks:
                if ask_cum_size + size > depth:
                    remaining_size = depth - ask_cum_size
                    ask_size_weighted_sum += price * remaining_size
                    ask_cum_size += remaining_size
                    break

                ask_size_weighted_sum += price * size
                ask_cum_size += size

                if ask_cum_size >= depth:
                    break

            total_size = bid_cum_size + ask_cum_size

            return (bid_size_weighted_sum + ask_size_weighted_sum) / total_size

        return 0.0

    def get_slippage(self, book: np.ndarray, size: float) -> float:
        """
        Calculates the slippage cost for a hypothetical order of a given size, based on either the bid or ask side of the book.

        Parameters
        ----------
        book : np.ndarray
            The order book data for the side (bids or asks) being considered.

        size : float
            The size of the hypothetical order for which slippage is being calculated.

        Returns
        -------
        float
            The slippage cost, defined as the volume-weighted average deviation from the mid price for the given order size.
        """
        if self._warmed_up:
            # Avoid div 0 error by ensuring orderbook is warm.
            mid_price = self.mid_price
            cum_size = 0.0
            slippage = 0.0

            for level in range(book.shape[0]):
                cum_size += book[level, 1]
                slippage += np.abs(mid_price - book[level, 0]) * book[level, 1]

                if cum_size >= size:
                    slippage /= cum_size
                    break

            return slippage if slippage <= mid_price else mid_price

        return 0.0

    @property
    def bids(self) -> np.ndarray:
        return self._bids

    @property
    def asks(self) -> np.ndarray:
        return self._asks

    @property
    def seq_id(self) -> int:
        return self._seq_id

    @property
    def best_bid(self) -> np.ndarray:
        return self._bids[-1]

    @property
    def best_ask(self) -> np.ndarray:
        return self._asks[0]

    @property
    def bid_ask_spread(self) -> float:
        return self._asks[0, 0] - self._bids[-1, 0]

    @property
    def is_empty(self) -> bool:
        return np.all(self._bids == 0.0) and np.all(self._asks == 0.0)

    @property
    def mid_price(self) -> float:
        """
        Calculates the mid price of the order book based on the best bid and ask prices.

        Returns
        -------
        float
            The mid price, which is the average of the best bid and best ask prices.
        """
        if self._warmed_up:
            # Avoid div 0 error by ensuring orderbook is warm.
            return (self._bids[-1, 0] + self._asks[0, 0]) / 2.0
        else:
            return 0.0

    @property
    def wmid_price(self) -> float:
        """
        Calculates the weighted mid price of the order book, considering the volume imbalance
        between the best bid and best ask.

        Returns
        -------
        float
            The weighted mid price, which accounts for the volume imbalance at the top of the book.
        """
        if self._warmed_up:
            # Avoid div 0 error by ensuring orderbook is warm.
            bid_price, bid_size = self._bids[-1]
            ask_price, ask_size = self._asks[0]
            imb = bid_size / (bid_size + ask_size)
            return (bid_price * imb) + (ask_price * (1.0 - imb))
        else:
            return 0.0

    def __eq__(self, orderbook: "HFTOrderbook") -> bool:
        assert isinstance(orderbook, HFTOrderbook)
        return (
            orderbook._seq_id == self._seq_id
            and np.array_equal(orderbook._bids, self._bids)
            and np.array_equal(orderbook._asks, self._asks)
        )

    def __len__(self) -> int:
        return min(
            self._bids[self._bids[:, 1] != 0.0].shape[0],
            self._asks[self._asks[:, 1] != 0.0].shape[0],
        )

    def __str__(self) -> str:
        return (
            f"HFTOrderbook(size={self.size}, "
            f"seq_id={self._seq_id}, "
            f"bids={self._bids}, "
            f"asks={self._asks}"
        )

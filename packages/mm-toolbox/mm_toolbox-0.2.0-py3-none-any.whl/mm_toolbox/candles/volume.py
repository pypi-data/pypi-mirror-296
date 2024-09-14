from .base import BaseCandles


class VolumeCandles(BaseCandles):
    def __init__(self, volume_per_bucket: float, num_candles: int) -> None:
        self.volume_per_bucket = volume_per_bucket
        super().__init__(num_candles)

    def process_trade(
        self, timestamp: float, side: bool, price: float, size: float
    ) -> None:
        if self.total_trades == 0.0:
            self.open_timestamp = timestamp
            self.open_price = price

        self.high_price = max(self.high_price, price)
        self.low_price = min(self.low_price, price)
        self.close_price = price

        match side:
            case 0.0:
                self.buy_volume += size

            case 1.0:
                self.sell_volume += size

        self.vwap_price = self.calculate_vwap(price, size)
        self.total_trades += 1.0
        self.close_timestamp = timestamp

        total_volume = self.buy_volume + self.sell_volume

        if total_volume >= self.volume_per_bucket:
            remaining_volume = total_volume - self.volume_per_bucket

            match side:
                case 0.0:
                    self.buy_volume -= remaining_volume

                case 1.0:
                    self.sell_volume -= remaining_volume

            self.insert_candle()
            self.process_trade(timestamp, side, price, remaining_volume)

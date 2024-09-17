import re
from imps import *


class WebullTA:
    def __init__(self):
        self.intervals_to_scan = ['m1', 'm5', 'm60', 'm240', 'd', 'w']  # Add or remove intervals as needed
    def parse_interval(self,interval_str):
        pattern = r'([a-zA-Z]+)(\d+)'
        match = re.match(pattern, interval_str)
        if match:
            unit = match.group(1)
            value = int(match.group(2))
            if unit == 'm':
                return value * 60
            elif unit == 'h':
                return value * 3600
            elif unit == 'd':
                return value * 86400
            else:
                raise ValueError(f"Unknown interval unit: {unit}")
        else:
            raise ValueError(f"Invalid interval format: {interval_str}")





    # Simulating async TA data fetching for each timeframe
    async def fetch_ta_data(self, timeframe, data):
        # Simulate an async operation to fetch data (e.g., from an API)
        await asyncio.sleep(0.1)  # Simulate network delay
        return data.get(timeframe, {})
    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.

        Parameters:
        - df (pd.DataFrame): DataFrame containing market data with columns ['High', 'Low', 'Open', 'Close', 'Volume', 'Vwap', 'Timestamp']
        - interval (str): Resampling interval based on custom mappings (e.g., 'm5', 'm30', 'd', 'w', 'm')

        Returns:
        - pd.DataFrame: DataFrame with additional columns indicating detected candlestick patterns and their bullish/bearish nature
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm1': '1T',
            'm5': '5T',
            'm30': '30T',
            'm60': '60T',  # or '1H'
            'm120': '120T',  # or '2H'
            'm240': '240T',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
            # Add more mappings as needed
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # Since we want the most recent data first, reverse the DataFrame
        patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df

    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv

    async def async_scan_candlestick_patterns(self, df, interval):
        """
        Asynchronously scans for candlestick patterns in the given DataFrame over the specified interval.
        """
        # Mapping custom interval formats to Pandas frequency strings
        interval_mapping = {
            'm1': '1T',
            'm5': '5T',
            'm30': '30T',
            'm60': '60T',  # or '1H'
            'm120': '120T',  # or '2H'
            'm240': '240T',  # or '4H'
            'd': '1D',
            'w': '1W',
            'm': '1M'
        }

        # Convert the interval to Pandas frequency string
        pandas_interval = interval_mapping.get(interval)
        if pandas_interval is None:
            raise ValueError(f"Invalid interval '{interval}'. Please use one of the following: {list(interval_mapping.keys())}")

        # Ensure 'Timestamp' is datetime and set it as the index
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)

        # Since data is most recent first, sort in ascending order for resampling
        df.sort_index(ascending=True, inplace=True)

        # Asynchronous resampling (using run_in_executor to avoid blocking the event loop)
        loop = asyncio.get_event_loop()
        ohlcv = await loop.run_in_executor(None, self.resample_ohlcv, df, pandas_interval)

        # Asynchronous pattern detection
        patterns_df = await loop.run_in_executor(None, self.detect_patterns, ohlcv)

        # No need to reverse the DataFrame; keep it in ascending order
        # patterns_df = patterns_df.iloc[::-1].reset_index()

        return patterns_df.reset_index()

    def resample_ohlcv(self, df, pandas_interval):
        ohlcv = df.resample(pandas_interval).agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
            'Vwap': 'mean'
        }).dropna()
        return ohlcv

    def detect_patterns(self, ohlcv):
        # Initialize pattern columns
        patterns = ['Hammer', 'InvertedHammer', 'HangingMan', 'ShootingStar', 'Doji',
                    'BullishEngulfing', 'BearishEngulfing', 'BullishHarami', 'BearishHarami',
                    'MorningStar', 'EveningStar', 'PiercingLine', 'DarkCloudCover',
                    'ThreeWhiteSoldiers', 'ThreeBlackCrows']
        bullish_patterns = ['Hammer', 'InvertedHammer', 'BullishEngulfing', 'BullishHarami',
                            'MorningStar', 'PiercingLine', 'ThreeWhiteSoldiers']
        bearish_patterns = ['HangingMan', 'ShootingStar', 'BearishEngulfing', 'BearishHarami',
                            'EveningStar', 'DarkCloudCover', 'ThreeBlackCrows']

        for pattern in patterns:
            ohlcv[pattern] = False

        ohlcv['Signal'] = None  # To indicate Bullish or Bearish signal

        # Iterate over the DataFrame to detect patterns
        for i in range(len(ohlcv)):
            curr_row = ohlcv.iloc[i]
            prev_row = ohlcv.iloc[i - 1] if i >= 1 else None
            prev_prev_row = ohlcv.iloc[i - 2] if i >= 2 else None

            # Trend detection
            uptrend = self.is_uptrend(ohlcv, i)
            downtrend = self.is_downtrend(ohlcv, i)

            # Single-candle patterns
            if downtrend and self.is_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'Hammer'] = True
                ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bullish'
            if downtrend and self.is_inverted_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'InvertedHammer'] = True
                ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bullish'
            if uptrend and self.is_hanging_man(curr_row):
                ohlcv.at[ohlcv.index[i], 'HangingMan'] = True
                ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bearish'
            if uptrend and self.is_shooting_star(curr_row):
                ohlcv.at[ohlcv.index[i], 'ShootingStar'] = True
                ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bearish'
            if self.is_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'Doji'] = True
                ohlcv.at[ohlcv.index[i], 'Signal'] = 'Neutral'

            # Two-candle patterns
            if prev_row is not None:
                if downtrend and self.is_bullish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'BullishEngulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bullish'
                if uptrend and self.is_bearish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'BearishEngulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bearish'
                if downtrend and self.is_bullish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'BullishHarami'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bullish'
                if uptrend and self.is_bearish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'BearishHarami'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bearish'
                if downtrend and self.is_piercing_line(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'PiercingLine'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bullish'
                if uptrend and self.is_dark_cloud_cover(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'DarkCloudCover'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bearish'

            # Three-candle patterns
            if prev_row is not None and prev_prev_row is not None:
                if downtrend and self.is_morning_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'MorningStar'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bullish'
                if uptrend and self.is_evening_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'EveningStar'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bearish'
                if downtrend and self.is_three_white_soldiers(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'ThreeWhiteSoldiers'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bullish'
                if uptrend and self.is_three_black_crows(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'ThreeBlackCrows'] = True
                    ohlcv.at[ohlcv.index[i], 'Signal'] = 'Bearish'

        return ohlcv

    # Include the existing pattern detection functions here (unchanged)
    def is_uptrend(self,data, index, lookback=3):
        if index < lookback:
            return False
        closes = data['Close'].iloc[index - lookback:index]
        return all(x < y for x, y in zip(closes, closes[1:]))

    def is_downtrend(self,data, index, lookback=3):
        if index < lookback:
            return False
        closes = data['Close'].iloc[index - lookback:index]
        return all(x > y for x, y in zip(closes, closes[1:]))

    def is_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return (lower_shadow >= 2 * body_length) and (upper_shadow <= body_length)

    def is_inverted_hammer(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Open'], row['Close'])
        lower_shadow = min(row['Open'], row['Close']) - row['Low']
        return (upper_shadow >= 2 * body_length) and (lower_shadow <= body_length)

    def is_hanging_man(self, row):
        return self.is_hammer(row)

    def is_shooting_star(self, row):
        return self.is_inverted_hammer(row)

    def is_doji(self,row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range

    def is_bullish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_bearish_engulfing(self,prev_row, curr_row):
        return (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bullish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] > prev_row['Close']) and (curr_row['Open'] < curr_row['Close']) and \
            (curr_row['Open'] > prev_row['Close']) and (curr_row['Close'] < prev_row['Open'])

    def is_bearish_harami(self,prev_row, curr_row):
        return (prev_row['Open'] < prev_row['Close']) and (curr_row['Open'] > curr_row['Close']) and \
            (curr_row['Open'] < prev_row['Close']) and (curr_row['Close'] > prev_row['Open'])

    def is_morning_star(self,prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bullish = curr_row['Close'] > curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_above_first_mid = curr_row['Close'] > first_midpoint
        return first_bearish and second_small_body and third_bullish and third_close_above_first_mid

    def is_evening_star(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_small_body = abs(prev_row['Close'] - prev_row['Open']) < abs(prev_prev_row['Close'] - prev_prev_row['Open']) * 0.3
        third_bearish = curr_row['Close'] < curr_row['Open']
        first_midpoint = (prev_prev_row['Open'] + prev_prev_row['Close']) / 2
        third_close_below_first_mid = curr_row['Close'] < first_midpoint
        return first_bullish and second_small_body and third_bearish and third_close_below_first_mid

    def is_piercing_line(self,prev_row, curr_row):
        first_bearish = prev_row['Close'] < prev_row['Open']
        second_bullish = curr_row['Close'] > curr_row['Open']
        open_below_prev_low = curr_row['Open'] < prev_row['Low']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_above_prev_mid = curr_row['Close'] > prev_midpoint
        return first_bearish and second_bullish and open_below_prev_low and close_above_prev_mid

    def is_dark_cloud_cover(self,prev_row, curr_row):
        first_bullish = prev_row['Close'] > prev_row['Open']
        second_bearish = curr_row['Close'] < curr_row['Open']
        open_above_prev_high = curr_row['Open'] > prev_row['High']
        prev_midpoint = (prev_row['Open'] + prev_row['Close']) / 2
        close_below_prev_mid = curr_row['Close'] < prev_midpoint
        return first_bullish and second_bearish and open_above_prev_high and close_below_prev_mid

    def is_three_white_soldiers(self,prev_prev_row, prev_row, curr_row):
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bullish and second_bullish and third_bullish and
                prev_row['Open'] < prev_prev_row['Close'] and curr_row['Open'] < prev_row['Close'] and
                prev_row['Close'] > prev_prev_row['Close'] and curr_row['Close'] > prev_row['Close'])

    def is_three_black_crows(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        return (first_bearish and second_bearish and third_bearish and
                prev_row['Open'] > prev_prev_row['Close'] and curr_row['Open'] > prev_row['Close'] and
                prev_row['Close'] < prev_prev_row['Close'] and curr_row['Close'] < prev_row['Close'])
    

    async def get_ta(self, ticker):
        try:
            # Dictionary to collect patterns for each interval
            ticker_patterns = {}

            # Iterate through each interval for the ticker
            for interval in self.intervals_to_scan:
                # Fetch the DataFrame asynchronously
                df = await async_get_td9(ticker=ticker, interval=interval)

                # Call the asynchronous scan_candlestick_patterns function
                patterns_df = await self.async_scan_candlestick_patterns(df, interval)

                # Since the DataFrame is in ascending order (oldest first), the last row is the most recent data
                last_row = patterns_df.iloc[-1]

                # Identify patterns that are True
                pattern_columns = ['Hammer', 'InvertedHammer', 'HangingMan', 'ShootingStar', 'Doji',
                                'BullishEngulfing', 'BearishEngulfing', 'BullishHarami', 'BearishHarami',
                                'MorningStar', 'EveningStar', 'PiercingLine', 'DarkCloudCover',
                                'ThreeWhiteSoldiers', 'ThreeBlackCrows']

                true_patterns = [pattern for pattern in pattern_columns if last_row[pattern]]

                if true_patterns:
                    signal = last_row['Signal']
                    # Store the patterns and signal for this interval
                    ticker_patterns[interval] = {
                        'patterns': true_patterns,
                        'signal': signal
                    }

            # Return the ticker patterns
            return ticker_patterns

        except Exception as e:
            print(f"Exception in processing {ticker}: {e}")
            return None
        


    async def get_patterns_for_ticker(self, ticker):
        ta_data = await self.get_ta(ticker=ticker)

        # Prepare dictionary to store parsed data with dynamic column names
        timeframes = ['m1', 'm5', 'm60', 'm240', 'd', 'w', 'm']

        # Prepare dictionary to store parsed data with dynamic column names
        data_dict = {}

        # Initialize keys in data_dict for each timeframe (patterns and signal columns)
        for tf in timeframes:
            data_dict[f'patterns_{tf}'] = []
            data_dict[f'signal_{tf}'] = []

        # Create a list of tasks to fetch data for each timeframe concurrently
        tasks = [self.fetch_ta_data(tf, ta_data) for tf in timeframes]

        # Run the tasks concurrently and gather the results
        results = await asyncio.gather(*tasks)

        # Process the results and populate the data dictionary
        for tf, result in zip(timeframes, results):
            if result:
                data_dict[f'patterns_{tf}'].append(", ".join(result.get('patterns', [])))
                data_dict[f'signal_{tf}'].append(result.get('signal', ''))
            else:
                data_dict[f'patterns_{tf}'].append(None)
                data_dict[f'signal_{tf}'].append(None)

        # Create a DataFrame from the data_dict
        df = pd.DataFrame(data_dict)

        return df
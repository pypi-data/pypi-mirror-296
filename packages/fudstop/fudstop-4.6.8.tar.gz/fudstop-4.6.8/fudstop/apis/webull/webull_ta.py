import re
import pandas as pd
import asyncio
import time
from fudstop.apis.webull.webull_trading import WebullTrading
trading = WebullTrading()
import httpx


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


    async def async_get_td9(self, ticker, interval, headers):
        try:
            timeStamp = None
            if ticker == 'I:SPX':
                ticker = 'SPXW'
            elif ticker =='I:NDX':
                ticker = 'NDX'
            elif ticker =='I:VIX':
                ticker = 'VIX'
            elif ticker == 'I:RUT':
                ticker = 'RUT'
            elif ticker == 'I:XSP':
                ticker = 'XSP'
            



            tickerid = await trading.get_webull_id(ticker)
            if timeStamp is None:
                # if not set, default to current time
                timeStamp = int(time.time())

            base_fintech_gw_url = f'https://quotes-gw.webullfintech.com/api/quote/charts/query?tickerIds={tickerid}&type={interval}&timestamp={timeStamp}&count=800&extendTrading=1'

            interval_mapping = {
                'm5': '5 min',
                'm30': '30 min',
                'm60': '1 hour',
                'm120': '2 hour',
                'm240': '4 hour',
                'd': 'day',
                'w': 'week',
                'm': 'month'
            }

            timespan = interval_mapping.get(interval, 'minute')

            async with httpx.AsyncClient(headers=headers) as client:
                data = await client.get(base_fintech_gw_url)
                r = data.json()
                if r and isinstance(r, list) and 'data' in r[0]:
                    data = r[0]['data']
                    if data is not None:
                        parsed_data = []
                        for entry in data:
                            values = entry.split(',')
                            if values[-1] == 'NULL':
                                values = values[:-1]
                            parsed_data.append([float(value) if value != 'null' else 0.0 for value in values])
                        
                        sorted_data = sorted(parsed_data, key=lambda x: x[0], reverse=True)
                        
                        columns = ['Timestamp', 'Open', 'Close', 'High', 'Low', 'N', 'Volume', 'Vwap'][:len(sorted_data[0])]
                        
                        df = pd.DataFrame(sorted_data, columns=columns)
                        df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s', utc=True)
                        df['Timestamp'] = df['Timestamp'].dt.tz_convert('US/Eastern').dt.tz_localize(None)
                        df['Ticker'] = ticker
                        df['timespan'] = interval


                        return df
                    
        except Exception as e:
            print(e)


    # Simulating async TA data fetching for each timeframe
    async def fetch_ta_data(self, timeframe, data):
        # Simulate an async operation to fetch data (e.g., from an API)

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
            'm1': '1min',
            'm5': '5min',
            'm30': '30min',
            'm60': '60min',  # or '1H'
            'm120': '120min',  # or '2H'
            'm240': '240min',  # or '4H'
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
    def check_gap(self, ohlcv, index):
        """
        Checks if there's a gap up or gap down within the last 4 candles.
        - A gap up occurs when the current open is higher than the previous close.
        - A gap down occurs when the current open is lower than the previous close.
        
        :param ohlcv: The OHLCV dataframe with historical data.
        :param index: The current index in the dataframe.
        :return: 'gap_up' or 'gap_down' if a gap is found, else None.
        """
        # Ensure there are at least 4 candles to check
        if index < 1:
            return None

        # Get the current open and previous close
        curr_open = ohlcv.iloc[index]['Open']
        prev_close = ohlcv.iloc[index - 1]['Close']

        # Check for gap up
        if curr_open > prev_close:
            return 'gap_up'

        # Check for gap down
        if curr_open < prev_close:
            return 'gap_down'

        return None  # No gap detected
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
        patterns = ['hammer', 'inverted_hammer', 'hanging_man', 'shooting_star', 'doji',
                    'bullish_engulfing', 'bearish_engulfing', 'bullish_harami', 'bearish_harami',
                    'morning_star', 'evening_star', 'piercing_line', 'dark_cloud_cover',
                    'three_white_soldiers', 'three_black_crows', 'abandoned_baby',
                    'rising_three_methods', 'falling_three_methods', 'three_inside_up', 'three_inside_down',
                    'has_gap_up', 'has_gap_down']



        for pattern in patterns:
            ohlcv[pattern] = False

        ohlcv['signal'] = None  # To indicate Bullish or Bearish signal

        # Iterate over the DataFrame to detect patterns
        for i in range(len(ohlcv)):
            curr_row = ohlcv.iloc[i]
            prev_row = ohlcv.iloc[i - 1] if i >= 1 else None
            prev_prev_row = ohlcv.iloc[i - 2] if i >= 2 else None


            # Check for gap up or gap down
            gap_signal = self.check_gap(ohlcv, i)
            # Check for gap up or gap down
            gap_signal = self.check_gap(ohlcv, i)
            if gap_signal == 'gap_up':
                ohlcv.at[ohlcv.index[i], 'has_gap_up'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'gap_up'
            elif gap_signal == 'gap_down':
                ohlcv.at[ohlcv.index[i], 'has_gap_down'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'gap_down'
            # if gap_signal == 'gap_up':
            #     ohlcv.at[ohlcv.index[i], 'has_gap_up'] = True
            #     ohlcv.at[ohlcv.index[i], 'signal'] = 'gap_up'
            # elif gap_signal == 'gap_down':
            #     ohlcv.at[ohlcv.index[i], 'has_gap_down'] = True
            #     ohlcv.at[ohlcv.index[i], 'signal'] = 'gap_down'
            # Trend detection
            uptrend = self.is_uptrend(ohlcv, i)
            downtrend = self.is_downtrend(ohlcv, i)


            # Single-candle patterns
            if downtrend and self.is_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if downtrend and self.is_inverted_hammer(curr_row):
                ohlcv.at[ohlcv.index[i], 'inverted_hammer'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_hanging_man(curr_row):
                ohlcv.at[ohlcv.index[i], 'hanging_man'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if uptrend and self.is_shooting_star(curr_row):
                ohlcv.at[ohlcv.index[i], 'shooting_star'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
            if downtrend and self.is_dragonfly_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'dragonfly_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
            if uptrend and self.is_gravestone_doji(curr_row):
                ohlcv.at[ohlcv.index[i], 'gravestone_doji'] = True
                ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

            # Two-candle patterns
            if prev_row is not None:
                if downtrend and self.is_bullish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_engulfing(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_engulfing'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_bullish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bullish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_bearish_harami(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'bearish_harami'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_piercing_line(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'piercing_line'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_dark_cloud_cover(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'dark_cloud_cover'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_tweezer_bottom(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_bottom'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_tweezer_top(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'tweezer_top'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_harami_cross(prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'harami_cross'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'neutral'

            # Three-candle patterns
            if prev_row is not None and prev_prev_row is not None:
                if downtrend and self.is_morning_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'morning_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_evening_star(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'evening_star'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_white_soldiers(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_white_soldiers'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_black_crows(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_black_crows'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_three_inside_up(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_up'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_three_inside_down(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'three_inside_down'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if self.is_abandoned_baby(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'abandoned_baby'] = True
                    if curr_row['Close'] > prev_row['Close']:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                    else:
                        ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'
                if downtrend and self.is_rising_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'rising_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bullish'
                if uptrend and self.is_falling_three_methods(prev_prev_row, prev_row, curr_row):
                    ohlcv.at[ohlcv.index[i], 'falling_three_methods'] = True
                    ohlcv.at[ohlcv.index[i], 'signal'] = 'bearish'

        return ohlcv
    def is_gravestone_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and lower_shadow == 0 and upper_shadow > 2 * body_length
        
    def is_three_inside_up(self, prev_prev_row, prev_row, curr_row):
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        second_bullish = prev_row['Close'] > prev_row['Open']
        third_bullish = curr_row['Close'] > curr_row['Open']
        return (first_bearish and second_bullish and third_bullish and
                prev_row['Open'] > prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Open'] and
                curr_row['Close'] > prev_prev_row['Open'])


    def is_tweezer_top(self, prev_row, curr_row):
        return (prev_row['High'] == curr_row['High']) and (prev_row['Close'] > prev_row['Open']) and (curr_row['Close'] < curr_row['Open'])

    def is_tweezer_bottom(self, prev_row, curr_row):
        return (prev_row['Low'] == curr_row['Low']) and (prev_row['Close'] < prev_row['Open']) and (curr_row['Close'] > curr_row['Open'])

    def is_dragonfly_doji(self, row):
        body_length = abs(row['Close'] - row['Open'])
        total_range = row['High'] - row['Low']
        upper_shadow = row['High'] - max(row['Close'], row['Open'])
        lower_shadow = min(row['Close'], row['Open']) - row['Low']
        return total_range != 0 and body_length <= 0.1 * total_range and upper_shadow == 0 and lower_shadow > 2 * body_length


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
        
    def has_gap_last_4_candles(self, ohlcv, index):
        """
        Checks if there's a gap within the last 4 candles, either up or down.
        A gap up occurs when the current open is higher than the previous close,
        and a gap down occurs when the current open is lower than the previous close.
        
        :param ohlcv: The OHLCV dataframe with historical data.
        :param index: The current index in the dataframe.
        :return: Boolean value indicating whether a gap exists in the last 4 candles.
        """
        # Ensure there are at least 4 candles to check
        if index < 3:
            return False

        # Iterate through the last 4 candles
        for i in range(index - 3, index):
            curr_open = ohlcv.iloc[i + 1]['Open']
            prev_close = ohlcv.iloc[i]['Close']
            
            # Check for a gap (either up or down)
            if curr_open > prev_close or curr_open < prev_close:
                return True  # A gap is found

        return False  # No gap found in the last 4 candles

    def is_abandoned_baby(self, prev_prev_row, prev_row, curr_row):
        # Bullish Abandoned Baby
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        doji = self.is_doji(prev_row)
        third_bullish = curr_row['Close'] > curr_row['Open']
        
        # Check for gaps
        gap_down = prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] < prev_prev_row['Low']
        gap_up = curr_row['Open'] > prev_row['Close'] and curr_row['Close'] > prev_row['High']
        
        return first_bearish and doji and third_bullish and gap_down and gap_up

    def is_harami_cross(self, prev_row, curr_row):
        # Harami Cross is a special form of Harami with the second candle being a Doji
        return self.is_bullish_harami(prev_row, curr_row) and self.is_doji(curr_row)

    def is_rising_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Rising Three Methods (Bullish Continuation)
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        small_bearish = prev_row['Close'] < prev_row['Open'] and prev_row['Close'] > prev_prev_row['Open']
        final_bullish = curr_row['Close'] > curr_row['Open'] and curr_row['Close'] > prev_prev_row['Close']
        
        return first_bullish and small_bearish and final_bullish

    def is_falling_three_methods(self, prev_prev_row, prev_row, curr_row):
        # Falling Three Methods (Bearish Continuation)
        first_bearish = prev_prev_row['Close'] < prev_prev_row['Open']
        small_bullish = prev_row['Close'] > prev_row['Open'] and prev_row['Close'] < prev_prev_row['Open']
        final_bearish = curr_row['Close'] < curr_row['Open'] and curr_row['Close'] < prev_prev_row['Close']
        
        return first_bearish and small_bullish and final_bearish

    def is_three_inside_down(self, prev_prev_row, prev_row, curr_row):
        # Bearish reversal pattern
        first_bullish = prev_prev_row['Close'] > prev_prev_row['Open']
        second_bearish = prev_row['Close'] < prev_row['Open']
        third_bearish = curr_row['Close'] < curr_row['Open']
        
        return (first_bullish and second_bearish and third_bearish and
                prev_row['Open'] < prev_prev_row['Close'] and prev_row['Close'] > prev_prev_row['Open'] and
                curr_row['Close'] < prev_prev_row['Open'])
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
    

    async def get_ta(self, ticker, headers):
        try:
            # Dictionary to collect patterns for each interval
            ticker_patterns = {}

            # Iterate through each interval for the ticker
            for interval in self.intervals_to_scan:
                # Fetch the DataFrame asynchronously
                df = await self.async_get_td9(ticker=ticker, interval=interval, headers=headers)

                # Call the asynchronous scan_candlestick_patterns function
                patterns_df = await self.async_scan_candlestick_patterns(df, interval)

                # Since the DataFrame is in ascending order (oldest first), the last row is the most recent data
                last_row = patterns_df.iloc[-1]

                # Identify patterns that are True
                pattern_columns =  ['hammer', 'inverted_hammer', 'hanging_man', 'shooting_star', 'doji',
                    'bullish_engulfing', 'bearish_engulfing', 'bullish_harami', 'bearish_harami',
                    'morning_star', 'evening_star', 'piercing_line', 'dark_cloud_cover',
                    'three_white_soldiers', 'three_black_crows', 'abandoned_baby',
                    'rising_three_methods', 'falling_three_methods', 'three_inside_up', 'three_inside_down',
                    'has_gap_up', 'has_gap_down']

                true_patterns = [pattern for pattern in pattern_columns if last_row[pattern]]

                if true_patterns:
                    signal = last_row['signal']
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
        
    async def get_patterns_for_ticker(self, ticker, headers):
        try:
            ta_data = await self.get_ta(ticker=ticker, headers=headers)

            # Timeframes and their corresponding descriptive column names
            timeframes = {
                'm5': '5min',
                'm60': '1hr',
                'm240': '4hr',
                'd': 'day',
                'w': 'week',
                'm': 'month'  # Assuming 'm' stands for 'month'
            }

            # Prepare dictionary to store parsed data with dynamic column names
            data_dict = {}

            # Initialize keys in data_dict for each timeframe (patterns and signal columns)
            for tf_key, tf_label in timeframes.items():
                data_dict[f'patterns_{tf_label}'] = []
                data_dict[f'signal_{tf_label}'] = []

            # Create a list of tasks to fetch data for each timeframe concurrently
            tasks = [self.fetch_ta_data(tf_key, ta_data) for tf_key in timeframes]

            # Run the tasks concurrently and gather the results
            results = await asyncio.gather(*tasks)

            # Process the results and populate the data dictionary
            for (tf_key, tf_label), result in zip(timeframes.items(), results):
                if result:
                    data_dict[f'patterns_{tf_label}'].append(", ".join(result.get('patterns', [])))
                    data_dict[f'signal_{tf_label}'].append(result.get('signal', ''))
                else:
                    data_dict[f'patterns_{tf_label}'].append(None)
                    data_dict[f'signal_{tf_label}'].append(None)

            # Create a DataFrame from the data_dict
            df = pd.DataFrame(data_dict)

            return df
        except Exception as e:
            print(e)

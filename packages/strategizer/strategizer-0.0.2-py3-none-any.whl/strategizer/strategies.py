import datetime as dt
import pytz
import pandas as pd
import numpy as np
import math
import mtk_bulk as mtk
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.trend import MACD
from ta.volatility import BollingerBands
from sklearn.metrics import make_scorer, confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, GridSearchCV
import logging
from typing import Callable, Dict, List

# Set up logging to track the program's execution
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Class to manage strategy execution and signal generation
class StrategyExecutor:
    def __init__(self, data: pd.DataFrame):
        data = data

    def execute_strategy(self, strategy: Callable, **kwargs) -> pd.DataFrame:
        logger.info(f"Executing strategy: {strategy.__name__}")
        return strategy(data, **kwargs)

    def apply_strategies(self, strategies: Dict[str, Callable], **kwargs) -> pd.DataFrame:
        results = {}
        for name, strat in strategies.items():
            logger.info(f"Applying strategy: {name}")
            results[name] = execute_strategy(strat, **kwargs)
        return results

# TRADING STRATEGIES

ema_pairs = (5, 20), (9, 21), (10, 50), (20, 50)
fib_retracements = 0.236, 0.382, 0.5, 0.618, 0.786
fib_directions = 'long', 'short'
dip_sizes = 0.05, 0.1, 0.15, 0.2, 0.25
days_of_week = 0, 1, 2, 3
model_fits = {
    'RandomForest': randomForest_strategy
}
strategies = {
    'Test': (
        lambda x: test_strategy(x),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, False),
    'SMA Crossover': (
        lambda x: sma_crossover_strategy(x, 50, 200),
        timeframe, direction, None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Random': (
        random_strategy,
        timeframe, direction, None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Random wRules': (
        random_strategy,
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'RSI': (
        rsi_strategy,
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'RSI Divergence': (
        rsi_divergence_strategy,
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'MACD': (
        macd_strategy,
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'BollingerBands': (
        bollinger_bands_strategy,
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Stochastic': (
        stochastic_strategy,
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Volume': (
        lambda x: volume_strategy(x, 20,True),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Momentum': (
        lambda x: momentum_strategy(x, 20),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'MeanReversion': (
        lambda x: mean_reversion_strategy(x, 20),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'EMA Crossover': (
        lambda x, span_a, span_b: ema_crossover_strategy(x, span_a, span_b),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Fibonacci Retracement': (
        lambda x, fib_retracement, fib_direction: fibonacci_retracement_strategy(x, fib_retracement, fib_direction),
        timeframe, direction, None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Model': (
        lambda x, model_name, first_training_data, features2use, model_prediction_size, evaluate_model: model_rolling_window(
            x, model_name, first_training_data, features2use, model_fits, future_periods, model_prediction_size, evaluate_model),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Spread Scalping': (
        lambda x: spread_scalping_strategy(x, 'long'),
        timeframe, direction, None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, False),
    'buyAndHold': (
        buy_and_hold_strategy,
        LT_timeframes, 'long', None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, True),
    'Multi-Timeframe RSI Divergence': (
        lambda x: multi_timeframe_rsi_divergence_strategy(x, short_rsi_window=14, long_rsi_window=50),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Lunar Cycle Trading': (
        lambda x: lunar_cycle_trading_strategy(x),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'BTFD': (
        lambda x, dip_size: btfd_strategy(x, dip_size),
        '1d', 'long', stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'BTFD Open': (
        lambda x, dip_size: btfd_open_strategy(x, dip_size),
        '1d', 'long', stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'BTFD First': (
        lambda x, dip_size: btfd_first_strategy(x, dip_size),
        '1d', 'long', stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'BTFD Open First': (
        lambda x, dip_size: btfd_open_first_strategy(x, dip_size),
        '1d', 'long', stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Volatility Compression Breakout': (
        lambda x: volatility_compression_breakout_strategy(x, window=20, compression_threshold=0.01),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Fractal Dimension': (
        lambda x: fractal_dimension_strategy(x, lookback_period=5),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Sentiment-Based Trading': (
        lambda x: sentiment_keyword_strategy(x, sentiment_data=sentiment_data, threshold=0.05),
        timeframe, direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Weekly Continuation': (
        lambda x, day_of_week: weekly_continuation_strategy(x, day_of_week),
        '1d', direction, stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Buy Close Sell Open': (
        buy_close_sell_open_strategy,
        timeframe, 'long', None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Overnight Sell Off Buy Open': (
        lambda x: overnight_sell_off_buy_open_strategy(x, change_size=-0.05),
        '1d', 'long', stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Day2 Overnight Sell Off Gap Up Open Fade': (
        lambda x: day2_overnight_sell_off_gap_up_open_fade_strategy(x, change_size=-0.05),
        '1d', 'short', None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Intraday Sell Off Buy Close': (
        lambda x: intraday_sell_off_buy_close_strategy(x, change_size=-0.025),
        '1d', 'long', stop_loss_type, stop_loss_amt, SL_spike_avoidance, take_profit_prop, trailing_stop, general_active_strat),
    'Day1 Gap Fade Open': (
        lambda x: day1_gap_reversal_open_strategy(x, gap_size=0.03),
        '1d', 'short', None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Day1 Gap Bounce Open': (
        lambda x: day1_gap_reversal_open_strategy(x, gap_size=-0.03),
        '1d', 'long', None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Day1 Earnings Continuation Short': (
        lambda x: day1_earnings_continuation_short_strategy(x),
        '1d', 'short', None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
    'Day1 Earnings Continuation Long': (
        lambda x: day1_earnings_continuation_long_strategy(x),
        '1d', 'long', None, stop_loss_amt, SL_spike_avoidance, None, trailing_stop, general_active_strat),
}

# Strategy: Weekly Continuation
def weekly_continuation_strategy(info, day_of_week):
    """ If the chosen day of week is up, buy at the close of the day when weekly return goes flat/negative and unwind
    the trade at close of last day of the week."""

    # Ensure the index is a DatetimeIndex and Calculate the weekday, week number, and year for each date
    if not isinstance(info.index, pd.DatetimeIndex):
        info.index = pd.to_datetime(info.index)
    info['Weekday'] = info.index.weekday
    info['Week_Number'] = info.index.isocalendar().week
    info['Year'] = info.index.isocalendar().year
    info['Date'] = info.index

    # Calculate close of each week
    last_week_close = info.groupby(['Year', 'Week_Number'])['Close'].last().shift(1)
    info = info.join(last_week_close.rename('Last_Week_Close'), on=['Year', 'Week_Number'])

    # Calculate if the chosen day of the week closed up or down
    filtered_info = info[info['Weekday'] == day_of_week]
    chosen_day = filtered_info.groupby(['Year', 'Week_Number']).first()  # If day_of_week is too high or incorrect, no chosen day will be available and no signal will be issued.
    chosen_day['Chosen_Day_Prior_close'] = chosen_day['Date'].map(info['Close'].shift(1))
    chosen_day['chosen_day_closed_up'] = chosen_day['Close'] > chosen_day['Chosen_Day_Prior_close']
    chosen_day['chosen_day_closed_up'] = np.where(chosen_day['Close'] == chosen_day['Chosen_Day_Prior_close'], np.nan,
                                                  chosen_day['chosen_day_closed_up'])
    info['Chosen_Day_Closed_Up'] = info[['Year', 'Week_Number']].apply(tuple, axis=1).map(
        chosen_day['chosen_day_closed_up'])

    # Iterate through each unique week
    info['buy_signal'] = 0
    info['sell_signal'] = 0
    info['buy_price'] = np.nan
    info['sell_price'] = np.nan
    for (year, week), week_data in info.groupby(['Year', 'Week_Number']):
        if week_data.empty or day_of_week not in week_data['Weekday'].values:
            continue

        week_data = week_data[week_data['Weekday'] >= day_of_week]
        chosen_day_closed_up = week_data['Chosen_Day_Closed_Up'].iloc[0]

        # Calculate buy/sell signals
        if chosen_day_closed_up:
            buy_price = np.where((week_data['Weekday'] != day_of_week) & (week_data['Weekday'] != week_data['Weekday'].iloc[-1]),
                                 np.where(week_data['Last_Week_Close'] > week_data['Open'], week_data['Open'], week_data['Last_Week_Close']),
                                 week_data['Close'])
            trigger_buy_price = np.where(week_data['Weekday'] != day_of_week, week_data['Low'], week_data['Close'])
            buy_condition = (trigger_buy_price <= week_data['Last_Week_Close'].iloc[0]) & (week_data['Weekday'] != week_data['Weekday'].iloc[-1])
            buy_index = week_data[buy_condition].index
            if not buy_index.empty:
                info.at[buy_index[0], 'buy_signal'] = 1
                idx_buy_position = week_data.index.get_loc(buy_index[0])
                info.at[buy_index[0], 'buy_price'] = buy_price[idx_buy_position]
        elif not chosen_day_closed_up:
            sell_price = np.where((week_data['Weekday'] != day_of_week) & (week_data['Weekday'] != week_data['Weekday'].iloc[-1]),
                                  np.where(week_data['Last_Week_Close'] < week_data['Open'], week_data['Open'], week_data['Last_Week_Close']),
                                  week_data['Close'])
            trigger_sell_price = np.where(week_data['Weekday'] != day_of_week, week_data['High'], week_data['Close'])
            sell_condition = (trigger_sell_price >= week_data['Last_Week_Close'].iloc[0]) & (week_data['Weekday'] != week_data['Weekday'].iloc[-1])
            sell_index = week_data[sell_condition].index
            if not sell_index.empty:
                info.at[sell_index[0], 'sell_signal'] = 1
                idx_sell_position = week_data.index.get_loc(sell_index[0])
                info.at[sell_index[0], 'sell_price'] = sell_price[idx_sell_position]

        # Generate opposite signals on the last available day of the week if applicable
        last_day = week_data.iloc[[-1]]
        if info.loc[week_data.index, 'buy_signal'].sum() > 0:
            info.loc[last_day.index, 'sell_signal'] = 1
            info.loc[last_day.index, 'sell_price'] = last_day['Close']
        elif info.loc[week_data.index, 'sell_signal'].sum() > 0:
            info.loc[last_day.index, 'buy_signal'] = 1
            info.loc[last_day.index, 'buy_price'] = last_day['Close']

    info['buy_time'] = np.where(info['buy_price'] == info['Last_Week_Close'], 'anytime', np.where(info['buy_price'] == info['Open'], 'open', 'close'))
    info['sell_time'] = np.where(info['sell_price'] == info['Last_Week_Close'], 'anytime', np.where(info['sell_price'] == info['Open'], 'open', 'close'))
    return info


# Strategy: Random
def random_strategy(info, seed=42):
    # Set the random seed.
    np.random.seed(seed)

    # Generate random integers: 0 for no signal, 1 for buy, 2 for sell.
    signals = np.random.randint(0, 3, size=len(info))

    # Assign signals to df.
    info['buy_signal'] = np.where(signals == 1, 1, 0)
    info['sell_signal'] = np.where(signals == 2, 1, 0)
    info['buy_time'] = 'anytime'
    info['sell_time'] = 'anytime'
    return info


# Strategy: Buy Close Sell Open
def buy_close_sell_open_strategy(info):
    """Implement a strategy that buys at the close of every day and sells at the open of the next trading day."""

    # Generate signals.
    info['buy_signal'] = 1
    info['sell_signal'] = 1

    # Calculate execution prices.
    info['buy_price'] = info['Close']
    info['sell_price'] = info['Open']
    info['buy_time'] = 'close'
    info['sell_time'] = 'open if trade'

    return info


# Strategy: SMA Crossover
def sma_crossover_strategy(info, short_window=50, long_window=200):
    info['SMA_Short'] = info['Close'].rolling(window=short_window).mean()
    info['SMA_Long'] = info['Close'].rolling(window=long_window).mean()
    info['cross_up'] = np.where(info['SMA_Short'] > info['SMA_Long'], 1, 0)
    info['buy_signal'] = np.where(info['cross_up'].diff() == 1, 1, 0)
    info['cross_down'] = np.where(info['SMA_Short'] < info['SMA_Long'], 1, 0)
    info['sell_signal'] = np.where(info['cross_down'].diff() == 1, 1, 0)
    return info


# Strategy: Spread Scalping
def spread_scalping_strategy(info, scalping_side):
    info['buy_signal'] = 1
    info['sell_signal'] = 1
    if scalping_side == 'short':
        info['buy_time'] = 'anytime passive if trade'
        info['sell_time'] = 'anytime passive'
    else:  # Biased towards longs if error in param.
        info['buy_time'] = 'anytime passive'
        info['sell_time'] = 'anytime passive if trade'
    return info


# Strategy: Test
def test_strategy(info):
    info['buy_signal'] = 1
    info['sell_signal'] = np.random.randint(0, 1, size=len(info))
    info['buy_price'] = info['Close']
    info['sell_price'] = info['Close']
    info['buy_time'] = 'close'
    info['sell_time'] = 'close'
    return info


# Strategy: EMA Crossover
def ema_crossover_strategy(info, span_a, span_b):
    info['EMA_A'] = info['Close'].ewm(span=span_a, adjust=False).mean()
    info['EMA_B'] = info['Close'].ewm(span=span_b, adjust=False).mean()
    info['ema_cross_up'] = np.where(info['EMA_A'] > info['EMA_B'], 1, 0)
    info['buy_signal'] = np.where(info['ema_cross_up'].diff() == 1, 1, 0)
    info['ema_cross_down'] = np.where(info['EMA_A'] < info['EMA_B'], 1, 0)
    info['sell_signal'] = np.where(info['ema_cross_down'].diff() == 1, 1, 0)
    return info


# Strategy: Multi-Timeframe RSI Divergence
def multi_timeframe_rsi_divergence_strategy(info, short_rsi_window=14, long_rsi_window=50):
    """
    Implements a multi-timeframe RSI divergence strategy. Looks for RSI divergences between short-term and long-term periods.
    """
    # Calculate short-term RSI (e.g., 14-period)
    delta = info['Close'].diff(1)
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    avg_gain_short = pd.Series(gain).rolling(window=short_rsi_window).mean()
    avg_loss_short = pd.Series(loss).rolling(window=short_rsi_window).mean()
    rs_short = avg_gain_short / avg_loss_short
    info['RSI_Short'] = 100 - (100 / (1 + rs_short))

    # Calculate long-term RSI (e.g., 50-period)
    avg_gain_long = pd.Series(gain).rolling(window=long_rsi_window).mean()
    avg_loss_long = pd.Series(loss).rolling(window=long_rsi_window).mean()
    rs_long = avg_gain_long / avg_loss_long
    info['RSI_Long'] = 100 - (100 / (1 + rs_long))

    # Identify divergence: short-term RSI is rising while long-term RSI is falling
    info['buy_signal'] = np.where((info['RSI_Short'] > 30) & (info['RSI_Short'].diff() > 0) & (info['RSI_Long'] < 50), 1, 0)
    info['sell_signal'] = np.where((info['RSI_Short'] < 70) & (info['RSI_Short'].diff() < 0) & (info['RSI_Long'] > 50), 1, 0)

    # Execution prices
    info['buy_price'] = info['Close']
    info['sell_price'] = info['Close']
    info['buy_time'] = 'close'
    info['sell_time'] =


# Strategy: BTFD
def btfd_strategy(info, dip_size):
    # If no position, it keeps buying everytime it drops dip_size below ATH even if it's already below ATH.
    info['ATH'] = info['High'].cummax()
    # Create a flag to track if price comes from above the dip threshold or whether we were below it already before to avoid keep on issuing buy signals when below.
    info['above_threshold'] = np.where(info['Close'] > info['ATH'] * (1 - dip_size), 1, 0)
    info['above_threshold_1'] = info['above_threshold'].shift(1).fillna(1).astype(int)

    info['buy_signal'] = np.where((info['Close'] <= info['ATH'] * (1 - dip_size)) & (info['above_threshold_1'] == 1), 1, 0)
    info['sell_signal'] = np.where(info['Open'] >= info['ATH'], 1, 0)
    info['buy_price'] = info['Close']
    info['sell_price'] = info['ATH'].shift(1).combine(info['Open'], max).fillna(info['Open'])
    info['buy_time'] = 'close'
    info['sell_time'] = 'open'
    return info


# Strategy: BTFD Open
def btfd_open_strategy(info, dip_size):
    # If no position, it keeps buying everytime it drops dip_size below ATH even if it's already below ATH.
    info['ATH'] = info['High'].cummax()
    # Create a flag to track if price comes from above the dip threshold or we were below it already before to avoid keep on issuing buy signals when below.
    info['above_threshold'] = np.where(info['Open'] > info['ATH'] * (1 - dip_size), 1, 0)
    info['above_threshold_1'] = info['above_threshold'].shift(1).fillna(1).astype(int)
    info.drop(columns=['above_threshold'], inplace=True)

    info['buy_signal'] = np.where((info['Open'] <= info['ATH'] * (1 - dip_size)) & (info['above_threshold_1'] == 1), 1, 0)
    info['sell_signal'] = np.where(info['Open'] >= info['ATH'], 1, 0)
    info['buy_price'] = info['Open']
    info['sell_price'] = info['ATH'].shift(1).combine(info['Open'], max).fillna(info['Open'])
    info['buy_time'] = 'open'
    info['sell_time'] = 'open'
    return info


# Strategy: BTFD First
def btfd_first_strategy(info, dip_size):
    # If no position, it buys the first time the price drops dip_size below ATH.
    info['ATH'] = info['High'].cummax()
    info['buy_signal'] = 0
    info['sell_signal'] = 0
    in_dip = False
    for i in range(1, len(info)):
        if not in_dip and info['Close'].iloc[i] <= info['ATH'].iloc[i] * (1 - dip_size):
            info.at[info.index[i], 'buy_signal'] = 1
            in_dip = True
        elif in_dip and info['High'].iloc[i] >= info['ATH'].iloc[i]:
            info.at[info.index[i], 'sell_signal'] = 1
            in_dip = False
    info['buy_price'] = info['Close']
    info['sell_price'] = info['ATH'].shift(1).combine(info['Open'], max).fillna(info['Open'])
    info['buy_time'] = 'close'
    info['sell_time'] = 'open'
    return info


# Strategy: BTFD Open First
def btfd_open_first_strategy(info, dip_size):
    # If no position, it will buy only the first time it drops dip_size below ATH.
    info['ATH'] = info['High'].cummax()
    info['buy_signal'] = 0
    info['sell_signal'] = 0
    in_dip = False
    for i in range(1, len(info)):
        if not in_dip and info['Open'].iloc[i] <= info['ATH'].iloc[i] * (1 - dip_size):
            info.at[info.index[i], 'buy_signal'] = 1
            in_dip = True
        elif in_dip and info['High'].iloc[i] >= info['ATH'].iloc[i]:
            info.at[info.index[i], 'sell_signal'] = 1
            in_dip = False
    info['buy_price'] = info['Open']
    info['sell_price'] = info['ATH'].shift(1).combine(info['Open'], max).fillna(info['Open'])
    info['buy_time'] = 'open'
    info['sell_time'] = 'open'
    return info


# Strategy: Day2 Overnight Sell Off Gap Up Open Fade
def day2_overnight_sell_off_gap_up_open_fade_strategy(info, change_size):
    info['buy_signal'] = np.where(
        (info['Open'].shift(1) <= info['Close'].shift(2) * (1 + change_size)) & (info['Open'] > info['Close'].shift(1)),
        1, 0)
    info['sell_signal'] = info['buy_signal']
    info['buy_price'] = info['Close']
    info['sell_price'] = info['Open']
    info['buy_time'] = 'close'
    info['sell_time'] = 'open'
    return info


# Strategy: Overnight Sell Off Buy Open
def overnight_sell_off_buy_open_strategy(info, change_size):
    info['buy_signal'] = np.where(info['Open'] <= info['Close'].shift(1) * (1 + change_size), 1, 0)
    info['sell_signal'] = 0
    info['buy_price'] = info['Open']
    info['buy_time'] = 'open'
    return info


# Strategy: Lunar Cycle Trading
import ephem

def lunar_cycle_trading_strategy(info):
    """
    Implements a strategy based on lunar cycles. Buy around new moons, sell around full moons.
    """
    # Use ephem to calculate moon phases
    moon = ephem.Moon()
    info['moon_phase'] = 0
    for idx, date in enumerate(info['Date']):
        obs_date = ephem.Date(date)
        moon.compute(obs_date)
        info.at[info.index[idx], 'moon_phase'] = moon.phase  # Phase between 0 (new moon) and 100 (full moon)

    # Buy near new moon (phase ~ 0)
    info['buy_signal'] = np.where(info['moon_phase'] < 10, 1, 0)
    # Sell near full moon (phase ~ 100)
    info['sell_signal'] = np.where(info['moon_phase'] > 90, 1, 0)

    # Execution prices
    info['buy_price'] = info['Close']
    info['sell_price'] = info['Close']
    info['buy_time'] = 'close'
    info['sell_time'] = 'close'

    return info


# Strategy: Intraday Sell Off Buy Close
def intraday_sell_off_buy_close_strategy(info, change_size):
    info['buy_signal'] = np.where(info['Close'] <= info['Close'].shift(1) * (1 + change_size), 1, 0)
    info['sell_signal'] = 0
    info['buy_price'] = info['Close']
    info['buy_time'] = 'close'
    return info


# Strategy: Day1 Gap Fade Open, Day1 Gap Bounce Open
def day1_gap_reversal_open_strategy(info, gap_size):
    if gap_size >= 0:
        info['sell_signal'] = np.where(info['Open'] >= info['Close'].shift(1) * (1 + gap_size), 1, 0)
        info['buy_signal'] = info['sell_signal']
        info['sell_price'] = info['Open']
        info['buy_price'] = info['Close']
        info['sell_time'] = 'open'
        info['buy_time'] = 'close'
    elif gap_size <= 0:
        info['buy_signal'] = np.where(info['Open'] <= info['Close'].shift(1) * (1 + gap_size), 1, 0)
        info['sell_signal'] = info['buy_signal']
        info['buy_price'] = info['Open']
        info['sell_price'] = info['Close']
        info['buy_time'] = 'open'
        info['sell_time'] = 'close'
    return info


# Strategy: Volatility Compression Breakout
def volatility_compression_breakout_strategy(info, window=20, compression_threshold=0.01):
    """
    Implements a volatility compression breakout strategy. Buys when price breaks above a tight range after low volatility.
    """
    # Calculate volatility as the range between high and low prices over a window
    info['range'] = (info['High'] - info['Low']).rolling(window=window).mean()

    # Identify periods of low volatility (compressed price range)
    info['compression'] = np.where(info['range'] < compression_threshold, 1, 0)

    # Look for breakouts above the high during compressed periods
    info['breakout_high'] = info['High'].rolling(window=window).max()
    info['buy_signal'] = np.where((info['compression'] == 1) & (info['Close'] > info['breakout_high']), 1, 0)

    # Look for breakdowns below the low during compressed periods
    info['breakout_low'] = info['Low'].rolling(window=window).min()
    info['sell_signal'] = np.where((info['compression'] == 1) & (info['Close'] < info['breakout_low']), 1, 0)

    # Execution
    info['buy_price'] = info['Close']
    info['sell_price'] = info['Close']
    info['buy_time'] = 'close'
    info['sell_time'] = 'close'

    return info


# Strategy: Day1 Earnings Continuation Short
def day1_earnings_continuation_short_strategy(info):
    if 'earnings_surprise' not in info.columns:
        info['sell_signal'] = 0
        info['buy_signal'] = 0
        return info
    info['sell_signal'] = np.where((info['Open'] < info['Close'].shift(1)) & (~info['earnings_surprise'].isna()), 1, 0)
    info['buy_signal'] = info['sell_signal']
    info['sell_price'] = info['Open']
    info['buy_price'] = info['Close']
    info['sell_time'] = 'open'
    info['buy_time'] = 'close'
    return info


# Strategy: Day1 Earnings Continuation Long
def day1_earnings_continuation_long_strategy(info):
    if 'earnings_surprise' not in info.columns:
        info['sell_signal'] = 0
        info['buy_signal'] = 0
        return info
    info['buy_signal'] = np.where((info['Open'] > info['Close'].shift(1)) & (~info['earnings_surprise'].isna()), 1, 0)
    info['sell_signal'] = info['buy_signal']
    info['buy_price'] = info['Open']
    info['sell_price'] = info['Close']
    info['buy_time'] = 'open'
    info['sell_time'] = 'close'
    return info


# Strategy: buyAndHold
def buy_and_hold_strategy(info):
    info['buy_signal'] = np.ones(len(info))
    info['sell_signal'] = np.zeros(len(info))
    info['buy_time'] = 'anytime'
    info['sell_time'] = 'anytime'
    return info


# Strategy: RSI
def rsi_strategy(info):
    # from ta.momentum import RSIIndicator
    info['RSI'] = RSIIndicator(info['Close'], window=14).rsi()
    info['buy_signal'] = np.where(info['RSI'] < 30, 1, 0)
    info['sell_signal'] = np.where(info['RSI'] > 70, 1, 0)
    return info


# Strategy: RSI Divergence
def rsi_divergence_strategy(info):
    # from ta.momentum import RSIIndicator
    info['RSI'] = RSIIndicator(info['Close'], window=14).rsi()
    info.dropna(subset=['RSI'], inplace=True)

    # Find swing highs and lows for price
    info['price_swing_high'], info['price_swing_low'] = mtk.find_swing_highs_lows(info['High'], info['Low'])

    # Initialize signals
    info['bullish_divergence'] = 0
    info['bearish_divergence'] = 0

    # Loop through the data to find divergences
    for i in range(1, len(info)):
        # Bullish Divergence: Price is making lower lows, RSI at swing lows should be higher
        if info['price_swing_low'].iloc[i]:
            # Look back for the last price swing low
            last_price_low = info['price_swing_low'][:i][info['price_swing_low']].last_valid_index()
            if last_price_low is not None:
                # Check if current price is lower and RSI is higher compared to the last swing low
                if info['Low'].iloc[i] < info['Low'].loc[last_price_low] and info['RSI'].iloc[i] > info['RSI'].loc[last_price_low]:
                    info.at[info.index[i], 'bullish_divergence'] = 1

        # Bearish Divergence: Price is making higher highs, RSI at swing highs should be lower
        if info['price_swing_high'].iloc[i]:
            # Look back for the last price swing high
            last_price_high = info['price_swing_high'][:i][info['price_swing_high']].last_valid_index()
            if last_price_high is not None:
                # Check if current price is higher and RSI is lower compared to the last swing high
                if info['High'].iloc[i] > info['High'].loc[last_price_high] and info['RSI'].iloc[i] < info['RSI'].loc[last_price_high]:
                    info.at[info.index[i], 'bearish_divergence'] = 1

    # Generate buy and sell signals based on divergence
    info['buy_signal'] = np.where(info['bullish_divergence'].shift(2) == 1, 1, 0)  # For a swing, a three candle formation is required and divergence happens on the swing_high or swing_low.
    info['sell_signal'] = np.where(info['bearish_divergence'].shift(2) == 1, 1, 0)
    info['buy_price'] = info['Open']
    info['sell_price'] = info['Open']
    info['buy_time'] = 'open'
    info['sell_time'] = 'open'
    return info


# Strategy: Fractal Dimension Trading
def fractal_dimension_strategy(info, lookback_period=5):
    """
    Implements a strategy based on fractal dimension to identify potential reversals in the market.
    """
    # Calculate local highs and lows (fractal points)
    info['fractal_high'] = (info['High'] > info['High'].shift(1)) & (info['High'] > info['High'].shift(-1))
    info['fractal_low'] = (info['Low'] < info['Low'].shift(1)) & (info['Low'] < info['Low'].shift(-1))

    # Fractal dimension approximation using box-counting
    info['box_count'] = np.log10((info['High'] - info['Low']).rolling(window=lookback_period).mean())
    info['fractal_dimension'] = np.log10(lookback_period) / info['box_count']

    # Buy if fractal dimension signals an oversold state (below a threshold)
    info['buy_signal'] = np.where((info['fractal_dimension'] < 1.5) & info['fractal_low'], 1, 0)
    # Sell if fractal dimension signals an overbought state (above a threshold)
    info['sell_signal'] = np.where((info['fractal_dimension'] > 1.5) & info['fractal_high'], 1, 0)

    # Execution prices
    info['buy_price'] = info['Low']
    info['sell_price'] = info['High']
    info['buy_time'] = 'low'
    info['sell_time'] = 'high'

    return info


# Strategy: MACD
def macd_strategy(info):
    # from ta.trend import MACD
    macd_indicator = MACD(info['Close'])
    info['MACD'] = macd_indicator.macd()
    info['MACD_signal'] = macd_indicator.macd_signal()
    info['macd_cross_up'] = np.where(info['MACD'] > info['MACD_signal'], 1, 0)
    info['buy_signal'] = np.where(info['macd_cross_up'].diff() == 1, 1, 0)
    info['macd_cross_down'] = np.where(info['MACD'] < info['MACD_signal'], 1, 0)
    info['sell_signal'] = np.where(info['macd_cross_down'].diff() == 1, 1, 0)
    return info


# Strategy: BollingerBands
def bollinger_bands_strategy(info):
    # from ta.volatility import BollingerBands
    bb = BollingerBands(info['Close'])
    info['BB_upper'] = bb.bollinger_hband()
    info['BB_middle'] = bb.bollinger_mavg()
    info['BB_lower'] = bb.bollinger_lband()
    info['buy_signal'] = np.where(info['Close'] <= info['BB_lower'], 1, 0)
    info['sell_signal'] = np.where(info['Close'] >= info['BB_upper'], 1, 0)
    return info


# Strategy: Fibonacci Retracement
def fibonacci_retracement_strategy(info, fib_level, fib_side):
    fib_name = f'Fib_{fib_level * 100:.1f}'
    info[fib_name] = level = np.nan
    info['swing_high'] = np.nan
    info['swing_low'] = np.nan
    info['swing_high_exit'] = np.nan
    info['swing_low_exit'] = np.nan
    info['buy_signal'] = 0
    info['sell_signal'] = 0
    info['buy_price'] = np.nan
    info['sell_price'] = np.nan
    info['buy_time'] = 'anytime'
    info['sell_time'] = 'anytime'
    exit_action = 'buy' if fib_side == 'short' else 'sell'
    position_open = swing_high_update = False
    last_swing_type = swing_high = swing_low = swing_high_exit = swing_low_exit = exit_price_high = exit_price_low = exit_price = None

    for i in range(1, len(info) - 1):
        # Identify Swing Highs and Swing Lows with the correct order for longs and shorts. Not using find_swing_highs_lows() to track other aspects as we go
        if info['High'].iloc[i] > info['High'].iloc[i - 1] and info['High'].iloc[i] > info['High'].iloc[i + 1] and \
                last_swing_type != 'high' or last_swing_type == 'high' and info['High'].iloc[i] > swing_high:
            info.at[info.index[i], 'swing_high'] = swing_high = info['High'].iloc[i]
            last_swing_type = 'high'
            swing_high_update = True
        if info['Low'].iloc[i] < info['Low'].iloc[i - 1] and info['Low'].iloc[i] < info['Low'].iloc[i + 1] and \
                last_swing_type != 'low' and not swing_high_update or last_swing_type == 'low' and info['Low'].iloc[i] < swing_low:
            info.at[info.index[i], 'swing_low'] = swing_low = info['Low'].iloc[i]
            last_swing_type = 'low'

        if swing_high and swing_low:
            condition = info['High'].iloc[i] != swing_high and info['Low'].iloc[i] != swing_low
            diff = swing_high - swing_low  # Calculate the Fibonacci retracement level

            if fib_side == 'long' and last_swing_type == 'high':
                level = swing_high - fib_level * diff
                if condition and not position_open and info['Low'].iloc[i - 1] > level >= info['Low'].iloc[i]:
                    info.at[info.index[i], 'buy_signal'] = 1
                    info.at[info.index[i], 'buy_price'] = level if info['Open'].iloc[i] > level else info['Open'].iloc[i]
                    position_open = True
                    swing_high_exit = swing_high
                    swing_low_exit = swing_low

            elif fib_side == 'short' and last_swing_type == 'low':
                level = swing_low + fib_level * diff
                if condition and not position_open and info['High'].iloc[i - 1] < level <= info['High'].iloc[i]:
                    info.at[info.index[i], 'sell_signal'] = 1
                    info.at[info.index[i], 'sell_price'] = level if info['Open'].iloc[i] < level else info['Open'].iloc[i]
                    position_open = True
                    swing_high_exit = swing_high
                    swing_low_exit = swing_low

        if position_open:
            if info['High'].iloc[i] >= swing_high_exit:
                exit_price = exit_price_high = swing_high_exit if info['Open'].iloc[i] < swing_high_exit else info['Open'].iloc[i]
            if info['Low'].iloc[i] <= swing_low_exit:
                exit_price = exit_price_low = swing_low_exit if info['Open'].iloc[i] > swing_low_exit else info['Open'].iloc[i]
            if exit_price_high and exit_price_low:
                exit_price = exit_price_high if exit_price_high == info['Open'].iloc[i] else exit_price_low if exit_price_low == info['Open'].iloc[i] else None
                # If one exit_price is the Open, it means that price took place first.
                if not exit_price:
                    exit_price = exit_price_low if fib_side == 'long' else exit_price_high  # Prioritize SL if ambiguous.
            if exit_price:
                info.at[info.index[i], f'{exit_action}_signal'] = 1
                info.at[info.index[i], f'{exit_action}_price'] = exit_price
                position_open = False
                swing_high_exit = swing_low_exit = exit_price_high = exit_price_low = exit_price = None

        info.at[info.index[i], fib_name] = level
        info.at[info.index[i], 'swing_high_exit'] = swing_high_exit
        info.at[info.index[i], 'swing_low_exit'] = swing_low_exit
        swing_high_update = False

    return info


# Strategy: Stochastic
def stochastic_strategy(info):
    stoch = StochasticOscillator(info['High'], info['Low'], info['Close'])
    info['%K'] = stoch.stoch()
    info['%D'] = stoch.stoch_signal()
    info['stoch_cross_up'] = np.where(info['%K'] > info['%D'], 1, 0)
    info['buy_signal'] = np.where((info['%K'] < 20) & (info['stoch_cross_up'].diff() == 1), 1, 0)
    info['stoch_cross_down'] = np.where(info['%K'] < info['%D'], 1, 0)
    info['sell_signal'] = np.where((info['%K'] > 80) & (info['stoch_cross_down'].diff() == 1), 1, 0)
    return info


# Strategy: Volume
def volume_strategy(info, volume_mean=50, cross_mode=True):
    info['Volume_mean'] = info['Volume'].rolling(window=volume_mean).mean()
    if cross_mode:
        info['cross_up'] = np.where(info['Volume'] > info['Volume_mean'], 1, 0)
        info['buy_signal'] = np.where(info['cross_up'].diff() == 1, 1, 0)
        info['cross_down'] = np.where(info['Volume'] < info['Volume_mean'], 1, 0)
        info['sell_signal'] = np.where(info['cross_down'].diff() == 1, 1, 0)
    else:
        info['buy_signal'] = np.where(info['Volume'] > info['Volume_mean'], 1, 0)
        info['sell_signal'] = np.where(info['Volume'] < info['Volume_mean'], 1, 0)
    return info


# Strategy: Momentum
def momentum_strategy(info, lookback=20):
    info['Momentum'] = info['Close'].pct_change(periods=lookback)
    info['buy_signal'] = np.where(info['Momentum'] > 0, 1, 0)
    info['sell_signal'] = np.where(info['Momentum'] <= 0, 1, 0)
    return info


# Strategy: Sentiment-Based Keyword Trading
def sentiment_keyword_strategy(info, sentiment_data, threshold=0.05):
    """
    Implements a sentiment-based trading strategy. Uses keyword analysis from external sentiment data (e.g., news, social media).
    """
    # External sentiment data should be in a DataFrame with dates matching 'info'
    info = info.join(sentiment_data, on='Date', how='left')

    # Create a buy signal when sentiment is extremely positive
    info['buy_signal'] = np.where(info['sentiment_score'] > threshold, 1, 0)

    # Create a sell signal when sentiment is extremely negative
    info['sell_signal'] = np.where(info['sentiment_score'] < -threshold, 1, 0)

    # Execution prices
    info['buy_price'] = info['Open']
    info['sell_price'] = info['Close']
    info['buy_time'] = 'open'
    info['sell_time'] = 'close'

    return info


# Strategy: MeanReversion
def mean_reversion_strategy(info, lookback=20):
    info['Mean_Reversion'] = info['Close'].pct_change(periods=lookback)
    info['buy_signal'] = np.where(info['Mean_Reversion'] < 0, 1, 0)
    info['sell_signal'] = np.where(info['Mean_Reversion'] >= 0, 1, 0)
    return info


# Strategy: RandomForest
def randomForest_strategy(x, y, optimizing_data=None):
    # from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)

    if optimizing_data:
        # from sklearn.model_selection import GridSearchCV
        x, y = feature_engineering(optimizing_data.copy(), reason='train', future_periods=50)  # Needs fixing.
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['auto', 'sqrt', 'log2']
        }
        grid_search = GridSearchCV(estimator=clf, param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
        grid_search.fit(x, y)
        best_params = grid_search.best_params_
        cfl_best_params = RandomForestClassifier(best_params)

    clf.fit(x, y)
    return clf


# ======================================================================================================================
# PERFORMANCE METRICS AND BACKTESTING
# ======================================================================================================================

# Function to calculate cumulative returns
def calculate_cumulative_returns(info, initial_capital=10000):
    """Calculates cumulative returns based on buy/sell signals."""
    info['position'] = info['buy_signal'].cumsum() - info['sell_signal'].cumsum()
    info['daily_returns'] = info['Close'].pct_change()
    info['strategy_returns'] = info['position'].shift(1) * info['daily_returns']
    info['cumulative_returns'] = (1 + info['strategy_returns']).cumprod() * initial_capital
    return info


# Backtesting Function
def backtest_strategy(info, strategy_fn, **kwargs):
    """Run a backtest on the given strategy."""
    info = strategy_fn(info, **kwargs)
    info = calculate_cumulative_returns(info)

    # Print performance metrics
    final_value = info['cumulative_returns'].iloc[-1]
    total_return = (final_value - 10000) / 10000
    print(f"Final Portfolio Value: ${final_value:.2f}")
    print(f"Total Return: {total_return:.2%}")

    # Plot cumulative returns
    plot_cumulative_returns(info)

    return info


# Plotting function for cumulative returns
import matplotlib.pyplot as plt


def plot_cumulative_returns(info):
    """Plot the cumulative returns over time."""
    plt.figure(figsize=(12, 6))
    plt.plot(info.index, info['cumulative_returns'], label="Strategy Returns")
    plt.title('Cumulative Returns Over Time')
    plt.xlabel('Date')
    plt.ylabel('Portfolio Value ($)')
    plt.legend()
    plt.grid(True)
    plt.show()


# Performance evaluation using confusion matrix and classification metrics
def evaluate_signals(info):
    """Evaluate the buy/sell signals as a classification problem."""
    true_signals = info['Close'].pct_change().apply(lambda x: 1 if x > 0 else 0)  # True positive if price went up
    predicted_signals = info['buy_signal']  # Buy signal as positive class

    # Calculate confusion matrix and other classification metrics
    cm = confusion_matrix(true_signals, predicted_signals)
    accuracy = accuracy_score(true_signals, predicted_signals)
    precision = precision_score(true_signals, predicted_signals)
    recall = recall_score(true_signals, predicted_signals)
    f1 = f1_score(true_signals, predicted_signals)

    print(f"Confusion Matrix:\n{cm}")
    print(f"Accuracy: {accuracy:.2f}")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1 Score: {f1:.2f}")


# Example instantiation of StrategyExecutor and running strategies
if __name__ == "__main__":
    # Example data setup (You should replace this with actual data loading logic)
    data = pd.DataFrame({
        'Date': pd.date_range(start='2023-01-01', periods=100),
        'Close': np.random.randn(100).cumsum()
    })
    data.set_index('Date', inplace=True)

    executor = StrategyExecutor(data)
    strategies = {
        'Random': random_strategy,
        'BuyCloseSellOpen': buy_close_sell_open_strategy,
        'SMACrossover': sma_crossover_strategy
    }

    strategy_results = executor.apply_strategies(strategies)
    logger.info("Strategies executed successfully.")

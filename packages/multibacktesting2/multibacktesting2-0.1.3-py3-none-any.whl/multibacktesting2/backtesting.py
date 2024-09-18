"""
Core framework data structures.
Objects from this module can also be imported from the top-level
module directly, e.g.

    from backtesting import Backtest, Strategy
"""
import multiprocessing as mp
import os
import sys
import warnings
from abc import ABCMeta, abstractmethod
from concurrent.futures import ProcessPoolExecutor, as_completed
from copy import copy
from functools import lru_cache, partial
from itertools import chain, compress, product, repeat
from math import copysign
from numbers import Number
from typing import Callable, Dict, List, Optional, Sequence, Tuple, Type, Union
import datetime
import traceback

import numpy as np
import pandas as pd
from numpy.random import default_rng

from dask import dataframe as dd


try:
    from tqdm.auto import tqdm as _tqdm
    _tqdm = partial(_tqdm, leave=False)
except ImportError:
    def _tqdm(seq, **_):
        return seq

from ._plotting import plot  # noqa: I001
from ._stats import compute_stats, compute_multiple_stats
from ._util import _as_str, _Indicator, _Data, try_

__pdoc__ = {
    'Strategy.__init__': False,
    'Order.__init__': False,
    'Position.__init__': False,
    'Trade.__init__': False,
}


class Strategy(metaclass=ABCMeta):
    """
    A trading strategy base class. Extend this class and
    override methods
    `backtesting.backtesting.Strategy.init` and
    `backtesting.backtesting.Strategy.next` to define
    your own strategy.
    """
    def __init__(self, broker, data, params):
        self._indicators = []
        self._broker: _Broker = broker
        self._data: _Data = data
        self._params = self._check_params(params)

    def __repr__(self):
        return '<Strategy ' + str(self) + '>'

    def __str__(self):
        params = ','.join(f'{i[0]}={i[1]}' for i in zip(self._params.keys(),
                                                        map(_as_str, self._params.values())))
        if params:
            params = '(' + params + ')'
        return f'{self.__class__.__name__}{params}'

    def _check_params(self, params):
        for k, v in params.items():
            if not hasattr(self, k):
                raise AttributeError(
                    f"Strategy '{self.__class__.__name__}' is missing parameter '{k}'."
                    "Strategy class should define parameters as class variables before they "
                    "can be optimized or run with.")
            setattr(self, k, v)
        return params

    def I(self,  # noqa: E743
          func: Callable, *args,
          name=None, plot=True, overlay=None, color=None, scatter=False,
          **kwargs) -> np.ndarray:
        """
        Declare an indicator. An indicator is just an array of values,
        but one that is revealed gradually in
        `backtesting.backtesting.Strategy.next` much like
        `backtesting.backtesting.Strategy.data` is.
        Returns `np.ndarray` of indicator values.

        `func` is a function that returns the indicator array(s) of
        same length as `backtesting.backtesting.Strategy.data`.

        In the plot legend, the indicator is labeled with
        function name, unless `name` overrides it.

        If `plot` is `True`, the indicator is plotted on the resulting
        `backtesting.backtesting.Backtest.plot`.

        If `overlay` is `True`, the indicator is plotted overlaying the
        price candlestick chart (suitable e.g. for moving averages).
        If `False`, the indicator is plotted standalone below the
        candlestick chart. By default, a heuristic is used which decides
        correctly most of the time.

        `color` can be string hex RGB triplet or X11 color name.
        By default, the next available color is assigned.

        If `scatter` is `True`, the plotted indicator marker will be a
        circle instead of a connected line segment (default).

        Additional `*args` and `**kwargs` are passed to `func` and can
        be used for parameters.

        For example, using simple moving average function from TA-Lib:

            def init():
                self.sma = self.I(ta.SMA, self.data.Close, self.n_sma)
        """
        if name is None:
            params = ','.join(filter(None, map(_as_str, chain(args, kwargs.values()))))
            func_name = _as_str(func)
            name = (f'{func_name}({params})' if params else f'{func_name}')
        else:
            name = name.format(*map(_as_str, args),
                               **dict(zip(kwargs.keys(), map(_as_str, kwargs.values()))))

        try:
            value = func(*args, **kwargs)
        except Exception as e:
            raise RuntimeError(f'Indicator "{name}" error') from e

        if isinstance(value, pd.DataFrame):
            value = value.values.T

        if value is not None:
            value = try_(lambda: np.asarray(value, order='C'), None)
        is_arraylike = bool(value is not None and value.shape)

        # Optionally flip the array if the user returned e.g. `df.values`
        if is_arraylike and np.argmax(value.shape) == 0:
            value = value.T

        if not is_arraylike or not 1 <= value.ndim <= 2 or value.shape[-1] != len(self._data.Close):
            raise ValueError(
                'Indicators must return (optionally a tuple of) numpy.arrays of same '
                f'length as `data` (data shape: {self._data.Close.shape}; indicator "{name}" '
                f'shape: {getattr(value, "shape" , "")}, returned value: {value})')

        if plot and overlay is None and np.issubdtype(value.dtype, np.number):
            x = value / self._data.Close
            # By default, overlay if strong majority of indicator values
            # is within 30% of Close
            with np.errstate(invalid='ignore'):
                overlay = ((x < 1.4) & (x > .6)).mean() > .6

        value = _Indicator(value, name=name, plot=plot, overlay=overlay,
                           color=color, scatter=scatter,
                           # _Indicator.s Series accessor uses this:
                           index=self.data.index)
        self._indicators.append(value)
        return value

    @abstractmethod
    def init(self):
        """
        Initialize the strategy.
        Override this method.
        Declare indicators (with `backtesting.backtesting.Strategy.I`).
        Precompute what needs to be precomputed or can be precomputed
        in a vectorized fashion before the strategy starts.

        If you extend composable strategies from `backtesting.lib`,
        make sure to call:

            super().init()
        """

    @abstractmethod
    def next(self):
        """
        Main strategy runtime method, called as each new
        `backtesting.backtesting.Strategy.data`
        instance (row; full candlestick bar) becomes available.
        This is the main method where strategy decisions
        upon data precomputed in `backtesting.backtesting.Strategy.init`
        take place.

        If you extend composable strategies from `backtesting.lib`,
        make sure to call:

            super().next()
        """

    class __FULL_EQUITY(float):  # noqa: N801
        def __repr__(self): return '.9999'
    _FULL_EQUITY = __FULL_EQUITY(1 - sys.float_info.epsilon)

    def buy(self, *,
            size: float = _FULL_EQUITY,
            stock: str,
            limit: Optional[float] = None,
            stop: Optional[float] = None,
            sl: Optional[float] = None,
            tp: Optional[float] = None,
            tag: object = None):
        """
        Place a new long order. For explanation of parameters, see `Order` and its properties.

        See `Position.close()` and `Trade.close()` for closing existing positions.

        See also `Strategy.sell()`.
        """
        assert 0 < size < 1 or round(size) == size, \
            "size must be a positive fraction of equity, or a positive whole number of units"
 
        return self._broker.new_order(size,stock, limit, stop, sl, tp, tag)
 

    def sell(self, *,
             size: float = _FULL_EQUITY,
             stock: str,
             limit: Optional[float] = None,
             stop: Optional[float] = None,
             sl: Optional[float] = None,
             tp: Optional[float] = None,
             tag: object = None):
        """
        Place a new short order. For explanation of parameters, see `Order` and its properties.

        See also `Strategy.buy()`.

        .. note::
            If you merely want to close an existing long position,
            use `Position.close()` or `Trade.close()`.
        """
        assert 0 < size < 1 or round(size) == size, \
            "size must be a positive fraction of equity, or a positive whole number of units"

        return self._broker.new_order(-size,stock, limit, stop, sl, tp, tag)


    @property
    def equity(self) -> float:
        """Current account equity (cash plus assets)."""
        return self._broker.equity

    @property
    def data(self) -> _Data:
        """
        Price data, roughly as passed into
        `backtesting.backtesting.Backtest.__init__`,
        but with two significant exceptions:

        * `data` is _not_ a DataFrame, but a custom structure
          that serves customized numpy arrays for reasons of performance
          and convenience. Besides OHLCV columns, `.index` and length,
          it offers `.pip` property, the smallest price unit of change.
        * Within `backtesting.backtesting.Strategy.init`, `data` arrays
          are available in full length, as passed into
          `backtesting.backtesting.Backtest.__init__`
          (for precomputing indicators and such). However, within
          `backtesting.backtesting.Strategy.next`, `data` arrays are
          only as long as the current iteration, simulating gradual
          price point revelation. In each call of
          `backtesting.backtesting.Strategy.next` (iteratively called by
          `backtesting.backtesting.Backtest` internally),
          the last array value (e.g. `data.Close[-1]`)
          is always the _most recent_ value.
        * If you need data arrays (e.g. `data.Close`) to be indexed
          **Pandas series**, you can call their `.s` accessor
          (e.g. `data.Close.s`). If you need the whole of data
          as a **DataFrame**, use `.df` accessor (i.e. `data.df`).
        """
        return self._data

    @property
    def position(self) -> 'Position':
        """Instance of `backtesting.backtesting.Position`."""
        return self._broker.position

    @property
    def orders(self) -> 'Tuple[Order, ...]':
        """List of orders (see `Order`) waiting for execution."""
        return _Orders(self._broker.orders)

    @property
    def trades(self) -> 'Tuple[Trade, ...]':
        """List of active trades (see `Trade`)."""
        return tuple(self._broker.trades)

    @property
    def closed_trades(self) -> 'Tuple[Trade, ...]':
        """List of settled trades (see `Trade`)."""
        return tuple(self._broker.closed_trades)


class _Orders(tuple):
    """
    TODO: remove this class. Only for deprecation.
    """
    def cancel(self):
        """Cancel all non-contingent (i.e. SL/TP) orders."""
        for order in self:
            if not order.is_contingent:
                order.cancel()

    def __getattr__(self, item):
        # TODO: Warn on deprecations from the previous version. Remove in the next.
        removed_attrs = ('entry', 'set_entry', 'is_long', 'is_short',
                         'sl', 'tp', 'set_sl', 'set_tp')
        if item in removed_attrs:
            raise AttributeError(f'Strategy.orders.{"/.".join(removed_attrs)} were removed in'
                                 'Backtesting 0.2.0. '
                                 'Use `Order` API instead. See docs.')
        raise AttributeError(f"'tuple' object has no attribute {item!r}")


class Position:
    """
    Currently held asset position, available as
    `backtesting.backtesting.Strategy.position` within
    `backtesting.backtesting.Strategy.next`.
    Can be used in boolean contexts, e.g.

        if self.position:
            ...  # we have a position, either long or short
    """
    def __init__(self, broker: '_Broker'):
        self.__broker = broker

    def __bool__(self):
        return self.size != 0

    @property
    def size(self) -> float:
        """Position size in units of asset. Negative if position is short."""
        return sum(trade.size for trade in self.__broker.trades)

    @property
    def pl(self) -> float:
        """Profit (positive) or loss (negative) of the current position in cash units."""
        return sum(trade.pl for trade in self.__broker.trades)

    @property
    def pl_pct(self) -> float:
        """Profit (positive) or loss (negative) of the current position in percent."""
        weights = np.abs([trade.size for trade in self.__broker.trades])
        weights = weights / weights.sum()
        pl_pcts = np.array([trade.pl_pct for trade in self.__broker.trades])
        return (pl_pcts * weights).sum()

    @property
    def is_long(self) -> bool:
        """True if the position is long (position size is positive)."""
        return self.size > 0

    @property
    def is_short(self) -> bool:
        """True if the position is short (position size is negative)."""
        return self.size < 0

    def close(self, portion: float = 1.):
        """
        Close portion of position by closing `portion` of each active trade. See `Trade.close`.
        """
        for trade in self.__broker.trades:
            trade.close(trade.stock,portion)

    def __repr__(self):
        return f'<Position: {self.size} ({len(self.__broker.trades)} trades)>'


class _OutOfMoneyError(Exception):
    pass


class Order:
    """
    Place new orders through `Strategy.buy()` and `Strategy.sell()`.
    Query existing orders through `Strategy.orders`.

    When an order is executed or [filled], it results in a `Trade`.

    If you wish to modify aspects of a placed but not yet filled order,
    cancel it and place a new one instead.

    All placed orders are [Good 'Til Canceled].

    [filled]: https://www.investopedia.com/terms/f/fill.asp
    [Good 'Til Canceled]: https://www.investopedia.com/terms/g/gtc.asp
    """
    def __init__(self, broker: '_Broker',
                 size: float,
                 stock: int,
                 limit_price: Optional[float] = None,
                 stop_price: Optional[float] = None,
                 sl_price: Optional[float] = None,
                 tp_price: Optional[float] = None,
                 parent_trade: Optional['Trade'] = None,
                 tag: object = None):
        self.__broker = broker
        assert size != 0
        self.__size = size
        self._stock = stock
        self.__limit_price = limit_price
        self.__stop_price = stop_price
        self.__sl_price = sl_price
        self.__tp_price = tp_price
        self.__parent_trade = parent_trade
        self.__tag = tag
        self.__stock = stock

    def _replace(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, f'_{self.__class__.__qualname__}__{k}', v)
        return self

    def __repr__(self):
        return '<Order {}>'.format(', '.join(f'{param}={round(value, 5)}'
                                             for param, value in (
                                                 ('size', self.__size),
                                                 ('limit', self.__limit_price),
                                                 ('stop', self.__stop_price),
                                                 ('sl', self.__sl_price),
                                                 ('tp', self.__tp_price),
                                                 ('contingent', self.is_contingent),
                                                 ('tag', self.__tag),
                                             ) if value is not None))

    def cancel(self):
        """Cancel the order."""
        self.__broker.orders.remove(self)
        trade = self.__parent_trade
        if trade:
            if self is trade._sl_order:
                trade._replace(sl_order=None)
            elif self is trade._tp_order:
                trade._replace(tp_order=None)
            else:
                # XXX: https://github.com/kernc/backtesting.py/issues/251#issuecomment-835634984 ???
                assert False

    # Fields getters

    @property
    def size(self) -> float:
        """
        Order size (negative for short orders).

        If size is a value between 0 and 1, it is interpreted as a fraction of current
        available liquidity (cash plus `Position.pl` minus used margin).
        A value greater than or equal to 1 indicates an absolute number of units.
        """
        return self.__size

    @property
    def limit(self) -> Optional[float]:
        """
        Order limit price for [limit orders], or None for [market orders],
        which are filled at next available price.

        [limit orders]: https://www.investopedia.com/terms/l/limitorder.asp
        [market orders]: https://www.investopedia.com/terms/m/marketorder.asp
        """
        return self.__limit_price

    @property
    def stop(self) -> Optional[float]:
        """
        Order stop price for [stop-limit/stop-market][_] order,
        otherwise None if no stop was set, or the stop price has already been hit.

        [_]: https://www.investopedia.com/terms/s/stoporder.asp
        """
        return self.__stop_price

    @property
    def sl(self) -> Optional[float]:
        """
        A stop-loss price at which, if set, a new contingent stop-market order
        will be placed upon the `Trade` following this order's execution.
        See also `Trade.sl`.
        """
        return self.__sl_price

    @property
    def tp(self) -> Optional[float]:
        """
        A take-profit price at which, if set, a new contingent limit order
        will be placed upon the `Trade` following this order's execution.
        See also `Trade.tp`.
        """
        return self.__tp_price

    @property
    def parent_trade(self):
        return self.__parent_trade

    @property
    def tag(self):
        """
        Arbitrary value (such as a string) which, if set, enables tracking
        of this order and the associated `Trade` (see `Trade.tag`).
        """
        return self.__tag

    __pdoc__['Order.parent_trade'] = False

    # Extra properties

    @property
    def stock(self):

        return self.__stock

    @property
    def is_long(self):
        """True if the order is long (order size is positive)."""
        return self.__size > 0

    @property
    def is_short(self):
        """True if the order is short (order size is negative)."""
        return self.__size < 0

    @property
    def is_contingent(self):
        """
        True for [contingent] orders, i.e. [OCO] stop-loss and take-profit bracket orders
        placed upon an active trade. Remaining contingent orders are canceled when
        their parent `Trade` is closed.

        You can modify contingent orders through `Trade.sl` and `Trade.tp`.

        [contingent]: https://www.investopedia.com/terms/c/contingentorder.asp
        [OCO]: https://www.investopedia.com/terms/o/oco.asp
        """
        return bool(self.__parent_trade)
    
class Trade:
    """
    When an `Order` is filled, it results in an active `Trade`.
    Find active trades in `Strategy.trades` and closed, settled trades in `Strategy.closed_trades`.
    """
    def __init__(self, broker: '_Broker', size: int, entry_price: float, entry_bar, tag, stock):
        self.__broker = broker
        self.__size = size
        self.__entry_price = entry_price
        self.__exit_price: Optional[float] = None
        self.__entry_bar: int = entry_bar
        self.__exit_bar: Optional[int] = None
        self.__sl_order: Optional[Order] = None
        self.__tp_order: Optional[Order] = None
        self.__tag = tag
        self.__stock = stock

        # print(stock,self.entry_time)

    def __repr__(self):
        return f'<Trade size={self.__size} time={self.__entry_bar}-{self.__exit_bar or ""} ' \
               f'price={self.__entry_price}-{self.__exit_price or ""} pl={self.pl:.0f}' \
               f'{" tag="+str(self.__tag) if self.__tag is not None else ""}>'

    def _replace(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, f'_{self.__class__.__qualname__}__{k}', v)
        return self

    def _copy(self, **kwargs):
        return copy(self)._replace(**kwargs)

    def close(self, stock, portion: float = 1.):
        """Place new `Order` to close `portion` of the trade at next market price."""
        assert 0 < portion <= 1, "portion must be a fraction between 0 and 1"
        size = copysign(max(1, round(abs(self.__size) * portion)), -self.__size)
        order = Order(self.__broker, size,stock=stock, parent_trade=self, tag=self.__tag)
        self.__broker.orders.insert(0, order)

    # Fields getters
        
    @property
    def stock(self):
        """Trade size (volume; negative for short trades)."""
        return self.__stock

    @property
    def size(self):
        """Trade size (volume; negative for short trades)."""
        return self.__size

    @property
    def entry_price(self) -> float:
        """Trade entry price."""
        return self.__entry_price

    @property
    def exit_price(self) -> Optional[float]:
        """Trade exit price (or None if the trade is still active)."""
        return self.__exit_price

    @property
    def entry_bar(self) -> int:
        """Candlestick bar index of when the trade was entered."""
        return self.__entry_bar

    @property
    def exit_bar(self) -> Optional[int]:
        """
        Candlestick bar index of when the trade was exited
        (or None if the trade is still active).
        """
        return self.__exit_bar

    @property
    def tag(self):
        """
        A tag value inherited from the `Order` that opened
        this trade.

        This can be used to track trades and apply conditional
        logic / subgroup analysis.

        See also `Order.tag`.
        """
        return self.__tag

    @property
    def _sl_order(self):
        return self.__sl_order

    @property
    def _tp_order(self):
        return self.__tp_order

    # Extra properties

    @property
    def entry_time(self) -> Union[pd.Timestamp, int]:
        """Datetime of when the trade was entered."""
        # 直接計算所需位置的索引值
        # 假設self.__entry_bar是入場位置的整數索引
        entry_bar_value = self.__entry_bar
        unique_dates = self.__broker._data.__getdata__()['date'].compute().unique()

        # 使用Pandas的`.iloc`進行行選擇
        entry_time_date = unique_dates[entry_bar_value]
        return entry_time_date


    @property
    def exit_time(self) -> Optional[Union[pd.Timestamp, int]]:
        """Datetime of when the trade was exited."""
        if self.__exit_bar is None:
            return None
        # 直接計算所需位置的索引值

        # 假設self.__entry_bar是入場位置的整數索引
        exit_bar_value = self.__exit_bar
        unique_dates = self.__broker._data.__getdata__()['date'].compute().unique()

        # 使用Pandas的`.iloc`進行行選擇
        try:
            exit_time_date = unique_dates[exit_bar_value]
            return exit_time_date
        except:
            print("exit_bar_value:", exit_bar_value)
            print("Length of df_pandas:", len(unique_dates))


    @property
    def is_long(self):
        """True if the trade is long (trade size is positive)."""
        return self.__size > 0

    @property
    def is_short(self):
        """True if the trade is short (trade size is negative)."""
        return not self.is_long

    @property
    def pl(self):
        """Trade profit (positive) or loss (negative) in cash units."""
        price = self.__exit_price or self.__broker.last_price(self.__stock)
        return self.__size * (price - self.__entry_price)


    @property
    def pl_pct(self):
        """Trade profit (positive) or loss (negative) in percent."""
        price = self.__exit_price or self.__broker.last_price(self.__stock)
        return copysign(1, self.__size) * (price / self.__entry_price - 1)

    
    def value(self):
        """Trade total value in cash (volume × price)."""
        price = self.__exit_price or self.__broker.last_price(self.stock)
        return abs(self.__size) * price

    # SL/TP management API

    @property
    def sl(self):
        """
        Stop-loss price at which to close the trade.

        This variable is writable. By assigning it a new price value,
        you create or modify the existing SL order.
        By assigning it `None`, you cancel it.
        """
        return self.__sl_order and self.__sl_order.stop

    @sl.setter
    def sl(self, price: float):
        self.__set_contingent('sl', price)

    @property
    def tp(self):
        """
        Take-profit price at which to close the trade.

        This property is writable. By assigning it a new price value,
        you create or modify the existing TP order.
        By assigning it `None`, you cancel it.
        """
        return self.__tp_order and self.__tp_order.limit

    @tp.setter
    def tp(self, price: float):
        self.__set_contingent('tp', price)

    def __set_contingent(self, type, price):
        assert type in ('sl', 'tp')
        assert price is None or 0 < price < np.inf
        attr = f'_{self.__class__.__qualname__}__{type}_order'
        order: Order = getattr(self, attr)
        if order:
            order.cancel()
        if price:
            kwargs = {'stop': price} if type == 'sl' else {'limit': price}
            order = self.__broker.new_order(-self.size,stock=self.__stock, trade=self, tag=self.tag, **kwargs)
            setattr(self, attr, order)


class _Broker:
    def __init__(self, *, data, cash, commission, margin,
                 trade_on_close, hedging, exclusive_orders, index):
        assert 0 < cash, f"cash should be >0, is {cash}"
        assert -.1 <= commission < .1, \
            ("commission should be between -10% "
             f"(e.g. market-maker's rebates) and 10% (fees), is {commission}")
        assert 0 < margin <= 1, f"margin should be between 0 and 1, is {margin}"
        self._data: _Data = data
        self._cash = cash
        self._commission = commission
        self._leverage = 1 / margin
        self._trade_on_close = trade_on_close
        self._hedging = hedging
        self._exclusive_orders = exclusive_orders

        unique_dates = self._data.__getdata__()['date'].compute().unique()
        print(f'df_pandas: {unique_dates}')

        # 假設 self._data.df['date'] 是包含日期時間戳的列
        myData = self._data.__getdata__()
        if isinstance(myData, pd.DataFrame):
            print("這是一個 Pandas DataFrame")
            dateIndex = self._data.__getdata__()['date']
        elif isinstance(myData, dd.DataFrame):
            print("這是一個 Dask DataFrame")
            dateIndex = self._data.__getdata__()['date'].compute()
        else:
            print("未知的 DataFrame 類型")
        index = pd.to_datetime(dateIndex)  # 轉換為日期，並且標準化時間為00:00:00
        unique_dates = pd.Index(index.dt.date.unique())

        # 使用去重後日期建立 Series
        self._equity = pd.Series(index=unique_dates, dtype=float)

        self.orders: List[Order] = []
        self.trades: List[Trade] = []
        self.position = Position(self)
        self.closed_trades: List[Trade] = []
        self.positions = {}  # 字典，用於跟踪持倉
        self._current_date = None

    def __repr__(self):
        return f'<Broker: {self._cash:.0f}{self.position.pl:+.1f} ({len(self.trades)} trades)>'
    
    def update_current_date(self,current_date):
        self._current_date = current_date
    
    def new_order(self,
                  size: float,
                  stock: int,
                  limit: Optional[float] = None,
                  stop: Optional[float] = None,
                  sl: Optional[float] = None,
                  tp: Optional[float] = None,
                  tag: object = None,
                  *,
                  trade: Optional[Trade] = None):
        """
        Argument size indicates whether the order is long or short
        """
        size = float(size)
        stop = stop and float(stop)
        limit = limit and float(limit)
        sl = sl and float(sl)
        tp = tp and float(tp)

        is_long = size > 0
        adjusted_price = self._adjusted_price(size=size,stock=stock)
        price = self.last_price(stock)

        if is_long:
            if not (sl or -np.inf) < (limit or stop or adjusted_price) < (tp or np.inf):
                raise ValueError(
                    "Long orders require: "
                    f"SL ({sl}) < LIMIT ({limit or stop or adjusted_price}) < TP ({tp})")
        else:
            if not (tp or -np.inf) < (limit or stop or adjusted_price) < (sl or np.inf):
                raise ValueError(
                    "Short orders require: "
                    f"TP ({tp}) < LIMIT ({limit or stop or adjusted_price}) < SL ({sl})")

        order = Order(self, size, stock, limit, stop, sl, tp, trade, tag,)
        # Put the new order in the order queue,
        # inserting SL/TP/trade-closing orders in-front
        if trade:
            self.orders.insert(0, order)
            print('insert')
        else:
            # If exclusive orders (each new order auto-closes previous orders/position),
            # cancel all non-contingent orders and close all open trades beforehand
            if self._exclusive_orders:
                for o in self.orders:
                    if not o.is_contingent:
                        o.cancel()
                # for t in self.trades:
                #     t.close(t.stock)
            self.orders.append(order)
            # print('add order')

        self.update_position(stock, size, self.get_stock_price(stock))

        return order
    
    def update_position(self, stock, size, price):
        if stock in self.positions:
            position = self.positions[stock]
            new_quantity = position['quantity'] + size
            if new_quantity == 0:
                del self.positions[stock]  # 清空持倉
            else:

                new_average_price = (position['average_price'] * position['quantity'] + price * size) / new_quantity
                self.positions[stock] = {'quantity': new_quantity, 'average_price': new_average_price}
     
        else:
            self.positions[stock] = {'quantity': size, 'average_price': price}
        # print(self._current_date)
        self.update_equity(self._current_date)

    def update_equity(self, current_date, init_value=None):
        total_stock_value = 0
        if init_value is not None:
            total_equity = init_value
        else:
            for stock, position in self.positions.items():
                # 假設有方法 self.get_stock_price 來獲取當前股票價格
                try:
                    stock_price = self.get_stock_price(stock=stock)
                    # print(position['quantity'],stock_price)
                    total_stock_value += position['quantity'] * stock_price
                except:
                    # print(current_date)
                    pass

            total_equity = self._cash + total_stock_value

        # 更新 self._equity Series 的相應日期條目
        current_date = pd.Timestamp(current_date).date()
        # print('update_equity')
        self._equity[current_date] = total_equity
        
        return total_equity

    def get_stock_price(self, stock):
        stock_data = self._data.filtered_data[self._data.filtered_data['stock_id'] == stock].copy()
        stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date
        current_date = pd.Timestamp(self._current_date).date()
        current_date_str = current_date.strftime("%Y-%m-%d")
        current_date = datetime.datetime.strptime(current_date_str, "%Y-%m-%d").date()
        filtered_stock_data = stock_data.loc[stock_data['date'] == current_date]


        if not filtered_stock_data.empty:
            current_price = filtered_stock_data['Close'].iloc[0]
            return current_price
        else:
            for i in range(1,10):
                try:
                    adjust_date = (current_date - datetime.timedelta(days=i))
                    filtered_stock_data = stock_data.loc[stock_data['date'] == adjust_date]
                    adjust_price = filtered_stock_data['Close'].iloc[0]
                    return adjust_price
                except:
                    continue
    
    def last_price(self,stock) -> float:
        """ Price at the last (current) close. """
        try:
            return self._data.filtered_data[self._data.filtered_data['stock_id']==stock].Close.iloc[-1]
        except:
            print(self._data.filtered_data[self._data.filtered_data['stock_id']==stock].Close)

    def _adjusted_price(self,stock, size=None, price=None) -> float:
        """
        Long/short `price`, adjusted for commisions.
        In long positions, the adjusted price is a fraction higher, and vice versa.
        """
        return (price or self.last_price(stock)) * (1 + copysign(self._commission, size))

    @property
    def equity(self) -> float:
        return self._cash + sum(trade.pl for trade in self.trades)

    
    def margin_available(self) -> float:
        # From https://github.com/QuantConnect/Lean/pull/3768
        margin_used = sum(trade.value() / self._leverage for trade in self.trades)
        return max(0, self.equity - margin_used)

    def next(self):
        
        # 更新總資產並獲取當前的總資產淨值

        # i = self._i = len(self._data.filtered_data) - 1
        try:
            i = self._i = self._data._get_length()
            self._process_orders()
            # self._process_trades()
            equity = self.update_equity(self._current_date)
            # self._equity[i] = equity
            
            # If equity is negative, set all to 0 and stop the simulation
            if equity <= 0:
                print("stop")
                assert self.margin_available() <= 0
                for trade in self.trades:
                    price = self._data.filtered_data[self._data.filtered_data['stock_id']==trade.stock].Close.iloc[-1]
                    self._close_trade(trade, price, i)
                    print('test')
                self._cash = 0
                self._equity[i:] = 0
                raise _OutOfMoneyError
        except Exception as e:
            tb = traceback.format_exc()
            print(f"An error occurred: {e}")
            print("Traceback:")
            print(tb)


        # 如果總資產淨值為負，中止模擬
        
    def _handle_negative_equity(self, current_date):
        assert self.margin_available <= 0
        for trade in self.trades:
            self._close_trade(trade, self._data.filtered_data.Close.iloc[-1], current_date)  # Close at current price
        self._cash = 0
        self._equity[current_date:] = 0  
        raise _OutOfMoneyError
    
    def _process_orders(self):
        reprocess_orders = False

        # Process orders
        for order in list(self.orders): 
            try:
                data = self._data.filtered_data[self._data.filtered_data['stock_id']==order.stock]
                if data.empty:
                    # 跳過空數據集
                    continue
                open, high, low = data['Open'].iloc[-1], data['High'].iloc[-1], data['Low'].iloc[-1]

                if len(data) == 1:
                    open, high, low = data['Open'].iloc[-1], data['High'].iloc[-1], data['Low'].iloc[-1]
                    prev_close = open  # 如果只有一行數據，可以考慮將前收盤價設置為開盤價
                elif len(data) > 1:
                    open, high, low = data['Open'].iloc[-1], data['High'].iloc[-1], data['Low'].iloc[-1]
                    prev_close = data['Close'].iloc[-2]
                else:
                    continue 
                # Related SL/TP order was already removed
                if order not in self.orders:
                    continue

                # Check if stop condition was hit
                stop_price = order.stop
                if stop_price:
                    is_stop_hit = ((high > stop_price) if order.is_long else (low < stop_price))
                    if not is_stop_hit:
                        continue

                    # > When the stop price is reached, a stop order becomes a market/limit order.
                    # https://www.sec.gov/fast-answers/answersstopordhtm.html
                    # print(f'high : {high} stop_price : {stop_price}')
                    order._replace(stop_price=None)
                
                # Determine purchase price.
                # Check if limit order can be filled.
                if order.limit:
                    is_limit_hit = low < order.limit if order.is_long else high > order.limit
                    # When stop and limit are hit within the same bar, we pessimistically
                    # assume limit was hit before the stop (i.e. "before it counts")
                    is_limit_hit_before_stop = (is_limit_hit and
                                                (order.limit < (stop_price or -np.inf)
                                                if order.is_long
                                                else order.limit > (stop_price or np.inf)))
                    if not is_limit_hit or is_limit_hit_before_stop:
                        continue
                    # stop_price, if set, was hit within this bar
                    price = (min(stop_price or open, order.limit)
                            if order.is_long else
                            max(stop_price or open, order.limit))
                else:
                    # Market-if-touched / market order
                    price = prev_close if self._trade_on_close else open
                    price = (max(price, stop_price or -np.inf)
                            if order.is_long else
                            min(price, stop_price or np.inf))

                # Determine entry/exit bar index
                is_market_order = not order.limit and not stop_price
                time_index = (self._i - 1) if is_market_order and self._trade_on_close else self._i
                # If order is a SL/TP order, it should close an existing trade it was contingent upon
                if order.parent_trade:
                    trade = order.parent_trade
                    _prev_size = trade.size
                    # If order.size is "greater" than trade.size, this order is a trade.close()
                    # order and part of the trade was already closed beforehand
                    size = copysign(min(abs(_prev_size), abs(order.size)), order.size)
                    # If this trade isn't already closed (e.g. on multiple `trade.close(.5)` calls)
                    if trade in self.trades:
                        self._reduce_trade(trade, price, size, time_index)
                        assert order.size != -_prev_size or trade not in self.trades
                    if order in (trade._sl_order,
                                trade._tp_order):
                        assert order.size == -trade.size
                        assert order not in self.orders  # Removed when trade was closed
                    else:
                        # It's a trade.close() order, now done
                        assert abs(_prev_size) >= abs(size) >= 1
                        self.orders.remove(order)
                    continue

                # Else this is a stand-alone trade

                # Adjust price to include commission (or bid-ask spread).
                # In long positions, the adjusted price is a fraction higher, and vice versa.
                adjusted_price = self._adjusted_price(stock=order.stock,size=order.size, price=price )

                # If order size was specified proportionally,
                # precompute true size in units, accounting for margin and spread/commissions
                size = order.size
                if -1 < size < 1:
                    size = copysign(int((self.margin_available() * self._leverage * abs(size))
                                        // adjusted_price), size)
                    # Not enough cash/margin even for a single unit
                    if not size:
                        self.orders.remove(order)
                        continue
                assert size == round(size)
                need_size = int(size)
                if not self._hedging:
                    # Fill position by FIFO closing/reducing existing opposite-facing trades.
                    # Existing trades are closed at unadjusted price, because the adjustment
                    # was already made when buying.
                    for trade in list(self.trades):
                        if trade.is_long == order.is_long:
                            continue
                        assert trade.size * order.size < 0

                        # Order size greater than this opposite-directed existing trade,
                        # so it will be closed completely
                        if abs(need_size) >= abs(trade.size):
                            self._close_trade(trade, price, time_index)
                            need_size += trade.size
                        else:
                            # The existing trade is larger than the new order,
                            # so it will only be closed partially
                            self._reduce_trade(trade, price, need_size, time_index)
                            need_size = 0

                        if not need_size:
                            break

                # If we don't have enough liquidity to cover for the order, cancel it
                try:
                    if abs(need_size) * adjusted_price > self.margin_available() * self._leverage:
                        self.orders.remove(order)
                        continue
                except:
                    pass


                # Open a new trade
                if need_size:
                    self._open_trade(price=adjusted_price,
                                    size=need_size,
                                    sl=order.sl,
                                    tp=order.tp,
                                    time_index=time_index,
                                    tag=order.tag,
                                    stock=order.stock)

                    # We need to reprocess the SL/TP orders newly added to the queue.
                    # This allows e.g. SL hitting in the same bar the order was open.
                    # See https://github.com/kernc/backtesting.py/issues/119
                    if order.sl or order.tp:
                        if is_market_order:
                            reprocess_orders = True
                        elif (low <= (order.sl or -np.inf) <= high or
                            low <= (order.tp or -np.inf) <= high):
                            warnings.warn(
                                f"({data.index[-1]}) A contingent SL/TP order would execute in the "
                                "same bar its parent stop/limit order was turned into a trade. "
                                "Since we can't assert the precise intra-candle "
                                "price movement, the affected SL/TP order will instead be executed on "
                                "the next (matching) price/bar, making the result (of this trade) "
                                "somewhat dubious. "
                                "See https://github.com/kernc/backtesting.py/issues/119",
                                UserWarning)

                # Order processed

                self.orders.remove(order)
            except Exception as e:
                tb = traceback.format_exc()
                print(f"An error occurred: {e}")
                print("Traceback:")
                print(tb)
                
        if reprocess_orders:
            self._process_orders()
        # self.orders = []

    def _process_trades(self):
        
        # Process trades
        for trade in list(self.trades): 
            # print('entry_price: ',str(trade.entry_price))
            data = self._data.filtered_data[self._data.filtered_data['stock_id']==trade.stock]
            open, high, low = data['Open'].iloc[-1], data['High'].iloc[-1], data['Low'].iloc[-1]

            # Related SL/TP order was already removed
            if trade not in self.trades:
                continue
            time_index = self._i
            #  檢查止損條件是否觸發
            if  (low <= trade.entry_price * 0.8):
                # 執行止損交易，平倉
                self._close_trade(trade, trade.entry_price * 0.8,time_index)

            # 檢查止盈條件是否觸發

            if (high >= trade.entry_price * 1.2):
                # 執行止盈交易，平倉
                # 同樣，根據實際情況調整執行邏輯
                self._close_trade(trade, trade.entry_price * 1.2,time_index)

    def _reduce_trade(self, trade: Trade, price: float, size: float, time_index):
        assert trade.size * size < 0
        assert abs(trade.size) >= abs(size)

        # print('reduce')

        size_left = trade.size + size
        assert size_left * trade.size >= 0
        if not size_left:
            close_trade = trade
        else:
            # Reduce existing trade ...
            trade._replace(size=size_left)
            if trade._sl_order:
                trade._sl_order._replace(size=-trade.size)
            if trade._tp_order:
                trade._tp_order._replace(size=-trade.size)

            # ... by closing a reduced copy of it
            close_trade = trade._copy(size=-size, sl_order=None, tp_order=None)
            self.trades.append(close_trade)

        self._close_trade(close_trade, price, time_index)

    def _close_trade(self, trade: Trade, price: float, time_index):
        # print('close_trade')
        try:
            self.trades.remove(trade)
            if trade._sl_order:
                self.orders.remove(trade._sl_order)
            if trade._tp_order:
                self.orders.remove(trade._tp_order)
            self.closed_trades.append(trade._replace(exit_price=price, exit_bar=time_index))
            self._cash += trade.pl
        except Exception as e:
            tb = traceback.format_exc()
            print(f"An error occurred: {e}")
            print("Traceback:")
            print(tb)

    def _open_trade(self, price: float, size: int,
                    sl: Optional[float], tp: Optional[float], time_index, tag, stock):
        trade = Trade(self, size, price, time_index, tag, stock)
        self.trades.append(trade)
        # Create SL/TP (bracket) orders.
        # Make sure SL order is created first so it gets adversarially processed before TP order
        # in case of an ambiguous tie (both hit within a single bar).
        # Note, sl/tp orders are inserted at the front of the list, thus order reversed.
        if tp:
            trade.tp = tp
        if sl:
            trade.sl = sl


class Backtest:
    """
    Backtest a particular (parameterized) strategy
    on particular data.

    Upon initialization, call method
    `backtesting.backtesting.Backtest.run` to run a backtest
    instance, or `backtesting.backtesting.Backtest.optimize` to
    optimize it.
    """
    def __init__(self,
                 data: dd,
                 strategy: Type[Strategy],
                 *,
                 cash: float = 10_000,
                 commission: float = .0,
                 margin: float = 1.,
                 trade_on_close=False,
                 hedging=False,
                 exclusive_orders=False
                 ):
        """
        Initialize a backtest. Requires data and a strategy to test.

        `data` is a `pd.DataFrame` with columns:
        `Open`, `High`, `Low`, `Close`, and (optionally) `Volume`.
        If any columns are missing, set them to what you have available,
        e.g.

            df['Open'] = df['High'] = df['Low'] = df['Close']

        The passed data frame can contain additional columns that
        can be used by the strategy (e.g. sentiment info).
        DataFrame index can be either a datetime index (timestamps)
        or a monotonic range index (i.e. a sequence of periods).

        `strategy` is a `backtesting.backtesting.Strategy`
        _subclass_ (not an instance).

        `cash` is the initial cash to start with.

        `commission` is the commission ratio. E.g. if your broker's commission
        is 1% of trade value, set commission to `0.01`. Note, if you wish to
        account for bid-ask spread, you can approximate doing so by increasing
        the commission, e.g. set it to `0.0002` for commission-less forex
        trading where the average spread is roughly 0.2‰ of asking price.

        `margin` is the required margin (ratio) of a leveraged account.
        No difference is made between initial and maintenance margins.
        To run the backtest using e.g. 50:1 leverge that your broker allows,
        set margin to `0.02` (1 / leverage).

        If `trade_on_close` is `True`, market orders will be filled
        with respect to the current bar's closing price instead of the
        next bar's open.

        If `hedging` is `True`, allow trades in both directions simultaneously.
        If `False`, the opposite-facing orders first close existing trades in
        a [FIFO] manner.

        If `exclusive_orders` is `True`, each new order auto-closes the previous
        trade/position, making at most a single trade (long or short) in effect
        at each time.

        [FIFO]: https://www.investopedia.com/terms/n/nfa-compliance-rule-2-43b.asp
        """
        # data = self.load_stock_data()

        if not (isinstance(strategy, type) and issubclass(strategy, Strategy)):
            raise TypeError('`strategy` must be a Strategy sub-type')
        # if not isinstance(data, pd.DataFrame):
        #     raise TypeError("`data` must be a pandas.DataFrame with columns")
        if not isinstance(commission, Number):
            raise TypeError('`commission` must be a float value, percent of '
                            'entry order price')


        # 異步計算已確定索引類型
        index_type = data.index.compute()

        # 將索引轉換為 datetime index
        if (not isinstance(index_type, pd.DatetimeIndex) and
                not isinstance(index_type, pd.RangeIndex) and
                # 異步計算以檢查索引是否為數字，並且大多數值大於1975年的時間戳
                (data.index.map_partitions(lambda x: pd.to_numeric(x, errors='coerce').notnull()).mean().compute() > .8) and
                (data.index.map_partitions(lambda x: (x > pd.Timestamp('1975').timestamp())).mean().compute() > .8)):
            try:
                # 注意: 這將會導致所有分區的索引都被轉換為 datetime
                data['index_as_datetime'] = data.map_partitions(lambda df: pd.to_datetime(df.index, infer_datetime_format=True))
                data = data.set_index('index_as_datetime', sorted=True)
            except ValueError:
                pass

        # # 檢查Volume列是否存在
        # if 'Volume' not in data.columns:
        #     data['Volume'] = np.nan

        # # 異步計算已檢查數據是否為空
        # if len(data) == 0:
        #     raise ValueError('OHLC `data` is empty')

        # # 異步計算以檢查列是否存在
        # required_columns = {'Open', 'High', 'Low', 'Close', 'Volume'}
        # columns_exist = data.columns.intersection(required_columns)
        # if len(columns_exist.compute()) != len(required_columns):
        #     raise ValueError("`data` must be a dask.DataFrame with columns 'Open', 'High', 'Low', 'Close', and (optionally) 'Volume'")
        
        # 检查OHLC列是否有任何NaN值
        if data[['Open', 'High', 'Low', 'Close']].map_partitions(lambda df: df.isnull().values.any()).compute().any():
            raise ValueError('Some OHLC values are missing (NaN). Please strip those lines with `df.dropna()` or fill them in with `df.interpolate()` or whatever.')


        # 这里假设`cash`是一个已经定义的变量
        # 异步计算以检查Close价格是否大于初始现金值
        if data['Close'].map_partitions(lambda df: df.isnull().values.any()).compute().any():
            warnings.warn('Some prices are larger than initial cash value. Note that fractional trading is not supported. If you want to trade Bitcoin, increase initial cash, or trade μBTC or satoshis instead (GH-134).', stacklevel=2)


        # # 检查所有分区的索引是否都是单调递增的
        # if not data.map_partitions(lambda x: x.index.is_monotonic_increasing).all().compute():
        #     warnings.warn('Data index is not sorted in ascending order. Sorting.', stacklevel=2)
        #     data = data.map_partitions(lambda df: df.sort_index())


        # 再次检查索引是否为DatetimeIndex，这可能需要显式地将索引转换为DatetimeIndex
        # 由于Dask的惰性计算特性，这里我们不再进行检查，而是提出警告建议
        warnings.warn('Ensure data index is datetime. Assuming simple periods, but `pd.DateTimeIndex` is advised.', stacklevel=2)

        # # Convert index to datetime index
        # if (not isinstance(data.index, pd.DatetimeIndex) and
        #     not isinstance(data.index, pd.RangeIndex) and
        #     # Numeric index with most large numbers
        #     (data.index.is_numeric() and
        #      (data.index > pd.Timestamp('1975').timestamp()).mean() > .8)):
        #     try:
        #         data.index = pd.to_datetime(data.index, infer_datetime_format=True)
        #     except ValueError:
        #         pass

        # if 'Volume' not in data:
        #     data['Volume'] = np.nan

        # if len(data) == 0:
        #     raise ValueError('OHLC `data` is empty')
        # if len(data.columns.intersection({'Open', 'High', 'Low', 'Close', 'Volume'})) != 5:
        #     raise ValueError("`data` must be a pandas.DataFrame with columns "
        #                      "'Open', 'High', 'Low', 'Close', and (optionally) 'Volume'")
        # if data[['Open', 'High', 'Low', 'Close']].isnull().values.any():
        #     raise ValueError('Some OHLC values are missing (NaN). '
        #                      'Please strip those lines with `df.dropna()` or '
        #                      'fill them in with `df.interpolate()` or whatever.')
        # if np.any(data['Close'] > cash):
        #     warnings.warn('Some prices are larger than initial cash value. Note that fractional '
        #                   'trading is not supported. If you want to trade Bitcoin, '
        #                   'increase initial cash, or trade μBTC or satoshis instead (GH-134).',
        #                   stacklevel=2)
        # if not data.index.is_monotonic_increasing:
        #     warnings.warn('Data index is not sorted in ascending order. Sorting.',
        #                   stacklevel=2)
        #     data = data.sort_index()
        # if not isinstance(data.index, pd.DatetimeIndex):
        #     warnings.warn('Data index is not datetime. Assuming simple periods, '
        #                   'but `pd.DateTimeIndex` is advised.',
        #                   stacklevel=2)

        self._data: dd = data
        self._broker = partial(
            _Broker, cash=cash, commission=commission, margin=margin,
            trade_on_close=trade_on_close, hedging=hedging,
            exclusive_orders=exclusive_orders, index=data.index,
        )
        # print('data index is :' + str(data.index))
        self._strategy = strategy
        self._results: Optional[pd.Series] = None

        # all_dates = pd.to_datetime(self._data['date']).unique().normalize()
        # all_dates = pd.Series(all_dates).sort_values().values  # 转换为 Series，使用 sort_values，然后取 values

        # 獲取唯一的日期並排序
        unique_dates = self._data['date'].drop_duplicates().compute()
        unique_dates = unique_dates.sort_values()
        self._all_dates = unique_dates
        self._cash = cash

    
    def run(self, **kwargs) -> pd.Series:
        """
        Run the backtest. Returns `pd.Series` with results and statistics.

        Keyword arguments are interpreted as strategy parameters.

            >>> Backtest(GOOG, SmaCross).run()
            Start                     2004-08-19 00:00:00
            End                       2013-03-01 00:00:00
            Duration                   3116 days 00:00:00
            Exposure Time [%]                     93.9944
            Equity Final [$]                      51959.9
            Equity Peak [$]                       75787.4
            Return [%]                            419.599
            Buy & Hold Return [%]                 703.458
            Return (Ann.) [%]                      21.328
            Volatility (Ann.) [%]                 36.5383
            Sharpe Ratio                         0.583718
            Sortino Ratio                         1.09239
            Calmar Ratio                         0.444518
            Max. Drawdown [%]                    -47.9801
            Avg. Drawdown [%]                    -5.92585
            Max. Drawdown Duration      584 days 00:00:00
            Avg. Drawdown Duration       41 days 00:00:00
            # Trades                                   65
            Win Rate [%]                          46.1538
            Best Trade [%]                         53.596
            Worst Trade [%]                      -18.3989
            Avg. Trade [%]                        2.35371
            Max. Trade Duration         183 days 00:00:00
            Avg. Trade Duration          46 days 00:00:00
            Profit Factor                         2.08802
            Expectancy [%]                        8.79171
            SQN                                  0.916893
            Kelly Criterion                        0.6134
            _strategy                            SmaCross
            _equity_curve                           Eq...
            _trades                       Size  EntryB...
            dtype: object

        .. warning::
            You may obtain different results for different strategy parameters.
            E.g. if you use 50- and 200-bar SMA, the trading simulation will
            begin on bar 201. The actual length of delay is equal to the lookback
            period of the `Strategy.I` indicator which lags the most.
            Obviously, this can affect results.
        """
        data = _Data(self._data.copy(deep=False))
        broker: _Broker = self._broker(data=data)
        strategy: Strategy = self._strategy(broker, data, kwargs)
        strategy.init()
        data._update()  # Strategy.init might have changed/added to data.df
        # Indicators used in Strategy.next()
        # indicator_attrs = {attr: indicator
        #                    for attr, indicator in strategy.__dict__.items()
        #                    if isinstance(indicator, _Indicator)}.items()

        # def process_batch(current_batch, historical_data=None):
        #     # 合併當前批次和歷史數據
        #     if historical_data is not None:
        #         combined_data = pd.concat([historical_data, current_batch])
        #     else:
        #         combined_data = current_batch

        #     current_date_ts = pd.Timestamp(current_date)
        #     # 計算當前日期之前5天的日期
        #     five_days_ago = current_date_ts - pd.Timedelta(days=5)
        #     # 篩選出最新的五天數據
        #     # 注意: 這裡包含了當前日期
        #     current_data_up_to_date = combined_data[(combined_data['date'] > five_days_ago) & (combined_data['date'] <= current_date)]
        #     return  current_data_up_to_date  
        
        # 初始化歷史數據變量
        historical_data = None

        # progress_len = len(self._all_dates)
        
        with np.errstate(invalid='ignore'):
            i = 0
            print(f"len of all dates: {len(self._all_dates)}")
            for current_date in self._all_dates:
                print(f"current_date: {current_date}")

                # 選擇當前批次的數據
                current_batch = self._data.loc[self._data['date']==current_date].compute()
                # print('001')
                # 處理當前批次的數據
                # historical_data = process_batch(current_batch, historical_data)
                # 更新日期為當前日期
                broker.update_current_date(current_date)
                # print('002')
                # 更新數據
                # data.set_data(historical_data)
                data.set_data(current_batch)
                # print('003')

                # 處理訂單
                try:
                    broker.next()
                    # print('004')
                    # 進行策略迭代
                    strategy.next(current_batch)
                    # print('005')
                except _OutOfMoneyError:
                    pass

                data._set_length(i)
                i += 1
  
            else:
                # 關閉任何未平倉的交易
                print('test1')
                for trade in broker.trades:
                    trade.close(trade.stock)
                print('test2')
                # 重新運行broker.next()以更新最後一天的資產
                if self._all_dates.size > 0:
                    try_(broker.next, exception=_OutOfMoneyError)
            print('test3')
            data._set_length(len(self._data))
            print('test4')
            equity = pd.Series(broker._equity).bfill().fillna(broker._cash).values

            print(len(equity))

            self._results = compute_multiple_stats(
                trades=broker.closed_trades,
                equity=equity,
                ohlc_data=self._data,
                risk_free_rate=0.0,
                strategy_instance=strategy,
            )

        return self._results

    def optimize(self, *,
                 maximize: Union[str, Callable[[pd.Series], float]] = 'SQN',
                 method: str = 'grid',
                 max_tries: Optional[Union[int, float]] = None,
                 constraint: Optional[Callable[[dict], bool]] = None,
                 return_heatmap: bool = False,
                 return_optimization: bool = False,
                 random_state: Optional[int] = None,
                 **kwargs) -> Union[pd.Series,
                                    Tuple[pd.Series, pd.Series],
                                    Tuple[pd.Series, pd.Series, dict]]:
        """
        Optimize strategy parameters to an optimal combination.
        Returns result `pd.Series` of the best run.

        `maximize` is a string key from the
        `backtesting.backtesting.Backtest.run`-returned results series,
        or a function that accepts this series object and returns a number;
        the higher the better. By default, the method maximizes
        Van Tharp's [System Quality Number](https://google.com/search?q=System+Quality+Number).

        `method` is the optimization method. Currently two methods are supported:

        * `"grid"` which does an exhaustive (or randomized) search over the
          cartesian product of parameter combinations, and
        * `"skopt"` which finds close-to-optimal strategy parameters using
          [model-based optimization], making at most `max_tries` evaluations.

        [model-based optimization]: \
            https://scikit-optimize.github.io/stable/auto_examples/bayesian-optimization.html

        `max_tries` is the maximal number of strategy runs to perform.
        If `method="grid"`, this results in randomized grid search.
        If `max_tries` is a floating value between (0, 1], this sets the
        number of runs to approximately that fraction of full grid space.
        Alternatively, if integer, it denotes the absolute maximum number
        of evaluations. If unspecified (default), grid search is exhaustive,
        whereas for `method="skopt"`, `max_tries` is set to 200.

        `constraint` is a function that accepts a dict-like object of
        parameters (with values) and returns `True` when the combination
        is admissible to test with. By default, any parameters combination
        is considered admissible.

        If `return_heatmap` is `True`, besides returning the result
        series, an additional `pd.Series` is returned with a multiindex
        of all admissible parameter combinations, which can be further
        inspected or projected onto 2D to plot a heatmap
        (see `backtesting.lib.plot_heatmaps()`).

        If `return_optimization` is True and `method = 'skopt'`,
        in addition to result series (and maybe heatmap), return raw
        [`scipy.optimize.OptimizeResult`][OptimizeResult] for further
        inspection, e.g. with [scikit-optimize]\
        [plotting tools].

        [OptimizeResult]: \
            https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.OptimizeResult.html
        [scikit-optimize]: https://scikit-optimize.github.io
        [plotting tools]: https://scikit-optimize.github.io/stable/modules/plots.html

        If you want reproducible optimization results, set `random_state`
        to a fixed integer random seed.

        Additional keyword arguments represent strategy arguments with
        list-like collections of possible values. For example, the following
        code finds and returns the "best" of the 7 admissible (of the
        9 possible) parameter combinations:

            backtest.optimize(sma1=[5, 10, 15], sma2=[10, 20, 40],
                              constraint=lambda p: p.sma1 < p.sma2)

        .. TODO::
            Improve multiprocessing/parallel execution on Windos with start method 'spawn'.
        """
        if not kwargs:
            raise ValueError('Need some strategy parameters to optimize')

        maximize_key = None
        if isinstance(maximize, str):
            maximize_key = str(maximize)
            stats = self._results if self._results is not None else self.run()
            if maximize not in stats:
                raise ValueError('`maximize`, if str, must match a key in pd.Series '
                                 'result of backtest.run()')

            def maximize(stats: pd.Series, _key=maximize):
                return stats[_key]

        elif not callable(maximize):
            raise TypeError('`maximize` must be str (a field of backtest.run() result '
                            'Series) or a function that accepts result Series '
                            'and returns a number; the higher the better')
        assert callable(maximize), maximize

        have_constraint = bool(constraint)
        if constraint is None:

            def constraint(_):
                return True

        elif not callable(constraint):
            raise TypeError("`constraint` must be a function that accepts a dict "
                            "of strategy parameters and returns a bool whether "
                            "the combination of parameters is admissible or not")
        assert callable(constraint), constraint

        if return_optimization and method != 'skopt':
            raise ValueError("return_optimization=True only valid if method='skopt'")

        def _tuple(x):
            return x if isinstance(x, Sequence) and not isinstance(x, str) else (x,)

        for k, v in kwargs.items():
            if len(_tuple(v)) == 0:
                raise ValueError(f"Optimization variable '{k}' is passed no "
                                 f"optimization values: {k}={v}")

        class AttrDict(dict):
            def __getattr__(self, item):
                return self[item]

        def _grid_size():
            size = int(np.prod([len(_tuple(v)) for v in kwargs.values()]))
            if size < 10_000 and have_constraint:
                size = sum(1 for p in product(*(zip(repeat(k), _tuple(v))
                                                for k, v in kwargs.items()))
                           if constraint(AttrDict(p)))
            return size

        def _optimize_grid() -> Union[pd.Series, Tuple[pd.Series, pd.Series]]:
            rand = default_rng(random_state).random
            grid_frac = (1 if max_tries is None else
                         max_tries if 0 < max_tries <= 1 else
                         max_tries / _grid_size())
            param_combos = [dict(params)  # back to dict so it pickles
                            for params in (AttrDict(params)
                                           for params in product(*(zip(repeat(k), _tuple(v))
                                                                   for k, v in kwargs.items())))
                            if constraint(params)  # type: ignore
                            and rand() <= grid_frac]
            if not param_combos:
                raise ValueError('No admissible parameter combinations to test')

            if len(param_combos) > 300:
                warnings.warn(f'Searching for best of {len(param_combos)} configurations.',
                              stacklevel=2)

            heatmap = pd.Series(np.nan,
                                name=maximize_key,
                                index=pd.MultiIndex.from_tuples(
                                    [p.values() for p in param_combos],
                                    names=next(iter(param_combos)).keys()))

            def _batch(seq):
                n = np.clip(int(len(seq) // (os.cpu_count() or 1)), 1, 300)
                for i in range(0, len(seq), n):
                    yield seq[i:i + n]

            # Save necessary objects into "global" state; pass into concurrent executor
            # (and thus pickle) nothing but two numbers; receive nothing but numbers.
            # With start method "fork", children processes will inherit parent address space
            # in a copy-on-write manner, achieving better performance/RAM benefit.
            backtest_uuid = np.random.random()
            param_batches = list(_batch(param_combos))
            Backtest._mp_backtests[backtest_uuid] = (self, param_batches, maximize)  # type: ignore
            try:
                # If multiprocessing start method is 'fork' (i.e. on POSIX), use
                # a pool of processes to compute results in parallel.
                # Otherwise (i.e. on Windos), sequential computation will be "faster".
                if mp.get_start_method(allow_none=False) == 'fork':
                    with ProcessPoolExecutor() as executor:
                        futures = [executor.submit(Backtest._mp_task, backtest_uuid, i)
                                   for i in range(len(param_batches))]
                        for future in _tqdm(as_completed(futures), total=len(futures),
                                            desc='Backtest.optimize'):
                            batch_index, values = future.result()
                            for value, params in zip(values, param_batches[batch_index]):
                                heatmap[tuple(params.values())] = value
                else:
                    if os.name == 'posix':
                        warnings.warn("For multiprocessing support in `Backtest.optimize()` "
                                      "set multiprocessing start method to 'fork'.")
                    for batch_index in _tqdm(range(len(param_batches))):
                        _, values = Backtest._mp_task(backtest_uuid, batch_index)
                        for value, params in zip(values, param_batches[batch_index]):
                            heatmap[tuple(params.values())] = value
            finally:
                del Backtest._mp_backtests[backtest_uuid]

            best_params = heatmap.idxmax()

            if pd.isnull(best_params):
                # No trade was made in any of the runs. Just make a random
                # run so we get some, if empty, results
                stats = self.run(**param_combos[0])
            else:
                stats = self.run(**dict(zip(heatmap.index.names, best_params)))

            if return_heatmap:
                return stats, heatmap
            return stats

        def _optimize_skopt() -> Union[pd.Series,
                                       Tuple[pd.Series, pd.Series],
                                       Tuple[pd.Series, pd.Series, dict]]:
            try:
                from skopt import forest_minimize
                from skopt.callbacks import DeltaXStopper
                from skopt.learning import ExtraTreesRegressor
                from skopt.space import Categorical, Integer, Real
                from skopt.utils import use_named_args
            except ImportError:
                raise ImportError("Need package 'scikit-optimize' for method='skopt'. "
                                  "pip install scikit-optimize") from None

            nonlocal max_tries
            max_tries = (200 if max_tries is None else
                         max(1, int(max_tries * _grid_size())) if 0 < max_tries <= 1 else
                         max_tries)

            dimensions = []
            for key, values in kwargs.items():
                values = np.asarray(values)
                if values.dtype.kind in 'mM':  # timedelta, datetime64
                    # these dtypes are unsupported in skopt, so convert to raw int
                    # TODO: save dtype and convert back later
                    values = values.astype(int)

                if values.dtype.kind in 'iumM':
                    dimensions.append(Integer(low=values.min(), high=values.max(), name=key))
                elif values.dtype.kind == 'f':
                    dimensions.append(Real(low=values.min(), high=values.max(), name=key))
                else:
                    dimensions.append(Categorical(values.tolist(), name=key, transform='onehot'))

            # Avoid recomputing re-evaluations:
            # "The objective has been evaluated at this point before."
            # https://github.com/scikit-optimize/scikit-optimize/issues/302
            memoized_run = lru_cache()(lambda tup: self.run(**dict(tup)))

            # np.inf/np.nan breaks sklearn, np.finfo(float).max breaks skopt.plots.plot_objective
            INVALID = 1e300
            progress = iter(_tqdm(repeat(None), total=max_tries, desc='Backtest.optimize'))

            @use_named_args(dimensions=dimensions)
            def objective_function(**params):
                next(progress)
                # Check constraints
                # TODO: Adjust after https://github.com/scikit-optimize/scikit-optimize/pull/971
                if not constraint(AttrDict(params)):
                    return INVALID
                res = memoized_run(tuple(params.items()))
                value = -maximize(res)
                if np.isnan(value):
                    return INVALID
                return value

            with warnings.catch_warnings():
                warnings.filterwarnings(
                    'ignore', 'The objective has been evaluated at this point before.')

                res = forest_minimize(
                    func=objective_function,
                    dimensions=dimensions,
                    n_calls=max_tries,
                    base_estimator=ExtraTreesRegressor(n_estimators=20, min_samples_leaf=2),
                    acq_func='LCB',
                    kappa=3,
                    n_initial_points=min(max_tries, 20 + 3 * len(kwargs)),
                    initial_point_generator='lhs',  # 'sobel' requires n_initial_points ~ 2**N
                    callback=DeltaXStopper(9e-7),
                    random_state=random_state)

            stats = self.run(**dict(zip(kwargs.keys(), res.x)))
            output = [stats]

            if return_heatmap:
                heatmap = pd.Series(dict(zip(map(tuple, res.x_iters), -res.func_vals)),
                                    name=maximize_key)
                heatmap.index.names = kwargs.keys()
                heatmap = heatmap[heatmap != -INVALID]
                heatmap.sort_index(inplace=True)
                output.append(heatmap)

            if return_optimization:
                valid = res.func_vals != INVALID
                res.x_iters = list(compress(res.x_iters, valid))
                res.func_vals = res.func_vals[valid]
                output.append(res)

            return stats if len(output) == 1 else tuple(output)

        if method == 'grid':
            output = _optimize_grid()
        elif method == 'skopt':
            output = _optimize_skopt()
        else:
            raise ValueError(f"Method should be 'grid' or 'skopt', not {method!r}")
        return output

    @staticmethod
    def _mp_task(backtest_uuid, batch_index):
        bt, param_batches, maximize_func = Backtest._mp_backtests[backtest_uuid]
        return batch_index, [maximize_func(stats) if stats['# Trades'] else np.nan
                             for stats in (bt.run(**params)
                                           for params in param_batches[batch_index])]

    _mp_backtests: Dict[float, Tuple['Backtest', List, Callable]] = {}

    def plot(self, *, results: pd.Series = None, filename=None, plot_width=None,
             plot_equity=True, plot_return=False, plot_pl=True,
             plot_volume=True, plot_drawdown=False, plot_trades=True,
             smooth_equity=False, relative_equity=True,
             superimpose: Union[bool, str] = True,
             resample=True, reverse_indicators=False,
             show_legend=True, open_browser=True):
        """
        Plot the progression of the last backtest run.

        If `results` is provided, it should be a particular result
        `pd.Series` such as returned by
        `backtesting.backtesting.Backtest.run` or
        `backtesting.backtesting.Backtest.optimize`, otherwise the last
        run's results are used.

        `filename` is the path to save the interactive HTML plot to.
        By default, a strategy/parameter-dependent file is created in the
        current working directory.

        `plot_width` is the width of the plot in pixels. If None (default),
        the plot is made to span 100% of browser width. The height is
        currently non-adjustable.

        If `plot_equity` is `True`, the resulting plot will contain
        an equity (initial cash plus assets) graph section. This is the same
        as `plot_return` plus initial 100%.

        If `plot_return` is `True`, the resulting plot will contain
        a cumulative return graph section. This is the same
        as `plot_equity` minus initial 100%.

        If `plot_pl` is `True`, the resulting plot will contain
        a profit/loss (P/L) indicator section.

        If `plot_volume` is `True`, the resulting plot will contain
        a trade volume section.

        If `plot_drawdown` is `True`, the resulting plot will contain
        a separate drawdown graph section.

        If `plot_trades` is `True`, the stretches between trade entries
        and trade exits are marked by hash-marked tractor beams.

        If `smooth_equity` is `True`, the equity graph will be
        interpolated between fixed points at trade closing times,
        unaffected by any interim asset volatility.

        If `relative_equity` is `True`, scale and label equity graph axis
        with return percent, not absolute cash-equivalent values.

        If `superimpose` is `True`, superimpose larger-timeframe candlesticks
        over the original candlestick chart. Default downsampling rule is:
        monthly for daily data, daily for hourly data, hourly for minute data,
        and minute for (sub-)second data.
        `superimpose` can also be a valid [Pandas offset string],
        such as `'5T'` or `'5min'`, in which case this frequency will be
        used to superimpose.
        Note, this only works for data with a datetime index.

        If `resample` is `True`, the OHLC data is resampled in a way that
        makes the upper number of candles for Bokeh to plot limited to 10_000.
        This may, in situations of overabundant data,
        improve plot's interactive performance and avoid browser's
        `Javascript Error: Maximum call stack size exceeded` or similar.
        Equity & dropdown curves and individual trades data is,
        likewise, [reasonably _aggregated_][TRADES_AGG].
        `resample` can also be a [Pandas offset string],
        such as `'5T'` or `'5min'`, in which case this frequency will be
        used to resample, overriding above numeric limitation.
        Note, all this only works for data with a datetime index.

        If `reverse_indicators` is `True`, the indicators below the OHLC chart
        are plotted in reverse order of declaration.

        [Pandas offset string]: \
            https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects

        [TRADES_AGG]: lib.html#backtesting.lib.TRADES_AGG

        If `show_legend` is `True`, the resulting plot graphs will contain
        labeled legends.

        If `open_browser` is `True`, the resulting `filename` will be
        opened in the default web browser.
        """
        if results is None:
            if self._results is None:
                raise RuntimeError('First issue `backtest.run()` to obtain results.')
            results = self._results

        return plot(
            results=results,
            df=self._data,
            indicators=results._strategy._indicators,
            filename=filename,
            plot_width=plot_width,
            plot_equity=plot_equity,
            plot_return=plot_return,
            plot_pl=plot_pl,
            plot_volume=plot_volume,
            plot_drawdown=plot_drawdown,
            plot_trades=plot_trades,
            smooth_equity=smooth_equity,
            relative_equity=relative_equity,
            superimpose=superimpose,
            resample=resample,
            reverse_indicators=reverse_indicators,
            show_legend=show_legend,
            open_browser=open_browser)

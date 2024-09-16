"""
MIT License

Copyright (c) 2024-present Puncher1

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from .http import HTTPClient
from .finance import Stock, Commodity, Crypto, CurrencyWithAmount, CurrencyConversion, Currency
from .enums import CommodityType
from .errors import StockNotFound

if TYPE_CHECKING:
    from typing_extensions import Self


# fmt: off
__all__ = (
    "Client",
)
# fmt: on


class Client:
    """Represents a client that interacts with the API.

    .. container:: operations

        .. describe:: async with x

            Asynchronous context manager for the client that automatically cleans up.

    Parameters
    -----------
    api_key: :class:`str`
        The API key to authenticate.
    """

    __slots__ = ("_http", "_is_closed")

    def __init__(self, api_key: str):
        self._http: HTTPClient = HTTPClient(api_key)
        self._is_closed: bool = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def is_closed(self) -> bool:
        """:class:`bool`: Whether the client is closed or not."""
        return self._is_closed

    async def close(self) -> None:
        """Closes the client.

        This closes all connections to the API.
        """
        if not self.is_closed():
            self._is_closed = True
            await self._http.close()

    async def fetch_stock(self, ticker: str) -> Stock:
        """|coro|

        Retrieves a :class:`Stock` with the specified ticker.

        Parameters
        -----------
        ticker: :class:`str`
            The ticker to fetch from.

        Raises
        -------
        StockNotFound
            The stock with the specified ticker could not be found.
        HTTPException
            Retrieving the stock failed.

        Returns
        --------
        :class:`Stock`
            The retrieved stock.
        """
        data = await self._http.get_stock(ticker=ticker)
        if data:
            return Stock(http=self._http, data=data)
        else:
            raise StockNotFound(f"stock with ticker '{ticker}' could not be found")

    async def fetch_commodity(self, type: CommodityType) -> Commodity:
        """|coro|

        Retrieves a :class:`Commodity` with the specified type.

        Parameters
        -----------
        type: :class:`CommodityType`
            The type of the commodity to fetch from.

        Raises
        -------
        HTTPException
            Retrieving the commodity failed.

        Returns
        --------
        :class:`Commodity`
            The retrieved commodity.
        """
        if type == CommodityType.gold:
            data = await self._http.get_gold()
        else:
            data = await self._http.get_commodity(name=type.value)

        return Commodity(http=self._http, type=type, data=data)

    async def fetch_crypto(self, symbol: str) -> Crypto:
        """|coro|

        Retrieves a :class:`Crypto` with the specified symbol.

        Parameters
        -----------
        symbol: :class:`str`
            The symbol to fetch from.

        Raises
        -------
        HTTPException
            Retrieving the cryptocurrency failed.

        Returns
        --------
        :class:`Crypto`
            The retrieved cryptocurrency.
        """
        data = await self._http.get_crypto(symbol=symbol)
        return Crypto(http=self._http, data=data)

    async def fetch_crypto_symbols(self) -> List[str]:
        """|coro|

        Retrieves a list of all available cryptocurrency symbols.

        Raises
        -------
        HTTPException
            Retrieving the symbols failed.

        Returns
        --------
        List[:class:`str`]
            The retrieved list of available symbols.
        """
        data = await self._http.get_crypto_symbols()
        return data["symbols"]

    async def fetch_currency_conversion(
        self,
        *,
        have: str,
        have_amount: float,
        want: str,
    ) -> CurrencyConversion:
        """|coro|

        Retrieves a converted :class:`CurrencyWithAmount` from the specified ``have`` currency
        and ``have_amount`` and returns the old and new one.

        Parameters
        ----------
        have: :class:`str`
            The currency name to convert from (e.g. ``AUD``).
        have_amount: :class:`float`
            The amount of the ``have`` currency to convert from.
        want: :class:`str`
            The currency name to convert to (e.g. ``GBP``).

        Raises
        -------
        HTTPException
            Retrieving the currency failed.

        Returns
        -------
        Tuple[:class:`CurrencyWithAmount`, :class:`CurrencyWithAmount`]
            The old and newly retrieved currency with their respective amounts.
        """
        data = await self._http.get_currency_conversion(want=want, have=have, amount=have_amount)

        old_amount = data["old_amount"]
        new_amount = data["new_amount"]
        rate_new_old = new_amount / old_amount if old_amount != 0 else 0
        rate_old_new = old_amount / new_amount if new_amount != 0 else 0

        old_currency = Currency(
            http=self._http,
            name=data["old_currency"],
            exchange_rate=rate_old_new,
            reference=data["new_currency"],
        )

        new_currency = Currency(
            http=self._http,
            name=data["new_currency"],
            exchange_rate=rate_new_old,
            reference=data["old_currency"],
        )

        old_currency_with_amount = CurrencyWithAmount(currency=old_currency, amount=old_amount)
        new_currency_with_amount = CurrencyWithAmount(currency=new_currency, amount=new_amount)

        return CurrencyConversion(old=old_currency_with_amount, new=new_currency_with_amount)

    async def fetch_currency(self, name: str, *, reference: str) -> Currency:
        """|coro|

        Retrieves a :class:`Currency` with the specified name and reference.

        Parameters
        ----------
        name: :class:`str`
            The currency name to retrieve from (e.g. ``GBP``).
        reference: :class:`str`
            The currency reference for the equivalent value (e.g. ``AUD``).

        Raises
        -------
        HTTPException
            Retrieving the currency failed.

        Returns
        -------
        :class:`Currency`
            The retrieved currency.
        """

        pair = f"{reference}_{name}"
        data = await self._http.get_exchange_rate(pair=pair)
        currencies = data["currency_pair"].split("_")

        return Currency(
            http=self._http,
            name=currencies[1],
            exchange_rate=data["exchange_rate"],
            reference=currencies[0],
        )

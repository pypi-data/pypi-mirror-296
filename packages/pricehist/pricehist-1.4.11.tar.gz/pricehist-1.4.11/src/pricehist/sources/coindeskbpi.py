import dataclasses
import json
import logging
from decimal import Decimal

import requests

from pricehist import exceptions
from pricehist.price import Price

from .basesource import BaseSource


class CoinDeskBPI(BaseSource):
    def id(self):
        return "coindeskbpi"

    def name(self):
        return "CoinDesk Bitcoin Price Index"

    def description(self):
        return "The original CoinDesk Bitcoin Price Index v1 API."

    def source_url(self):
        return "https://www.coindesk.com/coindesk-api"

    def start(self):
        return "2013-10-01"

    def types(self):
        return ["close"]

    def notes(self):
        return (
            "Powered by CoinDesk, https://www.coindesk.com/price/bitcoin.\n"
            "\n"
            "Data currently starts from 2013-10-01 (originally 2010-07-17).\n"
            "\n"
            "Original API documentation:\n"
            "http://web.archive.org/web/20210802085504/https://www.coindesk.com/coindesk-api\n"
            "\n"
            "This source's ID has been changed from 'coindesk' to 'coindeskbpi'\n"
            "since CoinDesk now has a wider range of offerings: \n"
            "\n"
            "| API name   | Sample path                     | Data start |\n"
            "|------------|---------------------------------|------------|\n"
            "| v1 BPI     | /v1/bpi/historical/close.json   | 2013-10-01 |\n"
            "| v2         | /v2/tb/price/values/BTC         | 2014-11-03 |\n"
            "| indices v1 | /indices/api/v1/trend-indicator | 2018-01-01 |\n"
        )

    def symbols(self):
        return [(f"BTC/USD", f"Bitcoin against United States Dollar")]

    def fetch(self, series):
        if series.base != "BTC" or series.quote != "USD":
            # The only valid pair for historical data from the v1 BPI API
            raise exceptions.InvalidPair(series.base, series.quote, self)

        data = self._data(series)

        prices = [
            Price(d, Decimal(str(v)))
            for d, v in data.get("bpi", {}).items()
            if (d >= series.start and d <= series.end)
        ]

        return dataclasses.replace(series, prices=prices)

    def _data(self, series):
        url = "https://api.coindesk.com/v1/bpi/historical/close.json"
        headers = {
            "Accept-Encoding": "identity",
        }
        params = {
            "start": "2010-07-17",
            "end": "3000-12-31",
            "currency": "USD",
        }

        try:
            response = self.log_curl(requests.get(url, params=params, headers=headers))
        except Exception as e:
            raise exceptions.RequestError(str(e)) from e

        code = response.status_code
        text = response.text
        if code == 404 and "currency was not found" in text:
            raise exceptions.InvalidPair(series.base, series.quote, self)
        elif code == 404 and "only covers data from" in text:
            raise exceptions.BadResponse(text)
        elif code == 404 and "end date is before" in text and series.end < series.start:
            raise exceptions.BadResponse("End date is before start date.")
        elif code == 404 and "end date is before" in text:
            raise exceptions.BadResponse("The start date must be in the past.")
        elif code == 500 and "No results returned from database" in text:
            raise exceptions.BadResponse("No results returned from database.")
        else:
            try:
                response.raise_for_status()
            except Exception as e:
                raise exceptions.BadResponse(str(e)) from e

        if "age" in response.headers:
            logging.debug(
                f"The API returned a cached response that is {response.headers['age']}"
                " seconds old and may be incorrect for the current request parameters."
            )

        try:
            result = json.loads(response.content)
        except Exception as e:
            raise exceptions.ResponseParsingError(str(e)) from e

        return result

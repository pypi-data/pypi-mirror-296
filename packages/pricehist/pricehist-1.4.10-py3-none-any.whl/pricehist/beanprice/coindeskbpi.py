from pricehist import beanprice
from pricehist.sources.coindeskbpi import CoinDeskBPI

Source = beanprice.source(CoinDeskBPI())

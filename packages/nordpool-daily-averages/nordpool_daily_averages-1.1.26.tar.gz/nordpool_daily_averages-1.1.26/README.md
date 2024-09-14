
Python package for querying nordpool for average daily prices.
Prices can only be obtained for the current year and the previous year.
Incremet is how much you need to add to the price if you chargeback someone per kWh. It's optional and the default is zero

| Supported areacode's | Suported currency's | Increment |
| -------------------- | ------------------- | --------- |
| `"SE1"`              | `"SEK"`             | `"0.15"`  |
| `"SE2"`              | `"EUR"`             |
| `"SE3"`              |
| `"SE4"`              |
| `"NO1"`              |
| `"NO2"`              |
| `"NO3"`              |
| `"NO4"`              |
| `"NO5"`              |
| `"FI"`               |
| `"DK1"`              |
| `"DK2"`              |


| Environment variables | Usage                | Required | Syntax | Comment                      |
| --------------------- | -------------------- | -------- | ------ | ---------------------------- |
| LOGLEVEL              | stdout logging level | No       | DEBUG  | Defaults to INFO if not used |


## Usage:  
`pip install nordpool-daily-averages`  

~~~python
#Getting average price for 2024-08-30, for areacode SE3 and in Euro and 15 cents is added to the prices  
from nordpool import Nordpool as np
#instantiate class
price = np.Daily("SE3", "EUR", "0.15")
#Get the price
price.get_prices_for_one_date("2024-08-30")
~~~

~~~python
#Getting average price for 2024-08-29 for areacode SE3 in SEK and 15 öre is added to the prices  
from nordpool import Nordpools as np
#instantiate class
price = np.Daily("SE3", "SEK", "0.15")
#Get the price
price.get_prices_for_one_date("2024-08-29")
~~~

~~~python
#Getting average price for 2024-08-28 for areacode SE2 in SEK and no increment is added to the prices  
from nordpool import Nordpool as np
#instantiate class
price = np.Daily("SE2", "SEK")
#Get the price
price.get_prices_for_one_date("2024-08-28")
~~~

~~~python
#Getting all price's for current year and last year for areacode SE2 in SEK and no increment is added to the prices  
from nordpool import Nordpool as np
#instantiate class
price = np.Daily("SE2", "SEK")
#Get all price's
price.get_all_prices()
~~~

~~~python
import asyncio
from nordpool import Nordpool as np
#Getting hourly data prices for one date
async def main():
    #instantiate class
    daily_average = np.Hourly(areacode="SE3", currency="SEK")
    usage = await daily_average.get_hourly_prices("2024-09-04")
    print(usage)
asyncio.run(main())
~~~


### Alpha Research Online APIs

#### US Treasuries hub hosted on RapidAPI 
https://rapidapi.com/mikekipnis/api/us-treasuries

US Treasuries Online is an informational portal for risk management and pricing of U.S. Treasury securities. It allows users to explore publicly available historical key rates across different Treasury tenors, construct yield curves, estimate rates for other tenors, derive zero-coupon and discount curves, and reprice outstanding U.S. Treasury notes using the generated curve.

[us_treasuries_online.py](us_treasuries_online/us_treasuries_online.py)

#### End points
* /key_rates/ - The latest Market Yields on U.S. Treasury Securities at Constant Maturity, Quoted on an Investment Basis.
* /key_rates/ - Market Yield on U.S. Treasury Securities at Constant Maturity, Quoted on an Investment Basis for the specified date range
* /instruments/ - Outstanding notes and bonds
* /curve_price_request/ - Submit pricing request
* /curve_price_results/ - Get pricing results



#### Volatility hub hosted on RapidAPI
https://rapidapi.com/mikekipnis/api/volatlityhub

Volatility Hub delivers reliable implied volatility data for a curated set of stocks via a simple API, including smiles, and surface-level metrics.

[volatility_hub.py](volatility_hub/volatility_hub.py)

#### End points
* /vol_snapshot/ - This endpoint returns the complete snapshot required for option pricing, including underlying prices, dividends, risk-free rates, and volatilities.
* /volatility/ - This endpoint returns volatility data for the specified symbol. By default, it provides the latest volatility data, but users can specify start_date and end_date to retrieve data for a specific date range.
* /underlying_symbols/ - This endpoint retrieves a list of securities for which volatility data is available.



#### Stock Ownership Intel API hosted on RapidAPI
https://rapidapi.com/mikekipnis/api/stock-ownership-intel

Stock Ownership Intel is an API that provides research insights derived from SEC Form 13F filings, enabling analysis of institutional equity holdings and ownership trends.

[stock_ownership_intel.py](stock_ownership_intel/stock_ownership_intel.py)

* /security_info/ - Returns the information for the specified security.
* /industry_values/ - Returns the market values for every industry within the sector.
* /sector_values/ - Returns the market values for every sector
* /securities/ - Lists all SEC 13F–reportable securities, including their industry and sector classifications.
* /institutions/ - Lists all institutional investment managers that file SEC Form 13F reports.
* /filing_dates/ - Returns all available SEC Form 13F reporting dates.
* /holdings_for_institution/ - Returns the equity holdings disclosed by a specific institutional investment manager in its SEC Form 13F filings, providing a quarterly snapshot of the institution’s reported portfolio.
* /holders_of_security/ - Retrieves a list of institutional investment managers that have reported holdings of a specified security in their SEC Form 13F filings. Each institution entry includes details such as the filing manager, reported position size, and market value for the security.
* /holdings_for_institution_and_sector/ - Equity holdings reported in SEC Form 13F filings for a specific institutional manager, limited to companies classified within a given sector.
* /holdings_for_institution_and_industry/ - Equity holdings reported in SEC Form 13F filings for a specific institutional manager, limited to companies classified within a given industry.

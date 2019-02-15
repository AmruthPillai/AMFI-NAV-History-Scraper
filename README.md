# AMFI NAV History Scraper

This Python scraper is developed to parse information from AMFI (Association of Mutual Funds in India)'s NAV History Source to get a time-series dataset of all mutual fund schemes and store their NAV and associated information into a NoSQL database.

## What does it do?

It processes the following information from this URL: http://portal.amfiindia.com/DownloadNAVHistoryReport_Po.aspx?mf=3&frmdt=01-Feb-2019&todt=15-Feb-2019
```
Scheme Code;Scheme Name;ISIN Div Payout/ISIN Growth;ISIN Div Reinvestment;Net Asset Value;Repurchase Price;Sale Price;Date

Open Ended Schemes ( Equity Scheme - Multi Cap Fund )

Aditya Birla Sun Life Mutual Fund
120565;Aditya Birla Sun Life Equity Fund - Dividend - Direct Plan;INF209KA1LE0;INF209K01XY9;117.48;;;01-Feb-2019
120565;Aditya Birla Sun Life Equity Fund - Dividend - Direct Plan;INF209KA1LE0;INF209K01XY9;116.84;;;04-Feb-2019
120565;Aditya Birla Sun Life Equity Fund - Dividend - Direct Plan;INF209KA1LE0;INF209K01XY9;116.84;;;05-Feb-2019
120565;Aditya Birla Sun Life Equity Fund - Dividend - Direct Plan;INF209KA1LE0;INF209K01XY9;118.04;;;06-Feb-2019
120565;Aditya Birla Sun Life Equity Fund - Dividend - Direct Plan;INF209KA1LE0;INF209K01XY9;118.53;;;07-Feb-2019
120565;Aditya Birla Sun Life Equity Fund - Dividend - Direct Plan;INF209KA1LE0;INF209K01XY9;117.11;;;08-Feb-2019
...
```

and stores it into the MongoDB Collection in this format:
```
{"_id":"5c66aec0fad58f09079ea1d2","amc_code":39,"amc_name":"ABN AMRO Mutual Fund","scheme_code":102652,"scheme_name":"ABN AMRO  Monthly Income Plan-Regular Plan-Growth Option","isin":"","nav":11.7436,"timestamp":"2006-04-03T00:00:00.000Z"}
{"_id":"5c66aec0fad58f09079ea1d3","amc_code":39,"amc_name":"ABN AMRO Mutual Fund","scheme_code":102652,"scheme_name":"ABN AMRO  Monthly Income Plan-Regular Plan-Growth Option","isin":"","nav":11.738,"timestamp":"2006-04-04T00:00:00.000Z"}
{"_id":"5c66aec0fad58f09079ea1d4","amc_code":39,"amc_name":"ABN AMRO Mutual Fund","scheme_code":102652,"scheme_name":"ABN AMRO  Monthly Income Plan-Regular Plan-Growth Option","isin":"","nav":11.7663,"timestamp":"2006-04-05T00:00:00.000Z"}
{"_id":"5c66aec0fad58f09079ea1d5","amc_code":39,"amc_name":"ABN AMRO Mutual Fund","scheme_code":102652,"scheme_name":"ABN AMRO  Monthly Income Plan-Regular Plan-Growth Option","isin":"","nav":11.7392,"timestamp":"2006-04-07T00:00:00.000Z"}
...
```

## How do I use it?
Use `python3` to install the requirements, by running `pip install -r requirements.txt`. Make sure you have a running instance of `mongod` or have changed the database connection data. Then, run `script.py` and watch the magic unfold.

# tOtHemOoN-AI

### requirements
```bash
pip install -r requirements.txt
```

### GET Coin Data from UPBIT([https://github.com/sharebook-kr/pyupbit](https://github.com/sharebook-kr/pyupbit))

```bash
python data_parsing.py --ticker KRW-BTC --interval minute10
```

- you can check parsing options  `ticker_list.txt` and `interval_list.txt` in ./parsing_option
- If you use 'minute interval', we divide the data into 'day' and if you use 'year interval', we divide the data into 'year'
- I give delay 0.25 sec when get data from UPBIT webserver becasue if i request over 200 data, UPBIT webserver return 200 data every 0.1 sec
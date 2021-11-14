# tOtHemOoN-AI

### Environments

- Window10
- Anaconda
- Tensorflow

### Requirements

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

# 🎉Getting Start

### 🏃‍♂️Training

### Use .csv data

```bash
python training.py --data=./data --save_path=./checkpoints
```

- data structure

```
data
┣2017_09
	┣2017-09-26.csv
	┣2017-09-27.csv
	...
	┗2017-09-30.csv
┣2017_10
...
┣2021_10
┗2021_11
```

### Use upbit API

```bash
python training.py --ticker='KRW-BTC' --interval='minute10' --to='2021-11-11 23:11' --count 1000
```

- `ticker` :  Which coin do you want to use in training. Default is **KRW-BTC.**
- `interval` : Which time interval do you use. Reference is `interval_list.txt`. Default is **minute10.**
- `to` : Which date do you want to start counting the data. Default is **current time.**  
ex) to=2021-11-11 11:13 & count=2 → get 2021-11-11 11:00 and 2021-11-11 11:11
- `count` : How many data do you want to download from upbit. Default is **1000.**

### 🎯Inference

```bash
python inference.py --weight=./checkpoints/checkpointer.ckpt
```
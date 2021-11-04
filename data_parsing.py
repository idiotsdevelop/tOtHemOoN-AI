import pyupbit
import os
from tqdm import tqdm
import time
import datetime
import argparse

def calc_count(interval) :
    interval_count_min = \
        {
            'minute1': 1440,
            'minute3': 480,
            'minute5': 288,
            'minute10': 144,
            'minute15': 96,
            'minute30': 48,
            'minute60': 24,
            'minute240': 6
        }
    interval_count_year = \
        {
            'day': 365,
            'week': 52,
            'month': 12
        }

    if interval in interval_count_min :
        count = interval_count_min[interval]
        interval_term = 'min'
    else :
        count = interval_count_year[interval]
        interval_term = 'year'

    return count, interval_term


def calc_last_day(year, month):
    next_month = datetime.date(int(year), month, 1).replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def int_to_str(num) :
    if len(str(num)) < 2:
        num = "0" + str(num)
    else:
        num = str(num)

    return num


def coin_data(ticker, interval, count, date_y, date_m='01', date_d='01'):
    time.sleep(0.25)

    to = f'{date_y}-{date_m}-{date_d} 00:00'
    df = pyupbit.get_ohlcv(ticker=ticker, interval=interval, to=to, count=count)

    try:
        save_path = "./data/" + str(date_y) + "_" + date_m
        save_name = to.split(' ')[0]
        os.makedirs(save_path, exist_ok=True)
        df.to_csv(save_path + '/' + str(save_name) + '.csv')

    except:
        print("None data : ", to)


def minutes_interval(ticker, interval, count, years) :
    over = False
    for year in years:
        print("current year : " + year)
        start_month = 10 if year == '2017' else 1

        for month in tqdm(range(start_month, 13)):
            last_day = calc_last_day(year, month)
            month = int_to_str(month)

            for day in range(1, last_day.day + 1):
                day = int_to_str(day)

                if str(datetime.date.today()) == f'{year}-{month}-{day}':
                    over = True
                    break

                coin_data(ticker, interval, count, year, date_m=month, date_d=day)

            if over == True:
                break

def year_interval(ticker, interval, count, years) :
    for year in years :
        print("current year : " + year)
        coin_data(ticker, interval, count, year)


if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument('--ticker', type=str, required=True,
                        help='name of coin')
    parser.add_argument('--interval', type=str, required=True,
                        help='interval')

    args = parser.parse_args()


    ticker = args.ticker
    interval = args.interval
    count, interval_term = calc_count(interval)

    current_year = datetime.datetime.today().year
    years = [str(year) for year in range(2017, current_year + 1)]

    if interval_term == 'min' :
        minutes_interval(ticker, interval, count, years)

    else :
        year_interval(ticker, interval, count, years)

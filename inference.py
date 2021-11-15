import models
import dataset

import pyupbit
import pandas as pd
import datetime
import argparse

def current_time():
    now = datetime.datetime.now()
    return now


def comming_10m(current_t):
    remainder_min = 10 - current_t.minute % 10
    coming_10m = current_t + datetime.timedelta(minutes=int(remainder_min))
    return coming_10m


def latest_data(ticker, coming_10m):
    interval = 'minute10'
    to = coming_10m
    count = 1

    latest_data = pyupbit.get_ohlcv(ticker=ticker, interval=interval, to=to, count=count)
    return latest_data


def add_data(processed_data, latest_data) :
    processed_data.data, processed_data.label, processed_data.dataset = processed_data.preprocess(latest_data, latest=True)


def calc_UpDown(pred):
    rate_pred = pred[-1] / pred[-2]
    # print("이전 종가 : ", pred[-2])
    # print("현재 예측 종가 : ", pred[-1])
    # print("비율 : ", rate_pred)

    if rate_pred < 1:
        # Down
        return 0
    else:
        # Up
        return 1

def inference(lstm_model, processed_data, window_size, batch_size):
    dataset = processed_data.windowed_dataset(processed_data.data, processed_data.label, window_size, batch_size)
    pred = lstm_model.predict(dataset)
    pred = pred[:, 0]

    return pred


if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument('--weight', type=str, default='./checkpoints/ckeckpointer.ckpt',
                        help='model load')
    parser.add_argument('--ticker', type=str, default='KRW-BTC',
                        help='which coin do you use')
    parser.add_argument('--interval', type=str, default='minute10',
                        help='which time interval do you use')
    parser.add_argument('--to', type=str, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                        help='which date do you want to start downloading from upbit')
    parser.add_argument('--count', type=int, default=1000,
                        help='How many data do you want to download from upbit')

    args = parser.parse_args()

    WINDOW_SIZE = 6
    FEATURES = 6
    BATCH_SIZE = 1

    print("==== Build MODEL ====")
    init_model = models.Custom_Model((WINDOW_SIZE,FEATURES), args)
    model = init_model.model
    model = init_model.load_model(args.weight)


    print("==== Data Parsing ====")
    processed_data = dataset.Data_preprocess(args)

    # ## 다음 10분 체크 및 해당 시간대 데이터 가져오기.
    # latest_dataset = latest_data(ticker, comming_10m(to))
    # add_data(processed_data, latest_data)

    print("==== Inference ====")
    pred = inference(model, processed_data, WINDOW_SIZE, BATCH_SIZE)

    print("==== Make a Decision ====")
    answer = calc_UpDown(pred)

    if  answer == 0 :
        print("Down")
    elif answer == 1 :
        print("Up")

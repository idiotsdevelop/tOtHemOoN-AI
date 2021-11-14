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
    _, _, _ = processed_data.preprocess(latest_data, latest=True)


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

    args = parser.parse_args()

    WINDOW_SIZE = 6
    FEATURES = 6
    BATCH_SIZE = 1

    init_model = models.Custom_Model((WINDOW_SIZE,FEATURES), args)
    model = init_model.model
    model = init_model.load_model(args.weight)

    ticker = 'KRW-BTC'
    interval = 'minute10'
    to = f'2021-11-14 18:10'# str(current_time())
    count = 1000

    print("\n\nParsing Data 1000EA \n\n")
    processed_data = dataset.Data_preprocess(ticker, interval, to, count)

    # ## 다음 10분 체크 및 해당 시간대 데이터 가져오기.
    # latest_dataset = latest_data(ticker, comming_10m(to))
    # add_data(processed_data, latest_data)

    print("\n\nInference\n\n")
    pred = inference(model, processed_data, WINDOW_SIZE, BATCH_SIZE)

    print("\n\nMake a Decision\n\n")
    answer = calc_UpDown(pred)

    if  answer == 0 :
        print("Down")
    elif answer == 1 :
        print("Up")

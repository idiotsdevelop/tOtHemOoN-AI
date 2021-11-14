import tensorflow as tf
import pandas as pd
import numpy as np
import pyupbit
from sklearn.preprocessing import MinMaxScaler

import os
from glob import glob
from tqdm import tqdm

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split



class Data_preprocess():
    def __init__(self, args):
        if args.data is None :
            print(args)
            self.data, self.label, self.dataset = self.preprocess(
                pyupbit.get_ohlcv(ticker=args.ticker, interval=args.interval, to=args.to, count=args.count))
        else :
            self.data, self.label, self.dataset = self.csv_parsing(args.data)

    def MinMax(self, dataset_df):
        norm = MinMaxScaler()
        norm_dataset = norm.fit_transform(dataset_df)
        return pd.DataFrame(norm_dataset, columns=list(dataset_df.columns))

    def add_after10(self, dataset_df):
        after10 = np.zeros_like(self.norm_dataset['close'])
        for i in range(len(dataset_df['close']) - 1):
            after10[i] = dataset_df['close'][i + 1]
        return after10

    def drop_feature(self, dataset_df):
        # index(시간) 제거
        dataset_df = dataset_df.reset_index(drop=True)
        # value 제거
        dataset_df = dataset_df.drop(columns=['value'])
        return dataset_df

    def add_avgPrice(self, dataset_df):
        return (dataset_df['high'] + dataset_df['low'] +
                dataset_df['open'] + dataset_df['close']) // 4

    def preprocess(self, dataset, latest=False):

        # drop feature
        dataset_df = self.drop_feature(dataset)

        # avg_price 추가
        dataset_df['avg_price'] = self.add_avgPrice(dataset_df)

        if latest == True:
            # 가장 예전 데이터 삭제 - norm이랑 original 둘 다 적용
            self.dataset = self.dataset.drop([self.dataset.index[0]]).drop(columns=['after10'])
            self.norm_dataset = self.norm_dataset.drop([self.norm_dataset.index[0]])

            # ori dataset에 추가
            self.dataset = pd.concat([self.dataset, dataset_df])
            self.dataset = self.dataset.reset_index(drop=True)

            # min max 정규화 (MinMaxScaler) 적용
            self.norm_dataset = self.MinMax(self.dataset)

            # after10 추가
            self.dataset['after10'] = self.add_after10(self.dataset)


        else:
            # min max 정규화 (MinMaxScaler) 적용
            self.norm_dataset = self.MinMax(dataset_df)

            # after10 추가
            dataset_df['after10'] = self.add_after10(dataset_df)

        # 예측될 값(label)인 10분 후 가격
        self.norm_dataset['after10'] = self.add_after10(self.norm_dataset)

        return self.norm_dataset.drop(columns=['after10']), self.norm_dataset['after10'], dataset_df

    def csv_parsing(self, data_path):
        merge_df = pd.DataFrame()
        data_folders = glob(os.path.join(data_path, '*'))

        for data_folder in tqdm(data_folders):
            data_csvs = glob(os.path.join(data_folder,'*.csv'))

            for data_csv in data_csvs :
                csv_df = pd.read_csv(data_csv).drop(columns=["Unnamed: 0"])
                merge_df = pd.concat([merge_df, csv_df], ignore_index=True)

        return self.preprocess(merge_df)


    # dataset에 window 적용
    def windowed_dataset(self, data, label, window_size, batch_size):
        sliced_data = tf.data.Dataset.from_tensor_slices(data)
        sliced_data = sliced_data.window(window_size, shift=1, stride=1, drop_remainder=True)
        sliced_data = sliced_data.flat_map(lambda x: x.batch(window_size))

        sliced_label = tf.data.Dataset.from_tensor_slices(label[window_size:])

        sliced_dataset = tf.data.Dataset.zip((sliced_data, sliced_label))

        return sliced_dataset.batch(batch_size).prefetch(1)




import models
import dataset
from glob import glob
import argparse
import datetime
import os

from sklearn.model_selection import train_test_split
import numpy as np


def train(model, train_data, val_data, callbacks) :

    model.fit(train_data,
            validation_data=(val_data),
            epochs=150,
            callbacks=callbacks)



if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default=None,
                        help='data path')
    parser.add_argument('--ticker', type=str, default='KRW-BTC',
                        help='which coin do you use')
    parser.add_argument('--interval', type=str, default='minute10',
                        help='which time interval do you use')
    parser.add_argument('--to', type=str, default=datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
                        help='which date do you want to start downloading from upbit')
    parser.add_argument('--count', type=int, default=1000,
                        help='How many data do you want to download from upbit')

    parser.add_argument('--save_path', type=str, default='./checkpoints',
                        help='path that will be saved the training checkpoint')
    parser.add_argument('--val_size', type=int, default=0.1,
                        help='rate of validation set ')
    parser.add_argument('--lr', type=int, default=0.0001,
                        help='learning rate for training')
    parser.add_argument('--epoch', type=int, default=150,
                        help='epoch for for training')
    parser.add_argument('--batch', type=int, default=32,
                        help='batch size for training')
    parser.add_argument('--early_stop', type=int, default=10,
                        help='patience for early stopping')
    parser.add_argument('--weight', type=str, default=None,
                        help='model load')

    args = parser.parse_args()

    os.makedirs(args.save_path, exist_ok=True)

    WINDOW_SIZE = 6
    FEATURES = 6

    print("==== Build MODEL ====")
    init_model = models.Custom_Model((WINDOW_SIZE,FEATURES), args)
    model = init_model.model
    model = init_model.compile_model(model)
    callbacks = init_model.callback()

    print("==== Data Parsing ====")
    processed_data = dataset.Data_preprocess(args)

    train_data, val_data, train_label, val_label = train_test_split(
        processed_data.data,
        processed_data.label,
        test_size=0.1,
        random_state=0,
        shuffle=False)

    train_dataset = processed_data.windowed_dataset(train_data, train_label ,WINDOW_SIZE, args.batch)
    validation_dataset = processed_data.windowed_dataset(val_data, val_label ,WINDOW_SIZE, args.batch)

    print("==== Start Training ====")
    train(model, train_dataset, validation_dataset, callbacks)


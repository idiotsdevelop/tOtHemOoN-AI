import models
import dataset
from glob import glob
import argparse
from sklearn.model_selection import train_test_split
import numpy as np


def train(model, train_data, val_data, callbacks) :

    model.fit(train_data,
            validation_data=(val_data),
            epochs=150,
            callbacks=callbacks)



if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, required=True,
                        help='data path')
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

    WINDOW_SIZE = 6
    FEATURES = 6

    init_model = models.Custom_Model((WINDOW_SIZE,FEATURES), args)
    model = init_model.model
    model = init_model.compile_model(model)

    callbacks = init_model.callback()

    ticker = 'KRW-BTC'
    interval = 'minute10'
    to = f'2021-11-10 00:10'
    count = 1000

    processed_data =  dataset.Data_preprocess(ticker, interval, to, count)

    train_data, train_label, val_data, val_label = train_test_split(
        processed_data.data,
        processed_data.label,
        test_size=0.1,
        random_state=0,
        shuffle=False)

    train_dataset = processed_data.windowed_dataset(train_data, train_label ,WINDOW_SIZE, FEATURES)
    validation_dataset = processed_data.windowed_dataset(val_data, val_label ,WINDOW_SIZE, FEATURES)


    train(model, train_data, validation_dataset, callbacks)


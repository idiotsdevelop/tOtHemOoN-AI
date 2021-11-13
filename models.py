import os

import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, LSTM, Conv1D, Lambda, Input, GlobalAveragePooling1D
from tensorflow.keras.losses import Huber
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


class Custom_Model():
    def __init__(self, input_shape, args):
        self.args = args
        self.model = self.build_model(input_shape)


    def build_model(self, input_shape: tuple):
        input = Input(shape=input_shape)
        x = LSTM(128, return_sequences=True, activation='tanh', dropout=0.2)(input)
        x = LSTM(64, return_sequences=True, activation='tanh', dropout=0.2)(x)
        x = LSTM(32, return_sequences=True, activation='tanh', dropout=0.2)(x)
        x = GlobalAveragePooling1D()(x)
        output = Dense(1)(x)
        return Model(input, output)


    def compile_model(self, model):
        loss = Huber()
        optimizer = Adam(lr=self.args.lr)

        model.compile(loss=loss, optimizer=optimizer, metrics=['mse'])
        return model


    def callback(self):
        saveCheckpoint = ModelCheckpoint(os.path.join(self.args.save_path, 'checkpoint.ckpt'),
                                    save_weights_only=False,
                                    save_best_only=True,
                                    monitor='val_loss',
                                    verbose=1)
        earlyStopping = EarlyStopping(monitor='val_loss',
                                      patience=self.args.early_stop)
        return [saveCheckpoint, earlyStopping]


    def load_model(self, weight):
        self.model.load_weights(weight)
        return self.model

import pyupbit
import os
from tqdm import tqdm
from glob import glob
import time
import datetime
import argparse

class DataParser():
    def __init__(self, data_path):
        self.data_path = data_path

    def csv2df(self):
        data_folder = glob(self.data_path)




if __name__ == '__main__' :

    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, required=True,
                        help='name of coin')
    parser.add_argument('--ckpt', type=str, default='./checkpoints',
                        help='interval')

    args = parser.parse_args()




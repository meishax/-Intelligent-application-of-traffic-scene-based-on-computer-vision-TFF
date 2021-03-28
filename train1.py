import sys
import warnings
import argparse
import numpy as np
import pandas as pd
from dataProcess import process_data
from modle import get_lstm
from keras.models import Model
from keras.callbacks import EarlyStopping
warnings.filterwarnings("ignore")


def train_model(model, X_train, y_train, name, config):
    model.compile(loss="mse", optimizer="rmsprop", metrics=['mape'])
    # early = EarlyStopping(monitor='val_loss', patience=30, verbose=0, mode='auto')
    hist = model.fit(
        X_train, y_train,
        batch_size=config["batch"],
        epochs=config["epochs"],
        validation_split=0.05)

    model.save('model/' + name + '.h5')
    df = pd.DataFrame.from_dict(hist.history)
    df.to_csv('model/' + name + ' loss.csv', encoding='utf-8', index=False)


def train(trainFile,testFile,model_unit,lag=6,batch=16,epochs=50,bit=1,validaton=0.1,set='test_file'):
    config = {"batch": batch, "epochs": epochs}
    file1 = trainFile
    file2 = testFile

    X_train, y_train, _, _, _ = process_data(file1, file2, lag,set,validaton,bit)

    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    m = get_lstm(model_unit)
    train_model(m, X_train, y_train, 'lstm', config)

if __name__ == '__main__':
    train(trainFile='data/inputfile_train.csv', testFile='data/inputfile_test.csv', model_unit=[6,64,64,1], lag=6, batch=16,epochs=2, bit=1, validaton=0.1, set='test_file')
import math
import json
import warnings
import pandas as pd
import numpy as np
import sklearn.metrics as metrics
warnings.filterwarnings("ignore")


def MAPE(y_true, y_pred):
    y = [x for x in y_true if x > 0]
    y_pred = [y_pred[i] for i in range(len(y_true)) if y_true[i] > 0]

    num = len(y_pred)
    sums = 0

    for i in range(num):
        tmp = abs(y[i] - y_pred[i]) / y[i]
        sums += tmp

    mape = sums * (100 / num)

    return mape


def indicate(y_pred, y_true):
    mape = MAPE(y_true, y_pred)
    vs = metrics.explained_variance_score(y_true, y_pred)
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)
    print('explained_variance_score:%f' % vs)
    print('mape:%f%%' % mape)
    print('mae:%f' % mae)
    print('mse:%f' % mse)
    print('rmse:%f' % math.sqrt(mse))
    print('r2:%f' % r2)
    return json.dumps({'mape':mape,'vs':vs,'mae':mae,'mse':mse,'r2':r2,'rmse':math.sqrt(mse)})

def getLossAndMAPE():
    file='model/lstm loss.csv'
    attr1='loss'
    attr2='mean_absolute_percentage_error'
    df = pd.read_csv(file, encoding='utf-8').fillna(0)
    loss_flow=df[attr1].values
    mape_flow=df[attr2].values
    loss_flow=np.array(loss_flow)
    mape_flow=np.array(mape_flow)
    return loss_flow,mape_flow

if __name__ == '__main__':
    getLossAndMAPE()

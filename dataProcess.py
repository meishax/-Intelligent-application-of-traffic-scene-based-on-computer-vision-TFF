import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import random

def process_data(train, test, lags,setchoose,t_per,t_bit):
    """
    train:训练集文件
    test:数据集文件
    lags:滑动窗口大小
    setchoose:train_file（从训练集中随机抽取验证集），test_file（测试集进行测试）
    t_per:从训练集中抽取验证集的比例
    t_bit:预测下bit时刻的流量
    """
    attr = 'flow_data'
    df1 = pd.read_csv(train, encoding='utf-8').fillna(0)
    df2 = pd.read_csv(test, encoding='utf-8').fillna(0)

    scaler = MinMaxScaler(feature_range=(0, 1)).fit(df1[attr].values.reshape(-1, 1))    #特征缩放器，数据缩放到（-1，1）
    flow1 = scaler.transform(df1[attr].values.reshape(-1, 1)).reshape(1, -1)[0]
    flow2 = scaler.transform(df2[attr].values.reshape(-1, 1)).reshape(1, -1)[0]

    train, test = [], []
    for i in range(lags, len(flow1)-1,t_bit):                                              #提取特征向量
        train.append(flow1[i - lags: i + t_bit])
    for i in range(lags, len(flow2)-1,t_bit):
        test.append(flow2[i - lags: i + t_bit])

    train = np.array(train)
    test = np.array(test)

    if setchoose=='train_file':
        bit=-t_bit
        test_len=int(len(flow1)*t_per)
        test_begin=np.random.randint(0,len(flow1)-test_len-1)
        X_test = train[test_begin:test_begin + test_len, :bit]
        y_test = train[test_begin:test_begin+test_len, bit:]
    elif setchoose=='test_file':
        bit=-t_bit
        X_test = train[:, :bit]
        y_test = train[:, bit:]

    np.random.shuffle(train)    #随机排序
    X_train = train[:, :bit]  # 取时间序列前lags-1位作为输入
    y_train = train[:, bit:]  # 取时间序列最后以为作为输出标签

    return X_train, y_train, X_test, y_test, scaler

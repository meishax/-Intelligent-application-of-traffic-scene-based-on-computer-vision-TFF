import warnings
import numpy as np
from dataProcess import process_data
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras.models import load_model
warnings.filterwarnings("ignore")

def predict(modelFile,trainFile,testFile,lag=6,bit=1,validaton=0.1,set='test_file'):
    lstm = load_model(modelFile)
    model = lstm

    file1 = trainFile
    file2 = testFile
    _, _, X_test, y_test, scaler = process_data(file1, file2,lags=lag,t_bit=bit,t_per=validaton,setchoose=set)

    y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]  # 缩放后数据缩放为原数据
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted = model.predict(X_test)
    predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]

    y_pred = predicted
    return y_pred,y_test

def pre1(modelFile,dataList,bit):
    lstm=load_model(modelFile)
    model=lstm

    dataList=np.array(dataList)
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(dataList.reshape(-1, 1))  # 特征缩放器，数据缩放到（-1，1）
    dataList = scaler.transform(dataList.reshape(-1, 1)).reshape(1, -1)[0]
    dataList=np.array(dataList)
    X_test = np.reshape(dataList, (1,dataList.shape[0],1))
    predicted = model.predict(X_test)
    predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]
    print(predicted)
    y_pred = predicted
    return y_pred

if __name__ == '__main__':
    predict('model/lstm.h5','data/inputfile_train.csv','data/inputfile_test.csv')
    #pre1('model/lstm.h5', [7, 2, 6, 7, 4, 7], 1)
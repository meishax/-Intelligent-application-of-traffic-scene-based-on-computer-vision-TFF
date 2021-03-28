from flask import *
from train1 import train
from predict1 import predict
from predict1 import pre1
from indicator import indicate
from indicator import getLossAndMAPE
import numpy as np
import pymysql
import dataOpt

app = Flask(__name__)

db=pymysql.connect("localhost", "root", "admin", "traffic_flow")
#cursor=db.cursor()
#cursor.execute("select * from sjb")
#data=cursor.fetchone()
#print(data)

'''全局变量'''
train_file_path=''
test_file_path=''
choose_set=''

'''训练参数'''
t_lag=6
t_batch=16
t_epochs=2
t_bit=1
t_validaton=0.1
t_model_unit=[6,64,64,1]

@app.route('/')
def menu():
    return render_template('menu.html')

@app.route('/train')
def url_train1(trainFile_path='nothing',testFile_path='nothing'):
    #file_path={'trainFile_path':'未选择','textFile_path':'未选择'}
    return render_template('train1.html')

@app.route('/predict')
def url_predict1():
    return render_template('predict1.html')

@app.route('/dataManager')
def data_mannager():
    return render_template('dataManager.html')

@app.route('/show')
def show():
    return render_template('show.html')
@app.route('/show_1')
def show_1():
    return render_template('show_1.html')
@app.route('/show_2')
def show_2():
    return render_template('show_2.html')
@app.route('/show_3')
def show_3():
    return render_template('show_3.html')

@app.route('/train1_sendFile',methods=['POST'])
def train1_sendFile():
    global train_file_path                             #修改全局变量前声明
    global test_file_path
    request_file=request.form.to_dict()
    train_file_path='data/'+request_file['train_file']
    test_file_path='data/'+request_file['test_file']
    return json.dumps({'trainFile_path':train_file_path,'testFile_path':test_file_path})

@app.route('/train1_train',methods=['POST'])
def train1_train():
    global t_model_unit                               #修改全局变量前声明
    global t_batch
    global t_epochs
    global t_validaton
    global t_bit
    global t_lag
    request_file=request.form.to_dict()
    t_batch=eval(request_file['batch'])
    t_epochs=eval(request_file['epochs'])
    t_bit=eval(request_file['bit'])
    t_lag=6
    choose_set='test_file'
    # choose_set=request_file['choose_set']
    #t_validaton=request_file['validaton']
    t_model_unit=[t_lag,64,64,1]                  #网络结构参数
    #train(trainFile=train_file_path,testFile=test_file_path,model_unit=t_model_unit,lag=6,batch=t_batch,epochs=t_epochs,bit=1,validaton=0.1,set=choose_set)         #训练模型
    train(trainFile=train_file_path,testFile=test_file_path,model_unit=[6, 64, 64, 1], lag=6,batch=16, epochs=t_epochs, bit=1, validaton=0.1, set='test_file')
    pre_list,y_list=predict('model/lstm.h5',trainFile=train_file_path,testFile=test_file_path)         #pre_list:预测序列，y_list真实序列
    ind=indicate(pre_list,y_list)
    loss,mape=getLossAndMAPE()
    return json.dumps({'predictList':pre_list.tolist(),'trueList':y_list.tolist(),'indicationList':ind,'loss':loss.tolist(),'mape':mape.tolist()})

@app.route('/predict_pre1',methods=['POST'])
def predict_pre1():
    model_file=request.form.get('modelFile')
    data_list=list(map(int, request.form.getlist("dataList[]")))
    bit=eval(request.form.get('bit'))
    pre=pre1('model/lstm.h5',data_list,bit)
    return json.dumps({'prelist':pre.tolist()})

@app.route('/dataManager_importData',methods=['POST'])
def dataManager_importData():
    request_file = request.form.to_dict()
    fpath = request_file['filePath']
    dataOpt.readCSV(fpath)
    print(1)
    return json.dumps({'list':1})

@app.route('/dataManager_deleteAllData',methods=['POST'])
def dataManager_deleteAllData():
    request_file = request.form.to_dict()
    fpath = request_file['opt']
    dataOpt.deleteAll()
    return json.dumps({'list':1})

@app.route('/dataManager_search',methods=['POST'])
def dataManager_search():
    request_file = request.form.to_dict()
    region = request_file['region']
    time=request_file['time']
    data=dataOpt.searchByRegionAndTime(region,time)
    return json.dumps({'datalist':list(data)})

@app.route('/chart2_load_byregion',methods=['POST'])
def chart2_load_byregion():
    request_file = request.form.to_dict()
    region = request_file['region']
    timelist,flowlist=dataOpt.chart2ReadByRegion(region)
    return json.dumps({'timelist':timelist,'flowlist':flowlist})

@app.route('/chart3_load_byregion',methods=['POST'])
def chart3_load_byregion():
    request_file = request.form.to_dict()
    region = request_file['region']
    daylist,hourlist,flowlist=dataOpt.chart3ReadByRegion(region)
    return json.dumps({'daylist':daylist,'hourlist':hourlist,'flowlist':flowlist})

@app.route('/chart4_load_byday',methods=['POST'])
def chart4_load_byday():
    request_file = request.form.to_dict()
    day = eval(request_file['day'])
    regionlist,hourlist,flowlist=dataOpt.chart4ReadByDay(day)
    return json.dumps({'regionlist':regionlist,'hourlist':hourlist,'flowlist':flowlist})

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

@app.route('/predict_pre2',methods=['POST'])
def predict_pre2():
    model_file=request.form.get('modelFile')
    data_list=list(map(int, request.form.getlist("dataList[]")))
    bit=eval(request.form.get('bit'))
    data_list=np.array(data_list)
    prelist=[]
    for i in range(48):
        print('%s/48'%i)
        flowlist=data_list[-6:]
        flowlist=list(flowlist)
        pre=pre1(model_file,flowlist,bit)
        prelist.append(pre[0])
        data_list=np.append(data_list,int(pre[0]))
    return json.dumps({'prelist':prelist},cls=MyEncoder)



if __name__ == '__main__':
    app.run(debug=False)

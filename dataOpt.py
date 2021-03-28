import numpy as np
import pandas as pd
import pymysql
db = pymysql.connect("localhost", "root", "admin", "traffic_flow")
cursor = db.cursor()

def writeToDb(attr,datalist):
    db.ping(reconnect=True)
    dlen=len(datalist[0])
    for i in range(dlen):
        time=datalist[0][i].strip('\'')
        region=datalist[1][i]
        flow=datalist[2][i]
        cursor.execute("INSERT INTO sjb(qybh,sj,llz) VALUES(%s,'%s',%s)" % ( region,pymysql.escape_string(time),flow ) )
        db.commit()
    db.close()
    return 1;

def readCSV(fpath):
    attr = ['time','region','flow_data']
    df = pd.read_csv(fpath, encoding='utf-8').fillna(0)
    time=df[attr[0]].values
    region= df[attr[1]].values
    flow=df[attr[2]].values
    datalist=[]
    datalist.append(time)
    datalist.append(region)
    datalist.append(flow)
    writeToDb(attr,datalist)
    return 1;

def chart2ReadByRegion(region):
    db.ping(reconnect=True)
    cursor.execute("SELECT sj,llz from sjb WHERE qybh=%s"%(region))
    data=cursor.fetchall()
    data=np.array(data)
    timelist=list(data[:,0])
    flowlist=list(data[:,1])
    flowlist=list(map(lambda x:eval(x),flowlist))
    db.close()
    return timelist,flowlist;

def chart3ReadByRegion(region):
    db.ping(reconnect=True)
    step=4 #步长，两小时一步，如果数据是每半小时一组，步长为4，如果数据是每10分钟一组，步长为20
    cursor.execute("SELECT sj,llz from sjb WHERE qybh=%s"%(region))
    data=cursor.fetchall()
    data=np.array(data)
    time=list(data[:,0])
    day=np.unique(list(map(lambda x:x.split(' ')[0],time)))
    hour = np.unique(list(map(lambda x: x.split(' ')[1], time)))
    flow=list(data[:,1])
    flow=list(map(lambda x:eval(x),flow))

    daylist=[]
    hourlist=[]
    flowlist=[]
    daylist=day
    for i in range(0,len(hour),step):
        hourlist.append(hour[i])
    for i in range(0,len(flow),step):
        flowSum=0
        for j in range(step):
            flowSum=flowSum+flow[i+j]
        flowlist.append(flowSum)
    db.close()
    return list(daylist),list(hourlist),list(flowlist);

def chart4ReadByDay(day):
    db.ping(reconnect=True)
    step = 4  # 步长，两小时一步，如果数据是每半小时一组，步长为4，如果数据是每10分钟一组，步长为20
    if day<10:
        day='2016-11-0'+str(day)
    else:
        day='2016-11-'+str(day)

    cursor.execute("SELECT qybh,sj,llz from sjb WHERE sj like '%%%s%%'"%(day))
    data=cursor.fetchall()
    data=np.array(data)
    region=list(data[:,0])
    region=list(map(lambda x:eval(x),region))
    time=list(data[:,1])
    flow=list(data[:,2])
    flow=list(map(lambda x:eval(x),flow))

    regionlist=[]
    hourlist=[]
    flowlist=[]
    hour = np.unique(list(map(lambda x: x.split(' ')[1], time)))
    for i in range(0,len(region),step*12):
        regionlist.append(region[i])
    for i in range(0, len(hour), step):
        hourlist.append(hour[i])
    for i in range(0, len(flow), step):
        flowSum = 0
        for j in range(step):
            flowSum = flowSum + flow[i + j]
        flowlist.append(flowSum)
    db.close()
    return list(regionlist),list(hourlist),list(flowlist);

def deleteAll():
    db.ping(reconnect=True)
    cursor.execute("delete from sjb")
    db.commit()
    db.close()
    return ;

def searchByRegionAndTime(region,time):
    db.ping(reconnect=True)
    if region!='':
        cursor.execute("SELECT qybh,sj,llz from sjb WHERE qybh='%s' and sj like '%%%s%%'" % (region,time))
        data = cursor.fetchall()
    elif region=='':
        cursor.execute("SELECT qybh,sj,llz from sjb WHERE sj like '%%%s%%'" % (time))
        data = cursor.fetchall()
    db.close()
    return data;

if __name__ == '__main__':
    searchByRegionAndTime('','2016-11-02')


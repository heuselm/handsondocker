from flask import Flask
from flask import render_template
import os
import socket
import sys
import matplotlib.pyplot as plt
sys.path.append('../models')
import stock
import numpy as np

app = Flask(__name__)

@app.route("/stock/<name>")
def hello(name):
    df1=stock.test(name)
    count = len(df1)
    traincount = int(count*0.75)
    std_avg_predictions,mse_errors,all_mid_data,train_data,test_data=stock.standardaverage(df1)
    print('MSE error for standard averaging: %.5f'%(0.5*np.mean(mse_errors)))
    mse=0.5*np.mean(mse_errors)
    plt.figure(figsize = (18,9))
    plt.plot(range(df1.shape[0]),all_mid_data,color='b',label='True')
    plt.plot(range(100,traincount),std_avg_predictions,color='orange',label='Prediction')
    plt.xticks(range(0,df1.shape[0],500),df1['Date'].loc[::500],rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Mid Price')
    plt.legend(fontsize=18)
    plt.savefig('./static/'+name+'.png')
    N = traincount
    run_avg_predictions, mse_errors1=stock.movingaverage(df1)

    print('MSE error for EMA averaging: %.5f'%(0.5*np.mean(mse_errors1)))
    mse1=0.5*np.mean(mse_errors1)
    plt.figure(figsize = (18,9))
    plt.plot(range(df1.shape[0]),all_mid_data,color='b',label='True')
    plt.plot(range(0,N),run_avg_predictions,color='orange', label='Prediction')
    plt.xticks(range(0,df1.shape[0],500),df1['Date'].loc[::500],rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Mid Price')
    plt.legend(fontsize=18)
    plt.savefig('./static/'+name+'1.png')
    return render_template('index.html', name = name, hostname=socket.gethostname(),url ='/static/'+name+'.png',url1='/static/'+name+'1.png',mse_errors1=mse1,mse_errors=mse)

if __name__ == "__main__":
    app.config["CACHE_TYPE"] = "null"
    
    app.run(host='0.0.0.0', port=8011)
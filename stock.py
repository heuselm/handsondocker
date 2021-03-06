#!/usr/bin/python3
# coding: utf-8

# In[ ]:


# Make sure that you have all these libaries available to run the code successfully
from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import urllib.request, json
import os
import numpy as np
import tensorflow as tf # This code has been tested with TensorFlow 1.6
from sklearn.preprocessing import MinMaxScaler

def test(data1):
    # In[ ]:


    data_source = 'alphavantage' # alphavantage or kaggle

    if data_source == 'alphavantage':
        # ====================== Loading Data from Alpha Vantage ==================================

        api_key = 'UX64ZSMDKVH8KB48'

        # American Airlines stock market prices
        ticker = data1

        # JSON file with all the stock market data for AAL from the last 20 years
        url_string = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=%s"%(ticker,api_key)

        # Save data to this file
        file_to_save = 'stock_market_data-%s.csv'%ticker

        # If you haven't already saved data,
        # Go ahead and grab the data from the url
        # And store date, low, high, volume, close, open values to a Pandas DataFrame
        if not os.path.exists(file_to_save):
            with urllib.request.urlopen(url_string) as url:
                data = json.loads(url.read().decode())
                # extract stock market data
                data = data['Time Series (Daily)']
                df = pd.DataFrame(columns=['Date','Low','High','Close','Open'])
                for k,v in data.items():
                    date = dt.datetime.strptime(k, '%Y-%m-%d')
                    data_row = [date.date(),float(v['3. low']),float(v['2. high']),
                                float(v['4. close']),float(v['1. open'])]
                    df.loc[-1,:] = data_row
                    df.index = df.index + 1
            print('Data saved to : %s'%file_to_save)        
            df.to_csv(file_to_save)

        # If the data is already there, just load it from the CSV
        else:
            print('File already exists. Loading data from CSV')
            df = pd.read_csv(file_to_save)


    # In[ ]:


    # Sort DataFrame by date
    df = df.sort_values('Date')



    # In[ ]:


   
    return df


def standardaverage(df1):
    count = len(df1)
    #print(count)
    traincount = int(count*0.75)
    wind=int(count*0.35)
    windsize=int(count*0.1)
    print(traincount)
    #plt.figure(figsize = (18,9))
    #plt.plot(range(df1.shape[0]),(df1['Low']+df1['High'])/2.0)
    #plt.xticks(range(0,df1.shape[0],500),df1['Date'].loc[::500],rotation=45)
    #plt.xlabel('Date',fontsize=18)
    #plt.ylabel('Mid Price',fontsize=18)
    #plt.show()
    high_prices = df1.loc[:,'High'].values
    low_prices = df1.loc[:,'Low'].values
    mid_prices = (high_prices+low_prices)/2.0
    #print(traincount)
    train_data = mid_prices[:traincount]
    test_data = mid_prices[traincount:]
    #print(len(test_data))
    # Scale the data to be between 0 and 1
    # When scaling remember! You normalize both test and train data with respect to training data
    # Because you are not supposed to have access to test data
    scaler = MinMaxScaler()
    train_data = train_data.reshape(-1,1)
    test_data = test_data.reshape(-1,1)
    # Train the Scaler with training data and smooth data
    smoothing_window_size = windsize
    for di in range(0,wind,smoothing_window_size):
            scaler.fit(train_data[di:di+smoothing_window_size,:])
            train_data[di:di+smoothing_window_size,:] = scaler.transform(train_data[di:di+smoothing_window_size,:])

    # You normalize the last bit of remaining data
    scaler.fit(train_data[di+smoothing_window_size:,:])
    train_data[di+smoothing_window_size:,:] = scaler.transform(train_data[di+smoothing_window_size:,:])
    # Reshape both train and test data
    train_data = train_data.reshape(-1)

    # Normalize test data
    test_data = scaler.transform(test_data).reshape(-1)
    # Now perform exponential moving average smoothing
    # So the data will have a smoother curve than the original ragged data
    #print(count)
    #plt.figure(figsize = (18,9))
    #plt.plot(range(df1.shape[0]),(df1['Low']+df1['High'])/2.0)
    #plt.xticks(range(0,df1.shape[0],500),df1['Date'].loc[::500],rotation=45)
    #plt.xlabel('Date',fontsize=18)
    #plt.ylabel('Mid Price',fontsize=18)
    #plt.show()
    high_prices = df1.loc[:,'High'].values
    low_prices = df1.loc[:,'Low'].values
    mid_prices = (high_prices+low_prices)/2.0
    print(traincount)
    train_data = mid_prices[:traincount]
    test_data = mid_prices[traincount:]
    print(len(test_data))
    # Scale the data to be between 0 and 1
    # When scaling remember! You normalize both test and train data with respect to training data
    # Because you are not supposed to have access to test data
    scaler = MinMaxScaler()
    train_data = train_data.reshape(-1,1)
    test_data = test_data.reshape(-1,1)
    # Train the Scaler with training data and smooth data
    smoothing_window_size = windsize
    for di in range(0,wind,smoothing_window_size):
        scaler.fit(train_data[di:di+smoothing_window_size,:])
        train_data[di:di+smoothing_window_size,:] = scaler.transform(train_data[di:di+smoothing_window_size,:])

    # You normalize the last bit of remaining data
    scaler.fit(train_data[di+smoothing_window_size:,:])
    train_data[di+smoothing_window_size:,:] = scaler.transform(train_data[di+smoothing_window_size:,:])
    # Reshape both train and test data
    train_data = train_data.reshape(-1)

    # Normalize test data
    test_data = scaler.transform(test_data).reshape(-1)
    # Now perform exponential moving average smoothing
    # So the data will have a smoother curve than the original ragged data
    EMA = 0.0
    gamma = 0.1
    for ti in range(traincount):
     EMA = gamma*train_data[ti] + (1-gamma)*EMA
     train_data[ti] = EMA

    # Used for visualization and test purposes
    all_mid_data = np.concatenate([train_data,test_data],axis=0)
    print(len(all_mid_data))
    window_size = 100
    N = train_data.size
    std_avg_predictions = []
    std_avg_x = []
    mse_errors = []

    for pred_idx in range(window_size,N):

        if pred_idx >= N:
            date = dt.datetime.strptime(k, '%Y-%m-%d').date() + dt.timedelta(days=1)
        else:
            date = df1.loc[pred_idx,'Date']

        std_avg_predictions.append(np.mean(train_data[pred_idx-window_size:pred_idx]))
        mse_errors.append((std_avg_predictions[-1]-train_data[pred_idx])**2)
        std_avg_x.append(date)
    return std_avg_predictions,mse_errors,all_mid_data,train_data,test_data
    
#std_avg_predictions,mse_errors,all_mid_data,train_data,test_data=standardaverage()
#print('MSE error for standard averaging: %.5f'%(0.5*np.mean(mse_errors)))
#plt.figure(figsize = (18,9))
#plt.plot(range(df1.shape[0]),all_mid_data,color='b',label='True')
#plt.plot(range(100,traincount),std_avg_predictions,color='orange',label='Prediction')
#plt.xticks(range(0,df1.shape[0],500),df1['Date'].loc[::500],rotation=45)
#plt.xlabel('Date')
#plt.ylabel('Mid Price')
#plt.legend(fontsize=18)
#plt.savefig('new_plot.png')
def movingaverage(df1):
   count = len(df1)
   #print(count)
   traincount = int(count*0.75)
   wind=int(count*0.35)
   windsize=int(count*0.1)
   print(traincount)
   #plt.figure(figsize = (18,9))
   #plt.plot(range(df1.shape[0]),(df1['Low']+df1['High'])/2.0)
   #plt.xticks(range(0,df1.shape[0],500),df1['Date'].loc[::500],rotation=45)
   #plt.xlabel('Date',fontsize=18)
   #plt.ylabel('Mid Price',fontsize=18)
   #plt.show()
   high_prices = df1.loc[:,'High'].values
   low_prices = df1.loc[:,'Low'].values
   mid_prices = (high_prices+low_prices)/2.0
   #print(traincount)
   train_data = mid_prices[:traincount]
   test_data = mid_prices[traincount:]
   #print(len(test_data))
   # Scale the data to be between 0 and 1
   # When scaling remember! You normalize both test and train data with respect to training data
   # Because you are not supposed to have access to test data
   scaler = MinMaxScaler()
   train_data = train_data.reshape(-1,1)
   test_data = test_data.reshape(-1,1)
   # Train the Scaler with training data and smooth data
   smoothing_window_size = windsize
   for di in range(0,wind,smoothing_window_size):
            scaler.fit(train_data[di:di+smoothing_window_size,:])
            train_data[di:di+smoothing_window_size,:] = scaler.transform(train_data[di:di+smoothing_window_size,:])

   # You normalize the last bit of remaining data
   scaler.fit(train_data[di+smoothing_window_size:,:])
   train_data[di+smoothing_window_size:,:] = scaler.transform(train_data[di+smoothing_window_size:,:])
   # Reshape both train and test data
   train_data = train_data.reshape(-1)

   # Normalize test data
   test_data = scaler.transform(test_data).reshape(-1)
   # Now perform exponential moving average smoothing
   # So the data will have a smoother curve than the original ragged data
   #print(count)
   window_size = 100
   N = train_data.size
   run_avg_predictions = []
   run_avg_x = []
   mse_errors = []
   running_mean = 0.0
   run_avg_predictions.append(running_mean)
   decay = 0.5
   for pred_idx in range(1,N):

    running_mean = running_mean*decay + (1.0-decay)*train_data[pred_idx-1]
    run_avg_predictions.append(running_mean)
    mse_errors.append((run_avg_predictions[-1]-train_data[pred_idx])**2)
    #run_avg_x.append(date)
  
   return run_avg_predictions, mse_errors
#N = train_data.size
#run_avg_predictions, mse_errors=movingaverage()

#print('MSE error for EMA averaging: %.5f'%(0.5*np.mean(mse_errors)))
#plt.figure(figsize = (18,9))
#plt.plot(range(df1.shape[0]),all_mid_data,color='b',label='True')
#plt.plot(range(0,N),run_avg_predictions,color='orange', label='Prediction')
#plt.xticks(range(0,df1.shape[0],500),df1['Date'].loc[::500],rotation=45)
#plt.xlabel('Date')
#plt.ylabel('Mid Price')
#plt.legend(fontsize=18)
#plt.savefig('new_plot1.png')
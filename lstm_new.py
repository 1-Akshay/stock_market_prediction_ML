# -*- coding: utf-8 -*-
"""LSTM new.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vfCbFSYIOrcTSfchTs4h2TE5y0RQNOjF
"""

import yfinance
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import MinMaxScaler

start = '2000-01-01'
end = '2022-12-31'
ticker = 'AAPL'

df = yfinance.download(ticker, start, end)
print(df.head())
print(df.tail())

plt.figure(figsize=(15, 8))
plt.title('Stock Prices History')
plt.plot(df['Close'])
plt.xlabel('Date')
plt.ylabel('Prices ($)')

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.80)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.80):int(len(df))])

scaler = MinMaxScaler(feature_range=(0,1))
data_training_array = scaler.fit_transform(data_training)

x_train = []
y_train = []

for i in range(60, data_training_array.shape[0]):
    x_train.append(data_training_array[i-60:i])
    y_train.append(data_training_array[i,0])

x_train , y_train = np.array(x_train) , np.array(y_train)

past_60_days = data_training.tail(60)
final_df= past_60_days.append(data_testing,ignore_index=True)

input_data= scaler.fit_transform(final_df)

x_test=[]
y_test=[]

for i in range(60,input_data.shape[0]):
    x_test.append(input_data[i-60:i])
    y_test.append(input_data[i,0])

x_test , y_test = np.array(x_test) , np.array(y_test)

model = keras.Sequential()
model.add(layers.LSTM(100, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(layers.LSTM(100, return_sequences=False))
model.add(layers.Dense(25))
model.add(layers.Dense(1))
model.summary()

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, batch_size= 1, epochs=3)

y_predicted = model.predict(x_test)

y_predicted=scaler.inverse_transform(y_predicted)
y_test=y_test.reshape(-1,1)
y_test=scaler.inverse_transform(y_test)

fig2 = plt.figure(figsize=(12,8))
# plt.plot(ff,'b',label='CLosing')
plt.plot(y_test , 'r', label='OG price')
plt.plot(y_predicted , 'b', label='Predicted price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()

# last_60_days=df.Close[-60:]
# last_60_days=pd.DataFrame(last_60_days)

# last_60_days_scaled=scaler.transform(last_60_days)

# x_test=[]

# x_test.append(last_60_days_scaled)
# x_test=np.array(x_test)

# x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

# pred_price=model.predict(x_test)
# model.reset_states()

# pred_price=scaler.inverse_transform(pred_price)

n_steps=60
pred_days=30
x_input=input_data[len(input_data)-n_steps:].reshape(1,-1)
x_input.shape
temp_input=list(x_input)
temp_input=temp_input[0].tolist()

# demonstrate prediction for next N days
from numpy import array

lst_output=[]

i=0
while(i<pred_days):

    if(len(temp_input)>60):
        #print(temp_input)
        x_input=np.array(temp_input[1:])
        # print("{} day input {}".format(i,x_input))
        x_input=x_input.reshape(1,-1)
        x_input = x_input.reshape((1, n_steps, 1))
        #print(x_input)
        yhat = model.predict(x_input, verbose=0)
        # print("{} day output {}".format(i,yhat))
        temp_input.extend(yhat[0].tolist())
        temp_input=temp_input[1:]
        #print(temp_input)
        lst_output.extend(yhat.tolist())
        i=i+1
    else:
        x_input = x_input.reshape((1, n_steps,1))
        yhat = model.predict(x_input, verbose=0)
        # print(yhat[0])
        temp_input.extend(yhat[0].tolist())
        # print(len(temp_input))
        lst_output.extend(yhat.tolist())
        i=i+1

predictions=scaler.inverse_transform(lst_output)

day_new=np.arange(1,61)
day_pred=np.arange(61,61+pred_days)

fig2 = plt.figure(figsize=(12,8))
#plt.plot(ff,'b',label='CLosing')
plt.plot(day_new,(df.Close[len(df)-60:]) , 'g', label='OG price')
plt.plot(day_pred,scaler.inverse_transform(lst_output) , 'r', label='Predicted price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()


from pandas import DataFrame,concat,read_csv
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense,LSTM
import matplotlib.pyplot as plt
def construct_timeframe(data, n_in=1, n_out=1,dropna=False):
    features = 1 if type(data) is list else data.shape[1]
    df = DataFrame(data)
    rows , columns=list(),list()
    for i in range(n_in,0,-1):
        rows.append(df.shift(i))
        columns += [ "var{}(t-{})".format(j,i) for j in range(features) ]
        #print(columns)
    for i in range(0,n_out):
        rows.append(df.shift(-i))
        if i==0:
            columns +=  [ "var{}(t)".format(j) for j in range(features) ]
        else:
            columns += [ "var{}(t+{})".format(j,i) for j in range(features) ]
        #print(columns)
    result = concat(rows,axis=1)
    result.columns = columns
    if dropna:
        result.dropna(inplace=True)
    return result

'''

starts from 2017-04-03 09:15:00
ends   at   2019-12-31 15:29:00

'''

df = read_csv(
    'stocks.csv',
    delimiter=',',
    usecols=[2,3,4,5,6,7,8],
    index_col=0,
    skip_blank_lines=True).sort_values(by='datetime')

df.dropna(inplace=True)

'''
2018-06-20 09:15:00

2018-12-31 15:29:00
'''

values= df.values
values=values.astype('float32')

scalar = MinMaxScaler(feature_range=(0,1))
scaled_values = scalar.fit_transform(values)

scaled_values = scaled_values.astype('float32')

framed = construct_timeframe(scaled_values,1,1,True)
n_features=6
framed.drop(framed.columns[range(n_features+1,n_features*2)],axis=1,inplace=True)


values = framed.values

train_size = int(0.25 * values.shape[0])

train , test = values[:train_size] , values[train_size:]

trainX , trainY = train[: , :-1] , train[:,-1]
testX , testY = test[: , :-1] , test[:,-1]

trainX = trainX.reshape(trainX.shape[0],1,trainX.shape[1])
testX = testX.reshape(testX.shape[0],1,testX.shape[1])

print('shape => ',trainX.shape,trainY.shape,testX.shape,testY.shape)

model = Sequential()

model.add(LSTM(50,input_shape=(trainX.shape[1],trainX.shape[2])))
model.add(Dense(1))

model.compile(loss="mae",metrics=['val_loss','acc'],optimizer="adam")


history = model.fit(
    trainX,
    trainY,
    epochs=50,
    batch_size=64,
    validation_data=(testX,testY),
    shuffle=False,
    verbose=2
    )

plt.figure()
plt.plot(history.history['loss'],label="Train Loss")
plt.plot(history.history['val_loss'],label="Test Loss")
plt.legend()
plt.show()
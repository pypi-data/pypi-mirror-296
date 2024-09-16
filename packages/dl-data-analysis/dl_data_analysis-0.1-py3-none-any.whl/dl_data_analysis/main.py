import pandas as pd
import numpy as np

import sklearn
from sklearn.model_selection import train_test_split
from sklearn import preprocessing 
from sklearn.preprocessing import StandardScaler,MinMaxScaler

import matplotlib.pyplot as plt



def data_prep(x_dataframe, y_data, test_ratio=0.3, validation=False, scaler_type="min_max", verbose=False, seed=42, oversample=False):
    '''
        The input data must be a pandas dataframe
        The lables could be pandas sereis or dataframe
        scaler_type: "min_max" or "standard"
    '''
    x_dataframe.iloc[:,:] = x_dataframe.iloc[:,:].ewm(span=40,adjust=False).mean()

    # train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x_dataframe, y_data, test_size=test_ratio, random_state=seed)
    
    if validation == "True": 
        X_test, X_val, y_train, y_val = train_test_split(x_dataframe, y_data, test_size=0.5, random_state=seed)

    # If scler_type is MinMaxSxaler
    if scaler_type == "min_max":	
        train_scaler = MinMaxScaler().fit(X_train)
        X_train = train_scaler.transform(X_train)
        X_test = train_scaler.transform(X_test)
        if validation == "True":
            X_val = train_scaler.transform(X_val)

    # If scaler_type is StandardScaler
    elif scaler_type == "standard":
        train_scaler = MinMaxScaler().fit(X_train)
        X_train = train_scaler.transform(X_train)
        X_test = train_scaler.transform(X_test)
        if validation == "True":
            X_val = train_scaler.transform(X_val)

    # If scaler_type is StandardScaler
    elif scaler_type == "standard":
        train_scaler = MinMaxScaler().fit(X_train)
        X_train = train_scaler.transform(X_train)
        X_test = train_scaler.transform(X_test)
        if validation == "True":
            X_val = train_scaler.transform(X_val)
    if oversample:
        sub = SMOTE(
        sampling_strategy='auto',
        random_state=SEED,
        )
        X_train, y_train = sub.fit_resample(X_train, y_train)
    # If validation is True return validation split as well
    if validation == "True":
        return X_train, X_test, X_val, y_train, y_test, y_val

    # If Validation is False return train and test splits
    else:
        return X_train, X_test, y_train, y_test

def dataset_visualize(pd_dataframe, feature_list, Name, list):
	bearings_xy = [[Name + str(n)+"_"+str(o)+"_" for n in range(1,5)] for o in list] 
	for tf in time_features_list:
	    fig = plt.figure()
	    # Divide the figure into a 1x4 grid, and give me the first section
	    ax1 = fig.add_subplot(141)
	    # Divide the figure into a 1x4 grid, and give me the second section
	    ax2 = fig.add_subplot(142)
	    #...so on
	    ax3 = fig.add_subplot(143)
	    ax4 = fig.add_subplot(144)
	    axes = [ax1,ax2,ax3, ax4]
	    
	    for i in range(4):
	        col = bearings_xy[0][i]+tf
	        set1[col].plot(figsize = (36,6), title="Bearing{} x-y_".format(i+1)+tf , legend = True, ax=axes[i])
	        col = bearings_xy[1][i]+tf
	        set1[col].plot(figsize = (36,6) , legend = True, ax=axes[i])
	        axes[i].set(xlabel="cycle", ylabel="value")
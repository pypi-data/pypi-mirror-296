from tensorflow import keras
from tensorflow.keras import layers

import tensorflow as tf
import numpy as np
import os
import logging

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Suppress TensorFlow logs
logging.getLogger('tensorflow').setLevel(logging.ERROR)  # Hide all but errors

# Disable oneDNN optimizations to avoid further logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
# 0: All logs (default)
# 1: Filter out INFO logs
# 2: Filter out INFO and WARNING logs
# 3: Filter out all logs except errors

def clsfr(inputs,val_true,lrn_rt,steps):
    inputs = inputs.astype(np.float32)
    val_true = val_true.astype(np.float32)
    val_true = val_true.reshape(val_true.shape[0],1)
    # inputs - only hold the features no output 
    # val_true - only hold the outputs no features
    dim = [inputs.shape[1],val_true.shape[1]]
    # dim[0] ~ dimension of input , dim[1] ~ dimension of output

    # w ~ weights of dim_ input.shape[1]{no of features} X 1
    w = tf.Variable(initial_value = tf.random.uniform(shape=(dim[0],1)))
    # b ~ biases of dim_ 1 X 1
    b = tf.Variable(initial_value = tf.zeros(shape = (dim[1],1)))

    # input{2000 X 2}.weight{2 X 1} ~ 2000 x 2 + {1x1} - this happens due to broadcasting
    def model(inputs):
        return tf.matmul(inputs,w)+b
    
    #cost = (val_true - val_pred)**2/(2000{inputs.shape[0]})
    def cost(val_true,val_pred):
        sqred_loss = tf.square(val_true-val_pred)
        return tf.reduce_mean(sqred_loss)
    
    alpha = lrn_rt
    def train( val_true,inputs):
        with tf.GradientTape() as tape:
            val_pred = model(inputs)
            cost_grd = cost(val_true,val_pred)
        loss_wrt_w,loss_wrt_b = tape.gradient(cost_grd,[w,b])
        w.assign_sub(loss_wrt_w*alpha)
        b.assign_sub(loss_wrt_b*alpha)
        return cost_grd
    
    # print('hello beautiful')
    # for step in range(1,steps*10):
    #     loss = train(val_true,inputs)
    #     if(step%((step*10)/10)==0):
    #         print(f'Loss[{step}]:{loss}')

    if steps <= 10:
        step_interval = 1
    else:
        # Divide into 10 equal intervals
        step_interval = steps // 10
    
    printed_steps = 0  # Count the number of printed steps

    for step in range(0, steps + 1, step_interval):
        loss = train(val_true,inputs)
        if printed_steps < 10:
            print(f'Loss[{step}]:{loss}')
            printed_steps += 1

    # If we didn't hit exactly 10 steps (due to rounding), print the final step
    if printed_steps < 10 and step != steps:
        print(f'Loss[{step}]:{loss}')
        # Ensure the last step is always printed

    val_pred = model(inputs)
    return val_pred,w,b

def dataset_1(sample_size):
    positive = np.random.multivariate_normal(
    mean = [3,0],
    cov = [[1,0.5],[0.5,1]],
    size = sample_size )

    negative = np.random.multivariate_normal(
    mean = [0,3],
    cov = [[1,0.5],[0.5,1]],
    size = sample_size )

    inputs = np.vstack((negative,positive))
    val_true = np.vstack((np.zeros((sample_size, 1), dtype='float32'),
                    np.ones((sample_size,1),dtype='float32')))
    
    return inputs,val_true

def dataset_2(num):
    if(num == 1): # AND OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 0, 0, 1]) 
        return(test_inputs,test_val_true)
    
    elif(num == 2): # OR OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 1, 1, 1]) 
        return(test_inputs,test_val_true)
    
    elif(num == 3): # XOR OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 1, 1, 0]) 
        return(test_inputs,test_val_true)
    
    elif(num == 4): # XNOR OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([1, 0, 0, 1]) 
        return(test_inputs,test_val_true)
    
    else: # AND OPERATION
        test_inputs = np.array([[0,0], [0,1], [1,0], [1,1]])
        test_val_true = np.array([0, 0, 0, 1]) 
        return(test_inputs,test_val_true)
    
def hyper_tunner(x_train,y_train,x_test,y_test,epoch,mode):
    global train_x,train_y,test_x,test_y,epoch_global,optimizer_global,loss_global

    train_x = x_train
    train_y = y_train
    test_x = x_test
    test_y = y_test

    if(mode == 0): #binary_Classification

        def hypertuner(x_train,y_train,x_test,y_test,loss_set,optimizer_set,epoch,k):
            
            model = keras.Sequential([
            layers.Dense(16,activation='relu'),
            layers.Dense(16,activation='relu'),
            layers.Dense(1,activation='sigmoid')
            ])
            
            model.compile(optimizer=optimizer_set,
                    loss=loss_set,
                    metrics=['accuracy'])
            
            history = model.fit(x_train,
                        y_train,
                        epochs=epoch,
                        batch_size=512,
                        validation_data=(x_test,y_test))
            
            
            history_dict = history.history
            
            loss_values = history_dict['loss']
            accuracy = history_dict['accuracy']
            
            epochs = range(1,len(loss_values)+1)
            
            val_loss = history_dict['val_loss']
            val_accuracy = history_dict['val_accuracy']
            
            loss_index = val_loss.index(min(val_loss))+1
            
            if(k==0):
                return loss_index
            elif(k==1):
        #         return val_loss[loss_index-1],val_accuracy[loss_index-1]
                return history_dict
            else:
                return loss_index,val_loss[loss_index-1],val_accuracy[loss_index-1],model

        optimizer_global = None
        loss_global = None  
        epoch_global = None
        def hype(x_train,y_train,x_test,y_test,epoch):
            
            #optimizer - sgd,adam,rmsprop
            optimizer_set = ['sgd','adam','rmsprop']
            
            #loss - binary_crossentropy,mean_squared_error
            loss_set = ['binary_crossentropy','mean_squared_error']
            
            
            #operational_Set
            operational_loss = np.zeros(6,dtype=float)
            operational_accuracy = np.zeros(6,dtype=float)
            operational_set = ['SGD_$_BIN_CEY',
                            'SGD_$_MSE',
                            'ADAM_$_BIN_CEY',
                            'ADAM_$_MSE',
                            'RMS_PROP_$_BIN_CEY',
                            'RMS_PROP_$_MSE']
            
            #epoch_Finder
            epoch = hypertuner(x_train,
                                y_train,
                                x_test,y_test,
                                loss_set[0],
                                optimizer_set[2],
                                epoch,0)
                    
            def operational(x_train,y_train,x_test,y_test,epoch):
                operational_index = 0
                for optimizer_index in range(len(optimizer_set)):
                    for loss_index in range(len(loss_set)):
                        history_dict= hypertuner(x_train,
                                                                y_train,
                                                                x_test,y_test,
                                                                loss_set[loss_index],
                                                                optimizer_set[optimizer_index],
                                                                epoch,1)
                        operational_loss[operational_index] = history_dict['val_loss'][epoch-1]
                        operational_accuracy[operational_index] = history_dict['val_accuracy'][epoch-1]
                        operational_index+=1
            
            #calling_Function
            operational(x_train,y_train,x_test,y_test,epoch)
                    
            #hyperTunning_Results
            print('---------------HYPERTUNING RESULTS---------------')
            print(f'Optimal_epoch: {epoch}')
            print(f'------SETTING RESULTS------')
            print(f'{"--SETTING--":<20}{"--LOSS--":<20}{"--ACCURACY--":<20}')  # Column headers with fixed width
            for k in range(len(operational_set)):
                print(f'{operational_set[k]:<20}{operational_loss[k]:<20.4f}{(operational_accuracy[k] * 100):<0.2f}%')
        
            # Plotting_Setting
            
            # Instead of df.replace, directly handle np.inf in the numpy arrays
            operational_loss = np.where(np.isinf(operational_loss), np.nan, operational_loss)
            operational_accuracy = np.where(np.isinf(operational_accuracy), np.nan, operational_accuracy)

            # Getting indices for the lowest loss and highest accuracy
            min_loss_idx = np.argmin(operational_loss)
            max_acc_idx = np.argmax(operational_accuracy)

            epoch_global = epoch

            # Plotting using seaborn
            plt.figure(figsize=(10, 6))
            sns.set_style("whitegrid")
            # Plotting the loss
            sns.lineplot(x=np.arange(len(operational_set)), y=operational_loss, marker='o',markerfacecolor='none', color='black', label='Training Loss')
            # Plotting the accuracy
            sns.lineplot(x=np.arange(len(operational_set)), y=operational_accuracy, marker='o',markerfacecolor='none', color='#e76a28', label='Training Accuracy')

            
            # Marking the minimum loss and maximum accuracy points
            plt.scatter(min_loss_idx, operational_loss[min_loss_idx], color='#e76a28', s=100, zorder=5, label='Lowest Loss')
            plt.scatter(max_acc_idx, operational_accuracy[max_acc_idx], color='black', s=100, zorder=5, label='Highest Accuracy')

            # Adding labels for the min loss and max accuracy points
            plt.text(min_loss_idx, operational_loss[min_loss_idx], f'Loss: {operational_loss[min_loss_idx]:.4f}', 
                    horizontalalignment='right', verticalalignment='bottom', fontsize=10, color='#e76a28')
            plt.text(max_acc_idx, operational_accuracy[max_acc_idx], f'Acc: {operational_accuracy[max_acc_idx]:.4f}', 
                    horizontalalignment='left', verticalalignment='top', fontsize=10, color='black')

            # Adjusting x-axis to show the settings properly
            plt.xticks(np.arange(len(operational_set)), operational_set, rotation=0, fontsize=10)

            # Adding titles and labels
            plt.title('Training Loss & Accuracy for Different Settings', fontsize=14)
            plt.xlabel('Optimizer and Loss Settings', fontsize=12)
            plt.ylabel('Metric Values', fontsize=12)

            # Adding legend
            plt.legend()

            plt.tight_layout()
            plt.show()
            print('------SUGGESTED SETTINGS------')
            print(f'{"optimal epochs:":<20}{epoch}')
            suggest_index = 0
            for optimizer_suggest_index in range(len(optimizer_set)):
                    for loss_suggest_index in range(len(loss_set)):
                        indexation = np.argmax(operational_accuracy)
                        if(suggest_index == indexation):
                            print(f'{"optimizer setting:":<20}{optimizer_set[optimizer_suggest_index]}')
                            optimizer_global = optimizer_set[optimizer_suggest_index]
                            print(f'{"loss setting:":<20}{loss_set[loss_suggest_index]}')
                            loss_global = loss_set[loss_suggest_index]
                            print(f'{"loss:":<20}{operational_loss[indexation]:.4f}')
                            print(f'{"accuracy:":<20}{(operational_accuracy[indexation]*100):.2f}%')
                        suggest_index+=1
        
        hype(x_train,y_train,x_test,y_test,epoch)
    else:
        print('other modes will be availibale soon!')

def model():
    model = keras.Sequential([
            layers.Dense(16,activation='relu'),
            layers.Dense(16,activation='relu'),
            layers.Dense(1,activation='sigmoid')
            ])
            
    model.compile(optimizer=optimizer_global,
                    loss=loss_global,
                    metrics=['accuracy'])
            
    history = model.fit(train_x,
                        train_y,
                        epochs=epoch_global,
                        batch_size=512,
                        validation_data=(test_x,test_y))
    
    return model
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from datetime import datetime as dt
from matrixprofile import *
class Matrix_profile:

    def __init__(self):
        pass

    def get_date(self , df):
        max_ = df['temp'].max()
        min_ = df['temp'].min()
        print("max = " , max_)
        print("min = " , min_)
        # print(df['temp'])
        # print(type(df['temp'][0]))
        try:
            d = input("Enter the date you want to find pattern from in (dd/mm/yyyy) format only")
            d = d.split("/")
            temp = dt(int(d[-1]), int(d[-2]), int(d[-3]))
            ind_ = df.index[ df['temp'] == temp][0]
            print("index",type(ind_))
            if ind_ >= 0:
                return ind_
            else:
                print("entered date is not in range")
                self.get_date(df)
        except:
            print("entered date does not exist")
            self.get_date(df)

    def read_data(self):
        try:
            flag = 1
            path = input("Enter the path to csv file")
            df = pd.read_csv(path)
            df["index_"] = [i+1 for i in df.index]
            columns_ = df.columns
            while(flag==1):
                df_column = input("Enter the column name")
                if df_column not in columns_:
                    print("Entered column is not in data")
                    flag = 1
                else:
                    flag = 0
                    df[df_column] = pd.to_numeric(df[df_column])
                    df['temp'] = pd.to_datetime(df['Date'])
                    pattern_date = self.get_date(df)
            flag1 = 1
            test = int(input("Do you want to give size of pattern ? Enter 1 if yes 0 if no."))
            if test == 1:
                while(flag1):
                    m = int(input("enter the length of pattern"))
                    if (m >= 10) & (m <= 30):
                        flag1 = 0
                    else:
                        print("please enter the window of size between 10 to 30 only")
            else:
                m = 10
            return df[df_column] , df_column , df['Date'] , m , pattern_date
        except FileNotFoundError:
            print("File not found at " , path)
        except:
            print("some exception occured")

    def matrix_profile(self , df , df_column , m , date_):

        # plt.plot(df)
        # plt.show()
        # print(df.values)

        pattern = df.values[:]
        df1 = pd.DataFrame()
        df1[df_column]= pattern
        # print(pattern)
        mp = matrixProfile.stomp(pattern , m)
        df1['mp'] = np.append(mp[0] , np.zeros(m-1)+np.nan )
        df1["mp_loc"] = np.append(mp[1] , np.zeros(m-1)+np.nan)
        df1['date'] = date_[:]
        # plt.plot(df1['mp'])
        # plt.show()
        # df1.index = [i+2 for i in df1.index]
        df1.to_csv("D:/cloud_coe_work/timeseries/retail_ts_v4_2_op.csv")
        plt.plot(df1.index , df1[df_column] , color = "orange")

        max_val = df1.nlargest(1 , ['mp'])[df_column]
        i = max_val.index.values[0]
        print("anomoly ",i)
        rng = df1[df_column][i: (i+m)]
        max_val = range(i , i+m)

        print("max val " , max_val)

        plt.plot(max_val,rng, color = "red" , )
        date_val = [str(x)[:-5] for x in df1.date]
        # plt.xticks(df1.index[1::4] , date_val[1::4] ,rotation=45)
        plt.xlabel("Dates")
        plt.ylabel(df_column)
        plt.show()
        return  df1

    def plot_pattern_matching(self , data_copy , colnm ,m , p_d):
        # print("-----" , p_d)

        y = data_copy.index
        dt_ = [str(x) for x in data_copy.date]
        # dt_ = [str(x)[:-5] for x in data_copy.date]
        plt.plot(data_copy.index, data_copy[colnm] , color = 'orange')

        plt.xlabel("Dates")
        plt.xticks(y[1::2],dt_[1::2], rotation = 90)
        plt.ylabel(colnm)
        # ind_ = data_copy.iloc[data_copy.date == p_d]
        # print("----------date----" , ind_)
        # ind = dat.index.values.astype(int)
        #
        mp_val = data_copy['mp'][p_d]
        i = p_d

        indexces = []
        # print("i ",data_copy[i-1:i])
        # while( mp_val < 2 and i != 0) :
        while( mp_val < 2 ) :
            indexces.append(i)
            # print("mp_val ",mp_val)
            plt.plot(data_copy.index[ i : i + m ],data_copy[colnm][ i : i + m ]  , color = 'blue')
            print(data_copy[colnm][ i : i + m ])
            mp_val = data_copy['mp'][i]
            i = int(data_copy['mp_loc'][i])
            # print(" ",data_copy['mp_loc'][i-1:i])
            if i not in indexces:
                print("mp val",i)
                continue
            else:
                break
        plt.show()

if __name__ == '__main__':
    mp = Matrix_profile()
    temp = mp.read_data()
    if temp:
        data , column_name , date_  , m , p_d = temp[0], temp[1], temp[2], temp[3], temp[4]
        dt = mp.matrix_profile(data , column_name , m , date_)
        mp.plot_pattern_matching(dt ,column_name,  m , p_d)

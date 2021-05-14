import pandas as pd


def read_files_concat_and_sort(filename1, filename2, save_as): 
    
    df1 = pd.read_csv(filename1) 
    print(df1.head(5))
    df2 = pd.read_csv(filename2)
    print(df2.head(5))

    df1 = pd.concat([df1, df2])

    df1.sort_values(by=['timestamp'], inplace=True, ascending=True)
    print(df1.head(5))
    df1.to_csv("./csv_files/"+save_as, index=False)


read_files_concat_and_sort("./csv_files/sensor_data_0.csv", "./csv_files/sensor_data_1.csv", "sensor_data_merged.csv")


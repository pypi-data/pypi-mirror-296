#building a df subclass?
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

from datahandling.change_directory import chdir_sql_requests

import pandas as pd

class mydf(pd.DataFrame):
    def __init__(self,df) -> None:
        super().__init__(df)
        self.dropped_columns=None
    def to_numeric(self,inplace=False):
        non_num_cols=self.non_numeric_cols()
        if inplace==False:
            copy=self.drop(columns=non_num_cols)
            return copy
        elif inplace==True:
            self.drop(columns=non_num_cols,inplace=True)
    def knn_impute(self,n_neighbors=3):
        self.drop_nan_columns(0.7,inplace=True)
        numeric_cols=self.numeric_cols() #vielleicht noch option zu droppen 
        numeric_df=self[numeric_cols]
        imputer=KNNImputer(n_neighbors=n_neighbors)
        imputed=imputer.fit_transform(numeric_df)
        self[numeric_cols]=imputed 
        return self
    def numeric_cols(self,inplace=False):
        numeric=self.astype(float,errors="ignore")
        dtypes=numeric.dtypes
        numeric_cols=dtypes[dtypes==float]
        return numeric_cols.index
    def non_numeric_cols(self):
        numeric=self.astype(float,errors="ignore")
        dtypes=numeric.dtypes
        non_numeric_cols=dtypes[dtypes!=float]
        return non_numeric_cols.index
    def drop_nan_columns(self,max_allowed_na: float=1,inplace=False):
        na_bool=self.isna()
        for column_name in self.columns:
            na_percentage=na_bool[column_name].sum()/len(na_bool)
            if na_percentage > max_allowed_na:
                if inplace==False:
                    df=df.drop(columns=column_name,axis=1)
                if inplace==True:
                    self.drop(columns=column_name,axis=1,inplace=True)
        if inplace==False:
            return df


def concat_dfs(dataframes):
    concat_frames=[dataframe.reset_index(drop=True, inplace=True) for dataframe in dataframes]
    df=pd.concat(concat_frames,ignore_index=True)
    df.reset_index(drop=True,inplace=True)
    return df

def filter_numeric_columns(df):
    columns=df.columns
    new_df=pd.DataFrame()
    dropped_columns=[]
    for column_name in columns:
        column=df[column_name]
        try:
            pd.to_numeric(column)
            new_df[column_name]=column
            print(column_name)
        except ValueError:
            dropped_columns.append(column_name)
            print(f"{column_name} can't be converted to numeric")
    return new_df,dropped_columns

def drop_observations(dataframe_path,column,min_count,output_name):
    chdir_sql_requests()
    df=pd.read_csv(dataframe_path)
    company_counts = df[column].value_counts()
    companies_to_keep = company_counts[company_counts >= min_count].index
    df_filtered = df[df[column].isin(companies_to_keep)]
    df_filtered.to_csv(output_name)
    return df_filtered

def drop_nan_columns(df : pd.DataFrame,max_allowed_na: float=1):
    #should I copy here?
    #bool_df=df.notna()
    na_bool=df.isna()
    for column_name in df.columns:
        na_percentage=na_bool[column_name].sum()/len(na_bool)
        if na_percentage > max_allowed_na:
            df=df.drop(columns=column_name,axis=1)
            #print(f"dropped {column_name}")
    return df

def na_counts(df : pd.DataFrame):
    na_df=pd.isna(df)
    counts=na_df.sum()
    true_rows=counts[counts>=1]
    return true_rows

import numpy as np
import pandas as pd

###### OUTLIER FUNCTIONS #####
### get_iqr_outlier_bounds(df,include=None,exclude=None)
### trim_iqr_outliers(df,bounds)
### calc_outliers(x,lb,ub)
### add_outlier_columns(df,bounds)
### handle_iqr_outliers(df,trim=True,include=None,exclude=None)

##### IMPROVEMENT TO MAKE #####
# handle_iqr_outliers:
#   1) Investigate why python is updating my dataframe external to the function - needed to use df = old_df.copy() to prevent this
# get_iqr_outlier_bounds:
#   1) Add function to check if column only contains 0s and 1s.  If so, remove it from the list of columns to consider.

def get_iqr_outlier_bounds(df,include=None,exclude=None):
    """
    Returns dataframe with list of columns and the upper and lower bounds using the IQR method:
        LB = Q1 - 1.5 * IQR
        UB = Q3 + 1.5 * IQR
    If no columns passed to include or exclude, it defaults to finding outliers for all columns.
    Function will ignore non-numeric columns. FUTURE: Columns that contain only 0s and 1s.
    
    Returns: Pandas Dataframe 
    Parameters:
           df: dataframe in which to find outliers
      include: list of columns to find outliers for
       excude: list of columns to NOT find outliers for.  Ignored if 'include'is set.   
    
    C88
    """
    #Get Column List
    #if include and exclude are None
    if not include and not exclude:
        columns = df.columns #returns index - iterable
    elif include:
        columns = include
    else: columns = exclude
    
    #Only pull out numeric columns
    columns = df[columns].select_dtypes(include='number')
#     #TO DO: check if only 0s and 1s
#     for c in columns:
#         #if series contains only zeros and ones
#         if df[c].isin([0,1]).all():
    
    #create df for bounds
    bounds = pd.DataFrame()
    #for each column, 
    for col in columns:
        #find bounds
        q1, q3 = df[col].quantile([.25,.75])
        iqr = q3 - q1
        lb = q1 - (1.5 * iqr)
        ub = q3 + (1.5 * iqr)
        #put info in df
        bounds.loc['lb',col] = lb
        bounds.loc['ub',col] = ub
    return bounds

def trim_iqr_outliers(df,bounds):
    """
    Takes in the dataset dataframe, and dataframe of the bounds for each column to be trimmed.
    Returns: Trimmed dataframe
    """
    #loop over columns to work on
    for col in bounds.columns:
        #for each col, grab the outliers
        lb = bounds.loc['lb',col]
        ub = bounds.loc['ub',col]
        #create smaller df of only rows where column is in bounds
        df = df[(df[col] >= lb) & (df[col]<=ub)]
    return df

def calc_outliers(x,lb,ub):
    ''''
    Given a value, determines if it is between the provided upper and lower bounds.  
    If b/w bounds, returns 0, else returns the distance outside of the bounds
    '''
    #if not an outlier, set to zero
    if lb <= x <= ub: return 0
    elif x < lb: return x-lb
    else: return x-ub

def add_outlier_columns(df,bounds):
    #loop over columns in bounds
    for col in bounds.columns:
        #new column name
        col_name = col + '_outlier'
        #for each column, apply the outlier calculation and store to new column
        df[col_name] = df[col].apply(calc_outliers,args=(bounds.loc['lb',col],bounds.loc['ub',col]))
    return df


def handle_iqr_outliers(old_df,trim=False,include=None,exclude=None):
    """
    Takes in a dataframe and either trims outliers or creates column identifying outliers. 
    
    Outputs: None
    Returns: Pandas Dataframe
    Parameters:
                   df: dataframe in which to find outliers
                 trim: If True, will trim out any rows that contain any outliers.  
                        If False, creates new columns to indicate if row is an outlier or not.
                        Default: False
      include/exclude: list of columns to include or exclude for this function.  
                       Default is all, exclude will be ignored if include is provided.
    C88
    """    
    df= old_df.copy()    
    #Get bounds dataframe
    bounds = get_iqr_outlier_bounds(df,include,exclude)

    #If we want new column 
    if trim:
        #Function trims row if value not w/i bounds
        df = trim_iqr_outliers(df,bounds)
    else:
        #function determines if outlier and adds new columnadds new columns 
        df = add_outlier_columns(df,bounds)
        
    return df
##################################
##################################